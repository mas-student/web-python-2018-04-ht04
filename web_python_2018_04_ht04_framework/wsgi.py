#!/usr/bin/python
# -*- coding: utf8 -*-


from web_python_2018_04_ht04_framework.core import run_application

def application(env, start_response):

    try:
        return run_application(env, start_response, framework_app='samples/hello.py')

    except Exception as e:
        import traceback
        import sys
        print(e, traceback.format_exc())
        sys.exit(1)
