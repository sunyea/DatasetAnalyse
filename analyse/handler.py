import web
import pandas as pd
import json

from utils import HandlerConfig
from utils import Project
from class_kmeans import ClassKMeans

urls = ('/hiatus/(\w+)', 'HandHiatus'
        ,'/unusual/(\w+)', 'HandUnusual'
        ,'/distribution/(\w+)', 'HandDistribution'
        ,'/settings/(\w+)', 'HandSettings'
        ,'/p_hiatus/(\w+)', 'ParseHiatus'
        ,'/p_distribution/(\w+)', 'ParseDistribution'
        ,'/p_settings/(\w+)', 'ParseSettings')

class HandHiatus():
    def POST(self, parm):
        parms = parm.split('_')
        control = parms[0]
        proid = parms[1]
        handler = HandlerConfig(proid)
        form = web.input()
        if control == 'set':
            return handler.saveHiatus(form)
        else:
            return 0

class HandUnusual():
    def POST(self, proid):
        P = Project()
        this_proj = P.get(proid)
        df = pd.read_csv(this_proj['filename'], engine='python', encoding='utf-8')
        form = web.input()
        dd = dict(df[form['column']].describe())
        for k, v in dd.items():
            v_type = str(type(v))
            if 'int' in v_type.lower():
                dd[k] = int(v)
            elif 'float' in v_type.lower():
                dd[k] = float(v)
        return json.dumps(dd)

class HandDistribution():
    def POST(self, proid):
        handler = HandlerConfig(proid)
        form = web.input()
        return handler.saveDistribution(form)

class HandSettings():
    def POST(self, proid):
        handler = HandlerConfig(proid)
        form = web.input()
        return handler.saveSettings(form)

#处理缺失值
class ParseHiatus():
    def POST(self, proid):
        form = web.input()
        filename = form.filename
        column = form.column
        handler = form.handler
        value = form.value
        df = pd.read_csv(filename, engine='python', encoding='utf-8')
        if handler == '1':
            #插入固定值
            df[column].fillna(value)
        elif handler == '2':
            #上个值
            df[column].ffill()
        elif handler == '3':
            #下个值
            df[column].bfill()
        elif handler == '4':
            df[column].dropna(axis=0)
        df.to_csv(filename, index=False, encoding='utf-8')
        return json.dumps({'code': 0})

#处理属性特征值
class ParseDistribution():
    def POST(self, proid):
        form = web.input()
        filename = form.filename
        column = form.column
        handler = form.handler
        value = form.value
        df = pd.read_csv(filename, engine='python', encoding='utf-8')
        if handler == '1':
            #靠后归为其它类
            datalist = dict(df[column].value_counts())
            sorted(datalist.items(), key=lambda x: x[1], reverse=True)
            top = int(value)
            labels = list(datalist.keys())
            labels = labels[:top]
            df[column] = df[column].map(lambda x: x if x in labels else '其它')
        elif handler == '2':
            #通过聚类划分
            df = df.applymap(lambda x: x if x == x else 'null') #替换NaN的数据项
            c_kmens = ClassKMeans()
            df[column] = c_kmens.newClass(df[column], k=int(value))
        df.to_csv(filename, index=False, encoding='utf-8')
        return json.dumps({'code': 0})

#按设置处理属性值
class ParseSettings():
    def POST(self, proid):
        return json.dumps({'code': 0})

app_handler = web.application(urls, locals())
