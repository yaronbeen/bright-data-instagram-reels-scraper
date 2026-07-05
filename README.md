# Bright Data Instagram Reels Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

A Python wrapper for Bright Data's Instagram Reels scraper API. Collect detailed reel data by URL with optional geo-targeting.

> **All Instagram scrapers:** [Profile Scraper](https://github.com/yaronbeen/bright-data-instagram-profile-scraper) · [Profile Discovery](https://github.com/yaronbeen/bright-data-instagram-profile-discovery) · [Posts Scraper](https://github.com/yaronbeen/bright-data-instagram-posts-scraper) · [Posts Discovery](https://github.com/yaronbeen/bright-data-instagram-posts-discovery) · **Reels Scraper** · [Reels Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-discovery) · [Reels (All) Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-all-discovery) · [Comments Scraper](https://github.com/yaronbeen/bright-data-instagram-comments-scraper)

## Features

- **Collect by URL** - Fetch full reel data from one or more Instagram reel URLs
- **Batch support** - Process multiple URLs in a single API call
- **27 data fields** - Views, play count, likes, comments, video URL, thumbnail, duration, and more
- **Geo-targeting** - Pass a country code to collect location-specific reel data
- **Simple interface** - Clean Pythonic API with type hints
- **Fast** - Average response time of ~5 seconds

## Use Cases

- Benchmark reel performance (views vs. likes ratio)
- Track viral reel metrics and play counts
- Analyze top-performing reel formats by engagement
- Monitor competitor reel strategy

## Prerequisites

- Python 3.8 or higher
- A Bright Data account with API access (create an account at https://brightdata.com)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yaronbeen/bright-data-instagram-reels-scraper.git
cd bright-data-instagram-reels-scraper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your API token:

```bash
cp .env.example .env
# Edit .env and add your Bright Data API token
```

Or export it directly:

```bash
export BRIGHT_DATA_API_TOKEN="your_api_token_here"
```

## Quick Start

```python
from instagram_reels_scraper import InstagramReelsScraper

scraper = InstagramReelsScraper()

# Collect a specific reel
results = scraper.collect_by_url("https://www.instagram.com/reel/C5Rdyj_q7YN/")
for reel in results:
    print(f"{reel['user_posted']}: {reel['views']} views, {reel['likes']} likes")
```

## API Reference

### `InstagramReelsScraper(api_token=None)`

Create a scraper instance.

| Parameter   | Type            | Required | Description                                                                 |
|-------------|-----------------|----------|-----------------------------------------------------------------------------|
| `api_token` | `str` or `None` | No       | Bright Data API token. Falls back to `BRIGHT_DATA_API_TOKEN` env variable. |

---

### `collect_by_url(urls, country_code=None, limit_per_input=None)`

Collect reel data from specific Instagram reel URLs.

| Parameter         | Type               | Required | Description                                        |
|-------------------|--------------------|----------|----------------------------------------------------|
| `urls`            | `str` or `list`    | Yes      | Single URL string or list of Instagram reel URLs   |
| `country_code`    | `str` or `None`    | No       | 2-letter country code for geo-targeting (e.g. "US") |
| `limit_per_input` | `int` or `None`    | No       | Max records to return per input URL                |

**Returns:** `list[dict]` - List of reel data dictionaries.

**Example:**

```python
# Single reel
results = scraper.collect_by_url("https://www.instagram.com/reel/C5Rdyj_q7YN/")

# Multiple reels with geo-targeting
results = scraper.collect_by_url(
    [
        "https://www.instagram.com/reel/C5Rdyj_q7YN/",
        "https://www.instagram.com/reel/C85BZjeSHuO",
    ],
    country_code="US",
)
```

## Output Fields

Each reel record contains up to 27 fields. Key fields include:

| Field              | Type     | Description                            |
|--------------------|----------|----------------------------------------|
| `url`              | `str`    | Reel URL                              |
| `user_posted`      | `str`    | Username of the poster                |
| `description`      | `str`    | Reel caption / description            |
| `hashtags`         | `list`   | List of hashtags                      |
| `num_comments`     | `int`    | Number of comments                    |
| `date_posted`      | `str`    | ISO 8601 timestamp                    |
| `likes`            | `int`    | Number of likes                       |
| `views`            | `int`    | Number of views                       |
| `video_play_count` | `int`    | Total video play count                |
| `top_comments`     | `list`   | List of top comments with text/owner  |
| `video_url`        | `str`    | Direct URL to the reel video file     |
| `thumbnail_url`    | `str`    | Reel thumbnail image URL             |
| `duration`         | `float`  | Reel duration in seconds              |

## Example Output

```json
{
    "url": "https://www.instagram.com/reel/C5Rdyj_q7YN/",
    "user_posted": "minimalistbaker",
    "description": "5-ingredient peanut butter cups that take 15 minutes. Save this one.",
    "hashtags": ["veganrecipes", "minimalistbaker", "dessert"],
    "num_comments": 73,
    "date_posted": "2024-04-10T14:30:00.000Z",
    "likes": 11247,
    "views": 289413,
    "video_play_count": 341876,
    "top_comments": [
        {"text": "Making these tonight!", "owner": "healthy_habits_co"},
        {"text": "Tried it and it's amazing", "owner": "mealprep_sarah"}
    ],
    "video_url": "https://scontent.cdninstagram.com/v/t50.2886-16/reel1.mp4",
    "thumbnail_url": "https://scontent.cdninstagram.com/v/t51.2885-15/thumb1.jpg",
    "duration": 27.3
}
```

> Note: This is a representative example. Actual field values and available fields may vary.

## Error Handling

The scraper raises standard exceptions you can catch:

```python
import requests
from instagram_reels_scraper import InstagramReelsScraper

try:
    scraper = InstagramReelsScraper()
    results = scraper.collect_by_url("https://www.instagram.com/reel/C5Rdyj_q7YN/")
except ValueError as e:
    print(f"Configuration error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")
except requests.exceptions.ConnectionError:
    print("Could not connect to the API")
```

| Exception                          | Cause                                  |
|------------------------------------|----------------------------------------|
| `ValueError`                       | Missing API token.                     |
| `requests.exceptions.HTTPError`    | API returned 4xx/5xx (auth, rate limit, etc.). |
| `requests.exceptions.ConnectionError` | Network connectivity issue.         |
| `requests.exceptions.ReadTimeout`  | Request took longer than 30 seconds.   |

## Rate Limits

- **Sync mode:** Results returned directly in the response. Best for small batches (1-10 inputs).
- **Async mode:** For larger jobs, use the async API. See [Bright Data API docs](https://docs.brightdata.com/datasets/functions/introduction).
- **No hard rate limit** on API calls, but performance varies with batch size.
- **Pricing:** $0.0015 per record ($1.50 per 1,000 records).

## Running Tests

```bash
python -m pytest tests/ -v
```

## Why Bright Data?

Reel metrics like view counts and play counts aren't available through Instagram's public API. Bright Data fills the gap:

- **View counts, play counts, and engagement data** that Instagram doesn't expose publicly
- **Optional geo-targeting** with `country_code` parameter for location-specific data
- **Video URLs included** (note: may expire per Instagram's CDN policy)
- **$0.0015/record** with 27 structured fields per reel
- **Reliable delivery** - Handles Instagram's frequent anti-scraping updates automatically

For full API documentation, see the [Bright Data API Reference](https://docs.brightdata.com/datasets/functions/introduction).

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclosure:** Some links in this document are affiliate links. If you sign up for Bright Data through these links, I may earn a commission at no extra cost to you. This helps support the maintenance of this project.
