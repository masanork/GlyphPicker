import argparse
from fontTools.ttLib import TTFont

def extract_codepoints(font_path):
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    return set(cmap.keys())

def print_plain_ranges_as_hex(sorted_codepoints):
    # 最初のコードポイントで開始
    current_plain = sorted_codepoints[0] // 0x10000
    start = sorted_codepoints[0]
    end = start

    for cp in sorted_codepoints[1:]:
        # 現在のコードポイントが同じプレーンにあるかチェック
        if cp // 0x10000 == current_plain:
            end = cp
        else:
            # 現在のプレーンの範囲を出力して、次のプレーンに移動
            print(f"{hex(start)}-{hex(end)}")
            start = cp
            end = cp
            current_plain = cp // 0x10000

    # 最後のプレーンの範囲を出力
    print(f"{hex(start)}-{hex(end)}")

def main():
    parser = argparse.ArgumentParser(description="Extract codepoints from a TTF/OTF/WOFF/WOFF2 file and print ranges in hex format.")
    parser.add_argument("font_path", help="Path to the TTF/OTF/WOFF/WOFF2 font file.")
    
    args = parser.parse_args()
    codepoints = extract_codepoints(args.font_path)

    print_plain_ranges_as_hex(sorted(codepoints))

if __name__ == "__main__":
    main()
