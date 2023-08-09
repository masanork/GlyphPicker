GlyphPicker - mjfs: IPAmj Font Server
===

GlyphPicker - mjfsは、[IPAmj明朝](https://moji.or.jp/ipafont/ipamjfont/)のWOFF2フォントを動的に生成するWebサーバです。氏名漢字など必要な文字のみを抽出したWOFF2フォントを動的に生成することで、数十KBといった非常に小さな容量で異体字を含む氏名を表示できます。

動作環境
---

IPAmj明朝 Python3.x fonttools Brotli Flask

Usage
---

``` bash
python mjfs.py
```

Webサーバーを立ち上げたら、ブラウザで [テストページ http://localhost:5000/test](http://localhost:5000/test) を開いてください。必要なグリフのみ抽出されたIPAmj明朝を使ったテストページが表示されます。以下のようなHTMLを書いてWebfontとして参照することで、異体字を含む氏名を正確に表示できます。

``` html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webfont Dynamic Generation Test</title>
    <style>
        @font-face {
            font-family: 'SubsettedMJM';
            src: url('http://localhost:5000/font.woff2?text=辺辺󠄂邉邉󠄙邉󠄛邉󠄟邉󠄚邉󠄜邉󠄝邉󠄗邊󠄏邊邊󠄎邊󠄍邊󠄌邊󠄋邊󠄊邊󠄐邊󠄒') format('woff2');
        }

        body {
            font-family: 'SubsettedMJM', sans-serif;
        }
    </style>
</head>
<body>
    <h1>辺辺󠄂邉邉󠄙邉󠄛邉󠄟邉󠄚邉󠄜邉󠄝邉󠄗邊󠄏邊邊󠄎邊󠄍邊󠄌邊󠄋邊󠄊邊󠄐邊󠄒</h1>
</body>
</html>
```
