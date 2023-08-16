from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options
import toml

# font.tomlファイルから設定を読み込む
with open("font.toml", "r") as file:
    config = toml.load(file)
    FONT_PATH = config["paths"]["FONT_PATH"]
    STYLES = config["font"].get("styles", {})
    DEFAULT_FONT = STYLES.get("default")

def subset_font(text, style="default", output_file=None):
    # Get the list of fonts for the given style, including fallbacks
    font_list = STYLES.get(style)
    if not font_list:
        raise ValueError(f"Unknown font style: {style}")

    # Load the main font (first font in the list)
    main_font_path = FONT_PATH + font_list[0]
    print(f"Loading main font: {main_font_path}")
    font = TTFont(main_font_path)

    # Check for missing glyphs in the main font and try to fetch them from fallback fonts
    # Exclude control characters (e.g., 0xa) from missing glyphs
    missing_glyphs = [char for char in text if ord(char) not in font.getBestCmap() and not (0 <= ord(char) <= 0x1f)]

    for fallback_font_name in font_list[1:]:
        print(f"Loading fallback font: {fallback_font_name}")
        if not missing_glyphs:
            break

        # Load the fallback font
        fallback_font_path = FONT_PATH + fallback_font_name
        fallback_font = TTFont(fallback_font_path)

        # Try to fetch missing glyphs from the fallback font
        for char in missing_glyphs[:]:
            if ord(char) in fallback_font.getBestCmap():
                font['glyf'][char] = fallback_font['glyf'][char]
                font['cmap'].tables[0].cmap[ord(char)] = char
                missing_glyphs.remove(char)
            elif ord(char) >= 0xFE00 and ord(char) <= 0xFE0F:
                # Skip warning message for variation selectors
                missing_glyphs.remove(char)
            else:
                print(f"Glyph not found for codepoint: {hex(ord(char))}")

        # If there are still missing glyphs after checking the fallback font, print a warning message
        if missing_glyphs:
            missing_codepoints = [hex(ord(char)) for char in missing_glyphs]
            print(f"Warning: Glyphs not found for codepoints: {', '.join(missing_codepoints)}")

    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
    
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    
    output = output_file or "output.woff2"
    font.save(output)

    return output
