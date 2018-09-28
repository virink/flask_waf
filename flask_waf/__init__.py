# -*- coding: utf-8 -*-
"""
    Flask_Waf
    ---------

    Adds server Waf support to your application for CTFer.

    :copyright: (c) 2018 by Virink
    :license: BSD, see LICENSE for more details.
"""

__version__ = '0.0.1'

import os
import sys
import json
import linecache
from flask import request

ISPY3 = True if sys.version_info >= (3, 0) else False


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if ISPY3 and isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return obj


def tail(filename, taillines=20):
    res = []

    def get_line_count(filename):
        line_count = 0
        with open(filename, 'r+') as file:
            while True:
                buffer = file.read(8192 * 1024)
                if not buffer:
                    break
                line_count += buffer.count('\n')
        return line_count

    line_count = get_line_count(filename)
    print("line count: %d" % line_count)
    linecache.clearcache()
    for i in range(taillines):
        last_line = linecache.getline(filename, line_count)
        res.append(last_line)
        line_count -= 1
    return '<br>'.join(res)


def waf_init_utils(app, waf_log_dir):

    @app.before_request
    def flask_waf_log():
        if request.path != '/waflog':
            res = {}
            res['url'] = request.url
            res['remote_addr'] = request.remote_addr
            res['query'] = request.query_string
            # TODO Zi ji dong shou, feng yi zu shi
            with open("%s/log.log" % waf_log_dir, 'a+') as f:
                f.write(json.dumps(res, cls=MyEncoder) + '\n')
                f.flush()

    @app.before_request
    def flask_watch_log():
        print(request.path)
        if request.path == '/waflog':
            res = tail("%s/log.log" % waf_log_dir)
            return res


class Waf(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = app.config.copy()
        # WAF_LOG_DIR
        config.setdefault('WAF_LOG_DIR', './log')
        waf_log_dir = config.get('WAF_LOG_DIR')
        if not os.path.exists(waf_log_dir):
            os.mkdir(waf_log_dir)

        with app.app_context():
            waf_init_utils(app, waf_log_dir)
