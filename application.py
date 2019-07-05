from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os
from common.models import db


# 定义一个类 做按需分离
class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=None)
        self.config.from_pyfile('config/base_setting.py')

        # 动态设置加载
        if 'ops_config' in os.environ:
            self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])

        db.init_app(self)


# db = SQLAlchemy()
# app = False(__name__)
# db = SQLAlchemy(app)
app = Application(__name__, template_folder=os.getcwd() + '/web/templates/', root_path=os.getcwd())
manager = Manager(app)

'''
函数模板 注入
'''
from common.libs.UrlManager import UrlManager

app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildImage, 'buildImage')
