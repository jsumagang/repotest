"""Card viewer module for displaying card information."""

from typing import Dict, Any, Optional
from .api_client import RiftcodexClient


class CardViewer:
    """Viewer for displaying card information from riftcodex."""

    def __init__(self, client: Optional[RiftcodexClient] = None):
        """Initialize the card viewer.

        Args:
            client: RiftcodexClient instance. If None, a new one will be created.
        """
        self.client = client or RiftcodexClient()
        self._owns_client = client is None

    def get_card_details(self, card_id: str) -> Dict[str, Any]:
        """Retrieve detailed information about a card.

        Args:
            card_id: The unique identifier of the card.

        Returns:
            Dictionary containing card details.
        """
        return self.client.get_card(card_id)

    def format_card_text(self, card: Dict[str, Any]) -> str:
        """Format card information as human-readable text.

        Args:
            card: Card dictionary from the API.

        Returns:
            Formatted card information as a string.
        """
        lines = []
        lines.append(f"Name: {card.get('name', 'Unknown')}")
        lines.append(f"Type: {card.get('type', 'Unknown')}")
        lines.append(f"Rarity: {card.get('rarity', 'Unknown')}")
        lines.append(f"Cost: {card.get('cost', 'N/A')}")

        if "description" in card:
            lines.append(f"Description: {card['description']}")

        if "stats" in card:
            stats = card["stats"]
            if isinstance(stats, dict):
                stats_str = ", ".join(
                    f"{k}: {v}" for k, v in stats.items()
                )
                lines.append(f"Stats: {stats_str}")

        if "abilities" in card and card["abilities"]:
            lines.append("Abilities:")
            for ability in card["abilities"]:
                lines.append(f"  - {ability}")

        return "\n".join(lines)

    def format_card_detailed(self, card: Dict[str, Any]) -> str:
        """Format card information with enhanced visual layout.

        Args:
            card: Card dictionary from the API.

        Returns:
            Formatted card information with visual separators.
        """
        lines = []
        separator = "=" * 50
        lines.append(separator)
        
        # Header with name and ID
        name = card.get('name', 'Unknown')
        card_id = card.get('id', 'N/A')
        lines.append(f"  {name}")
        lines.append(f"  ID: {card_id}")
        lines.append(separator)
        
        # Basic properties
        lines.append("PROPERTIES:")
        lines.append(f"  Type:     {card.get('type', 'Unknown')}")
        lines.append(f"  Rarity:   {card.get('rarity', 'Unknown')}")
        lines.append(f"  Cost:     {card.get('cost', 'N/A')}")
        
        # Set information if available
        if "set" in card:
            lines.append(f"  Set:      {card['set']}")
        
        # Mana cost if available
        if "mana_cost" in card:
            lines.append(f"  Mana:     {card['mana_cost']}")
        
        # Description
        if "description" in card and card["description"]:
            lines.append("\nDESCRIPTION:")
            lines.append(f"  {card['description']}")
        
        # Stats
        if "stats" in card and card["stats"]:
            stats = card["stats"]
            if isinstance(stats, dict):
                lines.append("\nSTATS:")
                for key, value in stats.items():
                    lines.append(f"  {key.capitalize():12} {value}")
        
        # Abilities
        if "abilities" in card and card["abilities"]:
            lines.append("\nABILITIES:")
            for ability in card["abilities"]:
                lines.append(f"  • {ability}")
        
        # Keywords
        if "keywords" in card and card["keywords"]:
            lines.append("\nKEYWORDS:")
            keywords_str = ", ".join(card["keywords"])
            lines.append(f"  {keywords_str}")
        
        # Pricing if available
        if "price" in card or "market_price" in card:
            lines.append("\nPRICING:")
            if "price" in card:
                lines.append(f"  Price:    ${card['price']}")
            if "market_price" in card:
                lines.append(f"  Market:   ${card['market_price']}")
        
        lines.append(separator)
        return "\n".join(lines)

    def display_card(self, card: Dict[str, Any]) -> None:
        """Display card information to stdout.

        Args:
            card: Card dictionary from the API.
        """
        print(self.format_card_text(card))

    def display_card_detailed(self, card: Dict[str, Any]) -> None:
        """Display card information with enhanced formatting to stdout.

        Args:
            card: Card dictionary from the API.
        """
        print(self.format_card_detailed(card))

    def display_card_by_id(self, card_id: str) -> None:
        """Retrieve and display a card by ID.

        Args:
            card_id: The unique identifier of the card.
        """
        card = self.get_card_details(card_id)
        self.display_card(card)

    def display_card_by_id_detailed(self, card_id: str) -> None:
        """Retrieve and display a card by ID with enhanced formatting.

        Args:
            card_id: The unique identifier of the card.
        """
        card = self.get_card_details(card_id)
        self.display_card_detailed(card)

    def format_card_list(self, cards: list) -> str:
        """Format a list of cards as human-readable text.

        Args:
            cards: List of card dictionaries.

        Returns:
            Formatted card list as a string.
        """
        if not cards:
            return "No cards found."

        lines = []
        for i, card in enumerate(cards, 1):
            name = card.get("name", "Unknown")
            card_type = card.get("type", "Unknown")
            rarity = card.get("rarity", "Unknown")
            lines.append(f"{i}. {name} ({card_type}) - {rarity}")

        return "\n".join(lines)

    def format_card_list_detailed(self, cards: list) -> str:
        """Format a list of cards with enhanced visual layout.

        Args:
            cards: List of card dictionaries.

        Returns:
            Formatted card list with visual separators.
        """
        if not cards:
            return "No cards found."

        lines = []
        separator = "-" * 70
        lines.append(separator)
        lines.append(f"{'#':<4} {'Name':<25} {'Type':<12} {'Rarity':<10} {'Cost':<6}")
        lines.append(separator)
        
        for i, card in enumerate(cards, 1):
            name = card.get("name", "Unknown")[:24]
            card_type = card.get("type", "Unknown")[:11]
            rarity = card.get("rarity", "Unknown")[:9]
            cost = str(card.get("cost", "N/A"))[:5]
            lines.append(f"{i:<4} {name:<25} {card_type:<12} {rarity:<10} {cost:<6}")
        
        lines.append(separator)
        return "\n".join(lines)

    def display_card_list(self, cards: list) -> None:
        """Display a list of cards to stdout.

        Args:
            cards: List of card dictionaries.
        """
        print(self.format_card_list(cards))

    def display_card_list_detailed(self, cards: list) -> None:
        """Display a list of cards with enhanced formatting to stdout.

        Args:
            cards: List of card dictionaries.
        """
        print(self.format_card_list_detailed(cards))

    def close(self) -> None:
        """Close the viewer and its client if owned."""
        if self._owns_client:
            self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
