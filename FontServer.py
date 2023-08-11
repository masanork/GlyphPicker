from flask import Flask, request, send_file, render_template
import os
from GlyphPicker import subset_font

app = Flask(__name__)

@app.route('/font.woff2', methods=['GET'])
def get_font():
    text = request.args.get('text', '')
    output_font = "subsetted_font.woff2"

    subset_font(text, output_font)

    return send_file(output_font, mimetype='font/woff2', as_attachment=True)

@app.route('/test', methods=['GET'])
def test_page():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
