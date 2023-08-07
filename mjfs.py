from flask import Flask, request, send_file, render_template
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

app = Flask(__name__)

# 事前に読み込んでおくフォントファイル
FONT_PATH = 'ipamjm.ttf'

def subset_font(text, output_file):
    font = TTFont(FONT_PATH)
    
    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
    
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    
    font.save(output_file)

@app.route('/font.woff2', methods=['GET'])
def get_font():
    text = request.args.get('text', '')
    output_font = "subsetted_font.woff2"

    subset_font(text, output_font)

    return send_file(output_font, mimetype='font/woff2')

@app.route('/test', methods=['GET'])
def test_page():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
