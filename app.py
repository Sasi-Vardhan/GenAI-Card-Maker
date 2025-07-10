import streamlit as st
import os
from workflows import prompt_refiner as p
from workflows import csv_from_prompt as c
from cardCreation import imageUrlAdd as imgAdd
from support import JsonstringToJson as js
from cardCreation import Html_Code_GEN as htmG
from jinja2 import Environment, FileSystemLoader
from tempfile import NamedTemporaryFile
from PyPDF2 import PdfMerger


from fpdf import FPDF
from bs4 import BeautifulSoup


TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output_pdfs"
FINAL_PDF = os.path.join(OUTPUT_DIR, "combined_output.pdf")
os.makedirs(OUTPUT_DIR, exist_ok=True)


from fpdf import FPDF
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output_pdfs"
FINAL_PDF = os.path.join(OUTPUT_DIR, "combined_output.pdf")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_single_pdf():
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    for file_name in sorted(os.listdir(TEMPLATE_DIR)):
        if file_name.endswith(".html"):
            template = env.get_template(file_name)
            rendered_html = template.render()
            soup = BeautifulSoup(rendered_html, "html.parser")

            # Extract card content
            title = soup.find("h1") or soup.find("h2")
            paragraphs = soup.find_all("p")
            image_tag = soup.find("img")

            pdf.add_page()

            # Title
            if title:
                pdf.set_font("Helvetica", style="B", size=16)
                pdf.multi_cell(0, 10, title.get_text(strip=True), align="C")
                pdf.ln(5)

            # Image
            if image_tag and image_tag.get("src"):
                img_url = image_tag["src"]
                try:
                    response = requests.get(img_url)
                    img = Image.open(BytesIO(response.content)).convert("RGB")
                    img_buffer = BytesIO()
                    img.save(img_buffer, format="JPEG")
                    img_buffer.seek(0)

                    # Resize image to fit max width
                    page_width = 180  # mm
                    img_width = img.width * 0.264583  # px to mm
                    img_height = img.height * 0.264583
                    if img_width > page_width:
                        scale = page_width / img_width
                        img_width *= scale
                        img_height *= scale

                    x_center = (210 - img_width) / 2  # A4 width is 210mm
                    pdf.image(img_buffer, x=x_center, y=pdf.get_y(), w=img_width)
                    pdf.ln(img_height + 5)
                except Exception as e:
                    pdf.set_font("Helvetica", size=10)
                    pdf.multi_cell(0, 10, f"[Image failed to load: {img_url}]", align="C")
                    pdf.ln(5)

            # Description
            pdf.set_font("Helvetica", size=12)
            for para in paragraphs:
                text = para.get_text(strip=True)
                if text:
                    pdf.multi_cell(0, 10, text)
                    pdf.ln(2)

    pdf.output(FINAL_PDF)
    return FINAL_PDF



def main():
    st.title("🎴 AI Card Generator with PDF Export")

    with st.form("card_form"):
        user_prompt = st.text_area("📝 Enter your creative idea for the cards")
        number_cards = st.number_input("🔢 Number of cards", min_value=1, value=5)
        submitted = st.form_submit_button("Generate Cards")

    if submitted:
        with st.spinner("⚙️ Processing your prompt..."):
            exact_prompt = p.cardPromptRefinement(user_prompt, number_cards)
            card_string = c.csv_prompt(exact_prompt)
            jsonObj = js.json_to_card_list(card_string)
            enrichedObj = imgAdd.imageUrlAdder(jsonObj)
            htmG.html_code_gen(enrichedObj)
            final_pdf_path = generate_single_pdf()

        st.success("✅ All cards generated and compiled!")

        with open(final_pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name="cards_output.pdf",
                mime="application/pdf"
            )


if __name__ == "__main__":
    main()
