import urllib.request, sys, base64, json, os, time, baiduSearch
from PIL import Image
from aip import AipOcr
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

driver = webdriver.Chrome("./chromedriver.exe")
# 访问百度
driver.get('http://www.baidu.com')


'''

显示颜色格式：\033[显示方式;字体色;背景色m......[\033[0m]

-------------------------------------------
字体色     |       背景色     |      颜色描述
-------------------------------------------
30        |        40       |       黑色
31        |        41       |       红色
32        |        42       |       绿色
33        |        43       |       黃色
34        |        44       |       蓝色
35        |        45       |       紫红色
36        |        46       |       青蓝色
37        |        47       |       白色
-------------------------------------------
-------------------------------
显示方式     |      效果
-------------------------------
0           |     终端默认设置
1           |     高亮显示
4           |     使用下划线
5           |     闪烁
7           |     反白显示
8           |     不可见
-------------------------------
'''
def addColor(text, fontcolor, backcolor):
    return "\033[1;" + str(fontcolor) + ";" + str(backcolor) + "m" + text + "\033[0m"


start = time.time()
startx = time.time()

os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
os.system("adb pull /sdcard/screenshot.png ./screenshot.png")

""" （百度ocr）你的 APPID AK SK """
APP_ID = '你的key'
API_KEY = '你的key'
SECRET_KEY = '你的 secret_key'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

im = Image.open(r"./screenshot.png")

img_size = im.size
w = im.size[0]
h = im.size[1]
print("img size :{}".format(img_size))

print(addColor('截图获取图片用时：' + str(time.time() - start) + '秒\n', 34, 0))
start = time.time()

region = im.crop((70, 420, w - 70, 1400))  # 裁剪的区域
region.save(r"./crop_q.png")


# top_start = 732
# itme_hight = 190
# interval = 25
#
# for i in range(3):
# region1 = im.crop((
#         70,
#         top_start + itme_hight * i + interval * i,
#         w - 70,
#         top_start + itme_hight * (i+1) + interval * i
#     ))  # 裁剪的区域
#     region1.save(r"./crop_a"+str(i+1)+".png")


print(addColor('裁剪图片用时：' + str(time.time() - start) + '秒\n', 34, 0))
start = time.time()

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content(r"./crop_q.png")
respon = client.basicGeneral(image)
titles = respon['words_result']  # 获取问题

q = titles[0]['words']
a1 = titles[1]['words']
a2 = titles[2]['words']
a3 = titles[3]['words']

print(addColor('OCR识别用时：' + str(time.time() - start) + '秒\n', 34, 0))
start = time.time()

print(addColor("========================== ORC识别内容 ============================== ", 36, 0))
print(addColor("问题", 33, 0))
print(q)  # 打印问题
print(addColor("答案", 31, 0))

print(a1)
print(a2)
print(a3)

keyword = q  # 识别的问题文本

driver.find_element_by_id('kw').send_keys(Keys.CONTROL, 'a')
driver.find_element_by_id('kw').send_keys(Keys.BACK_SPACE)
driver.find_element_by_id('kw').send_keys(keyword)
driver.find_element_by_id('su').send_keys(Keys.ENTER)

convey = 'n'

if convey == 'y' or convey == 'Y':
    results = baiduSearch.search(keyword, convey=True)
elif convey == 'n' or convey == 'N' or not convey:
    results = baiduSearch.search(keyword)
else:
    print('输入错误')
    exit(0)
count = 0

print(addColor("========================== 搜索结果 ==============================", 36, 0) + " \n")
r_txt = ''
for result in results:
    r = '{0}'.format(result.abstract)
    r_txt = r_txt + r
    print(r)  # 此处应有格式化输出
    count = count + 1
    if (count > 20):
        break

len_a1 = len(re.findall(a1, r_txt))
len_a2 = len(re.findall(a2, r_txt))
len_a3 = len(re.findall(a3, r_txt))

if (len_a1 < 1):
    len_a1 = len(re.findall(a1[:-1], r_txt))

if (len_a2 < 1):
    len_a2 = len(re.findall(a2[:-1], r_txt))

if (len_a3 < 1):
    len_a3 = len(re.findall(a3[:-1], r_txt))

r = dict()
r[a1] = len_a1
r[a2] = len_a2
r[a3] = len_a3

print(addColor("========================== 统计 ==============================", 32, 0))

print(addColor(a1, 34, 0) + " 出现次数: " + addColor(str(len_a1), 31, 0))
print(addColor(a2, 34, 0) + " 出现次数: " + addColor(str(len_a2), 31, 0))
print(addColor(a3, 34, 0) + " 出现次数: " + addColor(str(len_a3), 31, 0))

print("\n")
print(addColor('总用时：' + str(time.time() - startx) + '秒', 33, 0))

time.sleep(30)

