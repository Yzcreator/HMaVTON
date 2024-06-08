from PIL import Image
import os

def convert_jpg_to_png(folder_path, output_folder):
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg'):
            # 构造输入和输出文件路径
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')

            # 打开 JPG 图片并转换为 PNG
            image = Image.open(input_path)
            image.save(output_path, 'PNG')

# 指定要转换图片的文件夹路径
folder_path = 'datasets/VITON-HD/train/agnostic-v3.2'

# 指定保存转换后图片的新文件夹路径
output_folder = 'datasets/VITON-HD-png/train/agnostic-v3.2'

# 创建保存转换后图片的新文件夹
os.makedirs(output_folder, exist_ok=True)

# 调用函数将 JPG 图片转换为 PNG 并保存
convert_jpg_to_png(folder_path, output_folder)