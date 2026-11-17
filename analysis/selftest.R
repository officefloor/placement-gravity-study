#!/usr/bin/env Rscript
# A self-test of analysis/analyse.R on simulated data with known effects (run by step1_setup.sh):
# bindings rise with host size in the methods arm and less so in the function arm; intrusion rises with
# bindings; later intrusions bound to what stood by rise with how much stood by; the shape measures are unrelated to intrusion; every checkpoint (problem) has its own level
# of bindings and of intrusion, shared by all chains. The models must recover each direction.

set.seed(20261116)
dir <- file.path(tempdir(), "pg-selftest")
dir.create(dir, showWarnings = FALSE, recursive = TRUE)

arms <- c("spring", "officefloor")
cp_binding <- rnorm(60, 0, 0.3)   # the problem's own level, the same for every chain
cp_int <- rnorm(60, 0, 0.5)
h1 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 150
  cp <- sample(1:60, n, replace = TRUE)
  pre <- round(exp(runif(n, log(3), log(120))))
  b <- if (arm == "spring") 0.45 else 0.10
  a <- if (arm == "spring") -0.6 else -1.4
  prior <- runif(n, 0.5, 2.5)
  binding <- rpois(n, exp(a + b * log(pre) + 0.006 * cp + cp_binding[cp] + 0.25 * prior + rnorm(1, 0, 0.1)))
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp, act = NA,
             binding = binding, binding_no_param = pmax(0, binding - rbinom(n, 1, 0.3)), binding_class = rpois(n, 1),
             binding_no_injected = pmax(0, binding - rbinom(n, 1, 0.3)), binding_class_no_injected = rpois(n, 0.5),
             pre_positions = pre, class_positions = pre * 3, prior_binding_mean = prior)
}))))
h2 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 400
  binding <- rpois(n, if (arm == "spring") 2 else 0.8)
  later <- sample(5:55, n, replace = TRUE)
  cp <- 60 - later
  new <- rbinom(n, 1, 0.4)
  binding <- ifelse(new == 1, rbinom(n, 1, 0.2), binding)      # new hosts have few bindings and are left alone
  jn <- as.numeric(seq_len(n) %% 5 < 2)                 # two in five are junctions (no random draw, so
                                                        # the other simulated effects keep their draws),
                                                        # followed by 35% more intrusion
  mu <- exp(-3.2 + log(1.35) * jn + 0.25 * binding - 0.8 * new + cp_int[cp] + (if (arm == "spring") 0 else -0.9)) * later
  # what stood by where the code was placed, and the later intrusions bound to it: 15% more per
  # field of the class, 10% more per value of the method
  byc <- rpois(n, if (arm == "spring") 6 else 1)
  bym <- rpois(n, if (arm == "spring") 3 else 1)
  dr <- exp(-4.5 + cp_int[cp]) * later
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "",
             cp = cp, act = NA,
             intrusion_class = rnbinom(n, size = 2, mu = 3 * mu), later_checkpoints = later,
             intrusion_method = rnbinom(n, size = 2, mu = 2 * mu),
             intrusion_lines = rnbinom(n, size = 2, mu = exp(-3.2 + cp_int[cp]) * later),
             intrusion_class_any = rnbinom(n, size = 2, mu = 4 * mu),
             intrusion_method_any = rnbinom(n, size = 2, mu = 3 * mu), bound = rbinom(n, 1, 0.8) == 1,
             bystanders_class = byc, bystanders_method = bym, class_positions = rpois(n, 60),
             m_cyclomatic = rpois(n, 3), c_wmc = rpois(n, 30), c_gini = runif(n), c_lcom_star = runif(n),
             m_fanout = rpois(n, 2), c_god_class = seq_len(n) %% 7 == 0,
             c_mi = rnorm(n, 80, 10), c_positions = rpois(n, 60) + 1,
             class_identity = paste0("C", sample(1:12, n, replace = TRUE)),
             drawn_class = rnbinom(n, size = 2, mu = dr * exp(log(1.15) * byc)),
             drawn_method = rnbinom(n, size = 2, mu = dr * exp(log(1.10) * bym)),
             binding = binding, binding_no_param = binding, binding_no_injected = binding, net_added = rpois(n, 4) + 1,
             addition_positions = rpois(n, 8) + 1, declared_crossings = rpois(n, 1),
             pre_positions = rpois(n, 20), host_new = new == 1, shape_found = TRUE,
             s1_long = rbinom(n, 1, 0.3) == 1, s2_stuck = rbinom(n, 1, 0.2) == 1,
             s3_junction = jn == 1, s3_junction_injection_aware = rbinom(n, 1, 0.5) == 1,
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
             place_class = paste0(arm, ch, "|C", sample(1:6, n, replace = TRUE)),
             place_method = paste0(arm, ch, "|M", sample(1:25, n, replace = TRUE)),
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
# reopening: the methods arm reopens about three places per checkpoint, the function arm one
reopen <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  r <- rpois(60, (if (arm == "spring") 3 else 1) * exp(cp_by))
  w <- if (arm == "spring") rep(0, 60) else rbinom(60, r, 0.5)
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = 1:60,
             reopened = r, reopened_classes = r - w, reopened_wiring = w)
}))))
write.csv(reopen, file.path(dir, "reopen.csv"), row.names = FALSE)
write.csv(by, file.path(dir, "by.csv"), row.names = FALSE)
write.csv(cap, file.path(dir, "capture.csv"), row.names = FALSE)
write.csv(h1, file.path(dir, "h1.csv"), row.names = FALSE)
write.csv(h2, file.path(dir, "h2.csv"), row.names = FALSE)
writeLines(jsonlite::toJSON(list(
  analysis = "selftest", role = "development", seed = 20261116, boot = 60, margin = c(0.8, 1.25),
  methods_arm = "spring", function_arm = "officefloor", checkpoints = 60,
  shape_kept = c("s1_long", "s4_cognitive", "s5_class_gini"), sinew_kept = c("s2_stuck", "s3_junction"),
  h3_measures = c("s1_long", "s4_cognitive", "m_cyclomatic", "c_gini", "c_wmc", "c_lcom_star"),
  reach = c("m_fanout"),
  literature = list(s1_long = list(level = "method", kind = "flag", source = "long"),
                    s4_cognitive = list(level = "method", kind = "level", source = "cognitive"),
                    c_gini = list(level = "class", kind = "plain", source = "Gini"),
                    c_lcom_star = list(level = "class", kind = "plain", source = "LCOM*"),
                    m_fanout = list(level = "method", kind = "level", source = "fan-out"),
                    m_cyclomatic = list(level = "method", kind = "level", source = "McCabe"),
                    c_wmc = list(level = "class", kind = "level", source = "CK"),
                    c_mi = list(level = "class", kind = "plain", source = "MI", reversed = TRUE),
                    c_god_class = list(level = "class", kind = "flag", source = "Lanza and Marinescu")),
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
check(e$H1$within_class$lower > 0 && e$H1$within_method$lower > 0,
      "H1 recovers bystanders rising within a class and within a method")
check(e$H1$within_class$places == 48, "H1 within a class is read on the classes with runs at two checkpoints")
for (lev in c("class", "method")) {
  m <- e$H2[[lev]]
  true <- if (lev == "class") 1.15 else 1.10
  check(m$irr_lower > 1, paste("H2 recovers later code bound to what stood by, at the", lev, "level"))
  check(abs(log(m$irr) - log(true)) < 0.05, paste("H2's ratio is within 5% of the true one,", lev))
  check(!is.null(e$reported[[paste0("H2_function_arm_", lev)]]$irr), paste("H2 in the function arm is reported,", lev))
  t <- e$reported[[paste0("bindings_intrusion_", lev)]]
  check(abs(log(t$irr) - 0.25) < 0.05, paste("the bindings' ratio in later intrusion is reported, near the true one,", lev))
}
for (lev in c("class", "method")) {
  x <- e$reported[[paste0("size_or_data_", lev)]]
  check(!is.null(x$bystanders$irr) && !is.null(x$size$irr) && !is.null(x$size_alone$irr) &&
        !is.null(x$correlation$spring), paste("size or data is reported at the", lev))
}
check(e$H2$n < e$reported$intrusion_rows$bound, "H2 is read on the methods arm's bound rows")
check(abs(log(e$reported$bindings_lines$irr)) < 0.05,
      "intrusion on the problem's own lines, simulated unrelated to bindings, is reported as such")
for (k in names(e$H3$measures)) {
  m <- e$H3$measures[[k]]
  check(m$irr_lower > 0.5 && m$irr_upper < 2, paste("H3 estimates", k, "near no effect"))
}
check(all(sapply(e$H3$measures, function(m) m$p_upper <= m$p_tost && !isTRUE(m$above))),
      "H3's one-sided p is no larger than the two-sided one, and no measure lies above the margin")
check(!is.null(e$reported$H3_class_level$s4_cognitive$irr), "the first block on class-level intrusion is reported")
for (k in c("m_cyclomatic", "c_wmc", "c_god_class")) {
  m <- e$reported$literature_shape[[k]]
  check(!is.null(m$irr) && m$irr_lower > 0.5 && m$irr_upper < 2,
        paste("the literature's", k, "simulated unrelated, is reported near no effect"))
}
check(e$reported$literature_shape$c_wmc$at == "class", "a class measure is read at the class")
check(e$reported$literature_class_rows < e$reported$intrusion_rows$bound,
      "a class measure is read on one row per class and checkpoint")
check(isTRUE(e$reported$literature_shape$c_mi$reversed), "a measure where higher is better is read reversed")
check(setequal(names(e$H3$measures), c("s1_long", "s4_cognitive", "m_cyclomatic", "c_gini", "c_wmc", "c_lcom_star")),
      "H3 is read on its six measures, each alone")
check(e$H3$measures$c_wmc$at == "class" && e$H3$measures$s4_cognitive$at == "method",
      "H3's measures are read at their own level")
check(!is.null(e$reported$shape_joint$measures$s4_cognitive$irr), "the block as first registered is reported")
check(is.null(e$H3$measures$s3_junction), "the junction is not among H3's shape measures")
check(e$reported$sinew$s3_junction$method$irr_lower > 1 && e$reported$sinew$s3_junction$class$irr_lower > 1,
      "the junction, simulated to be followed by more intrusion, is reported as such")
check(abs(log(e$reported$sinew$s2_stuck$method$irr)) < 0.1, "not slimmable, simulated unrelated, is reported near 1")
check(e$H4$arm$upper < 0, "H4 recovers the function arm's fewer bystanders half-way through")
check(e$H4$slope$upper < 0, "H4 recovers their slower growth")
check(e$H4$centre_checkpoint == 30.5, "H4's checkpoint index is centred at the middle of the stream")
for (lev in c("intrusion_class", "intrusion_method")) {
  check(e$H4[[lev]]$irr_upper < 1, paste("H4 recovers the function arm's lower", lev))
}
check(e$reported$intrusion_rows$bound < e$reported$intrusion_rows$all, "intrusion is read on the bound rows only")
check(abs(log(e$reported$reopen_with_wiring$irr) - log(1 / 3)) < 0.15, "reopening is reported, near the true ratio")
check(!is.null(e$reported$bindings_any_change_class$irr), "H2 on any later change is reported")
check(abs(e$reported$H1_levels$function_arm$estimate) < 0.01, "the function arm's slope is reported, near flat")
check(abs(e$reported$needed_arm$estimate) < 0.05, "the arms need the same")
check(e$reported$capture_spring$lower > 0, "capture is recovered in the methods arm")
check(e$reported$H1_bindings$log_host$lower > 0, "H1 as first registered (bindings) is reported")
check(e$reported$H4_bindings$arm$upper < 0, "H4 as first registered (bindings) is reported")
check(e$reported$H4_bindings$centre_positions > 3 && e$reported$H4_bindings$centre_positions < 120,
      "the binding-based H4's host size is centred within the data")
check(e$reported$H4_arm_at[["50"]]$estimate < e$reported$H4_arm_at[["10"]]$estimate,
      "the arm difference in bindings widens with host size, as simulated")
check(isTRUE(e$checkpoint_intercept$H1) && isTRUE(e$checkpoint_intercept$H4) &&
      isTRUE(e$checkpoint_intercept$H2_class), "the models carry the checkpoint's intercept")
check(e$reported$formation_lagged_spring$lower > 0, "the lagged formation term is recovered")
check(!is.null(e$reported$junction_x_arm_s3_junction$irr), "junction x arm is estimated")
check(e$reported$H1_without_injected$log_host$lower > 0, "H1 (bindings) without injected dependencies is estimated")
check(!is.null(e$reported$H1_class_level_without_injected$log_class$estimate),
      "class-level H1 (bindings) without injected dependencies is estimated")
check(!is.null(e$reported$H4_without_injected$slope$estimate), "H4 (bindings) without injected dependencies is estimated")
check(!is.null(e$reported$bindings_without_injected_class$irr), "H2 without injected dependencies is estimated")
cat("analysis/analyse.R self-test passed\n")
