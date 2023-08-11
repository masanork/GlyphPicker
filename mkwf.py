# mkwf.py

import argparse
from GlyphPicker import subset_font

def read_file_content(filename):
    """ファイルの内容を読み取るヘルパー関数"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(description="Generate a subsetted WOFF2 font.")
    
    # -s オプションの追加
    parser.add_argument("-s", "--string", type=str, help="The string for which the font should be subsetted.")
    
    # ファイル名の引数
    parser.add_argument("filename", type=str, nargs='?', help="Filename to read the content for subsetting the font.")
    
    # -o オプションの追加
    parser.add_argument("-o", "--output", type=str, help="Output filename. If not specified, uses the provided filename.")

    args = parser.parse_args()

    # サブセットする文字列の決定
    if args.string:
        subset_string = args.string
    elif args.filename:
        subset_string = read_file_content(args.filename)
    else:
        print("Please provide a string or a filename.")
        return

    # 出力ファイル名の決定
    output_name = args.output
    if not output_name:
        output_name = (args.filename or args.string)
        if not output_name.endswith(".woff2"):
            output_name += ".woff2"
    
    # フォントのサブセット
    subset_font(subset_string, output_name)
    print(f"Saved to {output_name}")

if __name__ == '__main__':
    main()
