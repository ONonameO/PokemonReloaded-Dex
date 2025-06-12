from PIL import Image

def crop_to_min_square(image_path, output_path):
    # 打开图片
    img = Image.open(image_path)
    
    # 获取图片的宽度和高度
    width, height = img.size
    
    # 找到非透明像素的边界
    # 使用 getbbox 方法获取非透明区域的边界框
    bbox = img.getbbox()
    
    if bbox:
        # 如果有非透明区域，裁剪图片
        cropped_img = img.crop(bbox)
        
        # 获取裁剪后图片的宽度和高度
        cropped_width, cropped_height = cropped_img.size
        
        # 计算最小外接正方形的边长
        max_side = max(cropped_width, cropped_height)
        
        # 创建一个新的正方形图片，背景为透明
        new_img = Image.new("RGBA", (max_side, max_side), (0, 0, 0, 0))
        
        # 计算裁剪后图片在正方形中的位置
        paste_x = (max_side - cropped_width) // 2
        paste_y = (max_side - cropped_height) // 2
        
        # 将裁剪后的图片粘贴到正方形图片中
        new_img.paste(cropped_img, (paste_x, paste_y))
        
        # 保存结果
        new_img.save(output_path)
        print(f"处理后的图片已保存到 {output_path}")
    else:
        print("图片中没有非透明像素，无法裁剪。")

# 示例用法
input_image_path = "res/evol/黑色眼镜.png"  # 替换为你的图片路径
output_image_path = "黑色眼镜.png"  # 替换为你想要保存的路径
crop_to_min_square(input_image_path, output_image_path)