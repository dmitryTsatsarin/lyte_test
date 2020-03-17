import json

from rest_framework.test import APITestCase, APIClient


class CommonTestCaseMixin(object):
    # add some common function here

    def content_to_dict(self, content):
        return json.loads(content)


class CommonTestCase(APITestCase, CommonTestCaseMixin):
    client_class = APIClient
