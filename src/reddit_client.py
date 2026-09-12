"""
Reddit API Client - Read-Only Wrapper

Provides a clean interface to the Reddit API using PRAW.
All operations are strictly read-only.
"""

import logging
import os
import time

import praw
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Rate limiting: max 60 requests per minute
REQUEST_INTERVAL = 1.0  # seconds between requests


class RedditClient:
    """A read-only Reddit API client with built-in rate limiting."""

    def __init__(self):
        """Initialize the Reddit client with OAuth2 credentials."""
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT")

        if not all([client_id, client_secret, user_agent]):
            raise ValueError(
                "Missing Reddit API credentials. "
                "Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, "
                "and REDDIT_USER_AGENT in your .env file."
            )

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        # IMPORTANT: Enforce read-only mode
        self.reddit.read_only = True

        self._last_request_time = 0
        logger.info("Reddit client initialized in read-only mode")

    def _rate_limit(self):
        """Enforce rate limiting between API requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < REQUEST_INTERVAL:
            sleep_time = REQUEST_INTERVAL - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self._last_request_time = time.time()

    def _post_to_dict(self, post):
        """Convert a PRAW submission object to a dictionary."""
        return {
            "id": post.id,
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
            "url": post.url,
            "selftext": post.selftext[:500] if post.selftext else "",
            "author": str(post.author) if post.author else "[deleted]",
            "subreddit": str(post.subreddit),
            "permalink": f"https://reddit.com{post.permalink}",
        }

    def fetch_posts(self, subreddit_name, sort="hot", limit=25):
        """
        Fetch posts from a subreddit.

        Args:
            subreddit_name: Name of the subreddit (without r/ prefix)
            sort: Sort order - 'hot', 'new', or 'top'
            limit: Maximum number of posts to fetch (max 100)

        Returns:
            List of post dictionaries
        """
        self._rate_limit()
        limit = min(limit, 100)  # Cap at 100 to be respectful

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            if sort == "hot":
                submissions = subreddit.hot(limit=limit)
            elif sort == "new":
                submissions = subreddit.new(limit=limit)
            elif sort == "top":
                submissions = subreddit.top(limit=limit, time_filter="week")
            else:
                submissions = subreddit.hot(limit=limit)

            posts = [self._post_to_dict(post) for post in submissions]
            logger.info(
                f"Fetched {len(posts)} posts from r/{subreddit_name} "
                f"(sort={sort})"
            )
            return posts

        except Exception as e:
            logger.error(
                f"Error fetching posts from r/{subreddit_name}: {e}"
            )
            raise

    def search_posts(self, subreddit_name, query, limit=25):
        """
        Search for posts in a subreddit by keyword.

        Args:
            subreddit_name: Name of the subreddit (without r/ prefix)
            query: Search keyword or phrase
            limit: Maximum number of results (max 100)

        Returns:
            List of matching post dictionaries
        """
        self._rate_limit()
        limit = min(limit, 100)

        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            results = subreddit.search(query, limit=limit, sort="relevance")

            posts = [self._post_to_dict(post) for post in results]
            logger.info(
                f"Found {len(posts)} results for '{query}' "
                f"in r/{subreddit_name}"
            )
            return posts

        except Exception as e:
            logger.error(
                f"Error searching r/{subreddit_name} for '{query}': {e}"
            )
            raise

    def fetch_comments(self, post_id, limit=50):
        """
        Fetch comments for a specific post.

        Args:
            post_id: The Reddit post ID
            limit: Maximum number of top-level comments (max 100)

        Returns:
            List of comment dictionaries
        """
        self._rate_limit()
        limit = min(limit, 100)

        try:
            submission = self.reddit.submission(id=post_id)
            submission.comment_sort = "best"
            submission.comments.replace_more(limit=0)  # Skip "load more"

            comments = []
            for comment in submission.comments[:limit]:
                comments.append(
                    {
                        "id": comment.id,
                        "body": comment.body[:500],
                        "score": comment.score,
                        "author": (
                            str(comment.author)
                            if comment.author
                            else "[deleted]"
                        ),
                        "created_utc": comment.created_utc,
                    }
                )

            logger.info(
                f"Fetched {len(comments)} comments for post {post_id}"
            )
            return comments

        except Exception as e:
            logger.error(
                f"Error fetching comments for post {post_id}: {e}"
            )
            raise
