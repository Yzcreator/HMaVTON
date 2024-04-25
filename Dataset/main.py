import requests
from PIL import Image
from io import BytesIO
import os
from urllib.parse import urlparse
import time
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
import random

# 打开文件并读取内容
with open('source/outfit_data.txt', 'rb') as file:
    lines = file.readlines()

# 遍历数量
sum = 0
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def download_image(url):
    retries = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[420, 500, 502, 503, 504]
    )
    s = requests.Session()

    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    count = 0
    while True:
        if count < 5:
            try:
                file = s.get(url, headers=headers)
                return file.content
            except Exception as e:
                print('Retry!')
                time.sleep(5)
                count += 1
                exception = e
        else:
            return False
    # try:
    #     response = requests.get(url, timeout=5)  # 设置超时时间为10秒
    #     response.raise_for_status()  # 如果发生错误，抛出异常
    #
    #     # 构建保存路径
    #     save_path = save_dir
    #
    #     # 保存图像文件
    #     with open(save_path, 'wb') as f:
    #         for chunk in response.iter_content(1024):
    #             f.write(chunk)
    #
    #     print(f"Downloaded {url} to {save_path}")
    # except requests.exceptions.Timeout:
    #     print(f"Timeout error while downloading {url}")
    # except requests.exceptions.RequestException as e:
    #     print(f"Error occurred while downloading {url}: {str(e)}")

for line in lines:

    if sum < 580000:
        sum = sum + 1
        continue

    line = line.strip()
    data_list = line.decode().split(';')
    print("第" + str(sum) + "组outfit数据：")
    up = False
    down = False
    up_url = ""
    down_url = ""
    save_up_path = "datasets/up/"
    save_down_path = "datasets/down/"
    POG_path = "datasets/POG.txt"
    up_type = "png"
    down_type = "png"
    up_item = ""
    up_category = ""
    up_text = ""
    down_item = ""
    down_category = ""
    down_text = ""


    for data in data_list:

        data = data.split(',')[-1]  # 使用逗号分割数据并取逗号后部分
        with open('source/item_data.txt', 'rb') as filelist:
            for line in filelist:
                line = line.strip()  # 去除首尾空白字符
                data_item = line.decode().split(',')
                if data_item[0] == data:
                    # print(data_item[2])
                    # print(data_item[3])
                    if '男' in data_item[3]:
                        break
                    if any(keyword in data_item[3] for keyword in ['衫', '外套', 't恤', '上衣', '衬', '体恤', '连衣裙']) and (up == False):
                        up = True
                        up_url = data_item[2]
                        if up_url.startswith("//"):
                            up_url = "http:" + up_url
                        if up_url.endswith("jpg"):
                            up_type = "jpg"
                        print("up = " + str(up))
                        print(up_url)
                        print(data_item[3])
                        up_item = data_item[0]
                        up_category = data_item[1]
                        up_text = data_item[3]
                        break
                    if any(keyword in data_item[3] for keyword in ['裤', '裙']) and (down == False):
                        if '连衣裙' in data_item[3]:
                            break
                        down = True
                        down_url = data_item[2]
                        if down_url.startswith("//"):
                            down_url = "http:" + down_url
                        if down_url.endswith("jpg"):
                            down_type = "jpg"
                        print("down = " + str(down))
                        print(down_url)
                        print(data_item[3])
                        down_item = data_item[0]
                        down_category = data_item[1]
                        down_text = data_item[3]
                        break
        if up == True and down == True and up_type == "png" and down_type == "png":
            print("匹配成功! save!")
            # 上衣
            save_up_path = save_up_path + str(sum) + "." + up_type
            image_up = download_image(up_url)
            image_down = download_image(down_url)
            if image_up == False or image_down == False:
                print("数据请求失败")
                break

            with open(save_up_path, "wb") as file_up:
                file_up.write(image_up)
            print(f"Downloaded {up_url} to {save_up_path}")

            # 下衣
            save_down_path = save_down_path + str(sum) + "." + down_type
            with open(save_down_path, "wb") as file_down:
                file_down.write(image_down)
            print(f"Downloaded {down_url} to {save_down_path}")
            # 写入数据
            data = str(sum) + "," + up_item + "," + up_category + "," + up_url + "," + up_text + "," + down_item + "," + down_category + "," + down_url + "," + down_text + '\n'
            with open(POG_path, 'a') as file:
                file.write(data)
            break
        filelist.close()



    sum = sum + 1
    if sum > 599999:
        break