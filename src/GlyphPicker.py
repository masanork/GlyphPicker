# GlyphPicker.py

from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

# FONT_PATH = 'your_font_file_path.ttf'
FONT_PATH = 'ipamjm.ttf'

def subset_font(text, output_file=None):
    font = TTFont(FONT_PATH)
    
    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
    
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    
    output = output_file or "output.woff2"
    font.save(output)

    return output
