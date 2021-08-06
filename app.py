#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/8/2 13:17
# @Author   : ReidChen
# Document  : 启动文件

from flaskr import create_app, jsonify
from flaskr.BaseError import BaseError,OrmError,ValidationError,NotFoundError,FormError
import os

app = create_app()

if __name__ == '__main__':
    
    @app.errorhandler(BaseError)
    def custom_error_handler(e):
        if e.level in [BaseError.LEVEL_WARN, BaseError.LEVEL_ERROR]:
            if isinstance(e, OrmError):
                app.logger.exception('%s %s' % (e.parent_error, e))
            else:
                app.logger.exception('错误信息: %s %s' % (e.extras, e))
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        return response
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='172.18.0.202', port=port)
