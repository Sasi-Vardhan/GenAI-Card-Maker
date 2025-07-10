import cohere
import os
import shutil
from multiprocessing import Pool
from functools import partial

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

# Few-shot prompt template for card generation
def get_card_prompt(details):
    return f"""
Generate a complete HTML file for a single card design with internal CSS. Follow these requirements:
- Full HTML structure: <!DOCTYPE html>, <html>, <head>, and <body> tags.
- Internal CSS within <style> tags in the <head> section (no external CSS files).
- A single card with modern styling: rounded corners (10px), box shadow, solid 2px border with specific color, responsive layout, and hover effects.
- Card content based on the following details:
  - Title: {details['name']}
  - Description: {details['description']}
  - Image URL: {details['url']}
- Use the provided Image URL directly for the card's image.
- Image should be object-fit: cover, 300px wide, 150px high.
- Card width: 300px, centered on page with flexbox.
- Responsive design for desktop and mobile (use max-width and media queries).
- Hover effects: scale(1.05) transform and darker border color.
- Border color: #4CAF50 for the card, darkening to #388E3C on hover.
- Use Google Fonts (Roboto) for typography.
- Do not include any external CSS or JavaScript files.
- Do not add any comments or text outside the HTML structure (e.g., no "this is html file").
- Return only the HTML code as a properly formatted string.

**Example 1:**
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
            font-family: 'Roboto', sans-serif;
        }}
        .card {{
            width: 300px;
            border: 2px solid #4CAF50;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s, border-color 0.3s;
        }}
        .card:hover {{
            transform: scale(1.05);
            border-color: #388E3C;
        }}
        .card img {{
            width: 100%;
            height: 150px;
            object-fit: cover;
        }}
        .card-content {{
            padding: 15px;
        }}
        .card-content h2 {{
            margin: 0 0 10px;
            font-size: 24px;
            color: #333;
        }}
        .card-content p {{
            margin: 0;
            font-size: 16px;
            color: #666;
        }}
        @media (max-width: 400px) {{
            .card {{
                width: 90%;
            }}
        }}
    </style>
</head>
<body>
    <div class="card">
        <img src="https://example.com/sample.jpg" alt="Sample">
        <div class="card-content">
            <h2>Sample Title</h2>
            <p>Sample description text here.</p>
        </div>
    </div>
</body>
</html>

**Example 2:**
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
            font-family: 'Roboto', sans-serif;
        }}
        .card {{
            width: 300px;
            border: 2px solid #4CAF50;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s, border-color 0.3s;
        }}
        .card:hover {{
            transform: scale(1.05);
            border-color: #388E3C;
        }}
        .card img {{
            width: 100%;
            height: 150px;
            object-fit: cover;
        }}
        .card-content {{
            padding: 15px;
        }}
        .card-content h2 {{
            margin: 0 0 10px;
            font-size: 24px;
            color: #333;
        }}
        .card-content p {{
            margin: 0;
            font-size: 16px;
            color: #666;
        }}
        @media (max-width: 400px) {{
            .card {{
                width: 90%;
            }}
        }}
    </style>
</head>
<body>
    <div class="card">
        <img src="https://example.com/another.jpg" alt="Another">
        <div class="card-content">
            <h2>Another Title</h2>
            <p>Another description text here.</p>
        </div>
    </div>
</body>
</html>

Generate HTML for the card with the provided details.
"""

# Generate card HTML and save to templates/
def cardGen(details, num):
    try:
        prompt = get_card_prompt(details)
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.6,
        )

        html_code = response.generations[0].text.strip()
        file_path = os.path.join(TEMPLATE_DIR, f"card{num}.html")

        # Ensure the HTML code is complete
        if not html_code.startswith('<!DOCTYPE html>'):
            html_code = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>Card</title>\n<style>\n</style>\n</head>\n<body>\n{html_code}\n</body>\n</html>'

        with open(file_path, "w") as f:
            f.write(html_code)

        print(f"✅ Saved: {file_path}")
    except Exception as e:
        print(f"❌ Error generating card {num}: {str(e)}")

# Wrapper for multiprocessing
def process_card(args):
    details, num = args
    cardGen(details, num)

# Loop over JSON list of card details with multiprocessing
def html_code_gen(jsonObj):
    clear_templates_folder()
    with Pool() as pool:
        pool.map(process_card, [(details, i) for i, details in enumerate(jsonObj)])

# Example usage
if __name__ == "__main__":
    example_cards = [
        {
            "name": "Red Apple",
            "description": "Juicy, sweet, and perfect for a snack.",
            "url": "https://example.com/images/red_apple.jpg",
        },
        {
            "name": "Golden Apple",
            "description": "A rare variety with a golden sheen and crisp bite.",
            "url": "https://example.com/images/golden_apple.jpg",
        }
    ]

    html_code_gen(example_cards)