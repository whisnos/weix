from werkzeug.utils import secure_filename

from application import app, db
from common.libs.Helper import geneTime
import os, stat, uuid
from common.models.Images import Image


class UploadService():
    @staticmethod
    def uploadByFile(file):
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1]
        # 取出上传文件的扩展名
        if ext not in app.config['UPLOAD']['ext']:
            resp['code'] = -1
            resp['msg'] = '不允许的扩展类型文件'
            return resp
        print('app.root_path', app.root_path)  # D:\Flask\weix + '/web/static/upload/'
        root_path = app.root_path + app.config['UPLOAD']['prefix_path']  # 获取绝对路径
        file_dir = geneTime("%Y%m%d")
        save_dir = root_path + file_dir  # 上传一个时间的 目录
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)  # 赋权限
        file_name = str(uuid.uuid4()).replace('-', '') + '.' + ext
        file.save("{0}/{1}".format(save_dir, file_name))  # 调用此方法 可直接进行保存
        resp['data'] = {
            'file_key': file_dir + '/' + file_name
        }
        model_image = Image()
        model_image.file_key = file_dir + '/' + file_name
        model_image.created_time = geneTime()
        db.session.add(model_image)
        db.session.commit()
        return resp
