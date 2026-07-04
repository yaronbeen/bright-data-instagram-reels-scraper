"""
Example: Discover All Reels from a Profile's Reels Tab

Retrieves reels from the profile's dedicated **Reels** tab (not the
Posts tab).  This is useful when you want every reel a profile has
published, regardless of whether it also appears in the Posts grid.

Usage:
    export BRIGHT_DATA_API_TOKEN="your_api_token_here"
    python examples/discover_all_reels.py
"""

from instagram_reels_scraper import InstagramReelsScraper


def main():
    scraper = InstagramReelsScraper()

    # --- Single profile ---
    print("=== All reels from a single profile ===")
    results = scraper.discover_all_reels(
        "https://www.instagram.com/natgeo"
    )
    for reel in results:
        print(f"  URL:        {reel.get('url')}")
        print(f"  User:       {reel.get('user_posted')}")
        print(f"  Views:      {reel.get('views')}")
        print(f"  Play count: {reel.get('video_play_count')}")
        print(f"  Likes:      {reel.get('likes')}")
        print(f"  Duration:   {reel.get('duration')}")
        print(f"  Video URL:  {reel.get('video_url')}")
        print()

    # --- Multiple profiles ---
    print("=== All reels from multiple profiles ===")
    results = scraper.discover_all_reels([
        "https://www.instagram.com/natgeo",
        "https://www.instagram.com/bbcnews",
    ])
    for reel in results:
        print(f"  URL:         {reel.get('url')}")
        print(f"  User:        {reel.get('user_posted')}")
        print(f"  Description: {reel.get('description', '')[:80]}...")
        print(f"  Views:       {reel.get('views')}")
        print(f"  Likes:       {reel.get('likes')}")
        print(f"  Thumbnail:   {reel.get('thumbnail_url')}")
        print()


if __name__ == "__main__":
    main()
