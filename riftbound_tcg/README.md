# Riftbound TCG Viewer

The viewer module provides enhanced card display functionality for the Riftbound TCG card database.

## Features

### Basic Card Display

The `CardViewer` class provides methods to retrieve and display card information from the riftcodex API.

#### Simple Text Format

```python
from riftbound_tcg import CardViewer

viewer = CardViewer()
card = viewer.get_card_details("card-001")
viewer.display_card(card)
```

Output:
```
Name: Fireball
Type: Spell
Rarity: common
Cost: 3
Description: Deal 3 damage to target.
Stats: attack: 2, defense: 3
Abilities:
  - Flying
  - Haste
```

#### Detailed Format (NEW)

For a more readable and comprehensive display:

```python
viewer.display_card_detailed(card)
```

Output:
```
==================================================
  Fireball
  ID: card-001
==================================================
PROPERTIES:
  Type:     Spell
  Rarity:   common
  Cost:     3
  Set:      Core Set
  Mana:     RR

DESCRIPTION:
  Deal 3 damage to target.

STATS:
  Attack           2
  Defense          3
  Health           5

ABILITIES:
  • Flying
  • Haste

KEYWORDS:
  Spell, Damage

PRICING:
  Price:    $2.50
  Market:   $2.49
==================================================
```

### Card Lists

#### Simple List Format

```python
cards = [card1, card2, card3]
viewer.display_card_list(cards)
```

Output:
```
1. Fireball (Spell) - common
2. Ancient Dragon (Unit) - legendary
3. Healing Potion (Spell) - common
```

#### Detailed List Format (NEW)

For better readability with multiple cards:

```python
viewer.display_card_list_detailed(cards)
```

Output:
```
----------------------------------------------------------------------
#    Name                     Type         Rarity     Cost 
----------------------------------------------------------------------
1    Fireball                 Spell        common     3    
2    Ancient Dragon           Unit         legendary  8    
3    Healing Potion           Spell        common     1    
----------------------------------------------------------------------
```

### Retrieve by ID

Display a card directly by its ID:

```python
# Simple format
viewer.display_card_by_id("card-001")

# Detailed format
viewer.display_card_by_id_detailed("card-001")
```

## API

### CardViewer Class

#### Methods

**`__init__(client: Optional[RiftcodexClient] = None)`**
- Initialize the viewer with an optional API client.
- If no client is provided, a new one will be created.

**`get_card_details(card_id: str) -> Dict[str, Any]`**
- Retrieve raw card data from the API.

**`format_card_text(card: Dict[str, Any]) -> str`**
- Format a card in simple text format.

**`format_card_detailed(card: Dict[str, Any]) -> str`** (NEW)
- Format a card with enhanced visual layout and all available fields.

**`display_card(card: Dict[str, Any]) -> None`**
- Print a card in simple text format.

**`display_card_detailed(card: Dict[str, Any]) -> None`** (NEW)
- Print a card with enhanced visual layout.

**`display_card_by_id(card_id: str) -> None`**
- Retrieve and display a card by ID in simple format.

**`display_card_by_id_detailed(card_id: str) -> None`** (NEW)
- Retrieve and display a card by ID in detailed format.

**`format_card_list(cards: list) -> str`**
- Format a list of cards in simple format.

**`format_card_list_detailed(cards: list) -> str`** (NEW)
- Format a list of cards in a table layout with visual separators.

**`display_card_list(cards: list) -> None`**
- Print a list of cards in simple format.

**`display_card_list_detailed(cards: list) -> None`** (NEW)
- Print a list of cards in table format.

**`close() -> None`**
- Close the viewer and its client if owned.

### Context Manager Support

The viewer supports context manager protocol for automatic resource cleanup:

```python
with CardViewer() as viewer:
    viewer.display_card_by_id("card-001")
# Client is automatically closed
```

## Card Data Structure

Cards retrieved from the API may contain the following fields:

- `id` (str): Unique card identifier
- `name` (str): Card name
- `type` (str): Card type (e.g., "Unit", "Spell", "Artifact")
- `rarity` (str): Rarity level (e.g., "common", "rare", "legendary")
- `cost` (int): Mana/resource cost to play
- `set` (str): Set the card belongs to
- `mana_cost` (str): Mana cost representation
- `description` (str): Card effect description
- `stats` (dict): Card statistics (e.g., attack, defense, health)
- `abilities` (list): List of card abilities
- `keywords` (list): List of associated keywords
- `price` (float): Card price
- `market_price` (float): Current market price

## Recent Improvements

### Version 0.1.0 Enhancements

- **Enhanced Display Formatting**: Added `format_card_detailed()` and `display_card_detailed()` methods for improved readability
- **Table Layout for Lists**: New `format_card_list_detailed()` and `display_card_list_detailed()` methods provide tabular display
- **Visual Separators**: Detailed formats include visual separators for better organization
- **Comprehensive Field Display**: All available card fields are now displayed in detailed format
- **Pricing Information**: Display card pricing when available
- **Better Organization**: Fields are grouped logically (Properties, Description, Stats, Abilities, Keywords, Pricing)
- **Improved Tests**: Comprehensive test coverage for all new features

## Testing

Run the test suite:

```bash
python -m pytest tests/test_viewer.py -v
```

All new features include dedicated test cases:
- `test_format_card_detailed_basic`: Basic detailed formatting
- `test_format_card_detailed_with_all_fields`: All optional fields
- `test_format_card_list_detailed_empty`: Empty list handling
- `test_format_card_list_detailed_multiple`: Multiple cards display
- `test_format_card_list_detailed_truncation`: Long value truncation
- `test_display_card_detailed`: Detailed display output
- `test_display_card_by_id_detailed`: Retrieve and display detailed
- `test_display_card_list_detailed`: List detailed display
