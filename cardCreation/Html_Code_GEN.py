import cohere
import os
import shutil

# Load API key from environment
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

TEMPLATE_DIR = "templates"

# Clear all HTML files in templates/ folder
def clear_templates_folder():
    if not os.path.exists(TEMPLATE_DIR):
        os.makedirs(TEMPLATE_DIR)
    else:
        for filename in os.listdir(TEMPLATE_DIR):
            file_path = os.path.join(TEMPLATE_DIR, filename)
            if os.path.isfile(file_path) and filename.endswith(".html"):
                os.remove(file_path)
        print("🧹 Cleaned 'templates/' folder.")

# Generate card HTML and save to templates/
def cardGen(details, num):
    prompt = f"""
    Generate a complete HTML file for a single card design with internal CSS. The HTML must include:
    - Full HTML structure: <!DOCTYPE html>, <html>, <head>, and <body> tags.
    - Internal CSS within <style> tags in the <head> section (no external CSS files).
    - A single card with modern styling: rounded corners, box shadow, responsive layout, and hover effects.
    - Card content based on the following details:
      - Title: {details['name']}
      - Description: {details['description']}
      - Image URL: {details['url']}
    - Use the provided Image URL directly for the card's image (do not use placeholder images).
    - Ensure the image is properly sized to fit the card (e.g., cover the top section, approximately 300px wide and 150px high).
    - Use a clean, professional design with a card width of approximately 300px, centered on the page.
    - Ensure the card is responsive and looks good on both desktop and mobile devices.
    - Include hover effects, such as a slight lift or shadow increase.
    - Do not include any external CSS or JavaScript files.
    Return the full HTML code as a single, properly formatted string.
    """

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=1000,  # Ensure enough tokens for complete HTML
        temperature=0.6,
    )

    html_code = response.generations[0].text.strip()
    file_path = os.path.join(TEMPLATE_DIR, f"card{num}.html")

    # Ensure the HTML code is complete by wrapping it if necessary
    if not html_code.startswith('<!DOCTYPE html>'):
        html_code = f'<!DOCTYPE html>\n<html>\n<head>\n<style>\n</style>\n</head>\n<body>\n{html_code}\n</body>\n</html>'

    with open(file_path, "w") as f:
        f.write(html_code)

    print(f"✅ Saved: {file_path}")

# Loop over JSON list of card details
def html_code_gen(jsonObj):
    clear_templates_folder()
    for i, details in enumerate(jsonObj):
        cardGen(details, i)

# Example usage
if __name__ == "__main__":
    example_cards = [
        {
            "title": "Red Apple",
            "description": "Juicy, sweet, and perfect for a snack.",
            "image_url": "https://example.com/images/red_apple.jpg",
        },
        {
            "title": "Golden Apple",
            "description": "A rare variety with a golden sheen and crisp bite.",
            "image_url": "https://example.com/images/golden_apple.jpg",
        }
    ]

    html_code_gen(example_cards)