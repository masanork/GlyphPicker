import re
import base64
import os
from bs4 import BeautifulSoup
import argparse

def embed_font_in_html(html_filepath):
    with open(html_filepath, 'r', encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Extract inline styles
    styles = [style_tag.string for style_tag in soup.find_all("style")]

    # Process each inline stylesheet
    for css_content in styles:
        # Find all @font-face rules
        font_face_rules = re.findall(r'@font-face\s*{([^}]+)}', css_content)

        for rule in font_face_rules:
            # Extract font URL
            url_matches = re.search(r'url\(([^)]+)\)', rule)
            if url_matches:
                font_url = url_matches.group(1).strip('\'"')
                font_filepath = os.path.join(os.path.dirname(html_filepath), font_url)

                # Read font file and encode as base64
                with open(font_filepath, 'rb') as font_file:
                    base64_encoded = base64.b64encode(font_file.read()).decode('utf-8')
                
                # Create data URI
                mime_type = "font/woff2"
                data_uri = f"data:{mime_type};base64,{base64_encoded}"

                # Replace font URL in CSS with data URI
                css_content = css_content.replace(font_url, data_uri)
                for style_tag in soup.find_all("style"):
                    style_tag.string.replace_with(css_content)

    # Return updated HTML
    return str(soup)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed webfonts in HTML as Data URI.")
    parser.add_argument("html_filepath", help="Path to the HTML file.")
    parser.add_argument("-o", "--output", help="Output file name. If not provided, print to stdout.")
    args = parser.parse_args()

    result_html = embed_font_in_html(args.html_filepath)
    if args.output:
        with open(args.output, 'w', encoding="utf-8") as out_file:
            out_file.write(result_html)
    else:
        print(result_html)
