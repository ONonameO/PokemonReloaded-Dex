import os
from PIL import Image

def batch_webp_to_png(input_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".webp"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.webp', '.png'))
            with Image.open(input_path) as img:
                img.save(output_path, 'PNG')
                print(f"图片 {filename} 已成功转换并保存到 {output_path}")

# 示例用法
batch_webp_to_png("webp", "png")