import json
import re

def json_to_card_list(json_string):
    """
    Converts a JSON string with a 'cards' array into a list of dictionaries.
    
    Args:
        json_string (str): JSON string containing a 'cards' array
    
    Returns:
        list: List of dictionaries representing cards
    """
    try:
        # Clean the input string (remove markdown, extra whitespace, etc.)
        cleaned_json = re.sub(r'^```json\s*|\s*```$', '', json_string).strip()
        
        # Log the cleaned input for debugging
        print(f"Cleaned JSON input (first 100 chars): {cleaned_json[:100]}...")
        
        # Parse JSON
        data = json.loads(cleaned_json)
        
        # Validate structure
        if not isinstance(data, dict) or 'cards' not in data:
            raise ValueError("Input JSON must be an object with a 'cards' key")
        if not isinstance(data['cards'], list):
            raise ValueError("'cards' must be an array")
        
        # Return the list of card dictionaries
        return data['cards']
    
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON - {str(e)}")
        print(f"Error position: line {e.lineno}, column {e.colno}")
        print(f"Problematic input snippet: {e.doc[max(0, e.pos-20):e.pos+20]}")
        return []
    except Exception as e:
        print(f"Error processing JSON: {str(e)}")
        return []

# Testing script
if __name__ == "__main__":
    # Sample JSON string (from your input)
    sample_json = '''{"cards": [
        {
            "name": "Clockwork Knight of Gears",
            "type": "Character",
            "description": "A valiant knight whose armor is interwoven with intricate clockwork mechanisms. His attacks are precise and powerful, fueled by steam and gears.",
            "flavor_text": "Time is on my side.",
            "rarity": "Rare",
            "image_keywords": ["clockwork armor", "gears", "steam", "sword", "knight"],
            "theme_colors": {"primary": "#8B4513", "secondary": "#D2B48C"},
            "layout_design": {
                "border_color": "#8B4513",
                "background_style": "gradient",
                "font_style": "gothic",
                "glow_effect": null,
                "text_alignment": "center"
            },
            "interactions": "Combines well with Item cards that enhance attack.",
            "suit": "Gears",
            "rank": "King",
            "attack": 10,
            "defense": 8
        },
        {
            "name": "Alchemist's Elixir of Swiftness",
            "type": "Item",
            "description": "A potent elixir brewed by master alchemists, granting incredible speed and agility to its user. Increases movement and action speed.",
            "flavor_text": "Haste makes waste... sometimes.",
            "rarity": "Uncommon",
            "image_keywords": ["flask", "glowing liquid", "alchemy symbols", "bubbles", "speed"],
            "theme_colors": {"primary": "#7FFF00", "secondary": "#008000"},
            "layout_design": {
                "border_color": "#7FFF00",
                "background_style": "solid",
                "font_style": "fantasy",
                "glow_effect": null,
                "text_alignment": "center"
            },
            "interactions": "Boosts Character card's Attack and movement.",
            "suit": "Cogs",
            "rank": "7"
        },
        {
            "name": "Mystical Resonance",
            "type": "Event",
            "description": "A powerful surge of mystical energy alters the battlefield. All characters gain a temporary boost to their abilities, but the effects are unpredictable.",
            "flavor_text": "The veil between worlds thins.",
            "rarity": "Legendary",
            "image_keywords": ["magical energy", "glowing aura", "mystical symbols", "purple mist", "chaos"],
            "theme_colors": {"primary": "#800080", "secondary": "#4B0082"},
            "layout_design": {
                "border_color": "#800080",
                "background_style": "glow",
                "font_style": "fantasy",
                "glow_effect": "purple glow",
                "text_alignment": "center"
            },
            "interactions": "Randomly affects all Characters; can be countered by protective Items.",
            "suit": "Springs",
            "rank": "Ace"
        }
    ]}'''
    
    try:
        # Convert JSON to list of dictionaries
        card_list = json_to_card_list(sample_json)
        
        # Print result
        print("\nList of Card Dictionaries:")
        print(json.dumps(card_list, indent=2))
        
        # Validate structure for HTML/CSS use
        if not card_list:
            print("Warning: No cards extracted")
        else:
            required_fields = [
                "name", "type", "description", "flavor_text", "rarity",
                "image_keywords", "theme_colors", "layout_design", "interactions"
            ]
            for card in card_list:
                if not all(field in card for field in required_fields):
                    print(f"Warning: Card {card.get('name', 'unknown')} missing required fields")
                if not isinstance(card.get('theme_colors'), dict) or not isinstance(card.get('layout_design'), dict):
                    print(f"Warning: Card {card.get('name', 'unknown')} has invalid theme_colors or layout_design")
                if 'text_alignment' not in card.get('layout_design', {}):
                    print(f"Warning: Card {card.get('name', 'unknown')} missing text_alignment in layout_design")
    
    except Exception as e:
        print(f"Test error: {str(e)}")