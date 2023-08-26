# mkfontcss.py
import os
import csv
import argparse
import base64
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter

def load_font_index(style=None, fonts_dir="fonts"):
    # --style オプションに基づいてCSVの名前を設定
    csv_name = style + ".csv" if style else "fontindex.csv"
    csv_path = os.path.join(fonts_dir, csv_name)
    
    font_index = {}
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            character, font_file = row
            font_index[character] = font_file
    return font_index

def generate_data_uri(font_path, characters):
    font = TTFont(font_path)
    
    # Get font's family name
    font_family_name = font["name"].getName(1, 3, 1, 1033).toUnicode()
    
    # Subset font to only include specified characters
    subsetter = Subsetter()
    subsetter.populate(text=characters)
    subsetter.subset(font)

    # Convert font to WOFF2 format
    from io import BytesIO
    font_stream = BytesIO()
    font.flavor = "woff2"
    font.save(font_stream)
    font_data = font_stream.getvalue()

    return font_family_name, f"data:font/woff2;base64,{base64.b64encode(font_data).decode('utf-8')}"

def inject_css_into_html(html_file, css_file):
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    font_family_names = [line.split("'")[1] for line in css_content.splitlines() if "font-family" in line]

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # CSSファイルの名前だけを取得
    css_filename_only = os.path.basename(css_file)

    # CSSファイルへのリンクを挿入
    css_link = f'<link rel="stylesheet" type="text/css" href="{css_filename_only}">'

    # すべてのフォントを参照するスタイルを追加
    style_content = f"<style>body {{ font-family: {', '.join(font_family_names)}; }}</style>"

    if '</head>' in content:
        content = content.replace('</head>', f'{css_link}{style_content}</head>', 1)
    else:
        content = css_link + style_content + content

    # ".wf.html" 拡張子で新しいファイル名を生成
    output_html_file = os.path.splitext(html_file)[0] + ".wf.html"
    
    with open(output_html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_html_file

def main():
    parser = argparse.ArgumentParser(description='Generate CSS with embedded font data for specified HTML file and update the HTML file to use the font.')
    parser.add_argument('file', help='The HTML file to process.')
    parser.add_argument('--style', help='Style name for selecting the appropriate CSV font index.')
    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    font_index = load_font_index(style=args.style)
    used_fonts = {font_index[char] for char in text if char in font_index}

    css_content = ""
    for font_file in used_fonts:
        relevant_chars = "".join([char for char in text if font_index.get(char) == font_file])
        font_family_name, data_uri = generate_data_uri(os.path.join("fonts", font_file), relevant_chars)
        css_content += f"""
        @font-face {{
            font-family: '{font_family_name}';
            src: url({data_uri}) format('woff2');
        }}
        """

    output_css_file = os.path.splitext(args.file)[0] + ".css"
    with open(output_css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)

    # Update HTML to reference the generated CSS
    inject_css_into_html(args.file, output_css_file)

    print(f"CSS file saved to {output_css_file} and HTML file updated to reference the CSS.")

if __name__ == "__main__":
    main()
