import os
import csv
import argparse
from fontTools.ttLib import TTFont

def extract_characters_from_font(font_path):
    font = TTFont(font_path)
    # cmap tableからUnicodeのコードポイントを取得
    cmap = font.getBestCmap()
    return set(cmap.keys())  # コードポイントを直接取得します

def main():
    parser = argparse.ArgumentParser(description="Create a font index based on code points.")
    parser.add_argument("fonts", nargs="*", help="List of fonts to be indexed.")
    parser.add_argument("--style", help="Style name for saving the CSV file.")
    
    args = parser.parse_args()
    
    fonts_dir = "fonts"

    if args.fonts:
        font_files = args.fonts  # フルパスのまま使用
    else:
        font_files = [os.path.join(fonts_dir, f) for f in os.listdir(fonts_dir) if f.endswith(('.ttf', '.otf'))]

    # 指定されたフォント名に基づいて優先順位をソート
    if args.fonts:
        font_files = [f for f in font_files if f in args.fonts]
        font_files.sort(key=lambda x: args.fonts.index(x))
    else:
        font_files.sort()

    character_to_font = {}

    for font_file in font_files:
        codepoints = extract_characters_from_font(font_file)
        for codepoint in codepoints:
            # コードポイントがまだ登録されていない場合のみ、現在のフォントのファイル名を登録する
            if codepoint not in character_to_font:
                character_to_font[codepoint] = os.path.basename(font_file)  # ファイル名のみをCSVに保存

    # --style オプションに基づいてCSVの名前を設定
    csv_name = args.style + ".csv" if args.style else "fontindex.csv"
    
    # fonts_dirを使わずに、直接"fonts"ディレクトリを指定
    csv_path = os.path.join("fonts", csv_name)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Character", "Font File"])
        for codepoint, font_file in character_to_font.items():
            writer.writerow([chr(codepoint), font_file])

    print(f"{csv_name} has been saved to fonts directory.")

if __name__ == "__main__":
    main()
