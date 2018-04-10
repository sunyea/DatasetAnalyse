import xml.etree.ElementTree as ET
import os
import json
import time


class Project():
    '''
    项目类，关于项目信息的操作
    '''
    projectFile = None

    def __init__(self, filename='projects.xml'):
        self.projectFile = filename

    #通过项目编号获取项目信息
    def get(self, proid):
        tree = ET.parse(self.projectFile)
        root = tree.getroot()
        projects = root.findall('project')
        this_proj = dict()
        for project in projects:
            pro_id = project.find('proid').text.strip()
            if pro_id == proid:
                this_proj['proid'] = proid
                this_proj['name'] = project.find('name').text.strip()
                this_proj['filename'] = project.find('filename').text.strip()
                this_proj['datetime'] = project.find('datetime').text.strip()
                this_proj['info'] = project.find('info').text
                break
        return this_proj

    #获取全部项目信息
    def list(self):
        tree = ET.parse(self.projectFile)
        root = tree.getroot()
        projects = list()
        for item in root.findall('project'):
            project = dict()
            project['proid'] = item.find('proid').text.strip()
            project['name'] = item.find('name').text.strip()
            project['filename'] = item.find('filename').text.strip()
            project['datetime'] = item.find('datetime').text.strip()
            project['info'] = item.find('info').text
            projects.append(project)
        return projects

    #新添项目信息
    def add(self, project):
        filename = project.filename
        #判断数据文件是否存在
        if not os.path.exists(filename):
            return json.dumps({'code': 1, 'msg': '文件不存在，请保证文件名正确'})
        #获取文件创建日期
        t = os.path.getctime(filename)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

        #写入xml文件
        tree = ET.parse(self.projectFile)
        root = tree.getroot()

        tag_pro = ET.Element('project')
        tag_proid = ET.Element('proid')
        tag_proid.text = time.strftime('%Y%m%d%H%M%S', time.localtime())
        tag_name = ET.Element('name')
        tag_name.text = project.name
        tag_filename = ET.Element('filename')
        tag_filename.text = filename
        tag_datetime = ET.Element('datetime')
        tag_datetime.text = date
        tag_info = ET.Element('info')
        tag_info.text = project.info

        tag_pro.append(tag_proid)
        tag_pro.append(tag_name)
        tag_pro.append(tag_filename)
        tag_pro.append(tag_datetime)
        tag_pro.append(tag_info)

        root.append(tag_pro)
        tree.write(self.projectFile)
        return json.dumps({'code': 0, 'msg': '添加成功'})

    #删除项目信息
    def delete(self, proid):
        tree = ET.parse(self.projectFile)
        root = tree.getroot()
        projects = root.findall('project')
        for project in projects:
            pro_id = project.find('proid').text.strip()
            if pro_id == proid:
                root.remove(project)
                break
        tree.write(self.projectFile)
        return json.dumps({'code': 0, 'msg': '删除成功！'})

class HandlerConfig():
    configFile = None

    dict_hiatus = {'0': '不处理', '1': '插入固定值', '2': '上个值', '3': '下个值', '4': '平均值', '5': '删除行'}
    dict_distribution = {'0': '不处理', '1': '靠后归为其它', '2': '通过聚类划分'}
    dict_settings = {'0': '不处理', '1': '去除', '2': '正则转换', '3': '聚类', '4': '离散化'}

    def __init__(self, proid):
        self.configFile = 'projects/'+proid+'_config.xml'
        if not os.path.exists(self.configFile):
            with open(self.configFile, 'w', encoding='utf-8') as f:
                f.write('<config_all></config_all>')

    #保存到xml文件
    def _saveXml(self, tag, column, handler, text):
        tree = ET.parse(self.configFile)
        root = tree.getroot()
        ele = root.find(tag)
        if ele is None:
            ele = ET.Element(tag)
            root.append(ele)
        tag_column = ele.find(column)
        if tag_column is None:
            tag_column = ET.Element(column)
            ele.append(tag_column)
        if handler == '0':
            ele.remove(tag_column)
        else:
            tag_column.set('handler', handler)
            tag_column.text = text
        tree.write(self.configFile)
    #从xml文件中读取
    def _getXml(self, tag):
        tree = ET.parse(self.configFile)
        root = tree.getroot()
        ele = root.find(tag)
        columns = dict()
        if ele is None:
            return columns
        for column in ele:
            columns[column.tag] = [column.get('handler'), column.text]
        return columns

    #保存缺失配置
    def saveHiatus(self, form):
        self._saveXml('hiatus', form.column, form.handler, form.value)
        return json.dumps({'code': 0, 'msg': '保存成功'})

    #获取缺失配置
    def getHiatus(self):
        return self._getXml('hiatus')

    #保存分布配置
    def saveDistribution(self, form):
        self._saveXml('distribution', form.column, form.handler, form.value)
        return json.dumps({'code': 0, 'msg': '保存成功'})

    #获取分布配置
    def getDistribution(self):
        return self._getXml('distribution')

    #保存属性处理配置
    def saveSettings(self, form):
        self._saveXml('settings', form.column, form.handler, form.value)
        return json.dumps({'code': 0, 'msg': '保存成功'})
    #获取属性处理配置
    def getSettings(self):
        return self._getXml('settings')

    #获取所有处理配置
    def getAllConfig(self):
        tree = ET.parse(self.configFile)
        root = tree.getroot()
        columns = dict()
        for ele in root:
            for column in ele:
                handler = '处理方式：'
                if ele.tag == 'hiatus':
                    handler += self.dict_hiatus[column.get('handler')]
                elif ele.tag == 'distribution':
                    handler += self.dict_distribution[column.get('handler')]
                elif ele.tag == 'settings':
                    handler += self.dict_settings[column.get('handler')]
                values = '' if column.text is None else '参数：'+column.text
                if column.tag in columns.keys():
                    columns[column.tag].append(handler+','+values)
                else:
                    columns[column.tag] = [handler+','+values]
        return columns



