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
        gemini_prompt = f"""You are a creative concept enhancer. Take the user prompt: '{prompt}' and transform it into a refined, structured version that:
- Stays true to the user's original intent.
- Incorporates exactly {cards} cards as a core element.
- Defines distinct roles or strategies for 2–4 participants.
- Introduces an immersive theme or setting to enhance engagement.
- Clarifies categories and interactions between cards (e.g., types, effects, combinations).
- Outlines clear objectives, progression structure, and outcome criteria.
- Encourages replayability through dynamic elements or variability.
- Is ready for another LLM to expand into a complete, self-contained concept.
Return only the refined prompt without any explanations."""

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