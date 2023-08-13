from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options
import toml

# font.tomlファイルから設定を読み込む
with open("font.toml", "r") as file:
    config = toml.load(file)
    FONT_DIRECTORY = config["font"]["directory"]
    DEFAULT_FONT = config["font"]["default"]
    STYLES = config["font"].get("styles", {})

def subset_font(text, style="default", output_file=None):
    # スタイルに応じたフォントを選択
    font_name = STYLES.get(style, DEFAULT_FONT)
    font_path = FONT_DIRECTORY + font_name
    
    font = TTFont(font_path)
    
    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
    
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    
    output = output_file or "output.woff2"
    font.save(output)

    return output
