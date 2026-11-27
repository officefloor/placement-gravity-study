#!/usr/bin/env Rscript
# Power of the four confirmatory hypotheses at the ui primary's design (PLAN.md §7, *Power for the
# confirmatory four*; §9 row 129). Reads no run named for analysis: only the development analysis
# (`data/analysis/pilot/`, the petclinic development chain, and `results/analysis/pilot/estimates.json`).
#
# How. For each part a hypothesis needs, the registered model is fitted to the development chain's
# rows, which gives its baseline: every coefficient, the dispersion and the checkpoint's spread.
# New data are then drawn at the ui primary's design, two front ends of ten chains each in each arm
# (20 chains an arm) over 250 checkpoints: each simulated chain resamples its arm's development rows,
# stretched from 60 checkpoints to 250 (four times as many rows), with a level of its own for the
# chain (sd_chain, which one chain an arm cannot estimate, so it is varied) and a level for each
# checkpoint that every chain shares (the same problem). The coefficients the part tests are set to
# the scenario's effect; the rest keep the development chain's values. The same model is fitted to
# each draw and the part passes where its one-sided 95% Wald interval lies on the predicted side.
#
# What it does not do. The test proper is on the cluster bootstrap (1,000 refits); here a part is
# read on its Wald interval with the chain's intercept in the model, which is cheaper by a thousand
# times and, with ten chains a stratum, about as wide (§7, *The bootstrap is over few chains*).
# The parts of one hypothesis are drawn apart, so their joint pass assumes they are independent.
# Counts that grow with the stream (how well-trodden a file is) are scaled only by the number of
# rows, not by the longer history. So the figures are a guide, not a promise.
#
# Scenarios: "dev", every tested coefficient at the development chain's estimate (H1's trend and
# H5 point the wrong way there, so they are expected to fail); and the ratios 0.8, 0.67 and 0.5 for
# every tested part (above 1 for H2's core against periphery: 1.25, 1.5, 2), a trend given as the
# ratio from the start of the stream to its end. Each with sd_chain 0.2 and 0.5.
# A hypothesis passes when every part passes. Its p is the largest of its parts, Holm-corrected over
# four: so it is shown at a part's alpha of 0.05 (the hypothesis whose p is the smallest of the four
# after the other three have passed) and 0.0125 (the first step of Holm, 0.05 / 4).
#
# Run: Rscript analysis/power.R [out_dir]   (default results/power). Environment: PG_CORES (default
# 4; each core holds its own copy of a model), POWER_REPS (default 100 a scenario), POWER_ONLY (a
# comma list of scenario names, for a quick try). Writes power.json and POWER.md after each scenario.

suppressPackageStartupMessages({
  library(glmmTMB)
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)
OUT <- if (length(args) >= 1) args[1] else "results/power"
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)
DEV <- "data/analysis/pilot"
EST <- fromJSON("results/analysis/pilot/estimates.json", simplifyVector = FALSE)
CORES <- suppressWarnings(as.integer(Sys.getenv("PG_CORES", "")))
if (is.na(CORES) || CORES < 1) CORES <- min(4L, parallel::detectCores())
REPS <- suppressWarnings(as.integer(Sys.getenv("POWER_REPS", "")))
if (is.na(REPS) || REPS < 1) REPS <- 100L
ONLY <- strsplit(Sys.getenv("POWER_ONLY", ""), ",")[[1]]
SEED <- 20261127
DEV_CP <- 60          # the development chain's checkpoints
CP <- 250             # the ui primary's
CHAINS <- 10          # a stack's chains
FRONTENDS <- c("angular", "tanstack")
M <- "spring"
F <- "officefloor"
FARM <- paste0("arm", F)

rd <- function(f) read.csv(file.path(DEV, f), stringsAsFactors = FALSE)
lgl <- function(x) as.logical(x) %in% TRUE | x %in% c("1", 1)

# ---------------------------------------------------------------- the parts, as analyse.R reads them

# the base model of intrusion (analyse.R, base()): the problem held fixed, the host's size
base_rhs <- function(d, lead = "") paste0(lead, "log_size + declared_crossings + log_host",
                                         if (length(unique(d$host_new)) > 1) " + host_new" else "")
