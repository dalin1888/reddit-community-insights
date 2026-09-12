# Reddit Community Insights

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Read Only](https://img.shields.io/badge/Reddit%20API-Read%20Only-orange.svg)](#data--privacy-policy)

> A personal, non-commercial research tool for analyzing Reddit community discussions and trends.

## 🎯 Purpose

Reddit Community Insights helps enthusiasts discover and analyze discussions across Reddit communities they care about. Instead of manually browsing multiple subreddits, users get a consolidated view of trending topics, popular discussions, and community engagement patterns.

**This tool is built for personal learning and research — it is NOT a commercial product.**

### Key Benefits for Redditors
- **Content Discovery** — Quickly find relevant and trending discussions across interest-based communities
- **Community Trends** — Understand what topics generate the most engagement in your favorite subreddits
- **Research** — Analyze discussion patterns for personal learning and academic research

## ✨ Features

- 🔒 **Strict Read-Only** — Never posts, comments, votes, or modifies any content
- 📊 **Trend Analysis** — Track trending topics and engagement metrics
- 🔍 **Keyword Search** — Filter posts across subreddits by topic
- 📈 **Basic Analytics** — Engagement stats, keyword extraction, subreddit comparison
- ⏱️ **Rate Limited** — Respects Reddit's API rate limits (≤60 req/min)
- 💾 **Local Caching** — Minimizes redundant API calls with 24-hour local cache
- 🛡️ **Privacy First** — No user data collected; all processing is local

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Reddit API | [PRAW](https://praw.readthedocs.io/) (Python Reddit API Wrapper) |
| Database | SQLite (local caching only) |
| Visualization | Matplotlib |
| Analysis | pandas |

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/dalin1888/reddit-community-insights.git
cd reddit-community-insights

# Install dependencies
pip install -r requirements.txt

# Configure API credentials
cp .env.example .env
# Edit .env with your Reddit API credentials
```

## 🚀 Usage

```bash
# Analyze default subreddits (gaming, movies, etc.)
python main.py

# Analyze a specific subreddit
python main.py --subreddit gaming --limit 50

# Search for specific topics
python main.py --subreddit movies --search "best films 2026"

# Sort by newest posts
python main.py --subreddit technology --sort new
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--subreddit`, `-s` | Specific subreddit to analyze | All defaults |
| `--limit`, `-l` | Number of posts to fetch (max 100) | 25 |
| `--sort` | Sort order: `hot`, `new`, `top` | `hot` |
| `--search` | Search keyword within subreddit | None |

## 🔌 API Endpoints Used

This project uses **only** the following read-only Reddit API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/r/{subreddit}/hot` | GET | Fetch trending/popular posts |
| `/r/{subreddit}/new` | GET | Fetch latest posts |
| `/r/{subreddit}/top` | GET | Fetch top posts by time period |
| `/r/{subreddit}/search` | GET | Search posts by keyword |
| `/comments/{article}` | GET | Read comments on a specific post |
| `/api/v1/me` | GET | Verify authenticated account |

**No write endpoints are used.** The application explicitly sets `reddit.read_only = True`.

## 📁 Project Structure

```
reddit-community-insights/
├── README.md               # Project documentation
├── LICENSE                  # MIT License
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── main.py                 # Main entry point with CLI
└── src/
    ├── __init__.py         # Package initialization
    ├── reddit_client.py    # Reddit API client (read-only, rate-limited)
    └── analyzer.py         # Post analysis and keyword extraction
```

## 🔒 Data & Privacy Policy

| Policy | Details |
|--------|---------|
| **Access Mode** | Strict read-only (`reddit.read_only = True`) |
| **Data Collection** | No personal user data is collected or stored |
| **Data Sharing** | No data is shared with any third party |
| **Data Storage** | All data processed and stored locally only |
| **Data Retention** | Local cache expires after 24 hours |
| **API Compliance** | Strict rate limiting (≤60 requests/minute) |
| **Content Modification** | Never posts, comments, votes, or sends messages |
| **Commercial Use** | None — this is a personal research project |
| **Web Scraping** | None — only official API endpoints are used |

## ⚙️ Configuration

Create a `.env` file based on `.env.example`:

```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=RedditCommunityInsights/1.0 by your_reddit_username
```

## 🤝 Contributing

This is a personal research project. Feel free to fork it for your own learning purposes.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: This tool is for personal research and educational purposes only. It is not affiliated with, endorsed by, or sponsored by Reddit, Inc. All data accessed through this tool is publicly available via Reddit's official API.
