"""
Post Analyzer - Basic analysis of Reddit posts.

Provides simple statistics and trend analysis for fetched posts.
All analysis is performed locally on publicly available data.
"""

import logging
from collections import Counter

logger = logging.getLogger(__name__)


class PostAnalyzer:
    """Analyzes collections of Reddit posts for basic insights."""

    def analyze_posts(self, posts):
        """
        Perform basic analysis on a list of posts.

        Args:
            posts: List of post dictionaries

        Returns:
            Dictionary with analysis results
        """
        if not posts:
            return {
                "total_posts": 0,
                "avg_score": 0,
                "avg_comments": 0,
                "total_engagement": 0,
            }

        scores = [p.get("score", 0) for p in posts]
        comments = [p.get("num_comments", 0) for p in posts]

        analysis = {
            "total_posts": len(posts),
            "avg_score": sum(scores) / len(scores),
            "avg_comments": sum(comments) / len(comments),
            "max_score": max(scores),
            "min_score": min(scores),
            "total_engagement": sum(scores) + sum(comments),
            "top_posts": self._get_top_posts(posts, n=5),
            "most_discussed": self._get_most_discussed(posts, n=5),
        }

        logger.info(f"Analyzed {len(posts)} posts")
        return analysis

    def _get_top_posts(self, posts, n=5):
        """Get the top N posts by score."""
        sorted_posts = sorted(
            posts, key=lambda p: p.get("score", 0), reverse=True
        )
        return sorted_posts[:n]

    def _get_most_discussed(self, posts, n=5):
        """Get the top N posts by comment count."""
        sorted_posts = sorted(
            posts, key=lambda p: p.get("num_comments", 0), reverse=True
        )
        return sorted_posts[:n]

    def extract_keywords(self, posts, top_n=20):
        """
        Extract the most common words from post titles.

        Args:
            posts: List of post dictionaries
            top_n: Number of top keywords to return

        Returns:
            List of (word, count) tuples
        """
        # Common words to exclude
        stop_words = {
            "the", "a", "an", "is", "it", "in", "on", "at", "to",
            "for", "of", "and", "or", "but", "not", "with", "this",
            "that", "from", "by", "are", "was", "were", "be", "been",
            "has", "have", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "can", "i", "you", "he",
            "she", "we", "they", "my", "your", "his", "her", "our",
            "their", "me", "him", "us", "them", "what", "which", "who",
            "when", "where", "why", "how", "all", "each", "every",
            "both", "few", "more", "most", "other", "some", "such",
            "no", "nor", "only", "own", "same", "so", "than", "too",
            "very", "just", "about", "up", "out", "if", "into", "as",
        }

        word_counter = Counter()

        for post in posts:
            title = post.get("title", "")
            words = title.lower().split()
            # Filter: remove short words, stop words, and non-alpha
            filtered_words = [
                w for w in words
                if len(w) > 2 and w.isalpha() and w not in stop_words
            ]
            word_counter.update(filtered_words)

        return word_counter.most_common(top_n)

    def compare_subreddits(self, subreddit_data):
        """
        Compare engagement metrics across multiple subreddits.

        Args:
            subreddit_data: Dict of {subreddit_name: [posts]}

        Returns:
            List of comparison dictionaries
        """
        comparisons = []

        for name, posts in subreddit_data.items():
            if not posts:
                continue

            analysis = self.analyze_posts(posts)
            comparisons.append(
                {
                    "subreddit": name,
                    "total_posts": analysis["total_posts"],
                    "avg_score": analysis["avg_score"],
                    "avg_comments": analysis["avg_comments"],
                    "total_engagement": analysis["total_engagement"],
                }
            )

        # Sort by total engagement
        comparisons.sort(
            key=lambda x: x["total_engagement"], reverse=True
        )

        return comparisons
