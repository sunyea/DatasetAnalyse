import web
from web.contrib.template import render_jinja

from utils import Project
from data import app_data
from handler import app_handler

render = render_jinja('templates', encoding='utf-8')
P = Project()

urls = ('/data', app_data
        ,'/handler', app_handler
        ,'/', 'index'
        ,'/project/(\w+)', 'project'
        ,'/analyse/(\w+)', 'analyse')

class index():
    def GET(self):
        return render.index(projects=P.list())

class project():
    def POST(self, control):
        if control == 'new':
            form = web.input()
            return P.add(form)
        elif control == 'del':
            form = web.input()
            return P.delete(form.proid)

class analyse():
    def GET(self, proid):
        return render.main(project=P.get(proid))

app = web.application(urls, locals())
if __name__ == '__main__':
    app.run()


