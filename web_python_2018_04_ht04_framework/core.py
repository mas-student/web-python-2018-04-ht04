# -*- coding: utf8 -*-


import os
import json
from collections import namedtuple
import re
import traceback
from http.client import responses
from jinja2 import Template


Request = namedtuple('Request', 'GET POST')
Url = namedtuple('Url', 'pattern methods callback')
Target = namedtuple('Target', 'callback args kwargs')
Response = namedtuple('Response', 'status_code reason_phrase headers message_body')


### API ###

def response(body, status=200, headers=None):
    if headers is None:
        headers = {}

    return make_response(status, None, headers, body)

def response_with_json(obj):
    return response(json.dumps(obj), headers={'Content-Type': 'application/json'})

def response_with_jinja2(filename, **kwargs):
    return response(render(filename, **kwargs))

def route(path, method, urls):
    if not path.endswith('/'):
        return response301(path, path + '/')

    for url in urls:
        m = re.match(url.pattern, path)

        if m:
            if url.methods is not None and method not in url.methods:
                return response405(path, method)
            return Target(url.callback, m.groups(), None)

    return response404(path)

#########

_application = {}

def add_url(url, methods=None, strict=False):
    if methods is None:
        methods = ['GET']

    def dec(func):
        global _application
        pattern = url
        if strict:
            pattern = '^' + url + '$'
        _application.setdefault('urls', []).append(Url(pattern, methods, func))

    return dec

def render(filename, **kwargs):
    template = Template(open(filename).read())
    return template.render(**kwargs)

def getApp():
    global _application
    return _application

def loadModule(path):
    import imp
    try:
        module = imp.load_source('module', path)
    except IOError:
        return None
    return module


def plain_to_html(text):
    return text.replace('\n', '</br>').replace(' ', '&nbsp;')

def make_response(status_code, reason_phrase, headers, message_body):
    if reason_phrase is None:
        reason_phrase = responses.get(status_code, 'Default reason phrase')
    if headers is None:
        headers = {'Content-Type': 'text/html'}

    message_body = message_body

    return Response(status_code, reason_phrase, list(headers.items()), message_body)

def response301(src, dst):
    return make_response(301, None, {'Location': dst}, 'Moved from {src} to {dst}'.format(src=src, dst=dst))

def response200(body):
    return make_response(200, None, None, body)

def response404(path):
    return make_response(404, None, None, plain_to_html('404 Not found {}'.format(path)))

def response405(path, method):
    msg = '''\
405 Method Not Allowed
path = {}
method = {}'
'''.format(path, method)
    return make_response(405, None, None, msg)

def response500(e, exc):
    msg = '''\
500 Internal Server Error: 
{}: {} 

{}
'''.format(type(e).__name__, str(e), str(exc))
    return make_response(500, None, None, msg)


def get_store():
    global _application
    return _application

def make_get(env):
    return dict([pair.split('=') for pair in env['QUERY_STRING'].split('&') if '=' in pair])

def make_post(env):
    return dict([line.split('=') for line in env['wsgi.input'].read().split('&')])

def execute(target, request):
    ##### Вызов контроллера #####
    try:
        return target.callback(request, *target.args)

    except Exception as e:
        return response500(e, traceback.format_exc())
    ##### #####

def send_response(response, start_response):
    starting_line = '{} {}'.format(response.status_code, response.reason_phrase)
    start_response(starting_line, response.headers)
    return response.message_body.encode('utf-8')

def process(env, start_response):
    global _application

    path = env['PATH_INFO']
    method = env['REQUEST_METHOD']

    store = get_store()
    target = None
    if 'urls' in store:
        target = route(path, method, store['urls'])

    if type(target) is Response:
        return send_response(target, start_response)

    get = make_get(env)
    post = {}
    if method == 'POST':
        post = make_post(env)

    request = Request(get, post)

    response = execute(target, request)

    if type(response) is Response:
        return send_response(response, start_response)

    elif isinstance(response, str):
        return send_response(response200(response), start_response)

    else:
        response = response500(TypeError('Incorrect response type {}'.format(type(response))), traceback.format_exc())
        return send_response(response, start_response)

def run_application(env, start_response, framework_app=None):
    if framework_app is None:
        framework_app = os.environ['FRAMEWORK_APP']

    app = loadModule(framework_app)

    if not app:
        return send_response(response500('Application "{}" not found'.format(framework_app)))

    return process(env, start_response)