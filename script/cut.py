import os
from PIL import Image
import glob


def crop_gif_to_square(image_path, output_path):
    # 打开GIF文件
    img = Image.open(image_path)

    # 转换为RGBA模式，以便处理透明度
    img = img.convert("RGBA")

    # 获取图像的尺寸
    width, height = img.size

    # 取得图像的像素数据
    pixels = img.load()

    # 查找最小和最大非透明像素坐标
    min_x, min_y, max_x, max_y = width, height, 0, 0

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 0:  # 如果不完全透明
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    # 根据最小外接矩形裁切图像
    img_cropped = img.crop((min_x, min_y, max_x + 1, max_y + 1))

    # 获取裁切后的宽高
    cropped_width, cropped_height = img_cropped.size

    # 计算正方形边长
    size = max(cropped_width, cropped_height)

    # 创建一个新的透明背景图像，大小为正方形
    new_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # 计算填充的位置
    offset_x = (size - cropped_width) // 2
    offset_y = (size - cropped_height) // 2

    # 将裁切后的图像粘贴到新的正方形图像中
    new_img.paste(img_cropped, (offset_x, offset_y))

    # 保存结果
    new_img.save(output_path)


def process_gif_folder(input_folder, output_folder):
    # 获取文件夹中所有.gif文件
    gif_files = glob.glob(os.path.join(input_folder, "*.png"))

    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历每个GIF文件并处理
    for gif_file in gif_files:
        # 构造输出文件路径
        output_file = os.path.join(output_folder, os.path.basename(gif_file))

        # 处理该GIF文件
        crop_gif_to_square(gif_file, output_file)
        print(f"Processed: {gif_file} -> {output_file}")


# 使用示例
input_folder = "res/item_icon"  # 替换为你的输入文件夹路径
output_folder = "cut"  # 替换为你的输出文件夹路径

process_gif_folder(input_folder, output_folder)

