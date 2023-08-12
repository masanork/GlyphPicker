import sys
import io
import os  # ファイル名取得のために追加
import base64
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

def subset_font(font_path, text):
    font = TTFont(font_path)
    
    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
    
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    
    output = io.BytesIO()  # メモリ内での保存のためのバッファ
    font.save(output)

    return output.getvalue()

def main():
    if len(sys.argv) != 3:
        print("Usage: python str2wfb64.py [string] [font_path]")
        return

    chars = sys.argv[1]
    font_path = sys.argv[2]

    woff2_data = subset_font(font_path, chars)

    # Convert to Base64
    base64_data = base64.b64encode(woff2_data).decode('utf-8')
    
    # Extract the font family name from the font file name
    font_family = os.path.splitext(os.path.basename(font_path))[0]

    # Print the @font-face CSS rule
    print(f"""
@font-face {{
    font-family: '{font_family}';
    src: url('data:font/woff2;base64,{base64_data}') format('woff2');
    font-weight: normal;
    font-style: normal;
}}
    """)

if __name__ == "__main__":
    main()
