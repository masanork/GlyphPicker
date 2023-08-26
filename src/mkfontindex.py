# mkfontindex.py

import os
import csv
from fontTools.ttLib import TTFont

def extract_characters_from_font(font_path):
    font = TTFont(font_path)
    # cmap tableからUnicodeのコードポイントを取得
    cmap = font.getBestCmap()
    return set(cmap.keys())  # コードポイントを直接取得します

def main():
    fonts_dir = "fonts"
    font_files = [f for f in os.listdir(fonts_dir) if f.endswith(('.ttf', '.otf'))]

    # 優先順位に従ってフォントファイルをソートする場合、この行を変更する
    font_files.sort()  # ここでは単純にアルファベット順としています

    character_to_font = {}

    for font_file in font_files:
        full_path = os.path.join(fonts_dir, font_file)
        codepoints = extract_characters_from_font(full_path)
        for codepoint in codepoints:
            # コードポイントがまだ登録されていない場合のみ、現在のフォントを登録する
            if codepoint not in character_to_font:
                character_to_font[codepoint] = font_file

    # CSVとして保存
    csv_path = os.path.join(fonts_dir, "fontindex.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Character", "Font File"])
        for codepoint, font_file in character_to_font.items():
            writer.writerow([chr(codepoint), font_file])

    print(f"fontindex.csv has been saved to {fonts_dir}")

if __name__ == "__main__":
    main()
