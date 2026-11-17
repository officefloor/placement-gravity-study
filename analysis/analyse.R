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
# H1 and H4: a Gaussian mixed model of log(1 + bystanders) per run of added logic (by.csv) on the
# checkpoint index: its slope in the methods arm (H1), and the arm term and the arm's interaction
# with the checkpoint (H4), the checkpoint index centred at the middle of the stream so that the arm
# term is the difference half-way through. Their intervals are a cluster bootstrap: chains
# resampled with replacement within arm, the model refitted (spec$boot refits, spec$seed).
# H1 and H4 as first registered, on the bindings of runs into existing methods (h1.csv), are reported.
# H1 also reads the same slope within a place: the class's bystanders over the runs in one class,
# and the method's over the runs in one method, the checkpoint index centred on the place's mean.
# H2 and H3: negative binomial (nbinom2) mixed models per problem and host whose code was bound
# there, at the class and at the method it was placed in, offset by the log of the later
# checkpoints; Wald intervals. H2, in the methods arm: the later intrusions bound to what stood by
# at the placement, on the number that stood by (the rate ratio per bystander). H3: the shape
# measures (long, complexity, concentration) shown not to raise it (one-sided, below the upper margin), on later intrusion at the method, with the bindings and the bystanders in the
# model. H4 also reads the arm's rate ratio in later intrusion, without either in the model.
# The bindings' rate ratio in later intrusion (H2 until 17 November 2026) is reported.
# Every model carries random intercepts for the chain and for the checkpoint: a checkpoint is one
# problem, solved by every chain, so the problem is held fixed by its identity. A model that does
# not converge with the checkpoint intercept is refitted without it, and that is recorded
# (res$checkpoint_intercept).

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
by <- read("by.csv")
cap <- read("capture.csv")
reopen <- read("reopen.csv")
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
  if (!is.finite(est) || !is.finite(se)) return(list(error = paste("standard error not computed:", term)))
  z <- qnorm(1 - (1 - level) / 2)
  list(estimate = est, se = se, lower = est - z * se, upper = est + z * se, level = level,
       p_greater = pnorm(est / se, lower.tail = FALSE), p_less = pnorm(est / se))
}

