import argparse
from fontTools.ttLib import TTFont

def extract_codepoints(font_path):
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    return set(cmap.keys())

def main():
    parser = argparse.ArgumentParser(description="Extract codepoints from a TTF file.")
    parser.add_argument("font_path", help="Path to the TTF font file.")
    parser.add_argument("--hex", action="store_true", help="Output in hex format instead of UTF-8 encoded characters.")
    
    args = parser.parse_args()
    codepoints = extract_codepoints(args.font_path)

    if args.hex:
        for cp in sorted(codepoints):
            print(hex(cp))
    else:
        for cp in sorted(codepoints):
            try:
                print(chr(cp), end="")
            except:
                print(f"Cannot decode codepoint {cp}")

if __name__ == "__main__":
    main()
