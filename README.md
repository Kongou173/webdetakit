# WebDetaKit

WebDetaKit は、ウェブサイトから情報を効率的に抽出し、構造化されたデータ（CSV、JSON、Pandas DataFrame）に正規化するためのPythonツールキットです。シンプルなAPIで、ウェブスクレイピングの基本的なニーズに対応します。

## 主な機能

* **HTML取得**: 指定されたURLからウェブページのHTMLコンテンツを取得します。
* **データ抽出**: CSSセレクタを使用して、HTMLから特定のテキストや属性値（例: リンクのURL、画像のソース）を抽出します。
* **データ正規化**: 抽出した複数のデータリストを結合し、Pandas DataFrameとして整形します。
* **ファイル保存**: 整形されたDataFrameをCSVまたはJSON形式でファイルに保存します。

## インストール

WebDetaKit は `pip` を使って簡単にインストールできます

```bash
pip install webdetakit使用方法
```
# コード例
## 1. HTMLコンテンツの取得

```python
from webdetakit.core import fetch_html

url = "[https://www.example.com](https://www.example.com)"
html_content = fetch_html(url)

if html_content:
    print("HTMLコンテンツを取得しました。")
else:
    print("HTMLコンテンツの取得に失敗しました。")
```

## 2. データ（テキスト）の抽出

```Python
from webdetakit.core import extract_text

#ここでは例として取得したHTMLコンテンツを使用
#html_content は fetch_html で取得したもの
#もしくはテスト用のダミーHTMLでも可
dummy_html = """
<html>
<body>
    <h1>メインタイトル</h1>
    <p class="summary">これは要約の段落です。</p>
    <div>
        <span class="item-name">商品A</span>
        <span class="price">1000円</span>
    </div>
    <div>
        <span class="item-name">商品B</span>
        <span class="price">2000円</span>
    </div>
</body>
</html>
"""

#H1タグのテキストを抽出
titles = extract_text(dummy_html, "h1")
print(f"タイトル: {titles}")

#'summary' クラスを持つPタグのテキストを抽出
summaries = extract_text(dummy_html, "p.summary")
print(f"要約: {summaries}")

#'item-name' クラスを持つspanタグのテキストをすべて抽出
item_names = extract_text(dummy_html, "span.item-name")
print(f"商品名: {item_names}")
```
## 3. データ（属性値）の抽出

```Python
from webdetakit.core import extract_attribute

#例としてHTMLコンテンツを使用
dummy_html_links = """
<html>
<body>
    <a href="/page1.html">ページ1</a>
    <img src="/images/pic1.jpg" alt="写真1">
    <a href="[https://www.google.com](https://www.google.com)">Google</a>
</body>
</html>
"""

#aタグのhref属性を抽出
links = extract_attribute(dummy_html_links, "a", "href")
print(f"リンクURL: {links}")

#imgタグのsrc属性を抽出
image_sources = extract_attribute(dummy_html_links, "img", "src")
print(f"画像ソース: {image_sources}")
```
## 4. データの正規化と保存

```Python
from webdetakit.core import normalize_to_dataframe, save_dataframe_to_csv, save_dataframe_to_json
import pandas as pd

#抽出したデータの例（リストの長さは揃っている必要があります）
data_to_normalize = {
    "商品名": ["商品A", "商品B", "商品C"],
    "価格": ["1000円", "2000円", "3000円"],
    "URL": ["/a.html", "/b.html", "/c.html"]
}

#Pandas DataFrameに正規化
df = normalize_to_dataframe(data_to_normalize)
print("\n正規化されたDataFrame:")
print(df)

#CSVファイルとして保存
save_dataframe_to_csv(df, "products.csv")
# 結果: products.csv が作成されます

#JSONファイルとして保存
save_dataframe_to_json(df, "products.json")
# 結果: products.json が作成されます
```
# ライセンス
このプロジェクトは MIT ライセンスの下で公開されています。詳細については LICENSE ファイルをご覧ください。
