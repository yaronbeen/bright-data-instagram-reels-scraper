"""
Comprehensive unit tests for InstagramReelsScraper.

All HTTP calls are mocked -- no real API traffic is generated.
Run with:
    python -m pytest tests/ -v
"""

import os
import unittest
from unittest.mock import patch, MagicMock

import requests

from instagram_reels_scraper import InstagramReelsScraper


# ---------------------------------------------------------------------------
# Sample response fixtures
# ---------------------------------------------------------------------------

SAMPLE_REEL = {
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
        {"text": "Nature is amazing", "owner": "user2"},
    ],
    "video_url": "https://scontent.cdninstagram.com/v/reel1.mp4",
    "thumbnail_url": "https://scontent.cdninstagram.com/v/thumb1.jpg",
    "duration": 29.5,
}

SAMPLE_REEL_2 = {
    "url": "https://www.instagram.com/reel/C85BZjeSHuO",
    "user_posted": "bbcnews",
    "description": "Breaking: latest developments from the summit.",
    "hashtags": ["news", "breaking"],
    "num_comments": 87,
    "date_posted": "2024-06-20T09:15:00.000Z",
    "likes": 42000,
    "views": 890000,
    "video_play_count": 1020000,
    "top_comments": [],
    "video_url": "https://scontent.cdninstagram.com/v/reel2.mp4",
    "thumbnail_url": "https://scontent.cdninstagram.com/v/thumb2.jpg",
    "duration": 15.0,
}


class TestInstagramReelsScraperInit(unittest.TestCase):
    """Initialization and token handling."""

    def test_init_with_explicit_token(self):
        scraper = InstagramReelsScraper(api_token="test_token_123")
        self.assertEqual(scraper.api_token, "test_token_123")

    @patch.dict(os.environ, {"BRIGHT_DATA_API_TOKEN": "env_token_456"})
    def test_init_from_env_var(self):
        scraper = InstagramReelsScraper()
        self.assertEqual(scraper.api_token, "env_token_456")

    def test_init_explicit_token_overrides_env(self):
        with patch.dict(os.environ, {"BRIGHT_DATA_API_TOKEN": "env_token"}):
            scraper = InstagramReelsScraper(api_token="explicit_token")
            self.assertEqual(scraper.api_token, "explicit_token")

    @patch.dict(os.environ, {}, clear=True)
    def test_init_missing_token_raises(self):
        os.environ.pop("BRIGHT_DATA_API_TOKEN", None)
        with self.assertRaises(ValueError) as ctx:
            InstagramReelsScraper()
        self.assertIn("API token is required", str(ctx.exception))


