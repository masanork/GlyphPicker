import re
import zipfile
import os

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
                    # Save the processed file in the same directory as the original file
                    output_file_name = os.path.join(os.path.dirname(zip_file_name), name)
                    with open(output_file_name, 'w', encoding='utf-8') as of:
                        of.write(content)
    return output_file_name

if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 1:
        print(f'usage: {sys.argv[0]} <zip_file_name>')
        exit()
    process_zip(sys.argv[1])