prep_h2 <- function(d) {
  d <- d[d$later_checkpoints > 0 & lgl(d$bound), ]
  d$log_size <- log1p(d$addition_positions)
  d$log_host <- log1p(d$pre_positions)
  d$host_new <- as.numeric(lgl(d$host_new))
  d
}
# core and periphery records (analyse.R, core_long()): one per kind with a value; the offset is the
# later checkpoints times the number of values; `n_values` kept so the offset can be rebuilt
core_long <- function(d, lev) {
  do.call(rbind, lapply(c("core", "periphery"), function(kind) {
    n <- d[[paste0(kind, "_", lev)]]
    x <- d[!is.na(n) & n > 0, ]
    if (nrow(x) == 0) return(NULL)
    x$uses <- x[[paste0("uses_", kind, "_", lev)]]
    x$core <- as.numeric(kind == "core")
    x$n_values <- x[[paste0(kind, "_", lev)]]
    x
  }))
}
# each part: its template rows (both arms or one), the response, the fixed part of the model, the
# family, its offset, the tested terms with their direction ("less": below 1; "greater": above 1),
# and where each tested term's development estimate is read
cpc_scaled <- function(cp, n) (cp - (n + 1) / 2) / max(n - 1, 1)
h2raw <- prep_h2(rd("h2.csv"))
PARTS <- list(
  H1_arm_trend = list(
    hyp = "H1", data = rd("h1_forced.csv"), y = "forced_class", rhs = "cp_c * arm", family = "nbinom2",
    cp_c = "scaled",
    terms = list(list(term = FARM, dir = "less", dev = EST$H1$contrast$arm$estimate),
                 list(term = paste0("cp_c:", FARM), dir = "less", dev = EST$H1$contrast$trend$estimate, trend = TRUE))),
  H4_bystanders = list(
    hyp = "H4", data = transform(rd("by.csv"), y = log1p(bystanders)), y = "y", rhs = "cp_c * arm",
    family = "gaussian", cp_c = "unscaled",
    # analyse.R centres the index on the middle without scaling it: the slope is a checkpoint's. A
    # scenario's trend is the ratio over the stream, so it is spread over the 249 steps of the ui's.
    terms = list(list(term = FARM, dir = "less", dev = EST$H4$arm$estimate),
                 list(term = paste0("cp_c:", FARM), dir = "less", dev = EST$H4$slope$estimate * (DEV_CP - 1),
                      trend = TRUE, per_step = TRUE))),
  H4_intrusion_class = list(
    hyp = "H4", data = h2raw, y = "intrusion_class", rhs = paste0(base_rhs(h2raw), " + arm"), family = "nbinom2",
    offset = "later", terms = list(list(term = FARM, dir = "less", dev = EST$H4$intrusion_class$estimate))),
  H4_intrusion_method = list(
    hyp = "H4", data = h2raw, y = "intrusion_method", rhs = paste0(base_rhs(h2raw), " + arm"), family = "nbinom2",
    offset = "later", terms = list(list(term = FARM, dir = "less", dev = EST$H4$intrusion_method$estimate))),
  H4_trodden = list(
    hyp = "H4", data = rd("reopen.csv"), y = "trodden", rhs = "arm", family = "nbinom2",
    terms = list(list(term = FARM, dir = "less", dev = EST$H4$trodden$estimate))),
  H5_arm_trend = list(
    hyp = "H5", data = rd("h5.csv"), y = "weight_added", rhs = "cp_c * arm + log1p(logic_added)",
    family = "nbinom2", cp_c = "scaled",
    terms = list(list(term = FARM, dir = "less", dev = EST$H5$arm$estimate),
                 list(term = paste0("cp_c:", FARM), dir = "less", dev = EST$H5$trend$estimate, trend = TRUE))),
  H2_core_class = list(
    hyp = "H2", data = core_long(h2raw[h2raw$arm == M, ], "class"), y = "uses",
    rhs = base_rhs(h2raw, "core + "), family = "nbinom2", offset = "later_values", one_arm = TRUE,
    terms = list(list(term = "core", dir = "greater", dev = EST$H2$class$estimate))),
  H2_core_method = list(
    hyp = "H2", data = core_long(h2raw[h2raw$arm == M, ], "method"), y = "uses",
    rhs = base_rhs(h2raw, "core + "), family = "nbinom2", offset = "later_values", one_arm = TRUE,
    terms = list(list(term = "core", dir = "greater", dev = EST$H2$method$estimate))),
  H2_reuse_method = list(
    hyp = "H2", data = (function(x) x[x$core == 1, ])(core_long(h2raw, "method")), y = "uses",
    rhs = paste0(base_rhs(h2raw), " + arm"), family = "nbinom2", offset = "later_values",
    terms = list(list(term = FARM, dir = "less", dev = EST$H2$reuse_method$estimate)))
)
# the binding levels that decide beside the registered rule (row 128), where the development chain
# is weakest: H4's later intrusion at the method with injection ignored and with it excluded, and
# H2's arm contrast at the method with injection ignored. At the class the levels gave the same
# estimates as registered on the development chain (H1) or far from 1 (H4), and are not drawn.
lv <- EST$reported$binding_levels
for (L in c("all", "none")) {
  raw <- prep_h2(rd(paste0("h2_", L, ".csv")))
  e <- lv[[L]]$H4_intrusion_method$estimate
  PARTS[[paste0("H4_intrusion_method_", L)]] <- list(
    hyp = "H4", data = raw, y = "intrusion_method", rhs = paste0(base_rhs(raw), " + arm"), family = "nbinom2",
    offset = "later", level = L,
    # on the development chain the ratio with injection excluded could not be fitted (three
    # intrusions in the function arm): its "dev" is then the registered level's
    terms = list(list(term = FARM, dir = "less", dev = if (is.null(e)) EST$H4$intrusion_method$estimate else e)))
}
raw_all <- prep_h2(rd("h2_all.csv"))
PARTS$H2_reuse_method_all <- list(
  hyp = "H2", data = (function(x) x[x$core == 1, ])(core_long(raw_all, "method")), y = "uses",
  rhs = paste0(base_rhs(raw_all), " + arm"), family = "nbinom2", offset = "later_values", level = "all",
  terms = list(list(term = FARM, dir = "less", dev = lv$all$H2_reuse_method$estimate)))

