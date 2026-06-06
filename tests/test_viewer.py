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

    def test_format_card_detailed_basic(self):
        """Test detailed formatting with basic card information."""
        card = {
            "id": "card-001",
            "name": "Fireball",
            "type": "Spell",
            "rarity": "common",
            "cost": 3,
        }

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_detailed(card)

        assert "Fireball" in formatted
        assert "card-001" in formatted
        assert "PROPERTIES:" in formatted
        assert "Type:" in formatted
        assert "Spell" in formatted
        assert "Rarity:" in formatted
        assert "common" in formatted
        assert "Cost:" in formatted
        assert "3" in formatted
        assert "=" * 50 in formatted

    def test_format_card_detailed_with_all_fields(self):
        """Test detailed formatting with all optional fields."""
        card = {
            "id": "card-002",
            "name": "Ancient Dragon",
            "type": "Unit",
            "rarity": "legendary",
            "cost": 8,
            "set": "Core Set",
            "mana_cost": "RRGG",
            "description": "A mighty dragon from ancient times.",
            "stats": {"attack": 8, "defense": 6, "health": 10},
            "abilities": ["Flying", "Haste", "Regenerate"],
            "keywords": ["Dragon", "Legendary"],
            "price": 25.50,
            "market_price": 24.99,
        }

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_detailed(card)

        assert "Ancient Dragon" in formatted
        assert "PROPERTIES:" in formatted
        assert "Set:" in formatted
        assert "Core Set" in formatted
        assert "Mana:" in formatted
        assert "RRGG" in formatted
        assert "DESCRIPTION:" in formatted
        assert "A mighty dragon from ancient times." in formatted
        assert "STATS:" in formatted
        assert "attack" in formatted
        assert "8" in formatted
        assert "ABILITIES:" in formatted
        assert "Flying" in formatted
        assert "KEYWORDS:" in formatted
        assert "Dragon" in formatted
        assert "PRICING:" in formatted
        assert "25.50" in formatted
        assert "24.99" in formatted

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

    def test_format_card_list_detailed_empty(self):
        """Test detailed formatting of empty card list."""
        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_list_detailed([])

        assert formatted == "No cards found."

    def test_format_card_list_detailed_multiple(self):
        """Test detailed formatting of multiple cards."""
        cards = [
            {
                "name": "Fireball",
                "type": "Spell",
                "rarity": "common",
                "cost": 3,
            },
            {
                "name": "Ancient Dragon",
                "type": "Unit",
                "rarity": "legendary",
                "cost": 8,
            },
        ]

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_list_detailed(cards)

        assert "#" in formatted
        assert "Name" in formatted
        assert "Type" in formatted
        assert "Rarity" in formatted
        assert "Cost" in formatted
        assert "Fireball" in formatted
        assert "Spell" in formatted
        assert "Ancient Dragon" in formatted
        assert "Unit" in formatted
        assert "-" * 70 in formatted

    def test_format_card_list_detailed_truncation(self):
        """Test that detailed list formatting truncates long values."""
        cards = [
            {
                "name": "A" * 30,  # Very long name
                "type": "B" * 20,  # Very long type
                "rarity": "C" * 15,  # Very long rarity
                "cost": 999,  # Large cost
            },
        ]

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        formatted = viewer.format_card_list_detailed(cards)

        # Should not raise an error and should contain truncated values
        assert formatted is not None
        assert "1." in formatted

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
    def test_display_card_detailed(self, mock_print):
        """Test displaying a card with detailed formatting."""
        card = {
            "id": "card-001",
            "name": "Test Card",
            "type": "Unit",
            "rarity": "common",
            "cost": 2,
            "description": "A test card.",
        }

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        viewer.display_card_detailed(card)

        mock_print.assert_called_once()
        printed_text = mock_print.call_args[0][0]
        assert "Test Card" in printed_text
        assert "PROPERTIES:" in printed_text
        assert "DESCRIPTION:" in printed_text

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
    def test_display_card_by_id_detailed(self, mock_print):
        """Test displaying a card by ID with detailed formatting."""
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
        viewer.display_card_by_id_detailed("1")

        mock_client.get_card.assert_called_once_with("1")
        mock_print.assert_called_once()
        printed_text = mock_print.call_args[0][0]
        assert "PROPERTIES:" in printed_text

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

    @patch("builtins.print")
    def test_display_card_list_detailed(self, mock_print):
        """Test displaying a card list with detailed formatting."""
        cards = [
            {
                "name": "Card 1",
                "type": "Unit",
                "rarity": "common",
                "cost": 2,
            },
        ]

        mock_client = Mock(spec=RiftcodexClient)
        viewer = CardViewer(client=mock_client)
        viewer.display_card_list_detailed(cards)

        mock_print.assert_called_once()
        printed_text = mock_print.call_args[0][0]
        assert "Name" in printed_text
        assert "Type" in printed_text
        assert "Card 1" in printed_text

    def test_context_manager(self):
        """Test viewer as context manager."""
        mock_client = Mock(spec=RiftcodexClient)
        with CardViewer(client=mock_client) as viewer:
            assert viewer is not None
