import sys
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

def subset_font(input_file, text, output_file):
    font = TTFont(input_file)
    
    # サブセット化のオプションを設定
    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
    
    # サブセットを実行
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    
    font.save(output_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python GlyphPicker.py [font_file_path] [text]")
        sys.exit(1)
    
    input_font = sys.argv[1]
    text = sys.argv[2]
    output_font = "subsetted_font.woff2"

    subset_font(input_font, text, output_font)

    with open(output_font, 'rb') as f:
        sys.stdout.buffer.write(f.read())
