#!/usr/bin/env Rscript
# Step 4, second half: the models of PLAN.md §5, fitted with glmmTMB.
#
#   Rscript analysis/analyse.R data/analysis/<name> results/analysis/<name>/estimates.json
#
# Reads h1.csv, h2.csv and spec.json (placement_gravity/prepare.py) and writes the estimates,
# intervals and one-sided p-values each hypothesis is decided on. The verdicts, the Holm correction
# and the conditions that are not models (the amount band, the wiring) are applied by
# placement_gravity/verdict.py, so every decision rule sits in one place.
#
# H1 and H3: a Gaussian mixed model of log(1 + ties) per run of added logic into an existing
# method, with a random intercept for the chain. Their intervals are a cluster bootstrap: chains
# resampled with replacement within arm, the model refitted (spec$boot refits, spec$seed).
# H2: a negative binomial (nbinom2) mixed model of later intrusion per problem and host, offset by
# the log of the later checkpoints, with a random intercept for the chain; Wald intervals.

suppressPackageStartupMessages({
  library(glmmTMB)
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("usage: analyse.R DATA_DIR OUT_JSON")
dir <- args[1]
out <- args[2]
spec <- fromJSON(file.path(dir, "spec.json"))

read <- function(f) {
  p <- file.path(dir, f)
  if (!file.exists(p) || file.info(p)$size == 0) return(NULL)
  read.csv(p, stringsAsFactors = FALSE)
}
h1 <- read("h1.csv")
h2 <- read("h2.csv")
set.seed(spec$seed)

FARM <- paste0("arm", spec$function_arm)
as_arm <- function(x) relevel(factor(x), ref = spec$methods_arm)
multi <- function(x) length(unique(x[!is.na(x) & x != ""])) > 1

# ---------------------------------------------------------------- helpers

fit_or_error <- function(expr) {
  tryCatch(suppressWarnings(expr), error = function(e) structure(list(msg = conditionMessage(e)),
                                                                   class = "fit_error"))
}

wald <- function(fit, term, level = 0.95) {
  if (inherits(fit, "fit_error")) return(list(error = fit$msg))
  co <- summary(fit)$coefficients$cond
  if (!term %in% rownames(co)) return(list(error = paste("term not estimated:", term)))
  est <- co[term, "Estimate"]
  se <- co[term, "Std. Error"]
  z <- qnorm(1 - (1 - level) / 2)
  list(estimate = est, se = se, lower = est - z * se, upper = est + z * se, level = level,
       p_greater = pnorm(est / se, lower.tail = FALSE), p_less = pnorm(est / se))
}

# Two one-sided tests that exp(estimate) lies within the bound; the 90% interval is reported.
tost <- function(fit, term, bound) {
  w <- wald(fit, term, 0.90)
  if (!is.null(w$error)) return(w)
  lo <- log(bound[1])
  hi <- log(bound[2])
  p_lo <- pnorm((w$estimate - lo) / w$se, lower.tail = FALSE)  # H0: effect <= lower bound
  p_hi <- pnorm((w$estimate - hi) / w$se)                     # H0: effect >= upper bound
  c(w, list(irr = exp(w$estimate), irr_lower = exp(w$lower), irr_upper = exp(w$upper),
            p_tost = max(p_lo, p_hi),
            outside = exp(w$upper) < bound[1] || exp(w$lower) > bound[2]))
}

irr <- function(w) {
  if (!is.null(w$error)) return(w)
  c(w, list(irr = exp(w$estimate), irr_lower = exp(w$lower), irr_upper = exp(w$upper)))
}

# Chains resampled with replacement within arm; the model refitted on each resample.
cluster_boot <- function(d, formula, family, terms, B) {
  ids <- unique(d$chain_id)
  strata <- split(ids, d$arm[match(ids, d$chain_id)])
  by_id <- split(d, d$chain_id)
  draws <- matrix(NA_real_, nrow = B, ncol = length(terms), dimnames = list(NULL, terms))
  for (b in seq_len(B)) {
    pick <- unlist(lapply(strata, function(s) s[sample.int(length(s), length(s), replace = TRUE)]),
                   use.names = FALSE)
    db <- do.call(rbind, lapply(seq_along(pick), function(i) {
      x <- by_id[[pick[i]]]
      x$chain_id <- paste0(pick[i], "#", i)
      x
    }))
    fit <- fit_or_error(glmmTMB(formula, data = db, family = family))
    if (!inherits(fit, "fit_error")) {
      f <- fixef(fit)$cond
      draws[b, ] <- f[terms]
    }
  }
  draws
}

boot_summary <- function(fit, draws, term) {
  if (inherits(fit, "fit_error")) return(list(error = fit$msg))
  x <- draws[, term]
  x <- x[!is.na(x)]
  n <- length(x)
  list(estimate = unname(fixef(fit)$cond[term]),
       lower = unname(quantile(x, 0.025)), upper = unname(quantile(x, 0.975)),
       p_greater = (sum(x <= 0) + 1) / (n + 1), p_less = (sum(x >= 0) + 1) / (n + 1),
       refits = n, failed = nrow(draws) - n)
}

# ---------------------------------------------------------------- H1 and H3

res <- list(analysis = spec$analysis,
            versions = list(R = R.version.string,
                            glmmTMB = as.character(packageVersion("glmmTMB")),
                            TMB = as.character(packageVersion("TMB"))),
            seed = spec$seed, boot = spec$boot)

if (!is.null(h1)) {
  h1$log_host <- log(pmax(h1$pre_positions, 1))
  h1$y <- log1p(h1$tie)
  h1$y_no_param <- log1p(h1$tie_no_param)
  h1$arm <- as_arm(h1$arm)
  fe_terms <- if (multi(h1$frontend)) " + frontend" else ""

  # H1: the methods arm
  d1 <- h1[h1$arm == spec$methods_arm, ]
  f1 <- y ~ log_host + cp + (1 | chain_id)
  fit1 <- fit_or_error(glmmTMB(f1, data = d1, family = gaussian()))
  b1 <- if (inherits(fit1, "fit_error")) NULL else
    cluster_boot(d1, f1, gaussian(), c("log_host", "cp"), spec$boot)
  res$H1 <- list(n_runs = nrow(d1), n_chains = length(unique(d1$chain_id)),
                 log_host = if (is.null(b1)) list(error = fit1$msg) else boot_summary(fit1, b1, "log_host"),
                 cp = if (is.null(b1)) list(error = fit1$msg) else boot_summary(fit1, b1, "cp"))

  # H1 read in the function arm, and at class level in the methods arm (reported)
  dF <- h1[h1$arm == spec$function_arm, ]
  fitF <- fit_or_error(glmmTMB(f1, data = dF, family = gaussian()))
  dc <- d1[!is.na(d1$class_positions) & d1$class_positions > 0, ]
  dc$log_class <- log(dc$class_positions)
  dc$y_class <- log1p(dc$tie_class)
  fitC <- fit_or_error(glmmTMB(y_class ~ log_class + cp + (1 | chain_id), data = dc,
                               family = gaussian()))
  res$reported$H1_function_arm <- list(log_host = wald(fitF, "log_host"), cp = wald(fitF, "cp"))
  res$reported$H1_class_level <- list(log_class = wald(fitC, "log_class"), cp = wald(fitC, "cp"))

  # without injected dependencies (PLAN.md 4.3): a field holding an injected dependency can be
  # declared by any class, so it may not pin code to this one
  d1$y_no_injected <- log1p(d1$tie_no_injected)
  fitNI <- fit_or_error(glmmTMB(y_no_injected ~ log_host + cp + (1 | chain_id), data = d1,
                                family = gaussian()))
  dc$y_class_no_injected <- log1p(dc$tie_class_no_injected)
  fitCNI <- fit_or_error(glmmTMB(y_class_no_injected ~ log_class + cp + (1 | chain_id), data = dc,
                                 family = gaussian()))
  res$reported$H1_without_injected <- list(log_host = wald(fitNI, "log_host"), cp = wald(fitNI, "cp"))
  res$reported$H1_class_level_without_injected <- list(log_class = wald(fitCNI, "log_class"),
                                                       cp = wald(fitCNI, "cp"))

  # H3: the arms against each other in the H1 model
  d3 <- h1[h1$arm %in% c(spec$methods_arm, spec$function_arm), ]
  d3$arm <- droplevels(d3$arm)
  f3 <- as.formula(paste0("y ~ log_host * arm + cp", fe_terms, " + (1 | chain_id)"))
  inter <- paste0("log_host:", FARM)
  fit3 <- fit_or_error(glmmTMB(f3, data = d3, family = gaussian()))
  b3 <- if (inherits(fit3, "fit_error")) NULL else
    cluster_boot(d3, f3, gaussian(), c(FARM, inter), spec$boot)
  res$H3 <- list(n_runs = nrow(d3), n_chains = length(unique(d3$chain_id)),
                 arm = if (is.null(b3)) list(error = fit3$msg) else boot_summary(fit3, b3, FARM),
                 slope = if (is.null(b3)) list(error = fit3$msg) else boot_summary(fit3, b3, inter))

  # H3 without the injection rule: ties counted without parameters, in both arms (reported)
  f3n <- as.formula(paste0("y_no_param ~ log_host * arm + cp", fe_terms, " + (1 | chain_id)"))
  fit3n <- fit_or_error(glmmTMB(f3n, data = d3, family = gaussian()))
  res$reported$H3_without_parameters <- list(arm = wald(fit3n, FARM), slope = wald(fit3n, inter))
  d3$y_no_injected <- log1p(d3$tie_no_injected)
  f3i <- as.formula(paste0("y_no_injected ~ log_host * arm + cp", fe_terms, " + (1 | chain_id)"))
  fit3i <- fit_or_error(glmmTMB(f3i, data = d3, family = gaussian()))
  res$reported$H3_without_injected <- list(arm = wald(fit3i, FARM), slope = wald(fit3i, inter))
  # the trajectory: the arm's interaction with the checkpoint index
  f3t <- as.formula(paste0("y ~ log_host * arm + cp * arm", fe_terms, " + (1 | chain_id)"))
  fit3t <- fit_or_error(glmmTMB(f3t, data = d3, family = gaussian()))
  res$reported$H3_trajectory <- wald(fit3t, paste0(FARM, ":cp"))
}

# ---------------------------------------------------------------- H2

if (!is.null(h2)) {
  h2 <- h2[h2$later_checkpoints > 0, ]
  h2$arm <- as_arm(h2$arm)
  h2$log_size <- log1p(h2$addition_positions)
  h2$log_host <- log1p(h2$pre_positions)
  h2$log_later <- log(h2$later_checkpoints)
  if (isTRUE(spec$acts)) h2$act <- factor(h2$act)
  base <- paste0("intrusion ~ log_size + declared_crossings + log_host",
                 if (isTRUE(spec$acts)) " + act" else "",
                 if (multi(as.character(h2$arm))) " + arm" else "",
                 if (multi(h2$frontend)) " + frontend" else "",
                 " + offset(log_later) + (1 | chain_id)")
  nb <- nbinom2()

  # H2a: every problem and host
  fit2a <- fit_or_error(glmmTMB(as.formula(sub("~", "~ tie +", base, fixed = TRUE)),
                                data = h2, family = nb))
  res$H2a <- c(list(n = nrow(h2)), irr(wald(fit2a, "tie")))
  fit2ai <- fit_or_error(glmmTMB(as.formula(sub("~", "~ tie_no_injected +", base, fixed = TRUE)),
                                 data = h2, family = nb))
  res$reported$H2a_without_injected <- irr(wald(fit2ai, "tie_no_injected"))

  # H2b: existing hosts with their shape at k - 1
  ex <- h2[!as.logical(h2$host_new) & as.logical(h2$shape_found) %in% TRUE, ]
  for (c in c("s1_long", "s2_stuck", "s3_junction", "s3_junction_injection_aware")) {
    ex[[c]] <- as.numeric(as.logical(ex[[c]]))
  }
  if ("s4_cognitive" %in% spec$shape_kept) ex$s4_cognitive <- as.numeric(scale(log1p(ex$s4_cognitive)))
  if ("s5_class_gini" %in% spec$shape_kept) ex$s5_class_gini <- as.numeric(scale(ex$s5_class_gini))
  kept <- spec$shape_kept
  res$H2b <- list(n = nrow(ex), kept = kept, testable = length(kept) > 0, bound = spec$bound)
  fit2a_ex <- fit_or_error(glmmTMB(as.formula(sub("~", "~ tie +", base, fixed = TRUE)),
                                   data = ex, family = nb))
  res$reported$H2a_existing_hosts <- irr(wald(fit2a_ex, "tie"))
  if (length(kept) > 0) {
    f2b <- as.formula(sub("~", paste0("~ tie + ", paste(kept, collapse = " + "), " +"), base,
                          fixed = TRUE))
    fit2b <- fit_or_error(glmmTMB(f2b, data = ex, family = nb))
    res$H2b$measures <- setNames(lapply(kept, function(k) tost(fit2b, k, spec$bound)), kept)
    # shape without the problem terms and the ties: how much association leaving the problem out makes
    fsh <- as.formula(paste0("intrusion ~ ", paste(kept, collapse = " + "),
                             if (multi(as.character(ex$arm))) " + arm" else "",
                             " + offset(log_later) + (1 | chain_id)"))
    fitsh <- fit_or_error(glmmTMB(fsh, data = ex, family = nb))
    res$reported$shape_without_problem <- setNames(lapply(kept, function(k) irr(wald(fitsh, k))), kept)
  }

  # junction x arm (secondary): conventional and injection-aware junctions
  for (j in c("s3_junction", "s3_junction_injection_aware")) {
    ok <- all(tapply(ex[[j]], droplevels(ex$arm), function(v) length(unique(v[!is.na(v)])) > 1))
    if (!isTRUE(ok) || !multi(as.character(ex$arm))) {
      res$reported[[paste0("junction_x_arm_", j)]] <- list(error = "junction does not vary in every arm")
      next
    }
    fj <- as.formula(sub("~", paste0("~ tie + ", j, " * arm +"), base, fixed = TRUE))
    fitj <- fit_or_error(glmmTMB(fj, data = ex, family = nb))
    res$reported[[paste0("junction_x_arm_", j)]] <- irr(wald(fitj, paste0(j, ":", FARM)))
  }
}

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
writeLines(toJSON(res, auto_unbox = TRUE, digits = NA, null = "null", na = "null", pretty = TRUE),
           out)
cat("wrote", out, "\n")
