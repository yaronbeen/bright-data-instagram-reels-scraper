"""
Bright Data Instagram Reels Scraper

A Python wrapper for Bright Data's Instagram Reels scraper API.
Collect reel data by URL with optional geo-targeting.

Dataset ID: gd_lyclm20il4r5helnj
Pricing: $0.0015/record
Avg Response Time: ~5s
"""

import os
import requests
from typing import List, Optional, Dict, Any, Union


class InstagramReelsScraper:
    """Client for the Bright Data Instagram Reels scraper API.

    Collect reel data for specific Instagram reel URLs with optional
    geo-targeting via ``collect_by_url``.
    """

    BASE_URL = "https://api.brightdata.com/datasets/v3/scrape"
    DATASET_ID = "gd_lyclm20il4r5helnj"

    def __init__(self, api_token: Optional[str] = None):
        """Initialize the scraper with a Bright Data API token.

        Args:
            api_token: Bright Data API token. If not provided, reads from
                       the BRIGHT_DATA_API_TOKEN environment variable.

        Raises:
            ValueError: If no API token is provided or found in env.
        """
        self.api_token = api_token or os.getenv("BRIGHT_DATA_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "API token is required. Pass it directly or set the "
                "BRIGHT_DATA_API_TOKEN environment variable."
            )

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def collect_by_url(
        self,
        urls: Union[str, List[str]],
        country_code: Optional[str] = None,
        limit_per_input: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Collect reel data from specific Instagram reel URLs.

        Args:
            urls: A single Instagram reel URL string or a list of URLs.
                  Example: "https://www.instagram.com/reel/C5Rdyj_q7YN/"
            country_code: Optional 2-letter country code applied to all
                          inputs (e.g. ``"US"``, ``"GB"``).
            limit_per_input: Optional cap on records returned per input URL.

        Returns:
            List of reel data dictionaries.
        """
        if isinstance(urls, str):
            urls = [urls]

        input_list = []
        for url in urls:
            entry: Dict[str, Any] = {"url": url}
            if country_code is not None:
                entry["country_code"] = country_code
            input_list.append(entry)

        payload: Dict[str, Any] = {"input": input_list}
        if limit_per_input is not None:
            payload["limit_per_input"] = limit_per_input

        params = {
            "dataset_id": self.DATASET_ID,
            "include_errors": "true",
        }

        return self._make_request(params, payload)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _make_request(
        self,
        params: Dict[str, str],
        payload: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Send a POST request to the Bright Data scraper API.

        Args:
            params: URL query parameters.
            payload: JSON body.

        Returns:
            Parsed JSON response (list of dicts).

        Raises:
            requests.exceptions.HTTPError: On 4xx / 5xx responses.
            requests.exceptions.RequestException: On connection failures.
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            params=params,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
