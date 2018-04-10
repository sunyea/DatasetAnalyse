数据集采集，分析和机器学习
==

# 1. 概述
本应用分三个部分独立运行，但数据流自上而下：采集系统从网络爬取原始数据，分析系统对原始数据进行分析和清洗，生成新的适合机器学习的数据集，机器学习系统通过原始数据进行建模学习，达到预测效果并生成分析结果。<br>
由于数据集很小，不适合深度学习模型，所以本应用采用传统ML学习模型完成，主要是为了探讨数据采集、清洗与分析的原理和流程。
## 1.1. 实验数据
本应用实验数据来自 http://www.51job.com 的数据，采用Scrapy框架搭建爬虫获取数据，为了实验方便，只检索关键字为"人工智能+机器学习+算法"的信息。
## 1.2. 开发环境
软件环境：Python 3.6 (Anaconda3)<br>
开发工具：PyCharm Edu版<br>
依赖包：scarpy,web.py,matplotlib,sklearn等

# 2. 数据采集
采集系统采用Scrapy框架完成，采集数据结构定义于getdata/getdata/items.py文件，爬虫定义于getdata/getdata/spiders/spider.py文件<br>
数据采集后存储于data目录下
## 2.1. 运行方式
在getdata目录下运行
```Bash
python run_getdata.py
```
## 2.2. 数据文件
文件存放在getdata/data目录下，采用:::对数据进行分割，保存为csv文件，第一行为字段名

# 3. 数据分析
分析系统使用web.py构建分析UI，使用者通过浏览器打开操作界面。
## 3.1. 运行方式
在analyse目录下运行
```Bash
python run_analyse.py 5050
```
然后在浏览器中输入 http://localhost:5050/ 即可访问到操作界面
![home](https://github.com/sunyea/DatasetAnalyse/raw/master/analyse/static/images/home.PNG)
![index](https://github.com/sunyea/DatasetAnalyse/raw/master/analyse/static/images/index.PNG)
## 3.2. 数据质量分析
![hiatus](https://github.com/sunyea/DatasetAnalyse/raw/master/analyse/static/images/hiatus.png)
## 3.3. 数据特征分析
![fb](https://github.com/sunyea/DatasetAnalyse/raw/master/analyse/static/images/fb.png)
## 3.4. 属性处理方式
![cl](https://github.com/sunyea/DatasetAnalyse/raw/master/analyse/static/images/cl.png)
## 3.5. 生成新数据
![gen](https://github.com/sunyea/DatasetAnalyse/raw/master/analyse/static/images/gen.png)
