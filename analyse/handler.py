import web
import pandas as pd
import json
import re
import numpy as np

from utils import HandlerConfig
from utils import Project
from class_kmeans import ClassKMeans
from class_kmeans import ClassValues

urls = ('/hiatus/(\w+)', 'HandHiatus'
        ,'/unusual/(\w+)', 'HandUnusual'
        ,'/distribution/(\w+)', 'HandDistribution'
        ,'/settings/(\w+)', 'HandSettings'
        ,'/p_hiatus/(\w+)', 'ParseHiatus'
        ,'/p_distribution/(\w+)', 'ParseDistribution'
        ,'/p_settings/(\w+)', 'ParseSettings'
        ,'/finally/(\w+)', 'Finally')

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
        form = web.input()
        filename = form.filename
        column = form.column
        handler = form.handler
        value = form.value
        df = pd.read_csv(filename, engine='python', encoding='utf-8')
        if handler == '1':
            #去除该属性
            df = df.drop([column], axis=1)
        elif handler == '2':
            #正则转换
            def split_column(col):
                if col is None:
                    return None
                if col != col:
                    return None
                reg_column = re.search(value, col)
                if reg_column is None:
                    return None
                new_col = list()
                for c in reg_column.groups():
                    new_col.append(c)
                return new_col
            df[column] = df[column].apply(split_column)
            num = len(df[column][0])
            for i in range(num):
                df.insert(i, column+'_'+str(i), df[column])
                df[column+'_'+str(i)] = df[column+'_'+str(i)].apply(lambda x: None if x is None else x[i])
            df = df.drop([column], axis=1)
        elif handler == '3':
            #离散映射
            class_values = ClassValues('{}_{}'.format(proid, column))
            df[column] = class_values.getClass(df[column], list(df[column].unique()))
        elif handler == '4':
            #One-Hot
            pass

        df.to_csv(filename, index=False, encoding='utf-8')
        return json.dumps({'code': 0})

#自定义函数处理特殊属性
class Finally():
    def POST(self, proid):
        form = web.input()
        filename = form.filename
        df = pd.read_csv(filename, engine='python', encoding='utf-8')
        #这里为自定义处理特殊属性
        #---自定义1：统一工资单位为"万/年"，删除单位属性
        unit = df['job_pay_2']
        min = df['job_pay_0']
        max = df['job_pay_1']
        min_i = np.zeros(min.shape)
        max_i = np.zeros(max.shape)
        for i, v in unit.items():
            if min[i] is not None:
                min_i[i] = float(min[i])
            if max[i] is not None:
                max_i[i] = float(max[i])
            if v is None:
                continue
            if v != v:
                continue
            if '千' in v:
                min_i[i] /= 10
                max_i[i] /= 10
            if '月' in v:
                min_i[i] *= 12
                max_i[i] *= 12
        df.insert(0, 'job_pay_min', min_i)
        df.insert(1, 'job_pay_max', max_i)
        df = df.drop(['job_pay_0','job_pay_1','job_pay_2'], axis=1)
        #自定义处理结束
        df.to_csv(filename, index=False, encoding='utf-8')
        return json.dumps({'code': 0})

app_handler = web.application(urls, locals())
