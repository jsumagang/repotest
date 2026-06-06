"""API client for riftcodex integration."""

import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin


class RiftcodexClient:
    """Client for interacting with the riftcodex API."""

    def __init__(self, base_url: str = "https://api.riftcodex.com"):
        """Initialize the riftcodex API client.

        Args:
            base_url: Base URL for the riftcodex API.
        """
        self.base_url = base_url
        self.session = requests.Session()

    def search_cards(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Search for cards in the riftcodex database.

        Args:
            query: Search query string.
            filters: Optional dictionary of filters to apply.
            limit: Maximum number of results to return.
            offset: Number of results to skip.

        Returns:
            Dictionary containing search results and metadata.

        Raises:
            requests.RequestException: If the API request fails.
        """
        endpoint = urljoin(self.base_url, "/cards/search")
        params = {"q": query, "limit": limit, "offset": offset}

        if filters:
            params.update(filters)

        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_card(
        self,
        card_id: str,
    ) -> Dict[str, Any]:
        """Retrieve a specific card by ID.

        Args:
            card_id: The unique identifier of the card.

        Returns:
            Dictionary containing card details.

        Raises:
            requests.RequestException: If the API request fails.
        """
        endpoint = urljoin(self.base_url, f"/cards/{card_id}")
        response = self.session.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_card_image(
        self,
        card_id: str,
    ) -> bytes:
        """Retrieve the image for a specific card.

        Args:
            card_id: The unique identifier of the card.

        Returns:
            Image data as bytes.

        Raises:
            requests.RequestException: If the API request fails.
        """
        endpoint = urljoin(self.base_url, f"/cards/{card_id}/image")
        response = self.session.get(endpoint)
        response.raise_for_status()
        return response.content

    def close(self) -> None:
        """Close the API client session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
