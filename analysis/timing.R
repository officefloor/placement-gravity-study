# The time one fit of the study's models takes, by the size of the data (PLAN.md 5: the cluster
# bootstrap refits each model, so the number of refits a history can afford follows from this).
# Simulated rows shaped as H2's base model: a negative binomial count of later intrusions on the
# addition's size, its declared crossings and its host's size, offset by the later checkpoints,
# with the chain's and the checkpoint's intercepts; 60 checkpoints, a chain per 300 rows.
#   Rscript analysis/timing.R OUT.json [ROWS ...]
suppressPackageStartupMessages({ library(glmmTMB); library(jsonlite) })
args <- commandArgs(trailingOnly = TRUE)
out <- args[1]
sizes <- if (length(args) > 1) as.numeric(args[-1]) else c(1800, 15000, 30000, 200000, 1000000)
set.seed(20261116)
time_one <- function(n) {
  chains <- max(2, round(n / 300))
  d <- data.frame(chain_id = factor(sample(chains, n, replace = TRUE)),
                  cp = factor(sample(60, n, replace = TRUE)),
                  log_size = rnorm(n, 2, 1), declared_crossings = rpois(n, 1),
                  log_host = rnorm(n, 3, 1), later = sample(1:59, n, replace = TRUE))
  ce <- rnorm(chains, 0, 0.3)[d$chain_id]
  mu <- exp(-2 + 0.3 * d$log_size + 0.2 * d$log_host + ce) * d$later
  d$y <- rnbinom(n, size = 1.5, mu = mu)
  t <- system.time(glmmTMB(y ~ log_size + declared_crossings + log_host + offset(log(later)) +
                             (1 | chain_id) + (1 | cp), data = d, family = nbinom2()))[["elapsed"]]
  cat(sprintf("%9.0f rows: %8.1f seconds\n", n, t))
  list(rows = n, seconds = unname(t))
}
res <- lapply(sizes, time_one)
info <- list(date = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"), cores = parallel::detectCores(),
             glmmTMB = as.character(packageVersion("glmmTMB")), fits = res)
write_json(info, out, auto_unbox = TRUE, pretty = TRUE, digits = NA)
