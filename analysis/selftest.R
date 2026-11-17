#!/usr/bin/env Rscript
# A self-test of analysis/analyse.R on simulated data with known effects (run by step1_setup.sh):
# ties rise with host size in the methods arm and less so in the function arm; intrusion rises with
# ties; the shape measures are unrelated to intrusion; every checkpoint (problem) has its own level
# of ties and of intrusion, shared by all chains. The models must recover each direction.

set.seed(20261116)
dir <- file.path(tempdir(), "pg-selftest")
dir.create(dir, showWarnings = FALSE, recursive = TRUE)

arms <- c("spring", "officefloor")
cp_tie <- rnorm(60, 0, 0.3)   # the problem's own level, the same for every chain
cp_int <- rnorm(60, 0, 0.5)
h1 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 150
  cp <- sample(1:60, n, replace = TRUE)
  pre <- round(exp(runif(n, log(3), log(120))))
  b <- if (arm == "spring") 0.45 else 0.10
  a <- if (arm == "spring") -0.6 else -1.4
  prior <- runif(n, 0.5, 2.5)
  tie <- rpois(n, exp(a + b * log(pre) + 0.006 * cp + cp_tie[cp] + 0.25 * prior + rnorm(1, 0, 0.1)))
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp, act = NA,
             tie = tie, tie_no_param = pmax(0, tie - rbinom(n, 1, 0.3)), tie_class = rpois(n, 1),
             tie_no_injected = pmax(0, tie - rbinom(n, 1, 0.3)), tie_class_no_injected = rpois(n, 0.5),
             pre_positions = pre, class_positions = pre * 3, prior_tie_mean = prior)
}))))
h2 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 400
  tie <- rpois(n, if (arm == "spring") 2 else 0.8)
  later <- sample(5:55, n, replace = TRUE)
  cp <- 60 - later
  new <- rbinom(n, 1, 0.4)
  tie <- ifelse(new == 1, rbinom(n, 1, 0.2), tie)      # new hosts have few ties and are left alone
  mu <- exp(-3.2 + 0.25 * tie - 0.8 * new + cp_int[cp]) * later
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "",
             cp = cp, act = NA,
             intrusion = rnbinom(n, size = 2, mu = mu), later_checkpoints = later,
             intrusion_host = rnbinom(n, size = 2, mu = 2 * mu),
             tie = tie, tie_no_param = tie, tie_no_injected = tie, net_added = rpois(n, 4) + 1,
             addition_positions = rpois(n, 8) + 1, declared_crossings = rpois(n, 1),
             pre_positions = rpois(n, 20), host_new = new == 1, shape_found = TRUE,
             s1_long = rbinom(n, 1, 0.3) == 1, s2_stuck = rbinom(n, 1, 0.2) == 1,
             s3_junction = rbinom(n, 1, 0.4) == 1, s3_junction_injection_aware = rbinom(n, 1, 0.5) == 1,
             s4_cognitive = rpois(n, 3), s5_class_gini = runif(n))
}))))
# bystanders: rising with the checkpoint in the methods arm, low and flat in the function arm;
# the needed values the same in both
cp_by <- rnorm(60, 0, 0.2)
by <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 250
  cp <- sample(1:60, n, replace = TRUE)
  mu <- if (arm == "spring") exp(1.2 + 0.02 * cp + cp_by[cp] + rnorm(1, 0, 0.1)) else
    exp(0.3 + 0.002 * cp + cp_by[cp] + rnorm(1, 0, 0.1))
  b <- rpois(n, mu)
  m <- rbinom(n, b, 0.3)
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp,
             host_new = rbinom(n, 1, 0.5) == 1, bystanders = b, by_method = m, by_class = b - m,
             bystanders_no_injected = rbinom(n, b, 0.7), bystanders_no_constants = rbinom(n, b, 0.6),
             need = rpois(n, 1.4))
}))))
cap <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  heavy <- if (arm == "spring") 3 + rpois(60, (1:60) / 6) else rpois(60, 1)
  p <- plogis(-1 + (if (arm == "spring") 0.8 else 0) * log1p(heavy) + rnorm(60, 0, 0.3))
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = 1:60,
             share_in_existing = p, heaviest_class = heavy, fields_added = rpois(60, 0.2))
}))))
write.csv(by, file.path(dir, "by.csv"), row.names = FALSE)
write.csv(cap, file.path(dir, "capture.csv"), row.names = FALSE)
write.csv(h1, file.path(dir, "h1.csv"), row.names = FALSE)
write.csv(h2, file.path(dir, "h2.csv"), row.names = FALSE)
writeLines(jsonlite::toJSON(list(
  analysis = "selftest", role = "development", seed = 20261116, boot = 60, bound = c(0.8, 1.25),
  methods_arm = "spring", function_arm = "officefloor", checkpoints = 60,
  shape_kept = c("s1_long", "s2_stuck", "s3_junction", "s4_cognitive", "s5_class_gini"),
  acts = FALSE, frontends = list()), auto_unbox = TRUE), file.path(dir, "spec.json"))