# H3 is one-sided: the test that exp(estimate) lies below the upper margin (p_upper), with the 90%
# interval, whose upper limit is that test at 5%. `above` marks an interval wholly above the margin.
# The two one-sided tests that it lies within the margin on both sides (p_tost, outside) are reported.
tost <- function(fit, term, margin) {
  w <- wald(fit, term, 0.90)
  if (!is.null(w$error)) return(w)
  lo <- log(margin[1])
  hi <- log(margin[2])
  p_lo <- pnorm((w$estimate - lo) / w$se, lower.tail = FALSE)  # H0: effect <= lower margin
  p_hi <- pnorm((w$estimate - hi) / w$se)                     # H0: effect >= upper margin
  c(w, list(irr = exp(w$estimate), irr_lower = exp(w$lower), irr_upper = exp(w$upper),
            p_upper = p_hi, above = exp(w$lower) > margin[2],
            p_tost = max(p_lo, p_hi),
            outside = exp(w$upper) < margin[1] || exp(w$lower) > margin[2]))
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

# The model with random intercepts for the chain and the checkpoint; without the checkpoint's when
# that does not converge. `fixed` is the formula without its random part, as text.
fit_cp <- function(fixed, d, family) {
  d$cp_f <- factor(d$cp)
  f1 <- as.formula(paste(fixed, "+ (1 | chain_id) + (1 | cp_f)"))
  f0 <- as.formula(paste(fixed, "+ (1 | chain_id)"))
  # on a history (corpora B and C) a unit is not a problem every chain solves: no intercept for it
  fit <- if (isFALSE(spec$problem_fixed)) structure(list(msg = "a history"), class = "fit_error") else
    if (length(unique(d$cp)) > 1) fit_or_error(glmmTMB(f1, data = d, family = family)) else
    structure(list(msg = "one checkpoint"), class = "fit_error")
  ok <- !inherits(fit, "fit_error") && isTRUE(fit$sdr$pdHess) && isTRUE(fit$fit$convergence == 0) &&
    all(is.finite(summary(fit)$coefficients$cond[, "Std. Error"]))
  if (ok) return(list(fit = fit, formula = f1, cp = TRUE, data = d))
  list(fit = fit_or_error(glmmTMB(f0, data = d, family = family)), formula = f0, cp = FALSE, data = d)
}

# A linear combination of fixed effects with its Wald interval.
combo <- function(fit, weights, level = 0.95) {
  if (inherits(fit, "fit_error")) return(list(error = fit$msg))
  b <- fixef(fit)$cond
  V <- vcov(fit)$cond
  if (!all(names(weights) %in% names(b))) return(list(error = "term not estimated"))
  w <- setNames(rep(0, length(b)), names(b))
  w[names(weights)] <- weights
  est <- sum(w * b)
  se <- sqrt(as.numeric(t(w) %*% V %*% w))
  if (!is.finite(se)) return(list(error = "standard error not computed"))
  z <- qnorm(1 - (1 - level) / 2)
  list(estimate = est, se = se, lower = est - z * se, upper = est + z * se, level = level)
}

# ---------------------------------------------------------------- H1 and H4 on the bindings (reported)

res <- list(analysis = spec$analysis,
            versions = list(R = R.version.string,
                            glmmTMB = as.character(packageVersion("glmmTMB")),
                            TMB = as.character(packageVersion("TMB"))),
            seed = spec$seed, boot = spec$boot, checkpoint_intercept = list())
note <- function(name, m) res$checkpoint_intercept[[name]] <<- m$cp

if (!is.null(h1)) {
  h1$log_host <- log(pmax(h1$pre_positions, 1))
  h1$y <- log1p(h1$binding)
  h1$y_no_param <- log1p(h1$binding_no_param)
  h1$y_no_injected <- log1p(h1$binding_no_injected)
  h1$arm <- as_arm(h1$arm)
  fe_terms <- if (multi(h1$frontend)) " + frontend" else ""

  # H1 as first registered (reported): bindings on host size and the checkpoint, the methods arm
  d1 <- h1[h1$arm == spec$methods_arm, ]
  fit1 <- fit_cp("y ~ log_host + cp", d1, gaussian())$fit
  res$reported$H1_bindings <- list(n_runs = nrow(d1), log_host = wald(fit1, "log_host"), cp = wald(fit1, "cp"))

  # H1 read in the function arm, and at class level in the methods arm (reported)
  dF <- h1[h1$arm == spec$function_arm, ]
  fitF <- fit_cp("y ~ log_host + cp", dF, gaussian())$fit
  dc <- d1[!is.na(d1$class_positions) & d1$class_positions > 0, ]
  dc$log_class <- log(dc$class_positions)
  dc$y_class <- log1p(dc$binding_class)
  dc$y_class_no_injected <- log1p(dc$binding_class_no_injected)
  fitC <- fit_cp("y_class ~ log_class + cp", dc, gaussian())$fit
  res$reported$H1_function_arm <- list(log_host = wald(fitF, "log_host"), cp = wald(fitF, "cp"))
  res$reported$H1_class_level <- list(log_class = wald(fitC, "log_class"), cp = wald(fitC, "cp"))

  # without injected dependencies (PLAN.md 4.3): a field holding an injected dependency can be
  # declared by any class, so it may not pin code to this one
  fitNI <- fit_cp("y_no_injected ~ log_host + cp", d1, gaussian())$fit
  fitCNI <- fit_cp("y_class_no_injected ~ log_class + cp", dc, gaussian())$fit
  res$reported$H1_without_injected <- list(log_host = wald(fitNI, "log_host"), cp = wald(fitNI, "cp"))
  res$reported$H1_class_level_without_injected <- list(log_class = wald(fitCNI, "log_class"),
                                                       cp = wald(fitCNI, "cp"))

  # Formation, lagged (reported, PLAN.md 5): for the same problem, is a chain that has been forced
  # more so far bound more now? The chain's mean bindings per run over its earlier checkpoints, per arm.
  for (a in c(spec$methods_arm, spec$function_arm)) {
    dl <- h1[h1$arm == a & !is.na(h1$prior_binding_mean), ]
    ml <- if (nrow(dl) > 0) fit_cp("y ~ log_host + cp + prior_binding_mean", dl, gaussian()) else
      list(fit = structure(list(msg = "no rows"), class = "fit_error"), cp = FALSE)
    res$reported[[paste0("formation_lagged_", a)]] <-
      c(wald(ml$fit, "prior_binding_mean"), list(n = nrow(dl), checkpoint_intercept = ml$cp))
  }

  # H4 as first registered (reported): the arms against each other on the bindings, the host size centred
  # so that the arm term is the difference at a typical host
  d3 <- h1[h1$arm %in% c(spec$methods_arm, spec$function_arm), ]
  d3$arm <- droplevels(d3$arm)
  centre <- mean(d3$log_host)
  d3$log_host_c <- d3$log_host - centre
  inter <- paste0("log_host_c:", FARM)
  fit3 <- fit_cp(paste0("y ~ log_host_c * arm + cp", fe_terms), d3, gaussian())$fit
  res$reported$H4_bindings <- list(n_runs = nrow(d3), centre_positions = exp(centre),
                               arm = wald(fit3, FARM), slope = wald(fit3, inter))
  # the arm difference at hosts of 10, 25 and 50 positions (reported)
  res$reported$H4_arm_at <- setNames(lapply(c(10, 25, 50), function(x)
    combo(fit3, setNames(c(1, log(x) - centre), c(FARM, inter)))), c("10", "25", "50"))

  # H4 (bindings) without the injection rule: bindings counted without parameters, in both arms (reported)
  fit3n <- fit_cp(paste0("y_no_param ~ log_host_c * arm + cp", fe_terms), d3, gaussian())$fit
  res$reported$H4_without_parameters <- list(arm = wald(fit3n, FARM), slope = wald(fit3n, inter))
  fit3i <- fit_cp(paste0("y_no_injected ~ log_host_c * arm + cp", fe_terms), d3, gaussian())$fit
  res$reported$H4_without_injected <- list(arm = wald(fit3i, FARM), slope = wald(fit3i, inter))
  # the trajectory: the arm's interaction with the checkpoint index
  fit3t <- fit_cp(paste0("y ~ log_host_c * arm + cp * arm", fe_terms), d3, gaussian())$fit
  res$reported$H4_trajectory <- wald(fit3t, paste0(FARM, ":cp"))
}

# ---------------------------------------------------------------- H1 and H4: bystanders

if (!is.null(by)) {
  by$arm <- as_arm(by$arm)
  by$y <- log1p(by$bystanders)
  mid <- if (!is.null(spec$checkpoints) && spec$checkpoints > 0) (spec$checkpoints + 1) / 2 else
    mean(range(by$cp))
  by$cp_c <- by$cp - mid
  fe_by <- if (multi(by$frontend)) " + frontend" else ""

  # H1: bystanders rise with the checkpoint index in the methods arm
  dm <- by[by$arm == spec$methods_arm, ]
  mb1 <- fit_cp("y ~ cp", dm, gaussian())
  note("H1", mb1)
  bb1 <- if (inherits(mb1$fit, "fit_error")) NULL else
    cluster_boot(mb1$data, mb1$formula, gaussian(), "cp", spec$boot)
  res$H1 <- list(n_runs = nrow(dm), n_chains = length(unique(dm$chain_id)),
                 cp = if (is.null(bb1)) list(error = mb1$fit$msg) else boot_summary(mb1$fit, bb1, "cp"))
  # H1 within a place: among the runs in one class, the class's bystanders, and among the runs in
  # one method, the method's, on the checkpoint index less the place's mean (the place's mean is in
  # the model, so the slope is not the code moving to places that hold more)
  within <- function(d, place, col) {
    d$yy <- log1p(d[[col]])
    d$cp_m <- ave(d$cp, d[[place]])
    d$cp_w <- d$cp - d$cp_m
    if (length(unique(d$cp_w)) < 2) return(list(error = "no place with runs at two checkpoints"))
    mw <- fit_cp("yy ~ cp_w + cp_m", d, gaussian())
    if (inherits(mw$fit, "fit_error")) return(list(error = mw$fit$msg))
    c(boot_summary(mw$fit, cluster_boot(mw$data, mw$formula, gaussian(), "cp_w", spec$boot), "cp_w"),
      list(places = sum(tapply(d$cp_w, d[[place]], function(v) length(unique(v)) > 1)),
           checkpoint_intercept = mw$cp))
  }
  if ("place_class" %in% names(dm)) {
    res$H1$within_class <- within(dm, "place_class", "by_class")
    res$H1$within_method <- within(dm, "place_method", "by_method")
    dfa <- by[by$arm == spec$function_arm, ]
    res$reported$H1_within_function_arm <- list(class = within(dfa, "place_class", "by_class"),
                                                method = within(dfa, "place_method", "by_method"))
  }
  # the same slope at each level, without injected dependencies, without constants, and in the
  # function arm (reported)
  slope_of <- function(d, col) {
    d$yy <- log1p(d[[col]])
    wald(fit_cp("yy ~ cp", d, gaussian())$fit, "cp")
  }
  res$reported$H1_levels <- list(
    method = slope_of(dm, "by_method"), class = slope_of(dm, "by_class"),
    without_injected = slope_of(dm, "bystanders_no_injected"),
    without_constants = slope_of(dm, "bystanders_no_constants"),
    function_arm = slope_of(by[by$arm == spec$function_arm, ], "bystanders"))

  # H4: the function arm has fewer bystanders half-way through, and they grow more slowly
  db <- by[by$arm %in% c(spec$methods_arm, spec$function_arm), ]
  db$arm <- droplevels(db$arm)
  interb <- paste0("cp_c:", FARM)
  mb3 <- fit_cp(paste0("y ~ cp_c * arm", fe_by), db, gaussian())
  note("H4", mb3)
  bb3 <- if (inherits(mb3$fit, "fit_error")) NULL else
    cluster_boot(mb3$data, mb3$formula, gaussian(), c(FARM, interb), spec$boot)
  res$H4 <- list(n_runs = nrow(db), n_chains = length(unique(db$chain_id)), centre_checkpoint = mid,
                 arm = if (is.null(bb3)) list(error = mb3$fit$msg) else boot_summary(mb3$fit, bb3, FARM),
                 slope = if (is.null(bb3)) list(error = mb3$fit$msg) else boot_summary(mb3$fit, bb3, interb))
  db$yn <- log1p(db$bystanders_no_injected)
  fitbn <- fit_cp(paste0("yn ~ cp_c * arm", fe_by), db, gaussian())$fit
  res$reported$H4_bystanders_without_injected <- list(arm = wald(fitbn, FARM), slope = wald(fitbn, interb))
  # the needed values: the same stream, so the arms are expected to need the same
  db$need_y <- log1p(db$need)
  res$reported$needed_arm <- wald(fit_cp(paste0("need_y ~ arm", fe_by), db, gaussian())$fit, FARM)
}

# Capture (reported): for the same problem, is a chain whose heaviest class holds more more likely
# to place the addition in an existing host? Per arm.
if (!is.null(cap)) {
  cap$log_heaviest <- log1p(cap$heaviest_class)
  for (a in c(spec$methods_arm, spec$function_arm)) {
    dcap <- cap[cap$arm == a, ]
    mc <- if (nrow(dcap) > 0 && length(unique(dcap$log_heaviest)) > 1)
      fit_cp("share_in_existing ~ log_heaviest", dcap, gaussian()) else
      list(fit = structure(list(msg = "no variation"), class = "fit_error"), cp = FALSE)
    res$reported[[paste0("capture_", a)]] <-
      c(wald(mc$fit, "log_heaviest"), list(n = nrow(dcap), checkpoint_intercept = mc$cp))
  }
}

# ---------------------------------------------------------------- H2 and H3

if (!is.null(h2)) {
  h2 <- h2[h2$later_checkpoints > 0, ]
  # intrusion applies only where the problem's code was bound to the place (PLAN.md 4.4)
  res$reported$intrusion_rows <- list(all = nrow(h2), bound = sum(as.logical(h2$bound)))
  h2 <- h2[as.logical(h2$bound), ]
  h2$arm <- as_arm(h2$arm)
  h2$log_size <- log1p(h2$addition_positions)
  h2$log_host <- log1p(h2$pre_positions)
  h2$log_later <- log(h2$later_checkpoints)
  h2$host_new <- as.numeric(as.logical(h2$host_new))
  if (isTRUE(spec$acts)) h2$act <- factor(h2$act)
  # the base model: the problem held fixed (its size, its declared crossings, the checkpoint's
  # intercept), the host's size and whether it is new
  base <- function(d, response = "intrusion", lead = "") {
    paste0(response, " ~ ", lead, "log_size + declared_crossings + log_host",
           if (length(unique(d$host_new)) > 1) " + host_new" else "",
           if (isTRUE(spec$acts) && length(unique(d$act)) > 1) " + act" else "",
           if (multi(as.character(d$arm))) " + arm" else "",
           if (multi(d$frontend)) " + frontend" else "",
           " + offset(log_later)")
  }
  nb <- nbinom2()

  # H2: data draws code in. In the methods arm, per problem and host whose code was bound there:
  # the later intrusions bound to a value that stood by at the placement, on the number that stood
  # by, at the class (its fields) and at the method (its values).
  drawn <- function(d, lev, term = paste0("bystanders_", lev)) {
    if (nrow(d) == 0 || length(unique(d[[term]])) < 2) return(list(fit = structure(
      list(msg = "the bystanders do not vary"), class = "fit_error"), cp = FALSE))
    fit_cp(base(d, paste0("drawn_", lev), paste0(term, " + ")), d, nb)
  }
  h2$log_by_class <- log1p(h2$bystanders_class)
  h2$log_by_method <- log1p(h2$bystanders_method)
  hm <- h2[h2$arm == spec$methods_arm, ]
  hf <- h2[h2$arm == spec$function_arm, ]
  res$H2 <- list(n = nrow(hm))
  for (lev in c("class", "method")) {
    term <- paste0("bystanders_", lev)
    md <- drawn(hm, lev)
    note(paste0("H2_", lev), md)
    res$H2[[lev]] <- irr(wald(md$fit, term))
    # reported: per doubling-like step, log(1 + bystanders); and the function arm
    res$reported[[paste0("H2_log_", lev)]] <- wald(drawn(hm, lev, paste0("log_by_", lev))$fit, paste0("log_by_", lev))
    res$reported[[paste0("H2_function_arm_", lev)]] <- irr(wald(drawn(hf, lev)$fit, term))
  }
  # H2 until 17 November 2026 (reported): the bindings and later intrusion, at the class and at the
  # method, every bound problem and host. The problem's own lines are for information.
  m2c <- fit_cp(base(h2, "intrusion_class", "binding + "), h2, nb)
  m2m <- fit_cp(base(h2, "intrusion_method", "binding + "), h2, nb)
  res$reported$bindings_intrusion_class <- irr(wald(m2c$fit, "binding"))
  res$reported$bindings_intrusion_method <- irr(wald(m2m$fit, "binding"))
  # Size or data (reported, with a stated direction): both arms pooled and no arm term, so that the
  # arms' difference in what stands by, at about the same amount of code, separates the two. Later
  # intrusion on what stood by with the size of the place held fixed (predicted above 1), the
  # size's own ratio beside it, the size alone, and the same with the arm term (within arms).
  if (multi(as.character(h2$arm))) {
    h2$log_class <- log1p(h2$class_positions)
    no_arm <- function(f) sub(" + arm", "", f, fixed = TRUE)
    for (lev in c("class", "method")) {
      d <- if (lev == "class") h2[!is.na(h2$log_class), ] else h2
      size <- if (lev == "class") "log_class" else "log_host"
      extra <- if (lev == "class") "log_class + " else ""
      byt <- paste0("bystanders_", lev)
      y <- paste0("intrusion_", lev)
      both <- fit_cp(no_arm(base(d, y, paste0(byt, " + ", extra))), d, nb)$fit
      alone <- fit_cp(no_arm(base(d, y, extra)), d, nb)$fit
      inarm <- fit_cp(base(d, y, paste0(byt, " + ", extra)), d, nb)$fit
      rho <- function(x) if (nrow(x) > 2) suppressWarnings(cor(x[[size]], x[[byt]], method = "spearman")) else NA
      res$reported[[paste0("size_or_data_", lev)]] <- list(
        n = nrow(d), bystanders = irr(wald(both, byt)), size = irr(wald(both, size)),
        size_alone = irr(wald(alone, size)),
        bystanders_within_arms = irr(wald(inarm, byt)), size_within_arms = irr(wald(inarm, size)),
        correlation = c(list(pooled = rho(d)), lapply(split(d, as.character(d$arm)), rho)))
    }
  }
  # H4: for the same problems, the function arm's bound code is come back to less, at the class and
  # at the method (the base model without the bindings, which the arm itself changes)
  if (multi(as.character(h2$arm))) {
    for (lev in c("class", "method")) {
      ma <- fit_cp(base(h2, paste0("intrusion_", lev)), h2, nb)
      note(paste0("H4_intrusion_", lev), ma)
      res$H4[[paste0("intrusion_", lev)]] <- irr(wald(ma$fit, FARM))
    }
  }
  # any later change, bound or not (as first built), reported
  for (lev in c("class", "method")) {
    res$reported[[paste0("bindings_any_change_", lev)]] <- irr(wald(fit_cp(
      base(h2, paste0("intrusion_", lev, "_any"), "binding + "), h2, nb)$fit, "binding"))
  }
  hl <- h2[!is.na(h2$intrusion_lines), ]
  res$reported$bindings_lines <- if (nrow(hl) > 0)
    irr(wald(fit_cp(base(hl, "intrusion_lines", "binding + "), hl, nb)$fit, "binding")) else list(error = "no lines followed")
  for (lev in c("class", "method")) {
    res$reported[[paste0("bindings_without_injected_", lev)]] <- irr(wald(fit_cp(
      base(h2, paste0("intrusion_", lev), "binding_no_injected + "), h2, nb)$fit, "binding_no_injected"))
  }

  # H3: existing hosts with their shape at k - 1, on method-level intrusion (the shape measures are
  # the method's), with the bindings and what stood by in the method in the model
  ex <- h2[h2$host_new == 0 & as.logical(h2$shape_found) %in% TRUE, ]
  for (c in c("s1_long", "s2_stuck", "s3_junction", "s3_junction_injection_aware")) {
    ex[[c]] <- as.numeric(as.logical(ex[[c]]))
  }
  ex_raw <- ex   # before the joint block standardises its levels in place
  if ("s4_cognitive" %in% spec$shape_kept) ex$s4_cognitive <- as.numeric(scale(log1p(ex$s4_cognitive)))
  if ("s5_class_gini" %in% spec$shape_kept) ex$s5_class_gini <- as.numeric(scale(ex$s5_class_gini))
  kept <- spec$shape_kept
  # the shape block as first registered, the measures together in one model (reported)
  res$reported$shape_joint <- list(n = nrow(ex), kept = kept)
  for (lev in c("class", "method")) {
    res$reported[[paste0("bindings_existing_hosts_", lev)]] <-
      irr(wald(fit_cp(base(ex, paste0("intrusion_", lev), "binding + "), ex, nb)$fit, "binding"))
  }
  if (length(kept) > 0) {
    shape_block <- paste0("binding + bystanders_method + ", paste(kept, collapse = " + "), " + ")
    m3s <- fit_cp(base(ex, "intrusion_method", shape_block), ex, nb)
    note("shape_joint", m3s)
    res$reported$shape_joint$measures <- setNames(lapply(kept, function(k) tost(m3s$fit, k, spec$margin)), kept)
    # the same block on class-level intrusion (reported)
    m3c <- fit_cp(base(ex, "intrusion_class", sub("bystanders_method", "bystanders_class", shape_block)), ex, nb)
    res$reported$H3_class_level <- setNames(lapply(kept, function(k) tost(m3c$fit, k, spec$margin)), kept)
    # shape without the problem terms (the checkpoint's intercept among them), the bindings and the
    # bystanders: how
    # much association leaving the problem out makes
    fsh <- as.formula(paste0("intrusion_method ~ ", paste(kept, collapse = " + "),
                             if (multi(as.character(ex$arm))) " + arm" else "",
                             " + offset(log_later) + (1 | chain_id)"))
    fitsh <- fit_or_error(glmmTMB(fsh, data = ex, family = nb))
    res$reported$shape_without_problem <- setNames(lapply(kept, function(k) irr(wald(fitsh, k))), kept)
  }

  # The literature's shape measures (reported): each one alone, at its own level. Read as H3 is:
  # the rate ratio against the upper margin, per standard deviation or present against absent; a
  # measure where higher is better (the Maintainability Index, TCC) is reversed, so that above 1
  # always means the worse shape is followed by more.
  # A method measure: added to the base model with the bindings and what stood by in the method,
  # on later intrusion at the method, existing hosts.
  # A class measure: one row per class a checkpoint's bound code went into (not one per method),
  # on later intrusion at the class, with the class's size at k - 1 held fixed and an intercept for
  # the class; the bindings are the most of its hosts, what stood by the least.
  lit <- spec$literature
  if (length(lit) > 0) {
    cl <- h2[!is.na(h2$c_positions), ]
    if (nrow(cl) > 0) {
      cl$place <- paste(cl$chain_id, cl$class_identity, sep = "|")
      key <- paste(cl$place, cl$cp)
      cl$binding <- ave(cl$binding, key, FUN = max)
      cl$bystanders_class <- ave(cl$bystanders_class, key, FUN = min)
      cl <- cl[!duplicated(key), ]
      cl$log_class <- log1p(cl$c_positions)
    }
    class_base <- function(d, lead, place = TRUE) {
      paste0("intrusion_class ~ ", lead, "log_size + declared_crossings + log_class",
             if (isTRUE(spec$acts) && length(unique(d$act)) > 1) " + act" else "",
             if (multi(as.character(d$arm))) " + arm" else "",
             if (multi(d$frontend)) " + frontend" else "",
             " + offset(log_later)", if (place) " + (1 | place)" else "")
    }
    res$reported$literature_class_rows <- nrow(cl)
    res$reported$literature_shape <- setNames(lapply(names(lit), function(k) {
      info <- lit[[k]]
      d <- if (info$level == "method") ex_raw else cl
      d <- d[!is.na(d[[k]]), ]
      d$x <- if (info$kind == "flag") as.numeric(as.logical(d[[k]])) else
        if (info$kind == "plain") as.numeric(scale(d[[k]])) else as.numeric(scale(log1p(d[[k]])))
      if (isTRUE(info$reversed)) d$x <- -d$x
      if (nrow(d) < 3 || !all(is.finite(d$x)) || sd(d$x) == 0)
        return(list(error = "does not vary", at = info$level, source = info$source))
      place <- TRUE
      if (info$level == "method") {
        f <- fit_cp(base(d, "intrusion_method", "binding + bystanders_method + x + "), d, nb)$fit
      } else {
        f <- fit_cp(class_base(d, "binding + bystanders_class + x + "), d, nb)$fit
        if (!is.null(wald(f, "x")$error)) {   # refitted without the class's intercept
          place <- FALSE
          f <- fit_cp(class_base(d, "binding + bystanders_class + x + ", FALSE), d, nb)$fit
        }
      }
      c(tost(f, "x", spec$margin), list(n = nrow(d), at = info$level, kind = info$kind,
                                         source = info$source, reversed = isTRUE(info$reversed),
                                         class_intercept = info$level == "class" && place))
    }), names(lit))
  }

  # H3: its measures are among those above, each fitted alone at its level (spec$h3_measures: the
  # ones that vary; length and complexity at the method; concentration, weight and lack of cohesion
  # at the class). Each has to lie below the upper margin.
  h3k <- spec$h3_measures
  res$H3 <- list(n = nrow(ex), n_class = res$reported$literature_class_rows, kept = h3k,
                 testable = length(h3k) > 0, margin = spec$margin)
  if (length(h3k) > 0) res$H3$measures <- res$reported$literature_shape[h3k]

  # The sinew measures (reported, predicted above 1): not slimmable and junction are measures of
  # data flow, not of shape, so they are read apart from H3: each one's rate ratio in later
  # intrusion, with the bindings and what stood by in the model, at the method and at the class.
  sinew <- spec$sinew_kept
  if (length(sinew) > 0) {
    block <- paste0("binding + bystanders_method + ", paste(sinew, collapse = " + "), " + ")
    ms <- fit_cp(base(ex, "intrusion_method", block), ex, nb)$fit
    mc <- fit_cp(base(ex, "intrusion_class", sub("bystanders_method", "bystanders_class", block)), ex, nb)$fit
    res$reported$sinew <- setNames(lapply(sinew, function(k)
      list(method = irr(wald(ms, k)), class = irr(wald(mc, k)))), sinew)
  }

  # junction x arm (secondary): conventional and injection-aware junctions
  for (j in c("s3_junction", "s3_junction_injection_aware")) {
    ok <- all(tapply(ex[[j]], droplevels(ex$arm), function(v) length(unique(v[!is.na(v)])) > 1))
    if (!isTRUE(ok) || !multi(as.character(ex$arm))) {
      res$reported[[paste0("junction_x_arm_", j)]] <- list(error = "junction does not vary in every arm")
      next
    }
    fj <- sub(" + arm", "", base(ex, "intrusion_method", paste0("binding + bystanders_method + ", j, " * arm + ")), fixed = TRUE)
    res$reported[[paste0("junction_x_arm_", j)]] <- irr(wald(fit_cp(fj, ex, nb)$fit, paste0(j, ":", FARM)))
  }
}

# Where unbound code lands (reported, §3.3): whether an unbound landing enters a class that
# existed, the function arm (on a history, the declared agent commits) against the methods arm;
# a binomial mixed model, the odds ratio.
landing <- read("landing.csv")
if (!is.null(landing) && multi(landing$arm)) {
  landing$arm <- as_arm(landing$arm)
  landing$existing <- as.numeric(as.logical(landing$existing_class))
  fl <- fit_or_error(glmmTMB(existing ~ arm + (1 | chain_id), data = landing, family = binomial()))
  res$reported$unbound_enters_existing_class <- c(irr(wald(fl, FARM)), list(
    n = nrow(landing), share = as.list(tapply(landing$existing, as.character(landing$arm), mean))))
}

# Reopening (reported): per checkpoint, the classes its bound code goes back into, and the wiring
# files it changes again; the function arm against the methods arm, a Poisson mixed model each.
if (!is.null(reopen)) {
  reopen$arm <- as_arm(reopen$arm)
  fe_r <- if (multi(reopen$frontend)) " + frontend" else ""
  res$reported$reopen_classes <- irr(wald(fit_cp(paste0("reopened_classes ~ arm", fe_r), reopen, poisson())$fit, FARM))
  res$reported$reopen_with_wiring <- irr(wald(fit_cp(paste0("reopened ~ arm", fe_r), reopen, poisson())$fit, FARM))
}

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
writeLines(toJSON(res, auto_unbox = TRUE, digits = NA, null = "null", na = "null", pretty = TRUE),
           out)
cat("wrote", out, "\n")
