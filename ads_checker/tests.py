from django.test import TestCase, Client


class ShopObject:
    def __init__(self):
        self.pages = []


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code
    return MockResponse("Ok", 200)


# class TestRequest(TestCase):
#     def setUp(self) -> None:
#         self.client = Client()


class GetSomePage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_main_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_target_page(self):
        response = self.client.get('/1/view_target')
        self.assertEqual(response.status_code, 200)

    def test_add_tagret_page(self):
        response = self.client.get('/add_target')
        self.assertEqual(response.status_code, 200)
