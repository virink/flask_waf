# -*- coding: utf-8 -*-
"""
    Flask_Waf
    ---------

    Adds server Waf support to your application for CTFer.

    :copyright: (c) 2018 by Virink
    :license: BSD, see LICENSE for more details.

    Usage:

        from flask_waf import Waf

        app = Flask(__name__)
        Waf(app)
"""

__version__ = '1.0.0'

import os
import sys
import json
import linecache
from flask import request

ISPY3 = True if sys.version_info >= (3, 0) else False


class MyResponse(Response):

    def __init__(self, res, **kwargs):
        # Fake just for ctfer~
        if 'flag' in res:
            # TODO do more for this
            res = res.replace("flag", "virink")
        kwargs['headers'] = {
            'X-Waf-By': 'FlaskWaf %s' % __version__}
        return super(MyResponse, self).__init__(res, **kwargs)


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if ISPY3 and isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return obj


def tail(filename, taillines=20):
    linecache.clearcache()
    res = linecache.getlines(filename)[-taillines:]
    return "[%s]" % ','.join(res)


def get_request(req):
    res = {}
    # files
    if req.files:
        res['files'] = dict(req.files)
        res['_files'] = {}
        for f in res['files']:
            res['_files'].update({f: []})
            fp = res['files'][f]
            for file in fp:
                data = file.stream.read()
                if len(data) <= 1024:
                    res['_files'][f].append(data)
                file.stream.truncate(6)
                file.stream.seek(0)
                file.stream.write(b"virink\n")
                file.stream.flush()
                file.stream.seek(0)
    # files end
    res['headers'] = dict(req.headers)
    if 'cookies' in res['headers'].keys():
        res['headers'].pop('cookies')
    res['authorization'] = req.authorization
    res['method'] = req.method
    res['scheme'] = req.scheme
    res['host'] = req.host
    res['url'] = req.url
    res['path'] = req.path
    res['query'] = req.query_string
    res['cookies'] = req.cookies
    res['remote_addr'] = req.remote_addr
    res['data'] = req.data
    res['form'] = dict(req.form)
    return res


def waf_init_utils(app, waf_log_dir):

    @app.before_request
    def flask_waf_log():
        if request.path != '/waflog':
            res = get_request(request)
            # TODO Scan and intercept the evil data
            # Zi ji dong shou, feng yi zu shi
            # Zi ji dong shou, feng yi zu shi
            # Zi ji dong shou, feng yi zu shi
            # ( Important things are to be repeated for 3 times. )
            with open("%s/log.log" % waf_log_dir, 'a+') as f:
                f.write(json.dumps(res, cls=MyEncoder) + '\n')
                f.flush()

    @app.before_request
    def flask_watch_log():
        print(request.path)
        if request.path == '/waflog':
            argv = request.args.get("line", 20)
            res = tail("%s/log.log" % waf_log_dir, argv)
            # TODO make beautiful UI
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
