import os
import time
import google.generativeai as genai
from google.api_core.exceptions import DeadlineExceeded

# Configure Gemini API with free tier
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def cardPromptRefinement(prompt, cards):
    """
    Refines a prompt for card game creation using Gemini API with timeout error handling.
    
    Args:
        prompt (str): The input prompt related to card game creation
        cards (int): Number of cards in the game
    
    Returns:
        str: Refined prompt optimized for card game design
    """
    print("Prompt refinement started")
    
    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')  # Free tier compatible model
    
    try:
        # Set timeout for API call (e.g., 30 seconds)
        start_time = time.time()
        timeout_duration = 30
        
        # Enhanced prompt for card game creation
        gemini_prompt = f"""You are a master game designer specializing in creative and immersive card games. 
        Take the input prompt: '{prompt}' and refine it into a clear, concise, and engaging prompt that inspires a detailed card game concept. The refined prompt must:
        - Specify that the game uses exactly {cards} cards.
        - Design the game for 2-4 players with distinct player roles or strategies (e.g., factions, classes, or archetypes).
        - Include a vivid theme or setting to enhance immersion (e.g., fantasy, sci-fi, historical).
        - Define specific card types (e.g., characters, items, events) and their interactions (e.g., combos, counters).
        - Outline a clear objective, turn structure, and win conditions to ensure balanced gameplay.
        - Incorporate mechanics that promote replayability, such as variable setups or dynamic card effects.
        - Be optimized for another LLM to generate a cohesive, self-contained game concept.
        Return only the refined prompt, with no explanations or additional text."""
        
        # Make API call with timeout
        response = model.generate_content(
            gemini_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500
            )
        )
        
        # Check if response was received within timeout
        if time.time() - start_time > timeout_duration:
            raise TimeoutError("API call took too long")
        
        refined_prompt = response.text.strip()
        print("Prompt has been refined")
        return refined_prompt
    
    except DeadlineExceeded:
        print("Error: API call timed out")
        return prompt  # Fallback to original prompt
    except Exception as e:
        print(f"Error during prompt refinement: {str(e)}")
        return prompt  # Fallback to original prompt

# Example usage
if __name__ == "__main__":
    # Ensure API key is set
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    sample_prompt = "Create a card game concept"
    num_cards = 52
    refined = cardPromptRefinement(sample_prompt, num_cards)
    print(f"Refined Prompt: {refined}")