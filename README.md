# Reddit Community Insights

A personal research tool for analyzing Reddit community discussions and trends. Built for learning and non-commercial research purposes.

## Purpose

This tool helps researchers and enthusiasts discover and analyze discussions across Reddit communities, focusing on:

- **Trend Analysis**: Track trending topics in specific subreddits
- **Discussion Insights**: Aggregate and summarize community discussions
- **Content Discovery**: Find relevant posts across communities of interest

## Features

- Read-only access to public Reddit posts and comments
- Keyword-based search and filtering
- Basic trend analysis and visualization
- Local caching to minimize API calls
- Rate-limited to respect Reddit API guidelines (≤60 req/min)

## Tech Stack

- Python 3.10+
- PRAW (Python Reddit API Wrapper)
- SQLite (local data caching)
- Matplotlib (data visualization)

## Data & Privacy Policy

- **Read-only**: This tool does NOT post, comment, vote, or modify any content on Reddit
- **No personal data collection**: No user personal information is collected or stored
- **No commercial use**: This is a personal research project
- **Local only**: All data is processed and stored locally
- **Rate limiting**: Strict adherence to Reddit API rate limits

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/reddit-community-insights.git
cd reddit-community-insights
pip install -r requirements.txt
cp .env.example .env
# Add your Reddit API credentials to .env
python main.py
```

## API Usage

This project uses the following Reddit API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/r/{subreddit}/hot` | GET | Fetch trending posts |
| `/r/{subreddit}/new` | GET | Fetch latest posts |
| `/r/{subreddit}/search` | GET | Search by keyword |
| `/comments/{article}` | GET | Read post comments |

## Project Structure

```
reddit-community-insights/
├── README.md               # Project documentation
├── LICENSE                  # MIT License
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── main.py                 # Main entry point
└── src/
    ├── __init__.py         # Package init
    ├── reddit_client.py    # Reddit API client wrapper
    └── analyzer.py         # Data analysis module
```

## License

MIT License - Personal research use only.
