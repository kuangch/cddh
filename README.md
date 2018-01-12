## 冲顶大会
适合问题和答案都比较直接的题目

## 环境
python3.6+，window，android手机（需要adb驱动，自行准备）

## 安装依赖
```bash
pip3 install -r requirements.txt
```

## 申请百度OCR/汉王OCR/阿里OCR Key
[申请地址](http://ai.baidu.com)

替换你的api key
```python
APP_ID = '你的id'
API_KEY = '你的key'
SECRET_KEY = '你的secret_key'
```

## 使用

每次出现题目的时候运行：
```bash
python cddh.py
```

## 效果

截图
![image](https://github.com/kuangch/cddh/blob/master/screenshot.png)
裁剪
![image](https://github.com/kuangch/cddh/blob/master/crop_q.png)
结果
![image](https://github.com/kuangch/cddh/blob/master/result.png)