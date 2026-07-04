"""
Example: Discover Instagram Reels from a Profile's Posts Tab

Discovers reels that appear on the profile's Posts tab, with
optional date range, post type, and count filters.

Note: This retrieves reels from the Posts tab.  To get reels from
the dedicated Reels tab, see discover_all_reels.py instead.

Usage:
    export BRIGHT_DATA_API_TOKEN="your_api_token_here"
    python examples/discover_reels_from_profile.py
"""

from instagram_reels_scraper import InstagramReelsScraper


def main():
    scraper = InstagramReelsScraper()

    # --- Simple: discover recent reels from a profile ---
    print("=== Discover reels from a profile (simple) ===")
    results = scraper.discover_by_profile(
        "https://www.instagram.com/natgeo",
        num_of_posts=5,
    )
    for reel in results:
        print(f"  URL:        {reel.get('url')}")
        print(f"  Date:       {reel.get('date_posted')}")
        print(f"  Views:      {reel.get('views')}")
        print(f"  Play count: {reel.get('video_play_count')}")
        print()

    # --- With date range and post type filter ---
    print("=== Discover reels with date range + type filter ===")
    results = scraper.discover_by_profile(
        "https://www.instagram.com/marcusfaberfdp",
        num_of_posts=10,
        start_date="01-01-2025",
        end_date="03-01-2025",
        post_type="Reel",
    )
    for reel in results:
        print(f"  URL:      {reel.get('url')}")
        print(f"  Date:     {reel.get('date_posted')}")
        print(f"  Views:    {reel.get('views')}")
        print(f"  Likes:    {reel.get('likes')}")
        print(f"  Hashtags: {reel.get('hashtags')}")
        print()

    # --- Batch: multiple profiles at once ---
    print("=== Batch discover from multiple profiles ===")
    results = scraper.discover_by_profile([
        {
            "url": "https://www.instagram.com/natgeo",
            "num_of_posts": 3,
        },
        {
            "url": "https://www.instagram.com/bbcnews",
            "num_of_posts": 3,
            "start_date": "01-01-2025",
            "end_date": "06-01-2025",
        },
    ])
    for reel in results:
        print(f"  URL:      {reel.get('url')}")
        print(f"  User:     {reel.get('user_posted')}")
        print(f"  Views:    {reel.get('views')}")
        print(f"  Duration: {reel.get('duration')}")
        print()


if __name__ == "__main__":
    main()