out <- file.path(dir, "estimates.json")
script <- file.path(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE),
                                                                  value = TRUE)))), "analyse.R")
status <- system2("Rscript", c(script, dir, out))
if (status != 0) stop("analyse.R failed")
e <- jsonlite::fromJSON(out)

check <- function(ok, what) {
  if (!isTRUE(ok)) stop("selftest failed: ", what)
  cat("ok:", what, "\n")
}
check(e$H1$cp$lower > 0, "H1 recovers bystanders rising with the checkpoint in the methods arm")
check(e$H1$cp$lower < 0.02 && 0.02 < e$H1$cp$upper + 0.01, "H1's slope is near the simulated one")
check(e$H3$arm$upper < 0, "H3 recovers the function arm's fewer bystanders half-way through")
check(e$H3$slope$upper < 0, "H3 recovers their slower growth")
check(e$H3$centre_checkpoint == 30.5, "H3's checkpoint index is centred at the middle of the stream")
check(abs(e$reported$H1_levels$function_arm$estimate) < 0.01, "the function arm's slope is reported, near flat")
check(e$reported$needed_arm$lower < 0 && e$reported$needed_arm$upper > 0, "the arms need the same")
check(e$reported$capture_spring$lower > 0, "capture is recovered in the methods arm")
check(e$reported$H1_ties$log_host$lower > 0, "H1 as first registered (ties) is reported")
check(e$reported$H3_ties$arm$upper < 0, "H3 as first registered (ties) is reported")
check(e$reported$H3_ties$centre_positions > 3 && e$reported$H3_ties$centre_positions < 120,
      "the tie-based H3's host size is centred within the data")
check(e$reported$H3_arm_at[["50"]]$estimate < e$reported$H3_arm_at[["10"]]$estimate,
      "the arm difference in ties widens with host size, as simulated")
check(isTRUE(e$checkpoint_intercept$H1) && isTRUE(e$checkpoint_intercept$H3) &&
      isTRUE(e$checkpoint_intercept$H2a), "the models carry the checkpoint's intercept")
check(e$reported$formation_lagged_spring$lower > 0, "the lagged formation term is recovered")
check(!is.null(e$reported$H2a_host_level$irr), "H2a on the host-level count is estimated")
check(e$H2a$irr_lower > 1, "H2a recovers intrusion rising with ties")
irr_true <- exp(0.25)
check(e$H2a$irr_lower < irr_true && irr_true < e$H2a$irr_upper, "H2a's interval covers the true ratio")
for (k in names(e$H2b$measures)) {
  m <- e$H2b$measures[[k]]
  check(m$irr_lower > 0.5 && m$irr_upper < 2, paste("H2b estimates", k, "near no effect"))
}
check(!is.null(e$reported$junction_x_arm_s3_junction$irr), "junction x arm is estimated")
check(e$reported$H1_without_injected$log_host$lower > 0, "H1 without injected dependencies is estimated")
check(!is.null(e$reported$H1_class_level_without_injected$log_class$estimate),
      "class-level H1 without injected dependencies is estimated")
check(!is.null(e$reported$H3_without_injected$slope$estimate), "H3 without injected dependencies is estimated")
check(!is.null(e$reported$H2a_without_injected$irr), "H2a without injected dependencies is estimated")
cat("analysis/analyse.R self-test passed\n")
