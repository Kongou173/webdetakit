# webdetakit/core.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_html(url: str) -> str:
    """
    指定されたURLからHTMLコンテンツを取得します。

    Args:
        url (str): 取得したいWebページのURL。

    Returns:
        str: 取得したWebページのHTMLコンテンツ。
             エラーが発生した場合は空文字列を返します。
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

def extract_text(html_content: str, css_selector: str) -> list[str]:
    """
    HTMLコンテンツから指定されたCSSセレクタに一致する要素のテキストを抽出します。

    Args:
        html_content (str): HTMLコンテンツ。
        css_selector (str): 抽出したい要素を指定するCSSセレクタ (例: 'h1', 'div.title', 'a[href]').

    Returns:
        list[str]: 抽出されたテキストのリスト。
    """
    soup = BeautifulSoup(html_content, 'lxml')
    elements = soup.select(css_selector)
    return [element.get_text(strip=True) for element in elements]

def extract_attribute(html_content: str, css_selector: str, attribute: str) -> list[str]:
    """
    HTMLコンテンツから指定されたCSSセレクタに一致する要素の属性値を抽出します。

    Args:
        html_content (str): HTMLコンテンツ。
        css_selector (str): 抽出したい要素を指定するCSSセレクタ。
        attribute (str): 抽出したい属性名 (例: 'href', 'src', 'alt').

    Returns:
        list[str]: 抽出された属性値のリスト。
    """
    soup = BeautifulSoup(html_content, 'lxml')
    elements = soup.select(css_selector)
    return [element.get(attribute) for element in elements if element.get(attribute)]

def normalize_to_dataframe(data: dict[str, list]) -> pd.DataFrame:
    """
    キーがデータカテゴリ、値がデータのリストである辞書をPandas DataFrameに正規化します。
    各リストの長さは同じである必要があります。

    Args:
        data (dict[str, list]): 抽出されたデータの辞書。
                                例: {'タイトル': ['A', 'B'], 'URL': ['url_a', 'url_b']}

    Returns:
        pd.DataFrame: 正規化されたデータを含むPandas DataFrame。
    """
    if not data:
        return pd.DataFrame()
    
    first_key = list(data.keys())[0]
    expected_length = len(data[first_key])
    for key, value_list in data.items():
        if len(value_list) != expected_length:
            raise ValueError(f"Length mismatch for key '{key}': expected {expected_length}, got {len(value_list)}")
            
    return pd.DataFrame(data)

def save_dataframe_to_csv(dataframe: pd.DataFrame, file_path: str, index: bool = False, encoding: str = 'utf-8') -> None:
    """
    Pandas DataFrameをCSVファイルとして保存します。

    Args:
        dataframe (pd.DataFrame): 保存するDataFrame。
        file_path (str): 保存先のファイルパス (例: 'output.csv')。
        index (bool): DataFrameのインデックスをCSVに書き込むかどうか。デフォルトはFalse。
        encoding (str): ファイルのエンコーディング。デフォルトは'utf-8'。
    """
    dataframe.to_csv(file_path, index=index, encoding=encoding)
    print(f"Data saved to {file_path}")

def save_dataframe_to_json(dataframe: pd.DataFrame, file_path: str, orient: str = 'records', indent: int = 4) -> None:
    """
    Pandas DataFrameをJSONファイルとして保存します。

    Args:
        dataframe (pd.DataFrame): 保存するDataFrame。
        file_path (str): 保存先のファイルパス (例: 'output.json')。
        orient (str): JSON形式の向き。'records' (デフォルト) は各行をオブジェクトとして保存します。
        indent (int): JSON出力のインデントレベル。デフォルトは4。
    """
    dataframe.to_json(file_path, orient=orient, indent=indent)
    print(f"Data saved to {file_path}")


if __name__ == "__main__":
    sample_url = "https://www.example.com"
    html_content = fetch_html(sample_url)
    if html_content:
        print(f"Successfully fetched HTML from {sample_url}")
        
        titles = extract_text(html_content, "h1")
        print(f"Extracted H1 titles: {titles}")

        links = extract_attribute(html_content, "a", "href")
        print(f"Extracted links (first 5): {links[:5]}")

        sample_data = {
            "Title": ["Example Domain"],
            "Link": ["http://www.iana.org/domains/example"]
        }
        
        try:
            df = normalize_to_dataframe(sample_data)
            print("\nNormalized DataFrame:")
            print(df)

            save_dataframe_to_csv(df, "example_output.csv")
            
            save_dataframe_to_json(df, "example_output.json")

        except ValueError as e:
            print(f"Error normalizing data: {e}")

    else:
        print(f"Failed to fetch HTML from {sample_url}")
