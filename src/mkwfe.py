import argparse
import base64
from GlyphPicker import subset_font

def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def write_file_content(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_title_and_author(txt_content):
    lines = txt_content.split('\n')
    title = lines[0] if len(lines) > 0 else "Unknown Title"
    author = lines[1] if len(lines) > 1 else "Unknown Author"
    content = '\n'.join(lines[2:]) if len(lines) > 2 else ""
    return title, author, content

def generate_font_data_uri(text, font_style="default"):
    font_filename = subset_font(text, style=font_style)
    with open(font_filename, "rb") as f:
        base64_encoded_font = base64.b64encode(f.read()).decode("utf-8")
    return f"data:application/font-woff2;charset=utf-8;base64,{base64_encoded_font}"

def convert_txt_to_html(txt_content, vertical=False):
    vertical_style = "writing-mode: vertical-rl; text-orientation: mixed; line-height: 1.5; font-size: 2em;" if vertical else "line-height: 1.5; font-size: 1.5em;"
    sepia_background = "background-color: #F4ECD8;"
    
    title, author, content = extract_title_and_author(txt_content)
    bold_font_data_uri = generate_font_data_uri(title + " " + author, font_style="bold")
    serif_font_data_uri = vertical and generate_font_data_uri(content, font_style="serif") or ""

    fonts_css = f"""
@font-face {{
    font-family: 'SubsetFontBold';
    src: url('{bold_font_data_uri}') format('woff2');
    font-weight: bold;
    font-style: normal;
}}
h1, h2 {{
    font-family: 'SubsetFontBold';
}}
"""
    if vertical:
        fonts_css += f"""
@font-face {{
    font-family: 'SubsetFontSerif';
    src: url('{serif_font_data_uri}') format('woff2');
    font-weight: normal;
    font-style: normal;
}}
body, p {{
    font-family: 'SubsetFontSerif';
}}
"""

    paragraphs = content.split('\n')
    html_paragraphs = [f"<p>{p}</p>" for p in paragraphs]
    html_body_content = f"<h1>{title}</h1>\n<h2>{author}</h2>" + '\n'.join(html_paragraphs)

    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} by {author}</title>
    <style>
        body {{
            {sepia_background}
            {vertical_style}
        }}
        {fonts_css}
    </style>
</head>
<body>
{html_body_content}
</body>
</html>"""

    return html_template

def append_webfont_to_html(html_content, font_filename, embed=False):
    if embed:
        with open(font_filename, "rb") as f:
            base64_encoded_font = base64.b64encode(f.read()).decode("utf-8")
        font_url = f"data:application/font-woff2;charset=utf-8;base64,{base64_encoded_font}"
    else:
        font_url = font_filename
    
    css = f"""<style>
@font-face {{
    font-family: 'SubsetFont';
    src: url('{font_url}') format('woff2');
    font-weight: normal;
    font-style: normal;
}}
body, pre {{
    font-family: 'SubsetFont';
}}
</style>"""
    head_close_index = html_content.lower().find("</head>")
    if head_close_index == -1:
        return html_content + css
    else:
        return html_content[:head_close_index] + css + html_content[head_close_index:]

def main():
    parser = argparse.ArgumentParser(description="Generate a subsetted WOFF2 font.")
    parser.add_argument("-v", "--vertical", action="store_true", help="Convert TXT to vertical writing mode in HTML.")
    parser.add_argument("--string", type=str, help="The string for which the font should be subsetted.")
    parser.add_argument("filename", type=str, nargs='?', help="Filename to read the content for subsetting the font.")
    parser.add_argument("-o", "--output", type=str, help="Output filename. If not specified, uses the provided filename.")
    parser.add_argument("-s", "--style", type=str, default="default", help="Font style to use (e.g., 'bold', 'serif'). Defaults to 'default'.")
    args = parser.parse_args()

    if args.string:
        subset_string = args.string
    elif args.filename:
        subset_string = read_file_content(args.filename)
    else:
        print("Please provide a string or a filename.")
        return

    if args.filename and args.filename.endswith('.txt'):
        subset_string = convert_txt_to_html(subset_string, args.vertical)

    output_name = args.output
    if not output_name:
        output_name = (args.filename or args.string)
        if not output_name.endswith(".woff2"):
            output_name += ".woff2"
    
    subset_font(subset_string, style=args.style, output_file=output_name)
    print(f"Saved WOFF2 to {output_name}")

    # If the input is an HTML file or converted from a TXT file
    if args.filename and (args.filename.endswith('.html') or args.filename.endswith('.txt')):
        # Generate both wf.html and wfe.html
        modified_html = append_webfont_to_html(subset_string, output_name)
        new_html_filename = args.filename.rsplit('.', 1)[0] + ".wf.html"
        write_file_content(new_html_filename, modified_html)
        print(f"Saved wf.html to {new_html_filename}")

        modified_html_embedded = append_webfont_to_html(subset_string, output_name, embed=True)
        new_html_embedded_filename = args.filename.rsplit('.', 1)[0] + ".wfe.html"
        write_file_content(new_html_embedded_filename, modified_html_embedded)
        print(f"Saved wfe.html to {new_html_embedded_filename}")

if __name__ == '__main__':
    main()
