"""Tests for the card viewer module."""

import pytest
from unittest.mock import Mock, patch
from riftbound_tcg.viewer import CardViewer
from riftbound_tcg.api_client import RiftcodexClient


class TestCardViewer:
    """Test cases for CardViewer."""

    def test_init_with_client(self):
        """Test viewer initialization with provided client."""
        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        assert viewer.client is mock_client
        assert viewer._owns_client is False

    def test_init_without_client(self):
        """Test viewer initialization without client."""
        with patch("riftbound_tcg.viewer.RiftcodexClient"):
            viewer = CardViewer()
            assert viewer._owns_client is True

    def test_get_card_details(self):
        """Test retrieving card details."""
        mock_client = Mock(spec=RiftcodexClient)
        card_data = {
            "id": "1",
            "name": "Test Card",
            "type": "Unit",
            "cost": 3,
        }
        mock_client.get_card.return_value = card_data

        viewer = CardViewer(client=mock_client)
        result = viewer.get_card_details("1")

        assert result["name"] == "Test Card"
        mock_client.get_card.assert_called_once_with("1")

    def test_format_card_text_basic(self):
        """Test formatting basic card information."""
        card = {
            "name": "Fireball",
            "type": "Spell",
            "rarity": "common",
            "cost": 3,
        }

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_text(card)

        assert "Name: Fireball" in formatted
        assert "Type: Spell" in formatted
        assert "Rarity: common" in formatted
        assert "Cost: 3" in formatted

    def test_format_card_text_with_description(self):
        """Test formatting card with description."""
        card = {
            "name": "Fireball",
            "type": "Spell",
            "rarity": "common",
            "cost": 3,
            "description": "Deal 3 damage to target.",
        }

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_text(card)

        assert "Description: Deal 3 damage to target." in formatted

    def test_format_card_text_with_stats(self):
        """Test formatting card with stats."""
        card = {
            "name": "Knight",
            "type": "Unit",
            "rarity": "common",
            "cost": 2,
            "stats": {"attack": 2, "defense": 3},
        }

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_text(card)

        assert "Stats:" in formatted
        assert "attack: 2" in formatted
        assert "defense: 3" in formatted

    def test_format_card_text_with_abilities(self):
        """Test formatting card with abilities."""
        card = {
            "name": "Dragon",
            "type": "Unit",
            "rarity": "rare",
            "cost": 5,
            "abilities": ["Flying", "Haste"],
        }

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_text(card)

        assert "Abilities:" in formatted
        assert "- Flying" in formatted
        assert "- Haste" in formatted

    def test_format_card_list_empty(self):
        """Test formatting empty card list."""
        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_list([])

        assert formatted == "No cards found."

    def test_format_card_list_multiple(self):
        """Test formatting multiple cards."""
        cards = [
            {"name": "Card 1", "type": "Unit", "rarity": "common"},
            {"name": "Card 2", "type": "Spell", "rarity": "rare"},
        ]

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_list(cards)

        assert "1. Card 1 (Unit) - common" in formatted
        assert "2. Card 2 (Spell) - rare" in formatted

    @patch("builtins.print")
    def test_display_card(self, mock_print):
        """Test displaying a card."""
        card = {
            "name": "Test Card",
            "type": "Unit",
            "rarity": "common",
            "cost": 2,
        }

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        viewer.display_card(card)

        mock_print.assert_called_once()
        printed_text = mock_print.call_args[0][0]
        assert "Name: Test Card" in printed_text

    @patch("builtins.print")
    def test_display_card_by_id(self, mock_print):
        """Test displaying a card by ID."""
        card = {
            "id": "1",
            "name": "Test Card",
            "type": "Unit",
            "rarity": "common",
            "cost": 2,
        }

        mock_client = Mock(spec=RiftcodexClient)
        mock_client.get_card.return_value = card
        viewer = CardViewer(client=mock_client)
        viewer.display_card_by_id("1")

        mock_client.get_card.assert_called_once_with("1")
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_display_card_list(self, mock_print):
        """Test displaying a card list."""
        cards = [
            {"name": "Card 1", "type": "Unit", "rarity": "common"},
        ]

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        viewer.display_card_list(cards)

        mock_print.assert_called_once()
        printed_text = mock_print.call_args[0][0]
        assert "Card 1" in printed_text

    def test_context_manager(self):
        """Test viewer as context manager."""
        mock_client = Mock(spec=RiftcodexClient)
        with CardViewer(client=mock_client) as viewer:
            assert viewer is not None
