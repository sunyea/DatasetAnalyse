import web
import pandas as pd
import json

from utils import HandlerConfig
from utils import Project

urls = ('/hiatus/(\w+)', 'HandHiatus'
        ,'/unusual/(\w+)', 'HandUnusual'
        ,'/distribution/(\w+)', 'HandDistribution'
        ,'/settings/(\w+)', 'HandSettings')

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
        df = pd.read_csv(this_proj['filename'], sep=':::', engine='python', encoding='utf-8')
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

app_handler = web.application(urls, locals())
