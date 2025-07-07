import cohere
import os

# Use your API key here
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(COHERE_API_KEY)

def cardGen(details,num):

    prompt = f"""
    Generate a clean HTML and CSS code for a single card design details for card are here {details} 
    - Nice styling with CSS (rounded corners, shadow, centered text)
    Return the full HTML code in a <style> and <body> tag. Keep it minimal and responsive.
    """

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=800,
        temperature=0.6,
    )

    # Save output to HTML file
    html_code = response.generations[0].text.strip()

    with open(f"card{num}.html", "w") as f:
        f.write(html_code)

    print(f"✅ Card generated as 'card{num}.html'")


def html_code_gen(jsonObj):
    for i in range(len(jsonObj)):
        details=jsonObj[i]
        cardGen(details,i)

if(__name__ == '__main__'):

    prompt = """
    Generate a clean HTML and CSS code for a single card design for a red apple.
    The card should include:
    - A title: "Red Apple"
    - A description: "Juicy, sweet, and perfect for a snack."
    - Image placeholder or Unsplash image
    - Nice styling with CSS (rounded corners, shadow, centered text)
    Return the full HTML code in a <style> and <body> tag. Keep it minimal and responsive.
    """

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=800,
        temperature=0.5,
    )

    # Save output to HTML file
    html_code = response.generations[0].text.strip()

    with open("apple_card.html", "w") as f:
        f.write(html_code)

    print("✅ Card generated as 'apple_card.html'")
