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
write.csv(h1, file.path(dir, "h1.csv"), row.names = FALSE)
write.csv(h2, file.path(dir, "h2.csv"), row.names = FALSE)
writeLines(jsonlite::toJSON(list(
  analysis = "selftest", role = "development", seed = 20261116, boot = 60, bound = c(0.8, 1.25),
  methods_arm = "spring", function_arm = "officefloor",
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
check(e$H1$log_host$lower > 0, "H1 recovers the slope on host size")
check(e$H1$cp$lower > 0, "H1 recovers the slope on the checkpoint index")
check(e$H3$arm$upper < 0, "H3 recovers the function arm's lower ties at a typical host")
check(e$H3$centre_positions > 3 && e$H3$centre_positions < 120, "H3's host size is centred within the data")
check(e$reported$H3_arm_at[["50"]]$estimate < e$reported$H3_arm_at[["10"]]$estimate,
      "the arm difference widens with host size, as simulated")
check(isTRUE(e$checkpoint_intercept$H1) && isTRUE(e$checkpoint_intercept$H3) &&
      isTRUE(e$checkpoint_intercept$H2a), "the models carry the checkpoint's intercept")
check(e$reported$formation_lagged_spring$lower > 0, "the lagged formation term is recovered")
check(!is.null(e$reported$H2a_host_level$irr), "H2a on the host-level count is estimated")
check(e$H3$slope$estimate < 0, "H3 recovers the flatter slope")
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
