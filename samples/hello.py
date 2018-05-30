from web_python_2018_04_ht04_framework import route, response, response_with_json, response_with_jinja2


@route('/', methods=['GET', 'POST'], strict=True)
def root(request):
    return '<html><head></head><body><p>This is index page</p></body></html>'

@route('/foo(.+).*', methods=['GET'])
def foo(request, arg1):
    return 'FOO'+str(request.GET)+str(request.POST)+str(arg1)

@route('/dump/', methods=['GET', 'POST'])
def dump(request):
    return response(str(request.GET)+str(request.POST))

@route('/json/', methods=['GET'])
def json(request):
    return response_with_json({'kind': 'stone'})

@route('/jinja/', methods=['GET'])
def jinja(request):
    return response_with_jinja2('samples/simple.jinja2', answer='All right')
