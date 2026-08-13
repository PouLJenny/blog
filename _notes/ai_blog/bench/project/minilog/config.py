"""Project-wide defaults."""

# Minimum level shown by the CLI when --min-level is not given.
DEFAULT_MIN_LEVEL = "INFO"

# A record with duration strictly greater than this many milliseconds
# counts as "slow".
SLOW_THRESHOLD_MS = 500

LEVEL_ORDER = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
