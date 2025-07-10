import os
import time
import json
import re
try:
    import google.generativeai as genai
except ImportError:
    raise ImportError("Please install google-generativeai: pip install google-generativeai")

from google.api_core.exceptions import DeadlineExceeded

def csv_prompt(prompt, max_retries=3):
    """
    Generates a JSON object with a 'cards' array for HTML/CSS rendering based on the input prompt using Gemini API.
    
    Args:
        prompt (str): Input prompt describing the card-based system
        max_retries (int): Number of retry attempts for API calls
    
    Returns:
        str: JSON object with a 'cards' array
    """
    print("Generating cards...")
    
    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Set GEMINI_API_KEY: export GEMINI_API_KEY='your-api-key'")
    
    # Configure Gemini API
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error setting up Gemini API: {str(e)}")
        return '{"cards": []}'
    
    for attempt in range(max_retries):
        try:
            # Set timeout (30 seconds)
            start_time = time.time()
            timeout_duration = 30
            
            # Enhanced prompt for card generation
            gemini_prompt = f"""You are a creative content designer. Based on the user prompt: '{prompt}', generate a collection of unique, visually-rich card-style entries suitable for display in a card-based system (e.g., storytelling, collectibles, learning tools).

Return a valid JSON object with a 'cards' key containing an array of cards. Each card must include:
- `name`: A unique, descriptive title.
- `type`: A broad category such as 'Concept', 'Person', 'Place', 'Object', or 'Moment'.
- `description`: 2–3 sentences conveying context, meaning, or narrative.
- `flavor_text`: A short, expressive phrase, quote, or motto.
- `image_keywords`: 3–5 keywords that guide visual representation (e.g., 'ancient ruins, glowing portal').
- `theme_colors`: Object with `primary` and `secondary` hex codes (e.g., '#1F2A44').
- `layout_design`: Object with:
  - `border_color`: A **distinct, non-white** hex code or color name that contrasts well against white backgrounds (e.g., '#4B0082', 'darkslategray', but never 'white' or '#FFFFFF').
  - `background_style`: 'solid', 'gradient', 'pattern', or 'glow'.
  - `font_style`: 'serif', 'sans-serif', 'gothic', 'handwritten', etc.
  - `glow_effect`: Optional glow effect (e.g., 'amber glow') or null.
  - `text_alignment`: 'left', 'center', or 'right'.

Ensure the cards are thematically aligned with the input prompt, visually consistent, and optimized for rendering in HTML/CSS. The cards must **stand out clearly against white or light PDF backgrounds**. Return only a valid JSON object — no markdown, code fences, or additional explanations."""
            response = model.generate_content(
                gemini_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=3000  # Increased to handle larger output
                )
            )
            
            # Check timeout
            if time.time() - start_time > timeout_duration:
                raise TimeoutError("API call timed out")
            
            # Clean response (remove markdown code fences)
            raw_response = response.text.strip()
            cleaned_response = re.sub(r'^```json\s*|\s*```$', '', raw_response).strip()
            print(f"Raw API response (first 100 chars): {cleaned_response[:100]}...")
            
            # Validate JSON
            try:
                result = json.loads(cleaned_response)
                if not isinstance(result, dict) or 'cards' not in result:
                    raise ValueError("Response is not a valid JSON object with 'cards' key")
                print("Card generation completed")
                return json.dumps(result)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON format - {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying... (Attempt {attempt + 2}/{max_retries})")
                    time.sleep(2)  # Increased delay for retry
                    continue
                return '{"cards": []}'
        
        except DeadlineExceeded:
            print("Error: API call timed out")
            if attempt < max_retries - 1:
                print(f"Retrying... (Attempt {attempt + 2}/{max_retries})")
                time.sleep(2)
                continue
            return '{"cards": []}'
        except Exception as e:
            print(f"Error generating cards: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying... (Attempt {attempt + 2}/{max_retries})")
                time.sleep(2)
                continue
            return '{"cards": []}'

# Testing script
if __name__ == "__main__":
    try:
        sample_prompt = "Create a card game set in rummy"
        result = csv_prompt(sample_prompt)
        parsed_result = json.loads(result)
        print("\nGenerated Cards:")
        print(json.dumps(parsed_result, indent=2))
        
        # Validate structure for HTML/CSS use
        if not parsed_result.get('cards'):
            print("Warning: No cards in response")
        else:
            required_fields = [
                "name", "type", "description", "flavor_text", "rarity",
                "image_keywords", "theme_colors", "layout_design", "interactions"
            ]
            for card in parsed_result['cards']:
                if not all(field in card for field in required_fields):
                    print(f"Warning: Card {card.get('name', 'unknown')} missing fields")
                if not isinstance(card.get('theme_colors'), dict) or not isinstance(card.get('layout_design'), dict):
                    print(f"Warning: Card {card.get('name', 'unknown')} has invalid theme_colors or layout_design")
                if 'text_alignment' not in card.get('layout_design', {}):
                    print(f"Warning: Card {card.get('name', 'unknown')} missing text_alignment in layout_design")
    except Exception as e:
        print(f"Test error: {str(e)}")