# ---------------------------------------------------------------- baseline from the development chain

derive <- function(p, d, n_cp) {
  if (identical(p$cp_c, "scaled")) d$cp_c <- cpc_scaled(d$cp, n_cp)
  if (identical(p$cp_c, "unscaled")) d$cp_c <- d$cp - (n_cp + 1) / 2
  if (identical(p$offset, "later")) d$log_later <- log(d$later_checkpoints)
  if (identical(p$offset, "later_values")) d$log_later <- log(d$later_checkpoints) + log(d$n_values)
  d$arm <- factor(as.character(d$arm), levels = c(M, F))
  d$cp_f <- factor(d$cp)
  d
}
fam <- function(name) switch(name, nbinom2 = nbinom2(), gaussian = gaussian(), poisson = poisson())
fixed_formula <- function(p, frontend = FALSE) {
  rhs <- p$rhs
  if (isTRUE(p$one_arm)) rhs <- gsub(" \\+ arm$", "", rhs)
  paste0(p$y, " ~ ", rhs, if (frontend) " + frontend" else "", if (!is.null(p$offset)) " + offset(log_later)" else "")
}
fit_baseline <- function(p) {
  d <- derive(p, p$data, DEV_CP)
  d <- d[!is.na(d[[p$y]]), ]
  f <- as.formula(paste(fixed_formula(p), "+ (1 | cp_f)"))
  fit <- tryCatch(glmmTMB(f, data = d, family = fam(p$family)), error = function(e) NULL)
  if (is.null(fit) || !isTRUE(fit$sdr$pdHess))
    fit <- glmmTMB(as.formula(fixed_formula(p)), data = d, family = fam(p$family))
  vc <- tryCatch(attr(VarCorr(fit)$cond$cp_f, "stddev"), error = function(e) NULL)
  list(beta = fixef(fit)$cond, sd_cp = if (is.null(vc)) 0 else unname(vc[1]),
       sigma = if (p$family == "poisson") NA else sigma(fit), rows = d)
}

# ---------------------------------------------------------------- one draw at the ui design

