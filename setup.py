from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='web-python-2018-04-ht04-framework',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'jinja2',
        'nose'
    ],
    entry_points={
        'console_scripts':
            ['web_python_2018_04_ht04_framework = web_python_2018_04_ht04_framework.cli:main']
    },
    test_suite='nose.collector',
    tests_require=[
        'nose',
    ],
)
