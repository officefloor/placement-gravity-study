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
h3 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
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
             left_class = byc + 1, left_method = bym + 2,
             core_class = 1 + (seq_len(n) %% 2), core_method = seq_len(n) %% 3,
             periphery_class = byc + 1, periphery_method = bym + 2,
             # a core value of the function arm is come back to 0.3 times as much as the methods arm's
             uses_core_class = rnbinom(n, size = 2, mu = dr * 3 * (1 + (seq_len(n) %% 2)) * (if (arm == "spring") 1 else 0.3)),
             uses_core_method = rnbinom(n, size = 2, mu = dr * 3 * (seq_len(n) %% 3) * (if (arm == "spring") 1 else 0.3)),
             uses_periphery_class = rnbinom(n, size = 2, mu = dr * (byc + 1)),
             uses_periphery_method = rnbinom(n, size = 2, mu = dr * (bym + 2)),
             core_class_fields = rep(1, n), periphery_class_fields = byc + 1,
             uses_core_class_fields = rnbinom(n, size = 2, mu = dr * 3),
             uses_periphery_class_fields = rnbinom(n, size = 2, mu = dr * (byc + 1)),
             drawn_class_left = rnbinom(n, size = 2, mu = dr * exp(log(1.15) * (byc + 1))),
             drawn_method_left = rnbinom(n, size = 2, mu = dr * exp(log(1.10) * (bym + 2))),
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
  # the existing files a change goes back into: 3 Java files in the methods arm; 1.4 Java files and
  # 0.7 wiring files in the function arm (0.7 times as many in all)
  ej <- rpois(60, (if (arm == "spring") 3 else 1.4) * exp(cp_by))
  ew <- if (arm == "spring") rep(0, 60) else rpois(60, 0.7)
  # how well-trodden those files were: rising over the stream in both arms, half as much in the
  # function arm
  tj <- rnbinom(60, size = 3, mu = (if (arm == "spring") 1 else 0.4) * (1:60) / 3 * exp(cp_by))
  tw <- if (arm == "spring") rep(0, 60) else rnbinom(60, size = 3, mu = 0.1 * (1:60) / 3)
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = 1:60,
             reopened = r, reopened_classes = r - w, reopened_wiring = w,
             existing_java_files = ej, existing_wiring_files = ew, existing_files = ej + ew,
             trodden_java = tj, trodden_wiring = tw, trodden = tj + tw)
}))))
write.csv(reopen, file.path(dir, "reopen.csv"), row.names = FALSE)
# logic and organisation: the same logic in both arms; the function arm hands 0.4 times the
# parameters to its new methods, and its rise over the stream is flat where the methods arm's doubles
split <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  cp <- 1:60
  lg <- rnbinom(60, size = 5, mu = 12 * exp(cp_by))
  pr <- rnbinom(60, size = 5, mu = if (arm == "spring") 3 * exp(log(2) * (cp - 30.5) / 59) else rep(1.2, 60))
  dl <- rpois(60, if (arm == "spring") 6 else 9)
  wl <- if (arm == "spring") rep(0, 60) else rpois(60, 2)
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp, logic_added = lg,
             organisation_added = rpois(60, 1), declaration_lines_added = dl, import_lines_added = rpois(60, 2),
             wiring_lines_added = wl, params_new_methods = pr + (if (arm == "spring") 0 else rpois(60, 1)),
             params_called_methods = pr, params_wired_functions = if (arm == "spring") rep(0, 60) else rpois(60, 1),
             new_called_methods = rpois(60, 2), new_wired_functions = 0, birth_binding = rpois(60, 2),
             logic_existing_methods = rpois(60, 3), logic_new_called_methods = rpois(60, 6),
             logic_new_wired_functions = if (arm == "spring") rep(0, 60) else rpois(60, 3),
             existing_methods_edited = rpois(60, 1),
             method_values_added = rpois(60, 5), fields_added = rpois(60, 0.5), organisation_all = dl + wl + 1)
}))))
write.csv(split, file.path(dir, "split.csv"), row.names = FALSE)
# surface against volume (H5, restated 24 November 2026), on its own random stream so that the
# simulations after it keep their draws: links added rise with the logic added; at
# the middle of the stream the function arm adds 0.6 times the links for the same logic, and where
# the methods arm's double over the stream the function arm's stay flat (the trend ratio 0.5)
kept_seed <- .Random.seed
set.seed(20261124)
lk <- do.call(rbind, lapply(seq_len(nrow(split)), function(i) split[i, c("chain_id", "arm", "frontend", "cp", "logic_added")]))
grow <- ifelse(lk$arm == "spring", exp(log(2) * (lk$cp - 30.5) / 59), 0.6)
lk$links_added <- rnbinom(nrow(lk), size = 6, mu = 0.8 * (1 + lk$logic_added)^0.8 * grow)
lk$flow_links_added <- ifelse(lk$arm == "spring", 0, rbinom(nrow(lk), lk$links_added, 0.4))
lk$state_links_added <- rbinom(nrow(lk), lk$links_added - lk$flow_links_added, 0.4)
lk$call_links_added <- lk$links_added - lk$flow_links_added - lk$state_links_added
lk$links_lost <- rpois(nrow(lk), 1)
# the weights: each link about twice its count, so the weighted model sees the same effects
lk$call_weight_added <- lk$call_links_added + rbinom(nrow(lk), lk$call_links_added * 2, 0.5)
lk$state_weight_added <- lk$state_links_added
lk$flow_weight_added <- lk$flow_links_added + rbinom(nrow(lk), lk$flow_links_added, 0.5)
lk$weight_added <- lk$call_weight_added + lk$state_weight_added + lk$flow_weight_added
lk$weight_lost <- lk$links_lost
write.csv(lk, file.path(dir, "h5.csv"), row.names = FALSE)
assign(".Random.seed", kept_seed, envir = .GlobalEnv)
write.csv(by, file.path(dir, "by.csv"), row.names = FALSE)
write.csv(cap, file.path(dir, "capture.csv"), row.names = FALSE)
write.csv(h3, file.path(dir, "h3.csv"), row.names = FALSE)
write.csv(h2, file.path(dir, "h2.csv"), row.names = FALSE)
# choice (H1): the methods arm's alternatives fall to about a third over the stream; the function
# arm's stay where they are
h1 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 120
  cp <- sample(1:60, n, replace = TRUE)
  mu <- if (arm == "spring") 3 * exp(log(1 / 3) * (cp - 1) / 59) else rep(4, n)
  a <- rnbinom(n, size = 4, mu = mu)
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp, act = NA,
             level = sample(c("class", "method"), n, replace = TRUE), alternatives = a, forced = a == 0,
             own = rbinom(n, 1, 0.3) == 1, untyped = rpois(n, 0.1), places = "",
             by_type = a + rpois(n, cp / 3), flow_methods = 20 + rpois(n, 5),
             calls_to_app_names = 10, calls_followed = 8)
}))))
write.csv(h1, file.path(dir, "h1.csv"), row.names = FALSE)
# H1's arm contrast, on its own random stream: placements forced at the class per checkpoint; the
# methods arm's rise from 0.3 to 0.9 over the stream, the function arm's stay at 0.1 (half-way, the
# ratio 0.1 / sqrt(0.27) = 0.19; the trend ratio 1/3)
kept_seed <- .Random.seed
set.seed(20261125)
h1f <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  cp <- 1:60
  mu <- if (arm == "spring") 0.3 * exp(log(3) * (cp - 1) / 59) else rep(0.1, 60)
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp, forced_class = rpois(60, mu))
}))))
write.csv(h1f, file.path(dir, "h1_forced.csv"), row.names = FALSE)
assign(".Random.seed", kept_seed, envir = .GlobalEnv)
# change spread (H7): in the methods arm the classes beyond the first double over the stream and
# are 1.5 times as many where a placement was forced; the function arm's stay where they are.
# Pairs changed together: their coupling rises over the stream in the methods arm
h7 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  cp <- 1:60
  forced <- rbinom(60, 1, 0.5) == 1
  methods <- 1 + rpois(60, ifelse(forced, 3, 1))           # a forced unit is a larger change
  positions <- methods * (3 + rpois(60, 2))
  mu <- (if (arm == "spring") 0.8 * exp(log(2) * (cp - 1) / 59) * ifelse(forced, 1.5, 1) else rep(0.8, 60)) *
    (1 + methods) / 3
  sp <- rnbinom(60, size = 5, mu = mu)
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp, act = NA,
             positions = positions, methods = methods,
             classes = sp + 1, spread = sp, all_classes = sp + 1, forced = forced, forced_classes = as.integer(forced),
             chosen = !forced, new_classes = 0, class_names = "")
}))))
write.csv(h7, file.path(dir, "h7.csv"), row.names = FALSE)
pairs <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  do.call(rbind, lapply(1:6, function(k) {
    cp <- sort(sample(1:60, 5))
    mu <- if (arm == "spring") 2 * exp(log(3) * (cp - 1) / 59) else rep(2, 5)
    data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp,
               pair = paste0(arm, "/r/chain", ch, "|A", k, "|B", k), coupling = rnbinom(5, size = 10, mu = mu),
               times = 1:5, in_tree = TRUE)
  }))
}))))
write.csv(pairs, file.path(dir, "pairs.csv"), row.names = FALSE)
# calls across the encapsulation (H8's dispersion; the rows of forced changes couple until 24 November 2026): in the methods arm
h5 <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  n <- 100
  forced <- rbinom(n, 1, 0.4) == 1
  cp <- sample(1:60, n, replace = TRUE)
  # ten classes a chain, each with its own level of coupling (a busy class gains more whatever forced it)
  k <- sample(1:10, n, replace = TRUE)
  level <- exp(rnorm(10, 0, 0.4))[k]
  mu <- (if (arm == "spring") 1.5 * ifelse(forced, 2, 1) else rep(1.5, n)) * level
  out <- rnbinom(n, size = 4, mu = mu * 0.6)
  inn <- rnbinom(n, size = 4, mu = mu * 0.4)
  op <- rbinom(n, out + inn, ifelse(forced & arm == "spring", 0.5, 0.2))
  data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = cp, unit = cp,
             class = paste0("C", k), forced = forced, chosen = !forced, new_out = out, new_in = inn,
             coupled = out + inn, opened = op, members_opened = rpois(n, ifelse(forced, 1, 0.5)))
}))))
write.csv(h5, file.path(dir, "calls_across.csv"), row.names = FALSE)
# surface against volume: across classes the surface grows as volume^0.7 in the methods arm; a class
# that grows gains surface as volume^1.3; a forced change adds 3 more calls at the same volume added
sf <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:8, function(ch) {
  cs <- data.frame(methods_before = sample(2:80, 60, replace = TRUE))
  cs$surface_before <- round(exp(0.7 * log(cs$methods_before) + rnorm(60, 0, 0.2))) - 1
  cs <- data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = 60,
                   class = paste0(arm, ch, "c", 1:60), cross_section = TRUE, forced = NA,
                   methods_before = cs$methods_before, surface_before = pmax(cs$surface_before, 0),
                   methods_after = NA, surface_after = NA)
  tr <- do.call(rbind, lapply(1:10, function(k) {
    m <- cumsum(sample(1:4, 6, replace = TRUE)) + 3
    forced <- rbinom(6, 1, 0.5)
    sb <- pmax(round(exp(1.3 * log(m) + rnorm(6, 0, 0.1) - 1)), 0)
    dm <- sample(1:3, 6, replace = TRUE)
    data.frame(chain_id = paste0(arm, "/r/chain", ch), arm = arm, frontend = "", cp = 1:6 * 10,
               class = paste0(arm, ch, "k", k), cross_section = FALSE, forced = forced == 1,
               methods_before = m, surface_before = sb, methods_after = m + dm,
               surface_after = sb + 2 * dm + 3 * forced + rpois(6, 1))
  }))
  rbind(cs, tr)
}))))
write.csv(sf, file.path(dir, "surface.csv"), row.names = FALSE)
# encapsulation and the reader (PLAN.md 4.2f): 20 repositories an author group, systems from 20k to
# 3M tokens; the officefloor group (standing for agents) makes members private at half the odds
# where the system is at the centre, the gap closing by 0.25 on the log odds per unit of log tokens;
# opens 1.5 times the members; lands in classes of the same size
ru <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:20, function(ch) {
  n <- 60
  tokens <- round(exp(runif(n, log(2e4), log(3e6))))
  lt <- log(tokens) - log(2.4e5)
  ag <- arm == "officefloor"
  introduced <- 1 + rpois(n, 4)
  p <- plogis(0.8 + rnorm(1, 0, 0.2) + (if (ag) log(0.5) else 0) + (if (ag) 0.25 * lt else 0))
  ex <- rpois(n, 12)
  data.frame(chain_id = paste0(arm, "/repo", ch), arm = arm, unit = 1:n, cp = 1:n, tokens = tokens,
             band = "", introduced = introduced, private = rbinom(n, introduced, p),
             existing_positions = ex, forced_positions = rbinom(n, ex, 0.4), splits = 0,
             positions = 1 + rpois(n, 10), methods = 1 + rpois(n, 2))
}))))
rcl <- do.call(rbind, lapply(arms, function(arm) do.call(rbind, lapply(1:20, function(ch) {
  n <- 80
  tokens <- round(exp(runif(n, log(2e4), log(3e6))))
  data.frame(chain_id = paste0(arm, "/repo", ch), arm = arm, unit = 1:n, cp = 1:n, class = paste0("C", 1:n),
             tokens = tokens, band = "", opened = rpois(n, if (arm == "officefloor") 1.5 else 1),
             forced = FALSE, methods_before = rnbinom(n, mu = 12, size = 3),
             positions = 1 + rpois(n, 6), methods = 1 + rpois(n, 1))
}))))
write.csv(ru, file.path(dir, "reader_units.csv"), row.names = FALSE)
write.csv(rcl, file.path(dir, "reader_classes.csv"), row.names = FALSE)
writeLines(jsonlite::toJSON(list(
  analysis = "selftest", role = "development", seed = 20261116, boot = 60, margin = c(0.8, 1.25),
  methods_arm = "spring", function_arm = "officefloor", checkpoints = 60,
  shape_kept = c("s1_long", "s4_cognitive", "s5_class_gini"), sinew_kept = c("s2_stuck", "s3_junction"),
  h6_measures = c("s1_long", "s4_cognitive", "m_cyclomatic", "c_gini", "c_wmc", "c_lcom_star"),
  reach = c("m_fanout"),
  h6_sensitivity = c("s1_long", "s4_cognitive", "m_cyclomatic", "m_fanout", "c_gini", "c_wmc", "c_lcom_star"),
  literature = list(s1_long = list(level = "method", kind = "flag", source = "long"),
                    s4_cognitive = list(level = "method", kind = "level", source = "cognitive"),
                    c_gini = list(level = "class", kind = "plain", source = "Gini"),
                    c_lcom_star = list(level = "class", kind = "plain", source = "LCOM*"),
                    m_fanout = list(level = "method", kind = "level", source = "fan-out"),
                    m_cyclomatic = list(level = "method", kind = "level", source = "McCabe"),
                    c_wmc = list(level = "class", kind = "level", source = "CK"),
                    c_mi = list(level = "class", kind = "plain", source = "MI", reversed = TRUE),
                    c_god_class = list(level = "class", kind = "flag", source = "Lanza and Marinescu")),
  acts = FALSE, frontends = list(), reader_models = TRUE), auto_unbox = TRUE), file.path(dir, "spec.json"))

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
check(e$H3$cp$lower > 0, "H3 recovers bystanders rising with the checkpoint in the methods arm")
check(e$H3$cp$lower < 0.02 && 0.02 < e$H3$cp$upper + 0.01, "H3's slope is near the simulated one")
check(e$H3$within_class$lower > 0 && e$H3$within_method$lower > 0,
      "H3 recovers bystanders rising within a class and within a method")
