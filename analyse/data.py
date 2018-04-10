import web
import pandas as pd
from web.contrib.template import render_jinja
import matplotlib.pyplot as plt
import numpy as np


from utils import Project
from utils import HandlerConfig

render = render_jinja('templates', encoding='utf-8')
P = Project()

urls = ('/info/(\w+)', 'info'
        ,'/hiatus/(\w+)', 'hiatus'
        ,'/unusual/(\w+)', 'unusual'
        ,'/distribution/(\w+)', 'distribution'
        ,'/settings/(\w+)', 'settings'
        ,'/precondition/(\w+)', 'precondition')

class info():
    '''
    项目信息概要
    项目名、数据文件、数据时间、描述
    显示前10条数据
    '''
    def GET(self, proid):
        this_proj = P.get(proid)
        df = pd.read_csv(this_proj['filename'], sep=':::', engine='python', encoding='utf-8')
        df10 = df.iloc[:10, :]
        return render.proj_info(project=this_proj, columns=list(df.columns), data=list(df10.to_dict('index').values()))

class hiatus():
    '''
    缺失值分析
    '''
    def GET(self, proid):
        this_proj = P.get(proid)
        df = pd.read_csv(this_proj['filename'], sep=':::', engine='python', encoding='utf-8')
        columns = list(df.columns)
        df = df.isnull()
        piesize = dict()
        for column in columns:
            b = list(df[column].value_counts())
            if len(b) > 1:
                isfalse = int(b[0])
                istrue = int(b[1])
            else:
                isfalse = int(b[0])
                istrue = 0
            size = dict()
            size['count'] = str(isfalse+istrue)
            size['hiatus'] = str(istrue)
            size['percent'] = '{:.2f}'.format((istrue/(istrue+isfalse))*100)
            piesize[column] = size
        handler = HandlerConfig(proid)
        configs = handler.getHiatus()
        return render.proj_hiatus(proid=proid, columns=columns, piesize=piesize, configs=configs)

class unusual():
    '''
    异常值处理
    '''
    def GET(self, proid):
        this_proj = P.get(proid)
        df = pd.read_csv(this_proj['filename'], sep=':::', engine='python', encoding='utf-8')
        columns = list(df.columns)
        return render.proj_unusual(proid=proid, columns=columns)

class distribution():
    '''
    分布分析
    '''
    def GET(self, proid):
        this_proj = P.get(proid)
        df = pd.read_csv(this_proj['filename'], sep=':::', engine='python', encoding='utf-8')
        columns = list(df.columns)
        return render.proj_distribution(proid=proid, columns=columns)
    def POST(self, proid):
        this_proj = P.get(proid)
        df = pd.read_csv(this_proj['filename'], sep=':::', engine='python', encoding='utf-8')
        columns = list(df.columns)
        form = dict(web.input())
        #绘制分布图
        plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
        plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(15, 7)
        fig.tight_layout(w_pad=10)
        #数据
        datalist = dict(df[form['column']].value_counts())
        sorted(datalist.items(), key=lambda x: x[1], reverse=True)
        labels = list(datalist.keys())
        labels = [x[:6] for x in labels]
        values = list(datalist.values())
        data_sum = sum(values)
        values2 = [x/data_sum for x in values]
        top = 0
        if 'top' in form.keys():
            if form['top'].strip() != '':
                top = int(form['top'])
        if top > 0:
            labels = labels[:top]
            labels.append('其它')

            other_sum = sum(values[top:])
            values = values[:top]
            values.append(other_sum)

            other_sum2 = sum(values2[top:])
            values2 = values2[:top]
            values2.append(other_sum2)
        #饼图
        explode = np.zeros(len(labels), dtype=np.float16)
        explode[-1] = 0.1
        ax1.set_aspect(1)
        ax1.pie(values2, labels=labels, autopct='%1.2f%%', explode=explode, startangle = 90, shadow=True)
        #条图
        # ax2.set_aspect(10)
        ax2.bar(labels, values)
        plt.xticks(rotation=17)
        img_path = 'static/images/{}_{}_distr.jpg'.format(proid, form['column'])
        plt.savefig(img_path)
        #绘制结束
        #获取配置
        handler = HandlerConfig(proid)
        config = handler.getDistribution()
        return render.proj_distribution_show(proid=proid, columns=columns, img=img_path, form=form, config=config)

class settings():
    def GET(self, proid):
        this_proj = P.get(proid)
        df = pd.read_csv(this_proj['filename'], sep=':::', engine='python', encoding='utf-8')
        columns = list(df.columns)
        row = list(df.iloc[0, :])
        data = dict(zip(columns, row))
        handler = HandlerConfig(proid)
        configs = handler.getSettings()
        return render.proj_settings(proid=proid, data=data, configs=configs)

class precondition():
    def GET(self, proid):
        handler = HandlerConfig(proid)
        configs = handler.getAllConfig()
        return render.proj_precondition(proid=proid, configs=configs)

app_data = web.application(urls, locals())