draw <- function(p, base, target, sd_chain) {
  tmpl <- base$rows
  cp_re <- rnorm(CP, 0, base$sd_cp)      # the problem's own level, shared by every chain
  arms <- if (isTRUE(p$one_arm)) M else c(M, F)
  d <- do.call(rbind, lapply(arms, function(a) {
    ta <- tmpl[as.character(tmpl$arm) == a, ]
    do.call(rbind, lapply(FRONTENDS, function(fe) do.call(rbind, lapply(seq_len(CHAINS), function(k) {
      n <- max(1, round(nrow(ta) * CP / DEV_CP))
      x <- ta[sample.int(nrow(ta), n, replace = TRUE), ]
      x$cp <- pmin(CP, pmax(1, ceiling((x$cp - runif(n)) * CP / DEV_CP)))
      if ("later_checkpoints" %in% names(x)) x$later_checkpoints <- pmax(1, CP - x$cp)
      x$frontend <- fe
      x$chain_id <- paste(a, fe, k, sep = "/")
      x$re_chain <- rnorm(1, 0, sd_chain)
      x
    }))))
  }))
  d <- derive(p, d, CP)
  d$frontend <- factor(d$frontend)
  # the linear predictor from the development chain's coefficients, the tested ones replaced
  rhs <- as.formula(paste("~", if (isTRUE(p$one_arm)) gsub(" \\+ arm$", "", p$rhs) else p$rhs))
  X <- model.matrix(rhs, d)
  b <- base$beta[colnames(X)]
  b[is.na(b)] <- 0
  for (t in p$terms) {
    if (!t$term %in% colnames(X)) stop("no column ", t$term, " in ", paste(colnames(X), collapse = ", "))
    b[t$term] <- target[[t$term]]
  }
  eta <- drop(X %*% b) + d$re_chain + cp_re[d$cp] + (if (!is.null(p$offset)) d$log_later else 0)
  d[[p$y]] <- switch(p$family,
    nbinom2 = rnbinom(nrow(d), size = base$sigma, mu = exp(pmin(eta, 20))),
    poisson = rpois(nrow(d), exp(pmin(eta, 20))),
    gaussian = rnorm(nrow(d), eta, base$sigma))
  d
}

test_draw <- function(p, d) {
  f1 <- as.formula(paste(fixed_formula(p, TRUE), "+ (1 | chain_id) + (1 | cp_f)"))
  fit <- tryCatch(glmmTMB(f1, data = d, family = fam(p$family)), error = function(e) NULL)
  if (is.null(fit) || !isTRUE(fit$sdr$pdHess)) {
    f0 <- as.formula(paste(fixed_formula(p, TRUE), "+ (1 | chain_id)"))
    fit <- tryCatch(glmmTMB(f0, data = d, family = fam(p$family)), error = function(e) NULL)
  }
  if (is.null(fit)) return(NULL)
  co <- summary(fit)$coefficients$cond
  vapply(p$terms, function(t) {
    nm <- t$term
    if (!nm %in% rownames(co) || !is.finite(co[nm, "Std. Error"])) return(NA_real_)
    z <- co[nm, "Estimate"] / co[nm, "Std. Error"]
    if (t$dir == "less") pnorm(z) else 1 - pnorm(z)      # the one-sided p
  }, numeric(1))
}

# a scenario's value for a tested term, on the model's scale
target_of <- function(t, scen) {
  if (scen == "dev") {
    v <- t$dev
  } else {
    r <- as.numeric(scen)
    v <- if (t$dir == "greater") log(1 / r) else log(r)
  }
  if (isTRUE(t$per_step)) v <- v / (CP - 1)    # a ratio over the stream, as a checkpoint's slope
  v
}

# ---------------------------------------------------------------- the run

set.seed(SEED)
cat("baselines from the development chain\n")
BASE <- lapply(PARTS, fit_baseline)
SCEN <- expand.grid(effect = c("dev", "0.8", "0.67", "0.5"), sd_chain = c(0.2, 0.5), stringsAsFactors = FALSE)
SCEN$name <- paste0(SCEN$effect, "/sd", SCEN$sd_chain)
if (length(ONLY) && nzchar(ONLY[1])) SCEN <- SCEN[SCEN$name %in% ONLY, ]
HYPS <- c("H1", "H2", "H4", "H5")
ALPHAS <- c(0.05, 0.0125)
results <- list()
started <- Sys.time()

summarise <- function(ps) {
  # ps: reps x parts matrix of the largest p of each part's terms (NA: not fitted)
  part <- lapply(setNames(colnames(ps), colnames(ps)), function(k)
    setNames(as.list(sapply(ALPHAS, function(a) mean(ps[, k] <= a, na.rm = TRUE))), paste0("alpha_", ALPHAS)))
  hyp <- lapply(setNames(HYPS, HYPS), function(h) {
    cols <- names(PARTS)[vapply(PARTS, function(p) p$hyp == h, logical(1))]
    worst <- apply(ps[, cols, drop = FALSE], 1, max)        # p is the largest of the parts
    setNames(as.list(sapply(ALPHAS, function(a) mean(worst <= a, na.rm = TRUE))), paste0("alpha_", ALPHAS))
  })
  list(parts = part, hypotheses = hyp, failed_fits = as.list(colSums(is.na(ps))))
}

