import requests
import re
from bs4 import BeautifulSoup

def get_google_photo_links(album_url):
    # 使用 requests 抓取相簿頁面
    response = requests.get(album_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 使用正則表達式提取所有圖片連結
    links = re.findall(r'https://lh3\.googleusercontent\.com/[^"]+', str(soup))
    
    # 去除重複連結並保持順序
    unique_links = list(dict.fromkeys(links))
    
    return unique_links

def convert_link(link):
    # 保留顯示部分的 s800
    display_link = re.sub(r'=[a-z0-9\-]+$', '', link)  # 移除所有末尾參數
    display_link = f"{display_link}=s800"             # 添加固定的 s800 參數
    
    # 點擊部分移除所有參數
    original_link = re.sub(r'=[a-z0-9\-]+$', '', link)
    
    return display_link, original_link

def generate_html(links):
    # 生成 HTML，顯示部分保留 s800，點擊部分移除所有參數
    html_content = ""
    for link in links:
        display_link, original_link = convert_link(link)
        html_content += f'<a href="{original_link}" target="_blank"><img src="{display_link}"/></a><br><br><br>\n'
    return html_content

def save_html_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"HTML 檔案已儲存為: {filename}")

def process_album(album_url, output_filename):
    links = get_google_photo_links(album_url)
    html_content = generate_html(links)
    save_html_file(html_content, output_filename)

# 使用範例
if __name__ == "__main__":
    album_url = input("請輸入 Google 相簿的 URL: ")
    output_filename = input("請輸入要儲存的 HTML 檔案名稱: ")
    process_album(album_url, output_filename)
