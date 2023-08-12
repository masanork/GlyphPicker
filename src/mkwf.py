import argparse
from GlyphPicker import subset_font

def read_file_content(filename):
    """ファイルの内容を読み取るヘルパー関数"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def write_file_content(filename, content):
    """ファイルに内容を書き込むヘルパー関数"""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def append_webfont_to_html(html_content, font_filename):
    """HTMLにWebFont CSSを追記する関数"""
    css = f"""<style>
@font-face {{
    font-family: 'SubsetFont';
    src: url('{font_filename}') format('woff2');
    font-weight: normal;
    font-style: normal;
}}
body {{
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
    
    parser.add_argument("-s", "--string", type=str, help="The string for which the font should be subsetted.")
    parser.add_argument("filename", type=str, nargs='?', help="Filename to read the content for subsetting the font.")
    parser.add_argument("-o", "--output", type=str, help="Output filename. If not specified, uses the provided filename.")

    args = parser.parse_args()

    if args.string:
        subset_string = args.string
    elif args.filename:
        subset_string = read_file_content(args.filename)
    else:
        print("Please provide a string or a filename.")
        return

    output_name = args.output
    if not output_name:
        output_name = (args.filename or args.string)
        if not output_name.endswith(".woff2"):
            output_name += ".woff2"
    
    subset_font(subset_string, output_name)
    print(f"Saved to {output_name}")

    # If the input is an HTML file, append the webfont CSS and save with new filename
    if args.filename and args.filename.endswith('.html'):
        modified_html = append_webfont_to_html(subset_string, output_name)
        new_html_filename = args.filename.rsplit('.', 1)[0] + ".wf.html"
        write_file_content(new_html_filename, modified_html)
        print(f"HTML with embedded webfont saved to {new_html_filename}")

if __name__ == '__main__':
    main()
