"""Tests for the riftcodex API client."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from riftbound_tcg.api_client import RiftcodexClient


class TestRiftcodexClient:
    """Test cases for RiftcodexClient."""

    def test_init_default_url(self):
        """Test client initialization with default URL."""
        client = RiftcodexClient()
        assert client.base_url == "https://api.riftcodex.com"
        client.close()

    def test_init_custom_url(self):
        """Test client initialization with custom URL."""
        custom_url = "https://custom.api.com"
        client = RiftcodexClient(base_url=custom_url)
        assert client.base_url == custom_url
        client.close()

    @patch("riftbound_tcg.api_client.requests.Session.get")
    def test_search_cards(self, mock_get):
        """Test card search functionality."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "cards": [
                {"id": "1", "name": "Test Card", "type": "Unit"},
                {"id": "2", "name": "Another Card", "type": "Spell"},
            ]
        }
        mock_get.return_value = mock_response

        client = RiftcodexClient()
        result = client.search_cards("test", limit=20, offset=0)

        assert "cards" in result
        assert len(result["cards"]) == 2
        mock_get.assert_called_once()
        client.close()

    @patch("riftbound_tcg.api_client.requests.Session.get")
    def test_search_cards_with_filters(self, mock_get):
        """Test card search with filters."""
        mock_response = Mock()
        mock_response.json.return_value = {"cards": []}
        mock_get.return_value = mock_response

        client = RiftcodexClient()
        client.search_cards(
            "test", filters={"rarity": "rare", "type": "Unit"}, limit=10
        )

        call_args = mock_get.call_args
        assert call_args[1]["params"]["rarity"] == "rare"
        assert call_args[1]["params"]["type"] == "Unit"
        client.close()

    @patch("riftbound_tcg.api_client.requests.Session.get")
    def test_get_card(self, mock_get):
        """Test retrieving a specific card."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "1",
            "name": "Test Card",
            "type": "Unit",
            "cost": 3,
        }
        mock_get.return_value = mock_response

        client = RiftcodexClient()
        result = client.get_card("1")

        assert result["id"] == "1"
        assert result["name"] == "Test Card"
        mock_get.assert_called_once()
        client.close()

    @patch("riftbound_tcg.api_client.requests.Session.get")
    def test_get_card_image(self, mock_get):
        """Test retrieving card image."""
        mock_response = Mock()
        mock_response.content = b"fake_image_data"
        mock_get.return_value = mock_response

        client = RiftcodexClient()
        result = client.get_card_image("1")

        assert result == b"fake_image_data"
        mock_get.assert_called_once()
        client.close()

    def test_context_manager(self):
        """Test client as context manager."""
        with RiftcodexClient() as client:
            assert client is not None
            assert client.session is not None
