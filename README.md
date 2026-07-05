# Bright Data Instagram Reels Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

A Python wrapper for [Bright Data's Instagram Reels scraper API](https://get.brightdata.com/1tndi4600b25). Collect detailed reel data by URL with optional geo-targeting.

## Features

- **Collect by URL** - Fetch full reel data from one or more Instagram reel URLs
- **Batch support** - Process multiple URLs in a single API call
- **27 data fields** - Views, play count, likes, comments, video URL, thumbnail, duration, and more
- **Geo-targeting** - Pass a country code to collect location-specific reel data
- **Simple interface** - Clean Pythonic API with type hints
- **Fast** - Average response time of ~5 seconds

## Prerequisites

- Python 3.8 or higher
- A Bright Data account with API access - [Sign up here](https://get.brightdata.com/1tndi4600b25)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/luminati-io/bright-data-instagram-reels-scraper.git
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
    "user_posted": "natgeo",
    "description": "Watch this incredible timelapse of the Northern Lights.",
    "hashtags": ["nature", "northernlights", "timelapse"],
    "num_comments": 218,
    "date_posted": "2024-04-10T14:30:00.000Z",
    "likes": 95000,
    "views": 2500000,
    "video_play_count": 3100000,
    "top_comments": [
        {"text": "Absolutely stunning!", "owner": "user1"},
        {"text": "Nature is amazing", "owner": "user2"}
    ],
    "video_url": "https://scontent.cdninstagram.com/v/reel1.mp4",
    "thumbnail_url": "https://scontent.cdninstagram.com/v/thumb1.jpg",
    "duration": 29.5
}
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Why Bright Data?

[Bright Data](https://get.brightdata.com/1tndi4600b25) provides the most reliable infrastructure for web data collection:

- **Pre-built scrapers** - No need to build or maintain scraping logic
- **Structured data** - Clean JSON output with 27+ fields per reel
- **High success rate** - Built-in proxy rotation and anti-blocking
- **Scalable** - Handle thousands of requests with consistent performance
- **Compliant** - Ethical data collection with full regulatory compliance
- **Pay per result** - Only $0.0015 per record with no upfront costs

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclosure:** Some links in this document are affiliate links. If you sign up for Bright Data through these links, I may earn a commission at no extra cost to you. This helps support the maintenance of this project.
