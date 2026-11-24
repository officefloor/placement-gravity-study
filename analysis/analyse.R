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
# checkpoints. The tests of the confirmatory family (H2, H4's intrusion ratios, H5, H7) take their
# interval and p from the same cluster bootstrap as H1 (chains resampled within arm, the model
# refitted; 22 November 2026): rows of one chain share its classes and methods, which a Wald interval
# does not see. The Wald reading is kept beside each (`wald`). Everything reported is Wald. H2, in the methods arm: the later intrusions bound to what stood by
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
CORES <- suppressWarnings(as.integer(Sys.getenv("PG_CORES", "")))
if (is.na(CORES) || CORES < 1) CORES <- max(1L, min(4L, parallel::detectCores() - 1L))
cluster_boot <- function(d, formula, family, terms, B, nest = NULL) {
  ids <- unique(d$chain_id)
  strata <- split(ids, d$arm[match(ids, d$chain_id)])
  by_id <- split(d, d$chain_id)
  # the resamples are drawn first, in order, from the one seeded stream; the refits, which draw
  # nothing, then run on several cores (PG_CORES; by default at most four, each holding its own copy
  # of the model, so more cores need more memory), so the result does not
  # depend on how many there are
  picks <- lapply(seq_len(B), function(b)
    unlist(lapply(strata, function(s) s[sample.int(length(s), length(s), replace = TRUE)]), use.names = FALSE))
  one <- function(pick) {
    db <- do.call(rbind, lapply(seq_along(pick), function(i) {
      x <- by_id[[pick[i]]]
      x$chain_id <- paste0(pick[i], "#", i)
      # a place inside the chain (H7's class): a chain drawn twice is two chains, with its own places
      if (!is.null(nest)) x$place <- paste(x$chain_id, x[[nest]], sep = "|")
      x
    }))
    fit <- fit_or_error(glmmTMB(formula, data = db, family = family))
    if (inherits(fit, "fit_error")) rep(NA_real_, length(terms)) else unname(fixef(fit)$cond[terms])
  }
  got <- parallel::mclapply(picks, function(pk) tryCatch(one(pk), error = function(e) rep(NA_real_, length(terms))),
                            mc.cores = CORES)
  draws <- matrix(NA_real_, nrow = B, ncol = length(terms), dimnames = list(NULL, terms))
  for (b in seq_len(B)) if (is.numeric(got[[b]]) && length(got[[b]]) == length(terms)) draws[b, ] <- got[[b]]
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

# A rate ratio decided on the cluster bootstrap (22 November 2026): the term's estimate from the
# fit, its 95% percentile interval and one-sided p-values from the refits, as exp(); the Wald reading
# beside it. With one chain an arm a resample is the data again, so the Wald reading is what there
# is; so too when fewer than half the refits could be fitted. Either is recorded (`interval`).
boot_irr <- function(fit, formula, d, family, term, nest = NULL) {
  w <- irr(wald(fit, term))
  if (!is.null(w$error)) return(w)
  chains <- tapply(d$chain_id, as.character(d$arm), function(v) length(unique(v)))
  if (min(chains) < 2) return(c(w, list(interval = "wald: one chain in an arm")))
  draws <- cluster_boot(d, formula, family, term, spec$boot, nest)
  if (sum(!is.na(draws[, term])) < max(2, spec$boot / 2))
    return(c(w, list(interval = "wald: fewer than half the bootstrap refits could be fitted",
                     failed = sum(is.na(draws[, term])))))
  b <- boot_summary(fit, draws, term)
  c(b, list(irr = exp(b$estimate), irr_lower = exp(b$lower), irr_upper = exp(b$upper),
            level = 0.95, interval = "cluster bootstrap", wald = w))
}

# Several terms of one model from one cluster bootstrap (H5's and H7's arm contrasts, shaped as H4).
boot_irrs <- function(fit, formula, d, family, terms) {
  ws <- lapply(setNames(terms, terms), function(t) irr(wald(fit, t)))
  if (any(vapply(ws, function(w) !is.null(w$error), logical(1)))) return(ws)
  chains <- tapply(d$chain_id, as.character(d$arm), function(v) length(unique(v)))
  if (min(chains) < 2) return(lapply(ws, function(w) c(w, list(interval = "wald: one chain in an arm"))))
  draws <- cluster_boot(d, formula, family, terms, spec$boot)
  lapply(setNames(terms, terms), function(t) {
    if (sum(!is.na(draws[, t])) < max(2, spec$boot / 2))
      return(c(ws[[t]], list(interval = "wald: fewer than half the bootstrap refits could be fitted",
                             failed = sum(is.na(draws[, t])))))
    b <- boot_summary(fit, draws, t)
    c(b, list(irr = exp(b$estimate), irr_lower = exp(b$lower), irr_upper = exp(b$upper),
              level = 0.95, interval = "cluster bootstrap", wald = ws[[t]]))
  })
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

  # H2 (since 19 November 2026): a core draws code in. In the methods arm, per problem and host
  # whose code was bound there, the values of the place are of two kinds: the core, the values the
  # code was bound to, and the periphery, the rest the place then held (what stood by and what the
  # change introduced). Each kind with at least one value is a record: the later intrusions' uses
  # of its values, offset by the later checkpoints and by the number of values, so the count is a
  # rate per value. H2 is the rate ratio of the core to the periphery.
  core_long <- function(d, lev) {
    parts <- lapply(c("core", "periphery"), function(kind) {
      n <- d[[paste0(kind, "_", lev)]]
      x <- d[!is.na(n) & n > 0, ]
      if (nrow(x) == 0) return(NULL)
      x$uses <- x[[paste0("uses_", kind, "_", lev)]]
      x$core <- as.numeric(kind == "core")
      x$log_later <- log(x$later_checkpoints) + log(x[[paste0(kind, "_", lev)]])
      x
    })
    do.call(rbind, parts)
  }
  cored <- function(d, lev) {
    if (!paste0("core_", lev) %in% names(d)) return(list(fit = structure(
      list(msg = "core and periphery not measured"), class = "fit_error"), cp = FALSE, n = 0))
    long <- core_long(d, lev)
    if (is.null(long) || length(unique(long$core)) < 2 || sum(long$uses) == 0) return(list(fit = structure(
      list(msg = "no core and periphery to compare"), class = "fit_error"), cp = FALSE, n = 0))
    c(fit_cp(base(long, "uses", "core + "), long, nb), list(n = nrow(long)))
  }
  # H2 until 19 November 2026 (reported): the later intrusions bound to a value that stood by at
  # the placement, on the number that stood by, at the class (its fields) and at the method.
  drawn <- function(d, lev, term = paste0("bystanders_", lev), response = paste0("drawn_", lev)) {
    if (nrow(d) == 0 || length(unique(d[[term]])) < 2) return(list(fit = structure(
      list(msg = "the bystanders do not vary"), class = "fit_error"), cp = FALSE))
    fit_cp(base(d, response, paste0(term, " + ")), d, nb)
  }
  h2$log_by_class <- log1p(h2$bystanders_class)
  h2$log_by_method <- log1p(h2$bystanders_method)
  hm <- h2[h2$arm == spec$methods_arm, ]
  hf <- h2[h2$arm == spec$function_arm, ]
  res$H2 <- list(n = nrow(hm))
  for (lev in c("class", "method")) {
    term <- paste0("bystanders_", lev)
    mk <- cored(hm, lev)
    note(paste0("H2_", lev), mk)
    res$H2[[lev]] <- c(boot_irr(mk$fit, mk$formula, mk$data, nb, "core"), list(records = mk$n))
    res$reported[[paste0("H2_core_function_arm_", lev)]] <- irr(wald(cored(hf, lev)$fit, "core"))
    # reported: the core's width, its number of values per row (the sinew's width), per arm and over
    # the thirds of the stream
    width <- list()
    for (a in unique(as.character(h2$arm))) {
      w <- h2[as.character(h2$arm) == a & h2[[paste0("core_", lev)]] > 0, ]
      if (nrow(w) == 0) next
      third <- cut(w$cp, breaks = c(-Inf, quantile(h2$cp, c(1/3, 2/3)), Inf), labels = FALSE)
      width[[a]] <- list(rows = nrow(w), mean = mean(w[[paste0("core_", lev)]]),
                         median = median(w[[paste0("core_", lev)]]),
                         thirds = as.list(tapply(w[[paste0("core_", lev)]], factor(third, levels = 1:3), mean)))
    }
    res$reported[[paste0("H2_core_width_", lev)]] <- width
    md <- drawn(hm, lev)
    res$reported[[paste0("H2_bystanders_", lev)]] <- irr(wald(md$fit, term))
    # reported: per doubling-like step, log(1 + bystanders); and the function arm
    res$reported[[paste0("H2_log_", lev)]] <- wald(drawn(hm, lev, paste0("log_by_", lev))$fit, paste0("log_by_", lev))
    res$reported[[paste0("H2_function_arm_", lev)]] <- irr(wald(drawn(hf, lev)$fit, term))
    # reported (PLAN.md 4.3b): with what the change introduced there counted beside what stood by.
    # The later intrusions bound to either, on the number of both; a new method's own values are
    # then data it holds for later code, and it is no longer a row that can only read nought.
    left <- paste0("left_", lev)
    if (left %in% names(hm)) {
      res$reported[[paste0("H2_left_", lev)]] <-
        irr(wald(drawn(hm, lev, left, paste0("drawn_", lev, "_left"))$fit, left))
      res$reported[[paste0("H2_left_function_arm_", lev)]] <-
        irr(wald(drawn(hf, lev, left, paste0("drawn_", lev, "_left"))$fit, left))
    }
  }
  # reported: H2 at the class with every member the code was bound to in the core, private or not,
  # as until 22 November 2026 (the core is now its private part: PLAN.md 4.4, the author's decision)
  if ("core_class_all" %in% names(hm)) {
    res$reported$H2_class_all <- irr(wald(cored(hm, "class_all")$fit, "core"))
  }
  # reported: H2 at the class on its fields only (the class's methods not values), as it stood
  # until 19 November 2026, each later method still scored on its own
  if ("core_class_fields" %in% names(hm)) {
    res$reported$H2_class_fields <- irr(wald(cored(hm, "class_fields")$fit, "core"))
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
  # How much a core value is come back to, function arm against methods arm (H2's arm contrast): the
  # core's records of both arms, uses per value and later checkpoint, in the base model with the arm
  # term, decided on the cluster bootstrap. Needed at a level where each arm has at least MIN_CORE
  # core records; where the function arm forms too few cores to compare, that is reported and the
  # level's contrast is not needed. Where the function arm has the records and none of its core
  # values is ever come back to, no ratio can be fitted (it is nought): the arms' chains are then
  # compared by a rank-sum test on each chain's uses per value and later checkpoint.
  MIN_CORE <- 10
  reuse <- function(lev) {
    long <- if (paste0("core_", lev) %in% names(h2)) core_long(h2, lev) else NULL
    long <- if (is.null(long)) NULL else long[long$core == 1 & as.character(long$arm) %in% c(spec$methods_arm, spec$function_arm), ]
    if (is.null(long) || nrow(long) == 0) return(list(required = FALSE, error = "no core to compare"))
    fa <- as.character(long$arm) == spec$function_arm
    out <- list(records = nrow(long), function_records = sum(fa), methods_records = sum(!fa),
                function_uses = sum(long$uses[fa]), methods_uses = sum(long$uses[!fa]), min_records = MIN_CORE)
    if (sum(fa) < MIN_CORE || sum(!fa) < MIN_CORE)
      return(c(out, list(required = FALSE, note = "too few core records in an arm to compare")))
    if (out$methods_uses == 0) return(c(out, list(required = TRUE, error = "the methods arm's core is never come back to")))
    if (out$function_uses == 0) {
      rate <- tapply(long$uses, long$chain_id, sum) / tapply(exp(long$log_later), long$chain_id, sum)
      arm_of <- as.character(long$arm[match(names(rate), long$chain_id)])
      rf <- rate[arm_of == spec$function_arm]
      rm_ <- rate[arm_of == spec$methods_arm]
      if (length(rf) < 2 || length(rm_) < 2) return(c(out, list(required = TRUE, error = "one chain in an arm")))
      p <- suppressWarnings(wilcox.test(rf, rm_, alternative = "less", exact = FALSE)$p.value)
      return(c(out, list(required = TRUE, separated = TRUE, irr = 0, irr_lower = 0, irr_upper = 0,
                         p_less = p, p_greater = 1 - p,
                         interval = "rank-sum over chains: no core value of the function arm was come back to")))
    }
    long$arm <- droplevels(long$arm)
    m <- fit_cp(base(long, "uses"), long, nb)
    c(boot_irr(m$fit, m$formula, m$data, nb, FARM), out, list(required = TRUE))
  }
  # H4: for the same problems, the function arm's bound code is come back to less, at the class and
  # at the method (the base model without the bindings, which the arm itself changes)
  if (multi(as.character(h2$arm))) {
    for (lev in c("class", "method")) {
      ma <- fit_cp(base(h2, paste0("intrusion_", lev)), h2, nb)
      note(paste0("H4_intrusion_", lev), ma)
      res$H4[[paste0("intrusion_", lev)]] <- boot_irr(ma$fit, ma$formula, ma$data, nb, FARM)
      # reported beside it: how much a core value is come back to, function arm against methods
      # arm. The core's records of both arms (PLAN.md 4.4), uses per value; both arms solve the
      # same problems, so a core that is only the problems' shared data would be used alike.
      # Since 22 November 2026 this is part of H2's test (res$H2$reuse_*): within one arm a value
      # used once is likely to be used again whatever the place, so the core's advantage over the
      # periphery there can hardly fail; the arms solve the same problems with the same data, so a
      # core value come back to less in the function arm is the place, not the value's popularity.
      res$H2[[paste0("reuse_", lev)]] <- reuse(lev)
      res$reported[[paste0("core_reuse_", lev)]] <- res$H2[[paste0("reuse_", lev)]]
    }
  }
  if (isFALSE(spec$problem_fixed)) for (lev in c("class", "method"))
    res$H2[[paste0("reuse_", lev)]] <- list(required = FALSE, note = "a history: its arms do not solve the same problems")
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
  # reported, a sensitivity reading of H3 (22 November 2026): its measures with the literature's
  # coupling measures put back (fan-out, CBO, RFC), which the plan reads apart as reach
  h3s <- intersect(spec$h3_sensitivity, names(res$reported$literature_shape))
  res$reported$H3_with_coupling <- list(kept = h3s, margin = spec$margin,
                                        measures = res$reported$literature_shape[h3s])

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

# ---------------------------------------------------------------- H5: choice narrows
# Per bound host and level, the other places in the tree before the checkpoint that hold what the
# code was bound to there (PLAN.md 4.2a). In the methods arm, a negative binomial model of that count
# on the checkpoint index scaled from 0 (the first checkpoint) to 1 (the last), with the chain's
# intercept: exp(slope) is the ratio of the alternatives at the end of the stream to those at its
# start. H5 is a fall (22 November 2026): the ratio shown below 1, one-sided, at the class, by the
# cluster bootstrap; the method level is reported. A level where every placement was forced has no
# choice to narrow and is not testable. Since 24 November 2026 H5 also needs the arm contrast below.
# The reading against the upper margin (1.25, as H5 stood
# until then: a flat count passed) is reported. The share forced (no other place) is reported per
# arm and third; the function arm's slope and the arms' contrast too.
h5 <- read("h5.csv")
if (!is.null(h5) && nrow(h5) > 0) {
  h5$arm <- as_arm(h5$arm)
  span <- max(spec$checkpoints - 1, 1)
  h5$x <- if (isFALSE(spec$problem_fixed)) h5$cp else (h5$cp - 1) / span
  res$H5 <- list(margin = spec$margin)
  form5 <- function(d) as.formula(paste0("alternatives ~ x", if (multi(d$frontend)) " + frontend" else "",
                                         " + (1 | chain_id)"))
  fit5 <- function(d) {
    if (nrow(d) < 3 || length(unique(d$cp)) < 2) return(structure(list(msg = "too few rows"), class = "fit_error"))
    if (all(d$alternatives == 0)) return(structure(list(msg = "every placement forced"), class = "fit_error"))
    fit_or_error(glmmTMB(form5(d), data = d, family = nbinom2()))
  }
  for (lev in c("class", "method")) {
    d <- h5[h5$level == lev, ]
    dm <- d[d$arm == spec$methods_arm, ]
    df <- d[d$arm == spec$function_arm, ]
    forced <- function(x) if (nrow(x) == 0) NULL else list(rows = nrow(x), forced = mean(as.logical(x$forced)),
      mean_alternatives = mean(x$alternatives),
      thirds_forced = as.list(tapply(as.logical(x$forced), factor(cut(x$x, c(-Inf, 1/3, 2/3, Inf), labels = FALSE), levels = 1:3), mean)),
      thirds_alternatives = as.list(tapply(x$alternatives, factor(cut(x$x, c(-Inf, 1/3, 2/3, Inf), labels = FALSE), levels = 1:3), mean)))
    fm <- fit5(dm)
    res$H5[[lev]] <- c(boot_irr(fm, form5(dm), dm, nbinom2(), "x"), list(n = nrow(dm)),
                       if (inherits(fm, "fit_error")) list(note = fm$msg) else list(),
                       list(all_forced = nrow(dm) > 0 && all(dm$alternatives == 0)))
    # reported: against the upper margin, as H5 stood until 22 November 2026
    res$reported[[paste0("H5_margin_", lev)]] <- tost(fm, "x", spec$margin)
    res$reported[[paste0("H5_function_arm_", lev)]] <- irr(wald(fit5(df), "x"))
    res$reported[[paste0("H5_spread_", lev)]] <- list(methods = forced(dm), "function" = forced(df))
    if (multi(as.character(d$arm)) && !all(d$alternatives == 0)) {
      fa <- fit_or_error(glmmTMB(alternatives ~ x * arm + (1 | chain_id), data = d, family = nbinom2()))
      res$reported[[paste0("H5_arm_", lev)]] <- irr(wald(fa, FARM))
    }
    if (lev == "class") res$reported$H5_class_own <- mean(as.logical(dm$own), na.rm = TRUE)
    if (lev == "method") {
      res$reported$H5_method_untyped <- sum(dm$untyped, na.rm = TRUE)
      # reported: by type alone over the whole tree (as first built, 19 November 2026), the flow's
      # size, and how much of the call graph could be followed
      if ("by_type" %in% names(dm) && any(!is.na(dm$by_type))) {
        dt <- dm[!is.na(dm$by_type), ]
        dt$alternatives <- dt$by_type
        res$reported$H5_method_by_type <- irr(wald(fit5(dt), "x"))
        res$reported$H5_flow <- list(
          methods = as.list(tapply(d$flow_methods, as.character(d$arm), mean, na.rm = TRUE)),
          by_type = as.list(tapply(d$by_type, as.character(d$arm), mean, na.rm = TRUE)),
          followed = sum(d$calls_followed, na.rm = TRUE) / max(sum(d$calls_to_app_names, na.rm = TRUE), 1))
      }
    }
  }
}

# H5's arm contrast (24 November 2026, PLAN.md 9 row 92): per checkpoint and chain, the placements
# forced at the class (bound there with no other place to go). A negative binomial mixed model on the
# arm, the checkpoint index centred at the middle of the stream and scaled to its length, and their
# interaction, with the chain's and the checkpoint's intercepts (Poisson where the negative binomial
# cannot be fitted, recorded). The function arm's rate half-way through below 1, **and** its
# interaction with the index below 1 (forcing rises less), both from one cluster bootstrap. Corpus A
# only: on a history the arms do not solve the same problems.
hf <- read("h5_forced.csv")
if (!is.null(res$H5) && !isFALSE(spec$problem_fixed)) {
  if (is.null(hf) || nrow(hf) == 0 || !multi(hf$arm)) {
    res$H5$contrast <- list(error = "no checkpoints in both arms")
  } else {
    hf <- hf[as.character(hf$arm) %in% c(spec$methods_arm, spec$function_arm), ]
    hf$arm <- droplevels(as_arm(as.character(hf$arm)))
    hf$cp_c <- (hf$cp - (max(spec$checkpoints, 1) + 1) / 2) / max(spec$checkpoints - 1, 1)
    per5 <- as.list(tapply(hf$forced_class, as.character(hf$arm), mean))
    if (all(hf$forced_class == 0)) {
      res$H5$contrast <- list(error = "no placement forced at the class in either arm", mean = per5)
    } else {
      fixed5 <- paste0("forced_class ~ cp_c * arm", if (multi(hf$frontend)) " + frontend" else "")
      m5 <- fit_cp(fixed5, hf, nbinom2())
      fam5 <- nbinom2()
      ok5 <- function(m) !inherits(m$fit, "fit_error") && isTRUE(m$fit$sdr$pdHess) &&
        all(is.finite(summary(m$fit)$coefficients$cond[, "Std. Error"]))
      if (!ok5(m5)) {
        m5 <- fit_cp(fixed5, hf, poisson())
        fam5 <- poisson()
      }
      T5 <- paste0("cp_c:", FARM)
      b5 <- boot_irrs(m5$fit, m5$formula, m5$data, fam5, c(FARM, T5))
      res$H5$contrast <- list(arm = b5[[FARM]], trend = b5[[T5]], n = nrow(hf), family = fam5$family,
                              checkpoint_intercept = m5$cp, mean = per5,
                              methods_rise = irr(wald(m5$fit, "cp_c")))
    }
  }
}

# ---------------------------------------------------------------- H6: spread does not see it
# Per unit that placed or edited code in a class that existed before it, those classes beyond the
# first (spread; a new class is a free choice and is not counted; PLAN.md 4.2b). H6's test, in the
# methods arm: a negative binomial model of the spread on whether a placement in the unit was forced
# at the class, with the index scaled from 0 to 1 and the chain's intercept (forced: the ratio of the
# spread of a forced unit to one that was not, at the same point in the stream), one-sided below the
# upper margin (restated 21 November 2026; until then one-sided above 1).
# Reported: the spread's rise over the stream (exp(slope), end against start) over all units, and in
# forced and in unforced units apart. A model that cannot be fitted as negative binomial (a spread
# with less variance than its mean) is fitted as Poisson, and that is recorded. Reported too: the
# spread per arm and third, the function arm's forced ratio and rise, the arms' contrast, and, on
# the pairs of classes changed together, their coupling (the calls between them before the unit) on
# the index, the pair's intercept in the chain's. Every H6 model holds the change's size fixed:
# log(1 + positions it added) and log(1 + methods it placed or edited code in) (20 November 2026,
# after a forced unit was seen to be a larger change); the forced ratio without them is reported.
SIZE <- function(d) if (all(c("positions", "methods") %in% names(d))) " + log1p(positions) + log1p(methods)" else ""
h6 <- read("h6.csv")
if (!is.null(h6) && nrow(h6) > 0) {
  h6$arm <- as_arm(h6$arm)
  span6 <- max(spec$checkpoints - 1, 1)
  h6$x <- if (isFALSE(spec$problem_fixed)) h6$cp else (h6$cp - 1) / span6
  h6$forced <- as.numeric(as.logical(h6$forced))
  res$H6 <- list()
  fit6 <- function(d, rhs) {
    if (nrow(d) < 3 || length(unique(d$cp)) < 2) return(list(fit = structure(list(msg = "too few rows"), class = "fit_error")))
    if (all(d$spread == 0)) return(list(fit = structure(list(msg = "every change in one class"), class = "fit_error")))
    if (grepl("forced", rhs) && length(unique(d$forced)) < 2) return(list(fit = structure(list(msg = "forced does not vary"), class = "fit_error")))
    fe <- if (multi(d$frontend)) " + frontend" else ""
    f <- as.formula(paste0("spread ~ ", rhs, fe, " + (1 | chain_id)"))
    nb <- fit_or_error(glmmTMB(f, data = d, family = nbinom2()))
    ok <- !inherits(nb, "fit_error") && isTRUE(nb$sdr$pdHess)
    if (ok) return(list(fit = nb, family = "nbinom2"))
    list(fit = fit_or_error(glmmTMB(f, data = d, family = poisson())), family = "poisson")
  }
  one <- function(m, term, n) c(irr(wald(m$fit, term)), list(n = n, family = m$family))
  dm <- h6[h6$arm == spec$methods_arm, ]
  df <- h6[h6$arm == spec$function_arm, ]
  sz <- SIZE(h6)
  # H6's test (restated 21 November 2026, PLAN.md 9 row 67): spread does not see the force. The
  # forced ratio shown below the upper margin (1.25), one-sided with the 90% interval, as H3.
  res$H6$margin <- spec$margin
  m6 <- fit6(dm, paste0("x + forced", sz))
  res$H6$forced <- c(tost(m6$fit, "forced", spec$margin), list(n = nrow(dm), family = m6$family))
  res$reported$H6_forced_without_size <- one(fit6(dm, "x + forced"), "forced", nrow(dm))
  if ("forced_bind" %in% names(dm)) {     # forced by binding with no alternative (H5's), reported
    db <- dm
    db$forced <- as.numeric(as.logical(db$forced_bind))
    res$reported$H6_forced_bind <- one(fit6(db, paste0("x + forced", sz)), "forced", nrow(db))
  }
  res$reported$H6_rise <- one(fit6(dm, paste0("x", sz)), "x", nrow(dm))
  res$reported$H6_rise_forced <- one(fit6(dm[dm$forced == 1, ], paste0("x", sz)), "x", sum(dm$forced == 1))
  res$reported$H6_rise_unforced <- one(fit6(dm[dm$forced == 0, ], paste0("x", sz)), "x", sum(dm$forced == 0))
  res$reported$H6_function_arm <- irr(wald(fit6(df, paste0("x", sz))$fit, "x"))
  res$reported$H6_function_arm_forced <- irr(wald(fit6(df, paste0("x + forced", sz))$fit, "forced"))
  thirds <- function(x) if (nrow(x) == 0) NULL else list(units = nrow(x),
    mean_classes = mean(x$classes), multi = mean(x$classes > 1), forced = mean(x$forced),
    thirds_classes = as.list(tapply(x$classes, factor(cut(x$x, c(-Inf, 1/3, 2/3, Inf), labels = FALSE), levels = 1:3), mean)),
    thirds_multi = as.list(tapply(x$classes > 1, factor(cut(x$x, c(-Inf, 1/3, 2/3, Inf), labels = FALSE), levels = 1:3), mean)),
    thirds_forced = as.list(tapply(x$classes[x$forced == 1], factor(cut(x$x[x$forced == 1], c(-Inf, 1/3, 2/3, Inf), labels = FALSE), levels = 1:3), mean)),
    thirds_unforced = as.list(tapply(x$classes[x$forced == 0], factor(cut(x$x[x$forced == 0], c(-Inf, 1/3, 2/3, Inf), labels = FALSE), levels = 1:3), mean)),
    all_classes = if ("all_classes" %in% names(x)) mean(x$all_classes) else NULL,
    classes_forced = if (any(x$forced == 1)) mean(x$classes[x$forced == 1]) else NULL,
    classes_not_forced = if (any(x$forced == 0)) mean(x$classes[x$forced == 0]) else NULL)
  res$reported$H6_spread <- list(methods = thirds(dm), "function" = thirds(df))
  if (multi(as.character(h6$arm)) && !all(h6$spread == 0)) {
    fa <- fit_or_error(glmmTMB(as.formula(paste0("spread ~ x * arm", sz, " + (1 | chain_id)")), data = h6, family = nbinom2()))
    res$reported$H6_arm <- irr(wald(fa, FARM))
  }
  pairs <- read("pairs.csv")
  if (!is.null(pairs) && nrow(pairs) > 0) {
    pairs$x <- if (isFALSE(spec$problem_fixed)) pairs$cp else (pairs$cp - 1) / span6
    pm <- pairs[pairs$arm == spec$methods_arm & as.logical(pairs$in_tree), ]
    again <- pm[pm$pair %in% pm$pair[duplicated(pm$pair)], ]
    res$reported$H6_pair_coupling <- if (nrow(again) < 3 || length(unique(again$cp)) < 2 || all(again$coupling == 0))
      list(error = "too few pairs changed together more than once") else {
      # refitted without the chain's intercept where its standard error is not computed (PLAN.md 9
      # row 88: on the development histories two chains carry it), as H3's class measures are
      w <- wald(fit_or_error(glmmTMB(coupling ~ x + (1 | chain_id) + (1 | pair), data = again, family = nbinom2())), "x")
      kept <- is.null(w$error)
      if (!kept) w <- wald(fit_or_error(glmmTMB(coupling ~ x + (1 | pair), data = again, family = nbinom2())), "x")
      c(irr(w), list(n = nrow(again), pairs = length(unique(again$pair)), chain_intercept = kept))
    }
  }
}

# ---------------------------------------------------------------- calls across the encapsulation (H8)
# Per unit and class that existed before it that the unit changed, the calls across the class's
# boundary the unit added, outward and inward (coupled; PLAN.md 4.2c). H8's *dispersion stronger*
# (Run D, PLAN.md 3.1a): the arms against each other in the calls added, at the same point in the
# stream (the index scaled from 0 to 1) and change size (log(1 + positions added there), log(1 +
# methods changed there)), forced not in the model (the instruction changes what is forced), with
# the chain's intercept and the class's within the chain, decided on the cluster bootstrap; Poisson
# where the negative binomial cannot be fitted, recorded. (Until 24 November 2026 the old H7,
# *forced changes couple*, was read on these rows too; deleted, PLAN.md 9 row 90.)
h7 <- read("calls_across.csv")
if (!is.null(h7) && nrow(h7) > 0) {
  h7$arm <- as_arm(h7$arm)
  span7 <- max(spec$checkpoints - 1, 1)
  h7$x <- if (isFALSE(spec$problem_fixed)) h7$cp else (h7$cp - 1) / span7
  h7$forced <- as.numeric(as.logical(h7$forced))
  if ("class" %in% names(h7)) h7$place <- paste(h7$chain_id, h7$class, sep = "|")
  fit7 <- function(d, y, rhs) {
    if (nrow(d) < 3 || length(unique(d$cp)) < 2) return(list(fit = structure(list(msg = "too few rows"), class = "fit_error")))
    if (all(d[[y]] == 0)) return(list(fit = structure(list(msg = paste("no", y)), class = "fit_error")))
    if (grepl("forced", rhs) && length(unique(d$forced)) < 2) return(list(fit = structure(list(msg = "forced does not vary"), class = "fit_error")))
    fe <- if (multi(d$frontend)) " + frontend" else ""
    f <- as.formula(paste0(y, " ~ ", rhs, fe, " + (1 | chain_id)"))
    good <- function(m) !inherits(m, "fit_error") && isTRUE(m$sdr$pdHess) &&
      all(is.finite(summary(m)$coefficients$cond[, "Std. Error"]))
    if ("place" %in% names(d) && length(unique(d$place)) > length(unique(d$chain_id))) {
      fp <- as.formula(paste0(y, " ~ ", rhs, fe, " + (1 | chain_id) + (1 | place)"))
      nbp <- fit_or_error(glmmTMB(fp, data = d, family = nbinom2()))
      if (good(nbp)) return(list(fit = nbp, family = "nbinom2", formula = fp, fam = nbinom2(),
                                 class_intercept = TRUE, data = d))
    }
    nb <- fit_or_error(glmmTMB(f, data = d, family = nbinom2()))
    if (good(nb)) return(list(fit = nb, family = "nbinom2", formula = f, fam = nbinom2(),
                              class_intercept = FALSE, data = d))
    list(fit = fit_or_error(glmmTMB(f, data = d, family = poisson())), family = "poisson", formula = f,
         fam = poisson(), class_intercept = FALSE, data = d)
  }
  sz7 <- SIZE(h7)
  if (multi(as.character(h7$arm)) && !all(h7$coupled == 0)) {
    ha <- h7
    ha$arm <- droplevels(ha$arm)
    mc <- fit7(ha, "coupled", paste0("x + arm", sz7))
    res$coupled_arm <- c(
      if (is.null(mc$formula)) irr(wald(mc$fit, FARM)) else
        boot_irr(mc$fit, mc$formula, mc$data, mc$fam, FARM, nest = if (isTRUE(mc$class_intercept)) "class" else NULL),
      list(n = nrow(ha), family = mc$family, class_intercept = isTRUE(mc$class_intercept)))
  }
}

# ---------------------------------------------------------------- H7: surface against volume
# Restated 24 November 2026 (PLAN.md §2, §4.2c, §9 row 89; the author's). The volume is the logic a
# checkpoint added (the essential complexity: the statements of method bodies, §4.9); the surface
# is the links it added between blocks of logic (the accidental complexity of getting them run and
# supplied with data): call links, state links and the wiring's flow links, each counted once,
# injection not among them. A negative binomial mixed model of the links added on the arm, the
# checkpoint index centred at the middle of the stream and scaled to its length, their interaction,
# and log(1 + logic added), with the chain's and the checkpoint's intercepts. Shaped as H4: the
# function arm's ratio half-way through below 1 (fewer links for the same logic), **and** its
# interaction with the index below 1 (the gap widens over the stream). Both from one cluster
# bootstrap (chains resampled within arm). Reported: each kind of link apart, the same model
# without the logic, and the methods arm's own rise over the stream.
lk <- read("h7.csv")
if (isFALSE(spec$problem_fixed)) {
  res$H7 <- list(not_applicable = TRUE)       # a history: no arms solving the same problems
} else if (is.null(lk) || nrow(lk) == 0 || !multi(lk$arm)) {
  res$H7 <- list(error = "no links measured in both arms")
} else {
  lk <- lk[as.character(lk$arm) %in% c(spec$methods_arm, spec$function_arm), ]
  lk$arm <- droplevels(as_arm(as.character(lk$arm)))
  lk$cp_c <- (lk$cp - (max(spec$checkpoints, 1) + 1) / 2) / max(spec$checkpoints - 1, 1)
  fe_l <- if (multi(lk$frontend)) " + frontend" else ""
  TREND <- paste0("cp_c:", FARM)
  ml <- fit_cp(paste0("links_added ~ cp_c * arm + log1p(logic_added)", fe_l), lk, nbinom2())
  note("H7", ml)
  per <- function(y) as.list(tapply(lk[[y]], as.character(lk$arm), mean))
  b <- boot_irrs(ml$fit, ml$formula, ml$data, nbinom2(), c(FARM, TREND))
  res$H7 <- list(arm = b[[FARM]], trend = b[[TREND]], n = nrow(lk), checkpoint_intercept = ml$cp,
                 links_added = per("links_added"), logic_added = per("logic_added"))
  kind <- function(y) {
    if (any(unlist(per(y)) == 0)) return(list(error = paste("no", y, "in an arm"), mean = per(y)))
    m <- fit_cp(paste0(y, " ~ cp_c * arm + log1p(logic_added)", fe_l), lk, nbinom2())$fit
    list(arm = irr(wald(m, FARM)), trend = irr(wald(m, TREND)), mean = per(y))
  }
  res$reported$H7_kinds <- lapply(c(call = "call_links_added", state = "state_links_added",
                                    flow = "flow_links_added", lost = "links_lost"), kind)
  mn <- fit_cp(paste0("links_added ~ cp_c * arm", fe_l), lk, nbinom2())$fit
  res$reported$H7_without_logic <- list(arm = irr(wald(mn, FARM)), trend = irr(wald(mn, TREND)))
  res$reported$H7_methods_rise <- irr(wald(ml$fit, "cp_c"))
  res$reported$H7_logic <- irr(wald(ml$fit, "log1p(logic_added)"))
}

# ---------------------------------------------------------------- surface against volume (reported)
# A class's surface (calls out of and into it) against its volume (its methods), PLAN.md 4.2e, per
# arm: across the classes of each chain's last tree, log(1 + surface) on log(methods) with the
# chain's intercept (the exponent across classes); and within a class over the units that changed
# it, the same on log(methods) centred on the class's mean, with the class's mean beside it (the
# exponent as a class grows). Below 1, surface grows slower than volume (concentration saves
# communication); above 1, faster. And per change: the surface it added against the methods it
# added, forced against unforced, at the same volume added (Gaussian, the chain's intercept).
sf <- read("surface.csv")
if (!is.null(sf) && nrow(sf) > 0) {
  sf$arm <- as.character(sf$arm)
  res$reported$surface <- list()
  for (a in unique(sf$arm)) {
    cs <- sf[sf$arm == a & as.logical(sf$cross_section) & sf$methods_before > 0, ]
    ch <- sf[sf$arm == a & !as.logical(sf$cross_section) & sf$methods_before > 0 & !is.na(sf$methods_after), ]
    r <- list()
    r$across <- if (nrow(cs) >= 5 && length(unique(cs$methods_before)) > 1)
      c(wald(fit_or_error(glmmTMB(log1p(surface_before) ~ log(methods_before) + (1 | chain_id), data = cs)),
             "log(methods_before)"), list(classes = nrow(cs))) else list(error = "too few classes")
    if (nrow(ch) >= 5) {
      ch$lm <- log(ch$methods_before)
      ch$lm_mean <- ave(ch$lm, ch$class)
      ch$lm_c <- ch$lm - ch$lm_mean
      ch$d_surface <- ch$surface_after - ch$surface_before
      ch$d_methods <- ch$methods_after - ch$methods_before
      ch$forced <- as.numeric(as.logical(ch$forced))
      r$within <- if (length(unique(ch$class)) < nrow(ch) && sd(ch$lm_c) > 0)
        c(wald(fit_or_error(glmmTMB(log1p(surface_before) ~ lm_c + lm_mean + (1 | chain_id), data = ch)), "lm_c"),
          list(rows = nrow(ch), classes = length(unique(ch$class)))) else list(error = "no class changed twice at different sizes")
      r$added_forced <- if (length(unique(ch$forced)) > 1)
        c(wald(fit_or_error(glmmTMB(d_surface ~ forced + d_methods + (1 | chain_id), data = ch)), "forced"),
          list(rows = nrow(ch))) else list(error = "forced does not vary")
      r$per_change <- list(
        forced = if (any(ch$forced == 1)) list(surface_added = mean(ch$d_surface[ch$forced == 1]), methods_added = mean(ch$d_methods[ch$forced == 1])) else NULL,
        unforced = if (any(ch$forced == 0)) list(surface_added = mean(ch$d_surface[ch$forced == 0]), methods_added = mean(ch$d_methods[ch$forced == 0])) else NULL)
    }
    res$reported$surface[[a]] <- r
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
# H4's symmetric count (22 November 2026): how well-trodden the files a change went back into were.
# Per checkpoint, for each file that existed and that it changed, production Java and wiring alike,
# bound or not, the earlier checkpoints of the chain that had created or changed that file, summed.
# The methods arm's return to its handler and the function arm's return to its wiring are counted
# alike, and going back into several files touched once before does not count as going back into
# one that every problem has been put in. A negative binomial mixed model on the arm with the
# chain's and the checkpoint's intercepts, decided on the cluster bootstrap; the function arm's
# ratio has to lie below 1. As first built that day (reported): the plain number of existing files
# gone back into, a Poisson model, which counts a change spread over small files as more.
files_model <- function(col, family, cols) {
  if (isFALSE(spec$problem_fixed)) return(list(not_applicable = TRUE))
  if (is.null(reopen) || !col %in% names(reopen) || all(is.na(reopen[[col]])))
    return(list(error = paste(col, "was not measured")))
  d <- reopen[!is.na(reopen[[col]]) & as.character(reopen$arm) %in% c(spec$methods_arm, spec$function_arm), ]
  d$arm <- droplevels(as_arm(as.character(d$arm)))
  if (all(d[[col]] == 0)) return(list(error = paste("no", col)))
  m <- fit_cp(paste0(col, " ~ arm", if (multi(d$frontend)) " + frontend" else ""), d, family)
  per <- function(x) as.list(tapply(d[[x]], as.character(d$arm), mean))
  c(boot_irr(m$fit, m$formula, m$data, family, FARM),
    list(n = nrow(d), mean = per(col), java = per(cols[1]), wiring = per(cols[2]), checkpoint_intercept = m$cp))
}
res$H4$trodden <- files_model("trodden", nbinom2(), c("trodden_java", "trodden_wiring"))
res$reported$existing_files <- files_model("existing_files", poisson(), c("existing_java_files", "existing_wiring_files"))

# ---------------------------------------------------------------- logic and organisation (reported)
# PLAN.md 4.9: per checkpoint and chain, the code a change added as logic (body statements) and as
# organisation (accessors and constructor wiring in bodies; declarations outside them; the wiring),
# and the state it handed along (the parameters of new methods, the values callers pass them, the
# values and fields it introduces). The arms solve the same problems, so the logic is predicted the
# same (its ratio inside the margin, 0.8 to 1.25, by the two one-sided tests) and the state handed
# along lower in the function arm (below 1) and flatter over the stream. Each a negative binomial
# mixed model on the arm with the chain's and the checkpoint's intercepts, Wald intervals; the
# trend is the arm's interaction with the checkpoint index centred at the middle of the stream.
sp <- read("split.csv")
if (!is.null(sp) && nrow(sp) > 0 && multi(sp$arm)) {
  sp$arm <- as_arm(sp$arm)
  sp <- sp[as.character(sp$arm) %in% c(spec$methods_arm, spec$function_arm), ]
  sp$arm <- droplevels(sp$arm)
  sp$cp_c <- (sp$cp - (max(spec$checkpoints, 1) + 1) / 2) / max(spec$checkpoints - 1, 1)
  fe_s <- if (multi(sp$frontend)) " + frontend" else ""
  part <- function(y) {
    per <- as.list(tapply(sp[[y]], as.character(sp$arm), mean))
    # none at all in an arm (a wired function's parameters in the methods arm): no ratio to fit
    if (any(unlist(per) == 0)) return(list(error = paste("no", y, "in an arm"), mean = per))
    m <- fit_cp(paste0(y, " ~ arm", fe_s), sp, nbinom2())$fit
    mt <- fit_cp(paste0(y, " ~ cp_c * arm", fe_s), sp, nbinom2())$fit
    c(tost(m, FARM, spec$margin), list(level_95 = irr(wald(m, FARM)), trend = irr(wald(mt, paste0("cp_c:", FARM))),
                                        mean = as.list(tapply(sp[[y]], as.character(sp$arm), mean))))
  }
  parts <- c(logic = "logic_added", organisation_in_bodies = "organisation_added",
             declarations = "declaration_lines_added", imports = "import_lines_added",
             organisation_all = "organisation_all", params_new_methods = "params_new_methods",
             params_called_methods = "params_called_methods", params_wired_functions = "params_wired_functions",
             new_called_methods = "new_called_methods", birth_binding = "birth_binding",
             method_values_added = "method_values_added", fields_added = "fields_added",
             logic_existing_methods = "logic_existing_methods", logic_new_called_methods = "logic_new_called_methods",
             logic_new_wired_functions = "logic_new_wired_functions", existing_methods_edited = "existing_methods_edited",
             new_wired_functions = "new_wired_functions")
  parts <- parts[parts %in% names(sp)]
  res$reported$split <- lapply(parts, part)
  res$reported$split$wiring_lines <- as.list(tapply(sp$wiring_lines_added, as.character(sp$arm), mean))
}

# ---------------------------------------------------------------- encapsulation and the reader (reported)
# PLAN.md 4.2f, 5: whether the author (on a history, declared agent commits against people) makes
# fewer members private, has less growth arriving forced, opens more members and lets classes grow
# larger, at the same system size and change size, and whether the difference changes with the
# system's size (log tokens, centred; the author x size interaction). Modelled on the histories only
# (spec$reader_models); corpus A reports the four measures per arm. Each model has the
# repository's (chain's) intercept. Reported: the author contrast (odds or rate ratio, 95% Wald)
# at the centre of log tokens, and the interaction per unit of log tokens (an e-fold larger system).
ru <- read("reader_units.csv")
rc <- read("reader_classes.csv")
if (isTRUE(spec$reader_models) && !is.null(ru) && nrow(ru) > 0 && multi(ru$arm)) {
  rr <- list()
  centre <- mean(log(ru$tokens[!is.na(ru$tokens) & ru$tokens > 0]))
  prep <- function(d) {
    d <- d[!is.na(d$tokens) & d$tokens > 0, ]
    d$arm <- as_arm(d$arm)
    d$ltok <- log(d$tokens) - centre
    d
  }
  two <- function(f, d, family, label) {
    if (nrow(d) < 10 || !multi(as.character(d$arm)))
      return(list(error = paste("too few rows:", label)))
    m <- fit_or_error(glmmTMB(f, data = d, family = family))
    list(author = irr(wald(m, FARM)), interaction = irr(wald(m, paste0(FARM, ":ltok"))),
         size = irr(wald(m, "ltok")), n = nrow(d), repositories = length(unique(d$chain_id)))
  }
  SZ <- " + log1p(positions) + log1p(methods)"
  u <- prep(ru)
  u1 <- u[!is.na(u$introduced) & u$introduced > 0, ]
  u1$kept <- u1$introduced - u1$private
  rr$private <- two(as.formula(paste0("cbind(private, kept) ~ arm * ltok", SZ, " + (1 | chain_id)")),
                    u1, binomial(), "private share")
  u2 <- u[u$existing_positions > 0, ]
  u2$free <- u2$existing_positions - u2$forced_positions
  rr$forced <- two(as.formula(paste0("cbind(forced_positions, free) ~ arm * ltok", SZ, " + (1 | chain_id)")),
                   u2, binomial(), "forced share")
  if (!is.null(rc) && nrow(rc) > 0) {
    cl <- prep(rc)
    rr$opened <- two(as.formula(paste0("opened ~ arm * ltok", SZ, " + (1 | chain_id)")), cl, nbinom2(), "opened")
    c4 <- cl[!is.na(cl$methods_before), ]
    rr$class_methods <- two(as.formula(paste0("methods_before ~ arm * ltok", SZ, " + (1 | chain_id)")),
                            c4, nbinom2(), "class size")
  }
  rr$centre_tokens <- exp(centre)
  res$reported$reader <- rr
}

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
writeLines(toJSON(res, auto_unbox = TRUE, digits = NA, null = "null", na = "null", pretty = TRUE),
           out)
cat("wrote", out, "\n")
