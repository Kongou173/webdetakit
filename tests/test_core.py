import pytest
import sys
import os
import pandas as pd
import json

from webdetakit.core import fetch_html, extract_text, extract_attribute, normalize_to_dataframe, save_dataframe_to_csv, save_dataframe_to_json

TEST_URL_SUCCESS = "https://www.example.com"
TEST_URL_FAIL = "https://this-is-a-non-existent-domain-1234567890.com"

# テスト用のダミーHTMLコンテンツ
DUMMY_HTML = """
<html>
<head><title>Test Page</title></head>
<body>
    <h1>Main Title</h1>
    <p class="intro">This is an introduction.</p>
    <a href="/page1">Link 1</a>
    <a href="https://example.com/page2">Link 2</a>
    <img src="/image.png" alt="Test Image">
</body>
</html>
"""

DUMMY_DATA_VALID = {
    "Name": ["Alice", "Bob"],
    "Age": [30, 24],
    "City": ["New York", "London"]
}

DUMMY_DATA_INVALID = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [30, 24]
}

def test_fetch_html_success():
    """
    有効なURLからHTMLが正常に取得できるかテスト。
    """
    html_content = fetch_html(TEST_URL_SUCCESS)
    assert isinstance(html_content, str)
    assert len(html_content) > 0
    assert "Example Domain" in html_content

def test_fetch_html_failure():
    """
    存在しないURLやアクセスできないURLの場合に空文字列が返されるかテスト。
    """
    html_content = fetch_html(TEST_URL_FAIL)
    assert html_content == ""

def test_extract_text_h1():
    """
    H1タグのテキストが正しく抽出されるかテスト。
    """
    extracted_texts = extract_text(DUMMY_HTML, "h1")
    assert extracted_texts == ["Main Title"]

def test_extract_text_class():
    """
    特定のクラスを持つPタグのテキストが正しく抽出されるかテスト。
    """
    extracted_texts = extract_text(DUMMY_HTML, "p.intro")
    assert extracted_texts == ["This is an introduction."]

def test_extract_attribute_href():
    """
    Aタグのhref属性が正しく抽出されるかテスト。
    """
    extracted_attrs = extract_attribute(DUMMY_HTML, "a", "href")
    assert "/page1" in extracted_attrs
    assert "https://example.com/page2" in extracted_attrs
    assert len(extracted_attrs) == 2

def test_extract_attribute_src():
    """
    Imgタグのsrc属性が正しく抽出されるかテスト。
    """
    extracted_attrs = extract_attribute(DUMMY_HTML, "img", "src")
    assert extracted_attrs == ["/image.png"]

def test_normalize_to_dataframe_valid_data():
    """
    有効なデータが正しくDataFrameに正規化されるかテスト。
    """
    df = normalize_to_dataframe(DUMMY_DATA_VALID)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["Name", "Age", "City"]
    assert len(df) == 2
    assert df.iloc[0]["Name"] == "Alice"
    assert df.iloc[1]["Age"] == 24

def test_normalize_to_dataframe_invalid_data():
    """
    長さの異なるリストが渡された場合にValueErrorが発生するかテスト。
    """
    with pytest.raises(ValueError, match="Length mismatch for key"):
        normalize_to_dataframe(DUMMY_DATA_INVALID)

def test_normalize_to_dataframe_empty_data():
    """
    空の辞書が渡された場合に空のDataFrameが返されるかテスト。
    """
    df = normalize_to_dataframe({})
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_save_dataframe_to_csv(tmp_path):
    """
    DataFrameが正しくCSVファイルに保存されるかテスト。
    """
    df = pd.DataFrame(DUMMY_DATA_VALID)
    file_path = tmp_path / "test_output.csv"
    save_dataframe_to_csv(df, str(file_path))
    
    assert file_path.exists()
    content = file_path.read_text(encoding='utf-8')
    assert "Name,Age,City" in content
    assert "Alice,30,New York" in content

def test_save_dataframe_to_json(tmp_path):
    """
    DataFrameが正しくJSONファイルに保存されるかテスト。
    """
    df = pd.DataFrame(DUMMY_DATA_VALID)
    file_path = tmp_path / "test_output.json"
    save_dataframe_to_json(df, str(file_path))
    
    assert file_path.exists()
    content = file_path.read_text(encoding='utf-8')
    parsed_json = json.loads(content)
    assert len(parsed_json) == 2
    assert parsed_json[0]["Name"] == "Alice"
    assert parsed_json[1]["Age"] == 24
