#!/usr/bin/env Rscript
# A self-test of analysis/analyse.R on simulated data with known effects (run by step1_setup.sh):
# ties rise with host size in the methods arm and less so in the function arm; intrusion rises with
# ties; the shape measures are unrelated to intrusion. The models must recover each direction.

set.seed(20261116)
dir <- file.path(tempdir(), "pg-selftest")
dir.create(dir, showWarnings = FALSE, recursive = TRUE)

arms <- c("spring", "officefloor")
h1 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 150
  cp <- sample(1:60, n, replace = TRUE)
  pre <- round(exp(runif(n, log(3), log(120))))
  b <- if (arm == "spring") 0.45 else 0.10
  a <- if (arm == "spring") -0.6 else -1.4
  tie <- rpois(n, exp(a + b * log(pre) + 0.006 * cp + rnorm(1, 0, 0.1)))
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp, act = NA,
             tie = tie, tie_no_param = pmax(0, tie - rbinom(n, 1, 0.3)), tie_class = rpois(n, 1),
             pre_positions = pre, class_positions = pre * 3)
}))))
h2 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 400
  tie <- rpois(n, if (arm == "spring") 2 else 0.8)
  later <- sample(5:55, n, replace = TRUE)
  mu <- exp(-3.2 + 0.25 * tie) * later
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "",
             cp = sample(1:60, n, replace = TRUE), act = NA,
             intrusion = rnbinom(n, size = 2, mu = mu), later_checkpoints = later,
             tie = tie, tie_no_param = tie, net_added = rpois(n, 4) + 1,
             addition_positions = rpois(n, 8) + 1, declared_crossings = rpois(n, 1),
             pre_positions = rpois(n, 20), host_new = FALSE, shape_found = TRUE,
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
check(e$H3$arm$upper < 0 || e$H3$slope$upper < 0, "H3 recovers the function arm's lower ties")
check(e$H3$slope$estimate < 0, "H3 recovers the flatter slope")
check(e$H2a$irr_lower > 1, "H2a recovers intrusion rising with ties")
irr_true <- exp(0.25)
check(e$H2a$irr_lower < irr_true && irr_true < e$H2a$irr_upper, "H2a's interval covers the true ratio")
for (k in names(e$H2b$measures)) {
  m <- e$H2b$measures[[k]]
  check(m$irr_lower > 0.5 && m$irr_upper < 2, paste("H2b estimates", k, "near no effect"))
}
check(!is.null(e$reported$junction_x_arm_s3_junction$irr), "junction x arm is estimated")
cat("analysis/analyse.R self-test passed\n")
