#!/usr/bin/env python3
# TODO: write non-networked class method tests
import json
import unittest

from app_impl.routes import app

# test urls
ROOT_API_URL      = "http://127.0.0.1:5000/api/v1.0/"
GIT_URL_MAILCHIMP = "http://127.0.0.1:5000/api/v1.0/repos/?"\
                    "mailchimp=github"
GIT_URL_PYGAME    = "http://localhost:5000/api/v1.0/repos/?" \
                    "pygame=github"
BIT_URL_MAILCHIMP = "http://localhost:5000/api/v1.0/repos/?" \
                    "mailchimp=bitbucket"
BIT_URL_PYGAME    = "http://localhost:5000/api/v1.0/repos/?" \
                    "pygame=bitbucket"
AGG_URL_MAILCHIMP = "http://localhost:5000/api/v1.0/repos/?" \
                    "mailchimp=github,bitbucket"
AGG_URL_PYGAME    = "http://localhost:5000/api/v1.0/repos/?" \
                    "pygame=github,bitbucket"
AGG_URL_MIXED_1   = "http://localhost:5000/api/v1.0/repos/?" \
                    "pygame=github&mailchimp=bitbucket"
AGG_URL_MIXED_2   = "http://localhost:5000/api/v1.0/repos/?" \
                    "mailchimp=github&pygame=bitbucket"
AGG_URL_MIXED_3   = "http://localhost:5000/api/v1.0/repos/?" \
                    "mailchimp=bitbucket,github&" \
                    "pygame=bitbucket,github"
ITEMS = 6


class TestFlaskApi(unittest.TestCase):
    ''' unittest class implementation '''

    def setUp(self):
        ''' setup the test client '''
        self.app = app.test_client()
        self.app.testing = True

    def test_root_api(self):
        ''' fetch root api contents '''
        response = self.app.get(ROOT_API_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), 1)

    def test_github_mailchimp(self):
        ''' fetch github mailchimp repo data '''
        response = self.app.get(GIT_URL_MAILCHIMP)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def test_github_pygame(self):
        ''' fetch github pygame repo data '''
        response = self.app.get(GIT_URL_PYGAME)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def test_bitbucket_mailchimp(self):
        ''' fetch bitbucket mailchimp repo data '''
        response = self.app.get(BIT_URL_MAILCHIMP)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def test_bitbucket_pygame(self):
        ''' fetch bitbucket pygame repo data '''
        response = self.app.get(GIT_URL_PYGAME)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def test_aggregate_mailchimp(self):
        ''' fetch aggregate mailchimp repo data '''
        response = self.app.get(AGG_URL_MAILCHIMP)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def test_aggregate_pygame(self):
        ''' fetch aggregate pygame repo data '''
        response = self.app.get(AGG_URL_PYGAME)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def test_aggregate_mixed_1(self):
        ''' fetch aggregate pygame repo data '''
        response = self.app.get(AGG_URL_MIXED_1)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def test_aggregate_mixed_2(self):
        ''' fetch aggregate pygame repo data '''
        response = self.app.get(AGG_URL_MIXED_2)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def test_aggregate_mixed_3(self):
        ''' fetch aggregate pygame repo data '''
        response = self.app.get(AGG_URL_MIXED_3)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data[0]), ITEMS)

    def tearDown(self):
        ''' reset app items to initial state '''
        # nothing was updated/deleted


if __name__ == "__main__":
    unittest.main()