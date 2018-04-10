数据集采集，分析和机器学习
==

# 1. 概述
本应用分三个部分独立运行，但数据流自上而下：采集系统从网络爬取原始数据，分析系统对原始数据进行分析和清洗，生成新的适合机器学习的数据集，机器学习系统通过原始数据进行建模学习，达到预测效果并生成分析结果。<br>
根据中文数据集特性：<br>
对类别繁多、分布均匀的类别属性进行中文切词并Kmeans聚类，然后再进行离散映射为数值分类。<br>
对类别繁多、分布不均匀的属性，将众多小类别归为一类进，然后再映射为数值分类。<br>
对中文内容繁多的信息类属性，提取多个关键字，将关键字汇总并聚类，通过对关键字进行One-Hot编码，分析关键字对因变量的影响权重。
## 1.1. 实验数据
本应用实验数据来自 http://www.51job.com 的数据，采用Scrapy框架搭建爬虫获取数据。
## 1.2. 开发环境
软件环境：Python 3.6 (Anaconda)<br>
开发工具：PyCharm<br>
依赖包：scikit-learn, pandas, matplotlib, scrapy, web.py, jinja2, jieba等<br>
前端依赖：Layui, JQuery

# 2. 数据采集
采集系统采用Scrapy框架完成，数据采集后存储于data目录下
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