class TestCollectByUrl(unittest.TestCase):
    """Tests for collect_by_url."""

    def setUp(self):
        self.scraper = InstagramReelsScraper(api_token="test_token")

    @patch("instagram_reels_scraper.requests.post")
    def test_single_url(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/"
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["url"], SAMPLE_REEL["url"])

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(len(payload["input"]), 1)
        self.assertEqual(
            payload["input"][0]["url"],
            "https://www.instagram.com/reel/C5Rdyj_q7YN/",
        )

    @patch("instagram_reels_scraper.requests.post")
    def test_multiple_urls(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL, SAMPLE_REEL_2]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        urls = [
            "https://www.instagram.com/reel/C5Rdyj_q7YN/",
            "https://www.instagram.com/reel/C85BZjeSHuO",
        ]
        result = self.scraper.collect_by_url(urls)

        self.assertEqual(len(result), 2)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(len(payload["input"]), 2)

    @patch("instagram_reels_scraper.requests.post")
    def test_collect_with_country_code(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/",
            country_code="US",
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(payload["input"][0]["country_code"], "US")

    @patch("instagram_reels_scraper.requests.post")
    def test_collect_country_code_applied_to_all(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL, SAMPLE_REEL_2]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            [
                "https://www.instagram.com/reel/C5Rdyj_q7YN/",
                "https://www.instagram.com/reel/C85BZjeSHuO",
            ],
            country_code="GB",
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        for entry in payload["input"]:
            self.assertEqual(entry["country_code"], "GB")

    @patch("instagram_reels_scraper.requests.post")
    def test_collect_no_country_code_omitted(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/"
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertNotIn("country_code", payload["input"][0])

    @patch("instagram_reels_scraper.requests.post")
    def test_collect_query_params(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/"
        )

        call_kwargs = mock_post.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1]["params"]
        self.assertEqual(params["dataset_id"], "gd_lyclm20il4r5helnj")
        self.assertEqual(params["include_errors"], "true")
        # collect endpoint should NOT have type/discover_by
        self.assertNotIn("type", params)
        self.assertNotIn("discover_by", params)

    @patch("instagram_reels_scraper.requests.post")
    def test_collect_limit_per_input(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/",
            limit_per_input=5,
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(payload["limit_per_input"], 5)

    @patch("instagram_reels_scraper.requests.post")
    def test_collect_default_limit_omitted(self, mock_post):
        """limit_per_input should be absent from payload when not set."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/"
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertNotIn("limit_per_input", payload)


class TestDiscoverByProfile(unittest.TestCase):
    """Tests for discover_by_profile."""

    def setUp(self):
        self.scraper = InstagramReelsScraper(api_token="test_token")

    @patch("instagram_reels_scraper.requests.post")
    def test_simple_url_string(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = self.scraper.discover_by_profile(
            "https://www.instagram.com/natgeo"
        )

        self.assertEqual(len(result), 1)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(len(payload["input"]), 1)
        self.assertEqual(
            payload["input"][0]["url"],
            "https://www.instagram.com/natgeo",
        )

    @patch("instagram_reels_scraper.requests.post")
    def test_url_with_filters(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_by_profile(
            "https://www.instagram.com/marcusfaberfdp",
            num_of_posts=10,
            start_date="01-01-2025",
            end_date="03-01-2025",
            post_type="Reel",
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        entry = payload["input"][0]
        self.assertEqual(entry["url"], "https://www.instagram.com/marcusfaberfdp")
        self.assertEqual(entry["num_of_posts"], 10)
        self.assertEqual(entry["start_date"], "01-01-2025")
        self.assertEqual(entry["end_date"], "03-01-2025")
        self.assertEqual(entry["post_type"], "Reel")

    @patch("instagram_reels_scraper.requests.post")
    def test_single_dict(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_by_profile(
            {"url": "https://www.instagram.com/natgeo", "num_of_posts": 5}
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(len(payload["input"]), 1)
        self.assertEqual(payload["input"][0]["num_of_posts"], 5)

    @patch("instagram_reels_scraper.requests.post")
    def test_batch_profiles_list_of_dicts(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL, SAMPLE_REEL_2]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        profiles = [
            {"url": "https://www.instagram.com/natgeo", "num_of_posts": 3},
            {
                "url": "https://www.instagram.com/bbcnews",
                "num_of_posts": 5,
                "post_type": "Reel",
            },
        ]
        result = self.scraper.discover_by_profile(profiles)

        self.assertEqual(len(result), 2)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(len(payload["input"]), 2)
        self.assertEqual(payload["input"][1]["post_type"], "Reel")

    @patch("instagram_reels_scraper.requests.post")
    def test_discover_query_params(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_by_profile("https://www.instagram.com/natgeo")

        call_kwargs = mock_post.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1]["params"]
        self.assertEqual(params["dataset_id"], "gd_lyclm20il4r5helnj")
        self.assertEqual(params["type"], "discover_new")
        self.assertEqual(params["discover_by"], "url")
        self.assertEqual(params["include_errors"], "true")

    @patch("instagram_reels_scraper.requests.post")
    def test_discover_limit_per_input(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_by_profile(
            "https://www.instagram.com/natgeo",
            limit_per_input=10,
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(payload["limit_per_input"], 10)

    @patch("instagram_reels_scraper.requests.post")
    def test_optional_params_omitted_when_none(self, mock_post):
        """When convenience kwargs are not provided, they should not appear."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_by_profile("https://www.instagram.com/natgeo")

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        entry = payload["input"][0]
        self.assertIn("url", entry)
        self.assertNotIn("num_of_posts", entry)
        self.assertNotIn("start_date", entry)
        self.assertNotIn("end_date", entry)
        self.assertNotIn("post_type", entry)

    @patch("instagram_reels_scraper.requests.post")
    def test_discover_default_limit_omitted(self, mock_post):
        """limit_per_input should be absent from payload when not set."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_by_profile("https://www.instagram.com/natgeo")

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertNotIn("limit_per_input", payload)


class TestDiscoverAllReels(unittest.TestCase):
    """Tests for discover_all_reels."""

    def setUp(self):
        self.scraper = InstagramReelsScraper(api_token="test_token")

    @patch("instagram_reels_scraper.requests.post")
    def test_single_url(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = self.scraper.discover_all_reels(
            "https://www.instagram.com/natgeo"
        )

        self.assertEqual(len(result), 1)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(len(payload["input"]), 1)
        self.assertEqual(
            payload["input"][0]["url"],
            "https://www.instagram.com/natgeo",
        )

    @patch("instagram_reels_scraper.requests.post")
    def test_multiple_urls(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL, SAMPLE_REEL_2]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        urls = [
            "https://www.instagram.com/natgeo",
            "https://www.instagram.com/bbcnews",
        ]
        result = self.scraper.discover_all_reels(urls)

        self.assertEqual(len(result), 2)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(len(payload["input"]), 2)

    @patch("instagram_reels_scraper.requests.post")
    def test_discover_all_reels_query_params(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_all_reels("https://www.instagram.com/natgeo")

        call_kwargs = mock_post.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1]["params"]
        self.assertEqual(params["dataset_id"], "gd_lyclm20il4r5helnj")
        self.assertEqual(params["type"], "discover_new")
        self.assertEqual(params["discover_by"], "url_all_reels")
        self.assertEqual(params["include_errors"], "true")

    @patch("instagram_reels_scraper.requests.post")
    def test_discover_all_reels_limit_per_input(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_all_reels(
            "https://www.instagram.com/natgeo",
            limit_per_input=20,
        )

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertEqual(payload["limit_per_input"], 20)

    @patch("instagram_reels_scraper.requests.post")
    def test_discover_all_reels_default_limit_omitted(self, mock_post):
        """limit_per_input should be absent from payload when not set."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = [SAMPLE_REEL]
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.discover_all_reels("https://www.instagram.com/natgeo")

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1]["json"]
        self.assertNotIn("limit_per_input", payload)


class TestMakeRequest(unittest.TestCase):
    """Tests for _make_request (auth headers, error handling)."""

    def setUp(self):
        self.scraper = InstagramReelsScraper(api_token="test_token")

    @patch("instagram_reels_scraper.requests.post")
    def test_authorization_header(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/"
        )

        call_kwargs = mock_post.call_args
        headers = call_kwargs.kwargs.get("headers") or call_kwargs[1]["headers"]
        self.assertEqual(headers["Authorization"], "Bearer test_token")
        self.assertEqual(headers["Content-Type"], "application/json")

    @patch("instagram_reels_scraper.requests.post")
    def test_base_url(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/"
        )

        call_args = mock_post.call_args
        url = call_args.args[0] if call_args.args else call_args[0][0]
        self.assertEqual(url, "https://api.brightdata.com/datasets/v3/scrape")

    @patch("instagram_reels_scraper.requests.post")
    def test_http_401_error(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=MagicMock(status_code=401)
        )
        mock_post.return_value = mock_resp

        with self.assertRaises(requests.exceptions.HTTPError):
            self.scraper.collect_by_url(
                "https://www.instagram.com/reel/C5Rdyj_q7YN/"
            )

    @patch("instagram_reels_scraper.requests.post")
    def test_http_500_error(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=MagicMock(status_code=500)
        )
        mock_post.return_value = mock_resp

        with self.assertRaises(requests.exceptions.HTTPError):
            self.scraper.discover_by_profile(
                "https://www.instagram.com/natgeo"
            )

    @patch("instagram_reels_scraper.requests.post")
    def test_http_500_error_on_discover_all_reels(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=MagicMock(status_code=500)
        )
        mock_post.return_value = mock_resp

        with self.assertRaises(requests.exceptions.HTTPError):
            self.scraper.discover_all_reels(
                "https://www.instagram.com/natgeo"
            )

    @patch("instagram_reels_scraper.requests.post")
    def test_connection_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError(
            "Connection refused"
        )

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.scraper.collect_by_url(
                "https://www.instagram.com/reel/C5Rdyj_q7YN/"
            )

    @patch("instagram_reels_scraper.requests.post")
    def test_request_timeout_is_set(self, mock_post):
        """requests.post must be called with timeout=30."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url(
            "https://www.instagram.com/reel/C5Rdyj_q7YN/"
        )

        call_kwargs = mock_post.call_args
        timeout = call_kwargs.kwargs.get("timeout") or call_kwargs[1].get("timeout")
        self.assertEqual(timeout, 30)


if __name__ == "__main__":
    unittest.main()
