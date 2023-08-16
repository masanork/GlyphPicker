import re
import zipfile
import os
import argparse
from mkwfe import convert_txt_to_html, append_webfont_to_html, write_file_content

def load_gaiji_table_corrected():
    with open('jisx0213-2004-std.txt') as f:
        ms = (re.match(r'(\d-\w{4})\s+U\+(\w{4})', l) for l in f if l[0] != '#')
        return {m[1]: chr(int(m[2], 16)) for m in ms if m}

gaiji_table = load_gaiji_table_corrected()

def get_gaiji(s):
    m = re.search(r'第(\d)水準\d-(\d{1,2})-(\d{1,2})', s)
    if m:
        key = f'{m[1]}-{int(m[2])+32:2X}{int(m[3])+32:2X}'
        return gaiji_table.get(key, s)
    m = re.search(r'U\+(\w{4})', s)
    if m:
        return chr(int(m[1], 16))
    return s

def sub_gaiji(text):
    return re.sub(r'※［＃.+?］', lambda m: get_gaiji(m[0]), text)

def remove_ruby_corrected(text):
    return re.sub(r'《.+?》', '', text)

def remove_section_and_notes(text):
    text = re.sub(r'[-]{15,}[\s\S]*?テキスト中に現れる記号について[\s\S]*?[-]{15,}', '', text)
    text = re.sub(r'［＃.+?：入力者注.+?］', '', text)
    return text

def remove_all_notes(text):
    return re.sub(r'［＃.+?］', '', text)

def process_zip(zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'r') as zipf:
        for name in zipf.namelist():
            if name.endswith('.txt'):
                with zipf.open(name) as f:
                    content = f.read().decode('shift_jis')
                    content = sub_gaiji(content)
                    content = remove_ruby_corrected(content)
                    content = remove_section_and_notes(content)
                    content = remove_all_notes(content)
                    # Check for "_ruby_" in filename and replace with "_"
                    base_name = os.path.basename(name)
                    base_name = base_name.replace("_ruby_", "_")
                    # Save the processed file in the same directory as the original file
                    output_file_name = os.path.join(os.path.dirname(zip_file_name), base_name)
                    with open(output_file_name, 'w', encoding='utf-8') as of:
                        of.write(content)
    return output_file_name

def aozip_to_html(input_file_name, horizontal=False):
    if input_file_name.endswith('.zip'):
        txt_file_name = process_zip(input_file_name)
    elif input_file_name.endswith('.txt'):
        txt_file_name = input_file_name
    else:
        raise ValueError(f"Unsupported file type: {input_file_name}")

    with open(txt_file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    # mkwfe.py の関数を使用してHTMLに変換
    html_content = convert_txt_to_html(content, vertical=not horizontal)
    # Check for "_ruby_" or "_ruby" in filename and replace with "_"
    base_html_name = os.path.splitext(input_file_name)[0]
    base_html_name = base_html_name.replace("_ruby_", "_").replace("_ruby", "")
    output_html_name = base_html_name + ".html"
    # HTMLファイルを保存
    write_file_content(output_html_name, html_content)
    return output_html_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Aozora Bunko zip file to HTML with embedded fonts.")
    parser.add_argument("zip_file_name", type=str, help="Aozora Bunko zip file to process.")
    parser.add_argument("-ho", "--horizontal", action="store_true", help="Convert TXT to horizontal writing mode in HTML.")
    args = parser.parse_args()

    output_html_name = aozip_to_html(args.zip_file_name, horizontal=args.horizontal)
    print(f"Converted to: {output_html_name}")