write_out <- function() {
  meta <- list(date = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"), seed = SEED, reps = REPS, cores = CORES,
               design = list(chains_per_stack = CHAINS, frontends = FRONTENDS, checkpoints = CP),
               glmmTMB = as.character(packageVersion("glmmTMB")),
               dev_estimates = lapply(PARTS, function(p) setNames(lapply(p$terms, function(t) exp(t$dev)),
                                                                 vapply(p$terms, `[[`, "", "term"))),
               minutes = round(as.numeric(difftime(Sys.time(), started, units = "mins")), 1))
  writeLines(toJSON(list(meta = meta, scenarios = results), auto_unbox = TRUE, pretty = TRUE, digits = 4),
             file.path(OUT, "power.json"))
  L <- c("# Power of the confirmatory four at the ui primary's design", "",
         paste0("Made by `analysis/power.R` (PLAN.md §7, *Power for the confirmatory four*), ", meta$date,
                "; ", REPS, " draws a scenario, ", CHAINS, " chains a stack, two front ends, ", CP,
                " checkpoints. Read on Wald intervals, not the cluster bootstrap; a guide, not a promise."), "",
         "Share of draws in which a hypothesis passes (every part on its side). *0.05*: its p at a part's alpha of",
         "0.05; *0.0125*: at 0.05 / 4, the first step of Holm.", "",
         "| scenario | H1 | H2 | H4 | H5 |", "|---|---|---|---|---|")
  for (nm in names(results)) {
    h <- results[[nm]]$hypotheses
    L <- c(L, paste0("| ", nm, " | ", paste(vapply(HYPS, function(k)
      sprintf("%.2f / %.2f", h[[k]]$alpha_0.05, h[[k]]$alpha_0.0125), ""), collapse = " | "), " |"))
  }
  L <- c(L, "", "Each part, at a part's alpha of 0.05:", "",
         paste0("| scenario | ", paste(names(PARTS), collapse = " | "), " |"),
         paste0("|---|", paste(rep("---", length(PARTS)), collapse = "|"), "|"))
  for (nm in names(results)) {
    pt <- results[[nm]]$parts
    L <- c(L, paste0("| ", nm, " | ", paste(vapply(names(PARTS), function(k) sprintf("%.2f", pt[[k]]$alpha_0.05), ""),
                                           collapse = " | "), " |"))
  }
  L <- c(L, "", "The development chain's estimates (*dev*), as ratios (a trend over its stream):", "")
  for (k in names(meta$dev_estimates))
    L <- c(L, paste0("- ", k, ": ", paste(names(meta$dev_estimates[[k]]), sprintf("%.3g", unlist(meta$dev_estimates[[k]])),
                                         sep = " ", collapse = "; ")))
  writeLines(L, file.path(OUT, "POWER.md"))
}

for (i in seq_len(nrow(SCEN))) {
  s <- SCEN[i, ]
  cat(sprintf("[%s] scenario %s (%d draws on %d cores)\n", format(Sys.time(), "%H:%M"), s$name, REPS, CORES))
  seeds <- SEED + i * 10000 + seq_len(REPS)
  got <- parallel::mclapply(seeds, function(sd) {
    set.seed(sd)
    vapply(names(PARTS), function(k) {
      p <- PARTS[[k]]
      target <- setNames(lapply(p$terms, target_of, scen = s$effect), vapply(p$terms, `[[`, "", "term"))
      pv <- tryCatch(test_draw(p, draw(p, BASE[[k]], target, s$sd_chain)), error = function(e) NULL)
      if (is.null(pv) || any(is.na(pv))) NA_real_ else max(pv)
    }, numeric(1))
  }, mc.cores = CORES, mc.preschedule = FALSE)
  ps <- do.call(rbind, lapply(got, function(x) if (is.numeric(x)) x else rep(NA_real_, length(PARTS))))
  colnames(ps) <- names(PARTS)
  results[[s$name]] <- summarise(ps)
  write_out()
}
cat("done:", file.path(OUT, "POWER.md"), "\n")
