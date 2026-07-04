"""
Example: Collect Instagram Reels by URL

Fetches reel data for specific Instagram reel URLs using the
Bright Data Instagram Reels scraper.  Optionally pass a country
code to geo-target the request.

Usage:
    export BRIGHT_DATA_API_TOKEN="your_api_token_here"
    python examples/collect_reels.py
"""

from instagram_reels_scraper import InstagramReelsScraper


def main():
    scraper = InstagramReelsScraper()

    # --- Single reel ---
    print("=== Collecting a single reel ===")
    results = scraper.collect_by_url(
        "https://www.instagram.com/reel/C5Rdyj_q7YN/"
    )
    for reel in results:
        print(f"  URL:        {reel.get('url')}")
        print(f"  User:       {reel.get('user_posted')}")
        print(f"  Views:      {reel.get('views')}")
        print(f"  Play count: {reel.get('video_play_count')}")
        print(f"  Likes:      {reel.get('likes')}")
        print(f"  Duration:   {reel.get('duration')}")
        print()

    # --- Multiple reels with country code ---
    print("=== Collecting multiple reels (geo: US) ===")
    results = scraper.collect_by_url(
        [
            "https://www.instagram.com/reel/C5Rdyj_q7YN/",
            "https://www.instagram.com/reel/C85BZjeSHuO",
        ],
        country_code="US",
    )
    for reel in results:
        print(f"  URL:         {reel.get('url')}")
        print(f"  User:        {reel.get('user_posted')}")
        print(f"  Description: {reel.get('description', '')[:80]}...")
        print(f"  Views:       {reel.get('views')}")
        print(f"  Likes:       {reel.get('likes')}")
        print(f"  Comments:    {reel.get('num_comments')}")
        print(f"  Hashtags:    {reel.get('hashtags')}")
        print()


if __name__ == "__main__":
    main()
