import workflows.prompt_refiner as p # used for making prompt better and all
import workflows.csv_from_prompt as c #used for making format of every card
import cardCreation.imageUrlAdd as imgAdd # used for adding Image url
import support.JsonstringToJson as js #used to convert the response as the json obj
import cardCreation.Html_Code_GEN as htmG #used for making html code for every card
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from weasyprint import CSS
from tempfile import NamedTemporaryFile
# import cardCreation.Card as cards
# Currently lets develop for the 



def generate_single_page_pdf(output_pdf='cards_single_page.pdf'):
    TEMPLATE_DIR = "templates"
    OUTPUT_FILE = "output_pdfs/combined_output.pdf"
    os.makedirs("output_pdfs", exist_ok=True)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    # List to collect temporary individual PDF paths
    temp_pdf_paths = []

    # Render and convert each HTML template to a temporary PDF
    for file_name in sorted(os.listdir(TEMPLATE_DIR)):
        if file_name.endswith(".html"):
            template = env.get_template(file_name)
            rendered_html = template.render()  # Pass context if needed

            # Save rendered HTML to a temporary PDF
            temp_pdf = NamedTemporaryFile(delete=False, suffix=".pdf")
            HTML(string=rendered_html).write_pdf(temp_pdf.name, stylesheets=[CSS(string='@page { size: A4; margin: 1in; }')])
            temp_pdf_paths.append(temp_pdf.name)
            print(f"✔️ Rendered {file_name} to temp PDF")

    # Combine all temporary PDFs into one final PDF
    from PyPDF2 import PdfMerger

    merger = PdfMerger()
    for pdf_path in temp_pdf_paths:
        merger.append(pdf_path)

    merger.write(OUTPUT_FILE)
    merger.close()

    print(f"\n🎉 All templates combined into: {OUTPUT_FILE}")



user_prompt=input("please enter what ever and how ever you want your cards to be as our model tries to reach your creative level : ")

number_cards= int(input("Enter number of cards you want to have in your game : "))

print("wait out will be generated model is being processing")

exact_prompt=p.cardPromptRefinement(user_prompt,number_cards) 

"""

#taking the prompt after the user given prompt is refined and all , it will be passed to the next stage in work flows

and model will be included here it shoule have capacity of creating own file/folder structure and process the request on it's own


"""
# print(exact_prompt)
print("----------------------- Format of each Card ----------------------")
string=c.csv_prompt(exact_prompt)
# print(string)

print(type(string))

jsonObj=js.json_to_card_list(string)



print("-------------- Add image URL    -------------------")

# print(type(jsonObj))
jObj=imgAdd.imageUrlAdder(jsonObj)

# print(jObj)

print("-------------- Going for Card Page Generation and all may be using COHERE LLM which is best in giving html structure --------------------- ")

htmG.html_code_gen(jObj)

print("-------------------------- started printing Cards --------------------------------------")
generate_single_page_pdf()