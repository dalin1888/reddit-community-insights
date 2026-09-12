"""
Configuration - Application settings and constants.

Centralizes all configuration values for easy review and auditing.
"""

# === API Rate Limiting ===
# Reddit API allows 60 requests per minute for OAuth clients.
# We use a conservative limit to be respectful.
MAX_REQUESTS_PER_MINUTE = 60
REQUEST_INTERVAL_SECONDS = 1.0  # Minimum time between requests

# === Cache Settings ===
CACHE_TTL_HOURS = 24  # How long to keep cached data
CACHE_TTL_SECONDS = CACHE_TTL_HOURS * 60 * 60

# === Fetch Limits ===
# Maximum posts/comments to fetch per request.
# Capped at 100 to avoid excessive API usage.
MAX_POSTS_PER_REQUEST = 100
MAX_COMMENTS_PER_REQUEST = 100
DEFAULT_POST_LIMIT = 25

# === Default Subreddits ===
# Interest-based communities for personal research
DEFAULT_SUBREDDITS = [
    "gaming",
    "movies",
    "television",
    "Music",
    "books",
]

# === Content Truncation ===
# Truncate long text fields to save memory
MAX_SELFTEXT_LENGTH = 500
MAX_COMMENT_LENGTH = 500
MAX_TITLE_DISPLAY_LENGTH = 60
