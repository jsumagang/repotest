"""Tests for the card searcher module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from riftbound_tcg.searcher import CardSearcher
from riftbound_tcg.api_client import RiftcodexClient


class TestCardSearcher:
    """Test cases for CardSearcher."""

    def test_init_with_client(self):
        """Test searcher initialization with provided client."""
        mock_client = Mock(spec=RiftcodexClient)
        searcher = CardSearcher(client=mock_client)
        assert searcher.client is mock_client
        assert searcher._owns_client is False

    def test_init_without_client(self):
        """Test searcher initialization without client."""
        with patch("riftbound_tcg.searcher.RiftcodexClient"):
            searcher = CardSearcher()
            assert searcher._owns_client is True

    def test_search(self):
        """Test basic card search."""
        mock_client = Mock(spec=RiftcodexClient)
        mock_client.search_cards.return_value = {
            "cards": [
                {"id": "1", "name": "Card 1"},
                {"id": "2", "name": "Card 2"},
            ]
        }

        searcher = CardSearcher(client=mock_client)
        results = searcher.search("test", limit=20)

        assert len(results) == 2
        assert results[0]["name"] == "Card 1"
        mock_client.search_cards.assert_called_once_with(
            query="test", filters=None, limit=20, offset=0
        )

    def test_search_with_filters(self):
        """Test card search with filters."""
        mock_client = Mock(spec=RiftcodexClient)
        mock_client.search_cards.return_value = {"cards": []}

        searcher = CardSearcher(client=mock_client)
        filters = {"rarity": "rare", "type": "Unit"}
        searcher.search("test", filters=filters, limit=10)

        mock_client.search_cards.assert_called_once_with(
            query="test", filters=filters, limit=10, offset=0
        )

    def test_search_by_name(self):
        """Test searching cards by name."""
        mock_client = Mock(spec=RiftcodexClient)
        mock_client.search_cards.return_value = {
            "cards": [{"id": "1", "name": "Fireball"}]
        }

        searcher = CardSearcher(client=mock_client)
        results = searcher.search_by_name("Fireball")

        assert len(results) == 1
        assert results[0]["name"] == "Fireball"

    def test_search_by_type(self):
        """Test searching cards by type."""
        mock_client = Mock(spec=RiftcodexClient)
        mock_client.search_cards.return_value = {
            "cards": [{"id": "1", "name": "Unit Card", "type": "Unit"}]
        }

        searcher = CardSearcher(client=mock_client)
        results = searcher.search_by_type("Unit")

        assert len(results) == 1
        mock_client.search_cards.assert_called_once_with(
            query="", filters={"type": "Unit"}, limit=20, offset=0
        )

    def test_search_by_rarity(self):
        """Test searching cards by rarity."""
        mock_client = Mock(spec=RiftcodexClient)
        mock_client.search_cards.return_value = {
            "cards": [{"id": "1", "name": "Rare Card", "rarity": "rare"}]
        }

        searcher = CardSearcher(client=mock_client)
        results = searcher.search_by_rarity("rare")

        assert len(results) == 1
        mock_client.search_cards.assert_called_once_with(
            query="", filters={"rarity": "rare"}, limit=20, offset=0
        )

    def test_context_manager(self):
        """Test searcher as context manager."""
        mock_client = Mock(spec=RiftcodexClient)
        with CardSearcher(client=mock_client) as searcher:
            assert searcher is not None
