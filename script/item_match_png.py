import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# 加载 PokeBalls.json 数据
with open('../output/Zcrystals.json', 'r', encoding='utf-8') as f:
    pokeballs = json.load(f)

# 加载 image_src.json 数据
with open('../image_src.json', 'r', encoding='utf-8') as f:
    image_src = json.load(f)

# 创建一个文件夹来保存下载的图片
output_folder = "../item_icon"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 创建一个锁用于线程安全操作
lock = Lock()

# 用于保存未找到图片链接的 cName
missing_cNames = []

def download_image(pokeball):
    cName = pokeball['cName']
    # 检查 image_src 中是否存在对应的图片链接
    if cName in image_src:
        image_url = image_src[cName]
        try:
            # 下载图片
            response = requests.get(image_url)
            if response.status_code == 200:
                # 保存图片到指定文件夹，文件名为 cName
                image_path = os.path.join(output_folder, f"{cName}.png")
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"图片已保存到 {image_path}")
            else:
                print(f"无法下载图片：{image_url}")
        except Exception as e:
            print(f"下载图片时发生错误：{e}")
    else:
        # 使用锁确保线程安全
        with lock:
            missing_cNames.append(cName)
        print(f"未找到图片链接：{cName}")

# 使用多线程下载图片
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_image, pokeballs)

# 将未找到图片链接的 cName 保存到一个 txt 文件中
missing_cNames_file = "../missing_cNames.txt"
with open(missing_cNames_file, 'a', encoding='utf-8') as f:
    for cName in missing_cNames:
        f.write(f"{cName}\n")

print(f"未找到图片链接的 cName 已保存到 {missing_cNames_file}")
print("图片下载完成！")