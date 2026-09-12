"""
Cache Manager - Local SQLite caching for Reddit data.

Implements a simple caching layer to minimize redundant API calls
and respect Reddit's rate limits. Cache entries expire after 24 hours.
"""

import json
import logging
import sqlite3
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# Cache expiration time: 24 hours
CACHE_TTL = 24 * 60 * 60  # seconds

# Database file location
DB_PATH = Path(__file__).parent.parent / "data" / "cache.db"


class CacheManager:
    """Local SQLite cache for Reddit API responses."""

    def __init__(self, db_path=None):
        """
        Initialize the cache manager.

        Args:
            db_path: Path to the SQLite database file.
                     Defaults to data/cache.db in the project root.
        """
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        logger.info(f"Cache initialized at {self.db_path}")

    def _init_db(self):
        """Create the cache table if it doesn't exist."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )
            conn.commit()

    def get(self, key):
        """
        Retrieve a cached value by key.

        Args:
            key: The cache key

        Returns:
            The cached value (deserialized from JSON), or None if not
            found or expired.
        """
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute(
                "SELECT value, created_at FROM cache WHERE key = ?",
                (key,),
            )
            row = cursor.fetchone()

            if row is None:
                logger.debug(f"Cache miss: {key}")
                return None

            value, created_at = row

            # Check if expired
            if time.time() - created_at > CACHE_TTL:
                logger.debug(f"Cache expired: {key}")
                conn.execute("DELETE FROM cache WHERE key = ?", (key,))
                conn.commit()
                return None

            logger.debug(f"Cache hit: {key}")
            return json.loads(value)

    def set(self, key, value):
        """
        Store a value in the cache.

        Args:
            key: The cache key
            value: The value to cache (must be JSON-serializable)
        """
        serialized = json.dumps(value)
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cache (key, value, created_at)
                VALUES (?, ?, ?)
                """,
                (key, serialized, time.time()),
            )
            conn.commit()
        logger.debug(f"Cache set: {key}")

    def clear(self):
        """Remove all entries from the cache."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("DELETE FROM cache")
            conn.commit()
        logger.info("Cache cleared")

    def clear_expired(self):
        """Remove only expired entries from the cache."""
        cutoff = time.time() - CACHE_TTL
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute(
                "DELETE FROM cache WHERE created_at < ?", (cutoff,)
            )
            conn.commit()
            count = cursor.rowcount
        logger.info(f"Cleared {count} expired cache entries")
        return count

    def stats(self):
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats (total entries, expired count, etc.)
        """
        with sqlite3.connect(str(self.db_path)) as conn:
            total = conn.execute(
                "SELECT COUNT(*) FROM cache"
            ).fetchone()[0]

            cutoff = time.time() - CACHE_TTL
            expired = conn.execute(
                "SELECT COUNT(*) FROM cache WHERE created_at < ?",
                (cutoff,),
            ).fetchone()[0]

        return {
            "total_entries": total,
            "active_entries": total - expired,
            "expired_entries": expired,
            "db_path": str(self.db_path),
        }
