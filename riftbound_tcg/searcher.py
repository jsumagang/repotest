"""Card searcher module for querying riftcodex."""

from typing import Dict, List, Optional, Any
from .api_client import RiftcodexClient


class CardSearcher:
    """Searcher for finding cards in the riftcodex database."""

    def __init__(self, client: Optional[RiftcodexClient] = None):
        """Initialize the card searcher.

        Args:
            client: RiftcodexClient instance. If None, a new one will be created.
        """
        self.client = client or RiftcodexClient()
        self._owns_client = client is None

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Search for cards matching the query.

        Args:
            query: Search query string (card name, text, etc.).
            filters: Optional dictionary of filters (e.g., rarity, type, cost).
            limit: Maximum number of results to return.
            offset: Number of results to skip for pagination.

        Returns:
            List of card dictionaries matching the search criteria.
        """
        result = self.client.search_cards(
            query=query, filters=filters, limit=limit, offset=offset
        )
        return result.get("cards", [])

    def search_by_name(self, name: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for cards by name.

        Args:
            name: Card name to search for.
            limit: Maximum number of results to return.

        Returns:
            List of cards matching the name.
        """
        return self.search(query=name, limit=limit)

    def search_by_type(
        self, card_type: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search for cards by type.

        Args:
            card_type: Type of card to search for.
            limit: Maximum number of results to return.

        Returns:
            List of cards of the specified type.
        """
        return self.search(query="", filters={"type": card_type}, limit=limit)

    def search_by_rarity(
        self, rarity: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search for cards by rarity.

        Args:
            rarity: Rarity level to search for.
            limit: Maximum number of results to return.

        Returns:
            List of cards with the specified rarity.
        """
        return self.search(query="", filters={"rarity": rarity}, limit=limit)

    def close(self) -> None:
        """Close the searcher and its client if owned."""
        if self._owns_client:
            self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
