from unittest import TestCase
from unittest import mock
from unittest.mock import patch, Mock

from web_python_2018_04_ht04_framework.core import \
    add_url, route, execute, process, \
    Url, Target, Request, \
    response200, response301, response404, response405, response500, make_post


class TestCore(TestCase):
    def setUp(self):
        self.start_response = mock.Mock()
        self.getEnv = {'PATH_INFO': '/', 'REQUEST_METHOD': 'GET', 'QUERY_STRING': ''}
        self.postEnv = {'PATH_INFO': '/', 'REQUEST_METHOD': 'POST', 'QUERY_STRING': ''}

    def cont200(self, request):
        return response200()

    def cont500(self, request):
        raise Exception('TEST500')

    def test_add_url(self):
        self.assertIsNotNone(add_url('/'))

    def test_route(self):
        self.assertEqual(route('/', 'GET', []), response404('/'))
        self.assertEqual(route('/', 'GET', [Url('/', 'GET', self.cont200)]), Target(self.cont200, tuple(), None))
        self.assertEqual(route('/', 'POST', [Url('/', 'GET', self.cont200)]), response405('/', 'POST'))
        self.assertEqual(route('/foo', 'POST', [Url('/foo', 'GET', self.cont200)]), response301('/foo'))
        self.assertEqual(route('/foo/', 'GET', [Url('/foo.*', 'GET', self.cont200)]), Target(self.cont200, tuple(), None))
        self.assertEqual(route('/177/', 'GET', [Url('/(.+)/', 'GET', self.cont200)]), Target(self.cont200, ('177', ), None))

    def test_execute(self):
        self.assertEqual(execute(Target(self.cont500, tuple(), None), Request({}, {})).status_code, response500('', '').status_code)

    @patch('web_python_2018_04_ht04_framework.core.get_store')
    @patch('web_python_2018_04_ht04_framework.core.route')
    @patch('web_python_2018_04_ht04_framework.core.Request')
    def test_process_200(self, mockRequest, routeMock, getStoreMock):
        getStoreMock.return_value = {'urls': []}

        process(self.getEnv, self.start_response)

        routeMock.assert_called()
        mockRequest.assert_called()
        self.start_response.assert_called()

    def test_make_post(self):
        input = Mock()
        input.read.return_value = 'a=1&b=2'
        self.assertEqual(input.read(), 'a=1&b=2')
        self.assertEqual(make_post({'wsgi.input': input}), {'a': '1', 'b': '2'})