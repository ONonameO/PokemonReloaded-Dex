from bs4 import BeautifulSoup
import json


# HTML 文件路径
html_file_path = '道具列表2.html'

# 读取 HTML 文件内容
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 创建一个字典来保存 alt 和 src 的键值对
image_data = {}

# 遍历所有 img 标签
for img in soup.find_all('img'):
    alt_text = img.get('alt')  # 获取 alt 属性
    src_url = img.get('data-loginonly-srcset')   # 获取 src 属性

    if alt_text and src_url:
        # 提取第一个 .png 文件路径
        # 找到第一个 .png 的位置
        png_index = src_url.find('.png')
        if png_index != -1:
            # 提取第一个 .png 文件路径
            first_png_url = src_url[:png_index + 4]  # 包含 .png
        else:
            first_png_url = src_url  # 如果没有找到 .png，保留原路径

        first_png_url = 'https:' + first_png_url.replace('/thumb','')

        # 检查 alt 是否已经存在于字典中
        if alt_text not in image_data:
            # 将 alt 和 src 保存为键值对
            image_data[alt_text] = first_png_url

# 将数据保存到 JSON 文件
json_file_path = 'image_src.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(image_data, json_file, ensure_ascii=False, indent=4)

print(f"数据已保存到 {json_file_path}")