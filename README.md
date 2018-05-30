# Framework

Framework is the python framework for uwsgi framework

## Prerequisites

### OS

Ubuntu LTS version will be enough.

### Python

```
sudo apt-get install python3
```

### Pip

```
sudo apt-get install python3-pip
```

### Git

```
sudo apt-get install git
```

## Installing

### Clone repo

```
git clone git@github.com:mas-student/web-python-2018-04-ht04.git
```

### Install requirements
```
sudo apt-get install uwsgi uwsgi-plugin-python3

pip install -r requirements.txt
```

### Example

Create files

app.py
```
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

```

wsgi.py
```
from web_python_2018_04_ht04_framework.core import run_application

def application(env, start_response):
    try:
        return run_application(env, start_response, framework_app='/path/to/app.py)

    except Exception as e:
        import traceback
        import sys
        print(e, traceback.format_exc())
        sys.exit(1)

```

The run

```
$ uwsgi_python3 --http-socket :9090 --wsgi-file "/path/to/your/wsgi.py"
```

### Help

## Authors

* **Student** - *Initial work* - [Student](https://github.com/mas-student)
