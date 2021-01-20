import unittest
from unittest.mock import call

from django.test import TestCase, Client
from .module import DoAsyncRequest, parser

import requests
from unittest import mock
from requests import request


# This is the class we want to test


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def data(self):
            return self.data

    return MockResponse("Ok", 200)


"""# Our test case class
class MyGreatClassTestCase(TestCase):

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch(self, mock_get):
        print("hrh")
        # Assert requests.get calls
        mgc = MyGreatClass()
        json_data = mgc.fetch_json('http://someurl.com/test.json')
        self.assertEqual(json_data, {"key1": "value1"})
        json_data = mgc.fetch_json('http://someotherurl.com/anothertest.json')
        self.assertEqual(json_data, {"key2": "value2"})
        json_data = mgc.fetch_json('http://nonexistenturl.com/cantfindme.json')
        self.assertIsNone(json_data)

        # We can even assert that our mocked method was called with the right parameters
        self.assertIn(mock.call('http://someurl.com/test.json'), mock_get.call_args_list)
        self.assertIn(mock.call('http://someotherurl.com/anothertest.json'), mock_get.call_args_list)

        self.assertEqual(len(mock_get.call_args_list), 3)
"""


class TestParser(TestCase):
    def test_parse_sample_page(self):
        page = 0
        parsed_page = parser(page)
        self.assertEqual(parsed_page, 0)


class TestDoAsyncRequest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get_main(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    # def test_get_view_target(self):
    #     response = self.client.get('/1/view_target')
    #     self.assertEqual(response.status_code, 200)

    def test_get_add_tagret(self):
        response = self.client.get('/add_target')
        self.assertEqual(response.status_code, 200)

    def test_DoAsyncRequest_create_object_without_price_limits(self):
        do_request = DoAsyncRequest("https://www.avito.ru", "RTX 3080")
        self.assertEqual(do_request.title, "RTX 3080")

    def test_DoAsyncRequest_create_object_with_price_limits(self):
        do_request_with_params = DoAsyncRequest("https://www.avito.ru", "RTX 3080", 100000, 150000)
        self.assertEqual(do_request_with_params.title, "RTX 3080")
        self.assertEqual(do_request_with_params.price_min, 100000)
        self.assertEqual(do_request_with_params.price_max, 150000)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_DoAsyncRequest_object_can_do_request(self, mock_get):
        do_request = DoAsyncRequest("https://www.avito.ru", "RTX 3080")
        resp = do_request.request()
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            mock.call(
                'https://www.avito.ru',
                params={'q': 'RTX 3080', 'pmin': None, 'pmax': None, 'p': 1}),
            mock_get.call_args_list)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def badtest_DoAsyncRequest_object_can_do_async_request(self, mock_get):  # need more pages
        do_request = DoAsyncRequest("https://www.avito.ru", "RTX 3080")
        do_request.async_request()
        resp = do_request.run_loop()
        self.assertEqual(resp[0].status_code, 200)
        self.assertIn(
            mock.call(
                'https://www.avito.ru',
                params={'q': 'RTX 3080', 'pmin': None, 'pmax': None, 'p': 1}),
            mock_get.call_args_list)
