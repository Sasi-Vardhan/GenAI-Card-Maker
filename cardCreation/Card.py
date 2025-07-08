import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def getCards(output_pdf='cards_output.pdf'):
    # Set up Jinja2 environment to load templates from 'templates' folder
    env = Environment(loader=FileSystemLoader('/Users/sasivardhanvemuri/Desktop/Card-Design/model/templates'))
    
    # Get list of all HTML files in the templates folder
    template_files = [f for f in os.listdir('templates') if f.endswith('.html')]
    
    # Placeholder data for Jinja2 templates (can be customized)
    data = {
        'card_title': 'Sample Card',
        'card_content': 'This is a sample card generated from a template.'
    }
    
    # List to store rendered HTML strings
    rendered_htmls = []
    
    # Process each template
    for template_file in template_files:
        try:
            # Load and render the template with data
            template = env.get_template(template_file)
            rendered_html = template.render(**data)
            rendered_htmls.append(rendered_html)
        except Exception as e:
            print(f"Error processing template {template_file}: {str(e)}")
    
    # Combine all rendered HTMLs into a single HTML string
    combined_html = '<div style="page-break-after: always;">' + '</div><div style="page-break-after: always;">'.join(rendered_htmls) + '</div>'
    
    # Generate PDF from combined HTML
    try:
        HTML(string=combined_html).write_pdf(output_pdf)
        print(f"PDF generated successfully: {output_pdf}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

if(__name__=="__main__"):
    getCards()