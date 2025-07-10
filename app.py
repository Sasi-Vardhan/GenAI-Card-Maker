import streamlit as st
import os
from workflows import prompt_refiner as p
from workflows import csv_from_prompt as c
from cardCreation import imageUrlAdd as imgAdd
from support import JsonstringToJson as js
from cardCreation import Html_Code_GEN as htmG
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from tempfile import NamedTemporaryFile
from PyPDF2 import PdfMerger


from fpdf import FPDF
from bs4 import BeautifulSoup


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

            # Strip HTML tags and get plain text
            soup = BeautifulSoup(rendered_html, "html.parser")
            text_content = soup.get_text(separator="\n")

            # Add new page and text
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in text_content.split("\n"):
                if line.strip():
                    pdf.multi_cell(0, 10, txt=line.strip())

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
