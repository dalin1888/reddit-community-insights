"""
Reddit Community Insights - Main Entry Point

A read-only research tool for analyzing Reddit community discussions
and trends. This tool is designed for personal learning and
non-commercial research purposes only.

Usage:
    python main.py                     # Run with default settings
    python main.py --subreddit gaming  # Analyze a specific subreddit
"""

import argparse
import logging
from datetime import datetime

from src.reddit_client import RedditClient
from src.analyzer import PostAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Default subreddits to analyze
DEFAULT_SUBREDDITS = ["gaming", "movies", "television", "Music", "books"]


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Reddit Community Insights - Research Tool"
    )
    parser.add_argument(
        "--subreddit",
        "-s",
        type=str,
        default=None,
        help="Specific subreddit to analyze (without r/ prefix)",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=25,
        help="Number of posts to fetch (default: 25)",
    )
    parser.add_argument(
        "--sort",
        choices=["hot", "new", "top"],
        default="hot",
        help="Sort order for posts (default: hot)",
    )
    parser.add_argument(
        "--search",
        type=str,
        default=None,
        help="Search keyword within subreddit",
    )
    return parser.parse_args()


def display_posts(posts, subreddit_name):
    """Display fetched posts in a formatted table."""
    print(f"\n{'=' * 70}")
    print(f"  r/{subreddit_name} - Top {len(posts)} Posts")
    print(f"  Fetched at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 70}")

    for i, post in enumerate(posts, 1):
        score = post.get("score", 0)
        comments = post.get("num_comments", 0)
        title = post.get("title", "No title")

        # Truncate long titles
        if len(title) > 60:
            title = title[:57] + "..."

        print(f"  {i:>3}. [{score:>6}↑ | {comments:>4}💬] {title}")

    print(f"{'=' * 70}\n")


def display_analysis(analysis):
    """Display analysis results."""
    print(f"\n📊 Analysis Summary")
    print(f"{'-' * 40}")
    print(f"  Total posts analyzed: {analysis.get('total_posts', 0)}")
    print(f"  Average score:        {analysis.get('avg_score', 0):.1f}")
    print(f"  Average comments:     {analysis.get('avg_comments', 0):.1f}")
    print(f"  Total engagement:     {analysis.get('total_engagement', 0)}")
    print(f"{'-' * 40}\n")


def main():
    """Main entry point for the application."""
    args = parse_args()

    print("\n🔍 Reddit Community Insights - Research Tool")
    print("   Read-only | Non-commercial | Personal Research\n")

    # Initialize Reddit client
    try:
        client = RedditClient()
        logger.info("Reddit client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Reddit client: {e}")
        print("❌ Error: Could not connect to Reddit API.")
        print("   Please check your .env file and API credentials.")
        print("   See .env.example for required variables.")
        return

    # Determine which subreddits to analyze
    subreddits = [args.subreddit] if args.subreddit else DEFAULT_SUBREDDITS

    analyzer = PostAnalyzer()

    for subreddit_name in subreddits:
        try:
            # Fetch posts
            if args.search:
                logger.info(
                    f"Searching r/{subreddit_name} for: {args.search}"
                )
                posts = client.search_posts(
                    subreddit_name, args.search, limit=args.limit
                )
            else:
                logger.info(
                    f"Fetching {args.sort} posts from r/{subreddit_name}"
                )
                posts = client.fetch_posts(
                    subreddit_name, sort=args.sort, limit=args.limit
                )

            if posts:
                display_posts(posts, subreddit_name)

                # Run basic analysis
                analysis = analyzer.analyze_posts(posts)
                display_analysis(analysis)
            else:
                print(f"  No posts found in r/{subreddit_name}")

        except Exception as e:
            logger.error(f"Error processing r/{subreddit_name}: {e}")
            print(f"  ⚠️ Could not fetch data from r/{subreddit_name}: {e}")

    print("✅ Done! Thank you for using Reddit Community Insights.\n")


if __name__ == "__main__":
    main()