check(e$reported$H2_left_class$irr_lower > 1 && e$reported$H2_left_method$irr_lower > 1,
      "the reading with what was introduced beside what stood by is estimated at both levels")
check(!is.null(e$reported$core_reuse_class$irr) && !is.null(e$reported$core_reuse_method$irr),
      "how much a core value is come back to is compared between the arms")
for (lev in c("class", "method")) {
  x <- e$H2[[paste0("reuse_", lev)]]
  check(isTRUE(x$required) && abs(log(x$irr) - log(0.3)) < 0.3 && x$irr_upper < 1 && x$p_less < 0.05 &&
          x$interval == "cluster bootstrap",
        paste("H2's arm contrast recovers a core value come back to 0.3 times as much in the function arm, at the", lev))
}
check(abs(log(e$H4$trodden$irr) - log(0.5)) < 0.2 && e$H4$trodden$irr_upper < 1 &&
        e$H4$trodden$interval == "cluster bootstrap",
      "H4's symmetric count recovers the function arm going back into files half as well-trodden")
check(abs(log(e$reported$existing_files$irr) - log(0.7)) < 0.15,
      "the plain number of existing files gone back into, as first built, is reported")
check(e$H3$within_class$places == 48, "H3 within a class is read on the classes with runs at two checkpoints")
for (lev in c("class", "method")) {
  m <- e$H2[[lev]]
  true <- if (lev == "class") 1.15 else 1.10
  check(m$irr_lower > 1 && m$irr_lower < 3 && 3 < m$irr_upper,
        paste("H2 recovers the core used three times as much per value as the periphery, at the", lev, "level"))
  check(e$reported[[paste0("H2_bystanders_", lev)]]$irr_lower > 1,
        paste("H2 as it stood (later code bound to what stood by) is still estimated, at the", lev, "level"))
  check(abs(log(e$reported[[paste0("H2_bystanders_", lev)]]$irr) - log(true)) < 0.05,
        paste("the ratio per value that stood by is within 5% of the true one,", lev))
  check(abs(log(m$irr) - log(3)) < 0.15, paste("H2's ratio is near the true one,", lev))
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
for (k in names(e$H6$measures)) {
  m <- e$H6$measures[[k]]
  check(m$irr_lower > 0.5 && m$irr_upper < 2, paste("H6 estimates", k, "near no effect"))
}
check(all(sapply(e$H6$measures, function(m) m$p_upper <= m$p_tost && !isTRUE(m$above))),
      "H6's one-sided p is no larger than the two-sided one, and no measure lies above the margin")
check(!is.null(e$reported$H6_class_level$s4_cognitive$irr), "the first block on class-level intrusion is reported")
for (k in c("m_cyclomatic", "c_wmc", "c_god_class")) {
  m <- e$reported$literature_shape[[k]]
  check(!is.null(m$irr) && m$irr_lower > 0.5 && m$irr_upper < 2,
        paste("the literature's", k, "simulated unrelated, is reported near no effect"))
}
check(e$reported$literature_shape$c_wmc$at == "class", "a class measure is read at the class")
check(e$reported$literature_class_rows < e$reported$intrusion_rows$bound,
      "a class measure is read on one row per class and checkpoint")
check(isTRUE(e$reported$literature_shape$c_mi$reversed), "a measure where higher is better is read reversed")
check(setequal(names(e$H6$measures), c("s1_long", "s4_cognitive", "m_cyclomatic", "c_gini", "c_wmc", "c_lcom_star")),
      "H6 is read on its six measures, each alone")
check(e$H6$measures$c_wmc$at == "class" && e$H6$measures$s4_cognitive$at == "method",
      "H6's measures are read at their own level")
check(!is.null(e$reported$shape_joint$measures$s4_cognitive$irr), "the block as first registered is reported")
check(is.null(e$H6$measures$s3_junction), "the junction is not among H6's shape measures")
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
check(abs(e$reported$H3_levels$function_arm$estimate) < 0.01, "the function arm's slope is reported, near flat")
check(abs(e$reported$needed_arm$estimate) < 0.05, "the arms need the same")
check(e$reported$capture_spring$lower > 0, "capture is recovered in the methods arm")
check(e$reported$H3_bindings$log_host$lower > 0, "H3 as first registered (bindings) is reported")
check(e$reported$H4_bindings$arm$upper < 0, "H4 as first registered (bindings) is reported")
check(e$reported$H4_bindings$centre_positions > 3 && e$reported$H4_bindings$centre_positions < 120,
      "the binding-based H4's host size is centred within the data")
check(e$reported$H4_arm_at[["50"]]$estimate < e$reported$H4_arm_at[["10"]]$estimate,
      "the arm difference in bindings widens with host size, as simulated")
check(isTRUE(e$checkpoint_intercept$H3) && isTRUE(e$checkpoint_intercept$H4) &&
      isTRUE(e$checkpoint_intercept$H2_class), "the models carry the checkpoint's intercept")
check(e$reported$formation_lagged_spring$lower > 0, "the lagged formation term is recovered")
check(!is.null(e$reported$junction_x_arm_s3_junction$irr), "junction x arm is estimated")
check(e$reported$H3_without_injected$log_host$lower > 0, "H3 (bindings) without injected dependencies is estimated")
check(!is.null(e$reported$H3_class_level_without_injected$log_class$estimate),
      "class-level H3 (bindings) without injected dependencies is estimated")
check(!is.null(e$reported$H4_without_injected$slope$estimate), "H4 (bindings) without injected dependencies is estimated")
check(!is.null(e$reported$bindings_without_injected_class$irr), "H2 without injected dependencies is estimated")
for (lev in c("class", "method")) {
  x <- e$H1[[lev]]
  check(!is.null(x$irr) && x$irr_upper < 1 && x$p_less < 0.05 && abs(log(x$irr) - log(1 / 3)) < 0.45,
        paste("H1 recovers the falling alternatives, below 1, at the", lev, "(ratio", signif(x$irr, 3), "interval",
              signif(x$irr_lower, 3), signif(x$irr_upper, 3), "p", signif(x$p_less, 3), x$interval, ")"))
  check(x$interval == "cluster bootstrap" && !is.null(x$wald$irr),
        paste("H1 is decided on the cluster bootstrap, the Wald reading beside it, at the", lev))
  check(e$reported[[paste0("H1_margin_", lev)]]$irr_upper < 1.25,
        paste("H1 against the upper margin, as it stood, is reported, at the", lev))
  check(abs(log(e$reported[[paste0("H1_function_arm_", lev)]]$irr)) < 0.3,
        paste("the function arm's flat alternatives are reported, at the", lev))
  check(!is.null(e$reported[[paste0("H1_spread_", lev)]]$methods$forced), paste("the share forced is reported,", lev))
  check(length(e$reported[[paste0("H2_core_width_", lev)]]) > 0, paste("the core's width is reported,", lev))
}
h1c <- e$H1$contrast
check(abs(log(h1c$arm$irr) - log(0.1 / sqrt(0.27))) < 0.35 && h1c$arm$irr_upper < 1 && h1c$arm$interval == "cluster bootstrap",
      "H1's arm contrast recovers fewer forced placements in the function arm half-way through")
check(abs(log(h1c$trend$irr) - log(1 / 3)) < 0.6 && h1c$trend$irr_upper < 1, "H1's arm contrast recovers forcing rising less in the function arm")
check(abs(log(h1c$methods_rise$irr) - log(3)) < 0.35, "the methods arm's forcing tripling over the stream is reported")
check(!is.null(e$reported$H2_class_fields$irr), "H2 at the class on its fields only is reported")
check(e$reported$H1_method_by_type$irr > 1, "H1 by type alone over the whole tree, simulated rising, is reported as such")
check(abs(e$reported$H1_flow$followed - 0.8) < 1e-9, "the share of calls followed is reported")
check(abs(log(e$reported$H7_rise$irr) - log(2)) < 0.3 && e$reported$H7_rise$irr_lower > 1, "the spread doubling over the stream is reported")
check(abs(log(e$reported$H7_rise_forced$irr) - log(2)) < 0.45 && abs(log(e$reported$H7_rise_unforced$irr) - log(2)) < 0.45,
      "the rise in forced and in unforced units is reported apart")
check(abs(log(e$H7$forced$irr) - log(1.5)) < 0.25 && e$H7$forced$irr_lower > 1, "H7 recovers forced units spreading wider at the same size")
check(is.numeric(e$H7$forced$p_upper) && e$H7$forced$level == 0.90 && e$H7$margin[2] == 1.25 &&
        e$H7$forced$p_upper > 0.5, "H7 is tested against the upper margin, 90% interval: a simulated spread of 1.5 is not shown below it")
check(e$reported$H7_forced_without_size$irr > e$H7$forced$irr * 1.2, "without the change's size, the forced ratio is inflated, as simulated")
check(abs(log(e$reported$H7_function_arm$irr)) < 0.35, "the function arm's flat spread is reported")
check(!is.null(e$reported$H7_spread$methods$thirds_classes), "the spread per third is reported")
check(abs(log(e$reported$H7_pair_coupling$irr) - log(3)) < 0.35, "the rising coupling of pairs changed together is recovered")
check(is.null(e$reported$H5_retired_forced) && is.null(e$H5$forced), "forced changes couple is gone")
check(identical(e$coupled_arm$interval, "cluster bootstrap"),
      "H8's calls across the encapsulation are decided on the cluster bootstrap")
check(abs(log(e$H5$arm$irr) - log(0.6)) < 0.2 && e$H5$arm$irr_upper < 1 && e$H5$arm$interval == "cluster bootstrap",
      "H5 recovers the function arm's 0.6 times the links for the same logic, on the cluster bootstrap")
check(abs(log(e$H5$trend$irr) - log(0.5)) < 0.3 && e$H5$trend$irr_upper < 1 && e$H5$trend$interval == "cluster bootstrap",
      "H5 recovers the gap widening over the stream (the trend ratio 0.5)")
check(abs(log(e$reported$H5_methods_rise$irr) - log(2)) < 0.3, "the methods arm's links doubling over the stream is reported")
check(abs(e$reported$H5_logic$estimate - 0.8) < 0.15, "links rising as logic^0.8 is recovered")
check(abs(log(e$reported$H5_unweighted$arm$irr) - log(0.6)) < 0.2, "the plain count of links is reported beside the weights")
check(is.null(e$reported$H5_kinds$flow$arm) && !is.null(e$reported$H5_kinds$call$arm$irr),
      "each kind of link is reported; flow links, none in the methods arm, have no ratio")
check(abs(log(e$coupled_arm$irr) - log(1 / 1.4)) < 0.3,
      "the arms' ratio in calls added at the same change size (Run D's dispersion test) is estimated")
check(e$H2$class$interval == "cluster bootstrap" && e$H4$intrusion_class$interval == "cluster bootstrap",
      "H2 and H4's intrusion ratios are decided on the cluster bootstrap")
check(setequal(names(e$reported$H6_with_coupling$measures),
               c("s1_long", "s4_cognitive", "m_cyclomatic", "m_fanout", "c_gini", "c_wmc", "c_lcom_star")),
      "H6's sensitivity reading puts the literature's coupling measures back")
sx <- e$reported$surface$spring
check(abs(sx$across$estimate - 0.7) < 0.1, "the exponent across classes is recovered")
check(abs(sx$within$estimate - 1.3) < 0.25, "the exponent within a growing class is recovered")
check(abs(sx$added_forced$estimate - 3) < 0.8, "the surface a forced change adds at the same volume is recovered")
rd <- e$reported$reader
check(abs(log(rd$private$author$irr) - log(0.5)) < 0.3 && rd$private$author$irr_upper < 1,
      "reader: the simulated agents' lower odds of making a member private are recovered")
check(abs(rd$private$interaction$estimate - 0.25) < 0.15 && rd$private$interaction$lower > 0,
      "reader: the gap closing as the system grows is recovered")
check(abs(log(rd$opened$author$irr) - log(1.5)) < 0.3, "reader: more members opened, as simulated")
check(abs(log(rd$class_methods$author$irr)) < 0.3 && abs(log(rd$forced$author$irr)) < 0.3,
      "reader: class size and the forced share, simulated equal, are not told apart")
sl <- e$reported$split
check(!is.null(sl$logic_existing_methods$irr) && sl$logic_new_wired_functions$mean$spring == 0,
      "where the logic landed is reported: existing methods, new called methods, new wired functions")
check(abs(log(sl$logic$irr)) < 0.1 && sl$logic$p_tost < 0.05, "logic, simulated the same in both arms, is shown inside the margin")
check(abs(log(sl$params_called_methods$level_95$irr) - log(0.4)) < 0.2 && sl$params_called_methods$level_95$irr_upper < 1,
      "the state handed to called methods, simulated 0.4 times in the function arm, is recovered")
check(abs(log(sl$params_called_methods$trend$irr) - log(0.5)) < 0.35, "its flatter trend in the function arm is recovered")
check(sl$params_new_methods$level_95$irr > sl$params_called_methods$level_95$irr && is.null(sl$params_wired_functions$irr),
      "a wired function's injected parameters are counted apart (none in the methods arm, so no ratio)")
check(sl$declarations$irr > 1.25 && sl$wiring_lines$officefloor > 1.5 && sl$wiring_lines$spring == 0,
      "declarations, simulated higher in the function arm, and the wiring lines are reported as they are")
cat("analysis/analyse.R self-test passed\n")
