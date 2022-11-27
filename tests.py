import json
import os
import unittest

import logging

from app import create_app

from models import setup_db, User, ShowerThought, insert_mock_data

TEST_DATABASE_URI = os.getenv('DATABASE_URL')
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')
REGULAR_TOKEN = os.getenv('REGULAR_TOKEN')


class TubAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.admin = ADMIN_TOKEN
        self.regular = REGULAR_TOKEN
        setup_db(self.app, TEST_DATABASE_URI)
        logging.disable(logging.CRITICAL)

    def test_get_all_showerthoughts(self):
        res = self.client().get('/all')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)

    def test_get_all_showerthoughts_bad_request(self):
        res = self.client().get('/all/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Resource not found.")

    def test_get_random_showerthought(self):
        res = self.client().get('/random')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn("creator", data["random"])
        self.assertIn("content", data["random"])

    def test_get_random_showerthought_bad_request(self):
        res = self.client().get('/random/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Resource not found.")

    def test_add_new_showerthought(self):
        req = {
            "creator": "okayletsgooo",
            "content": "Content goes in here."
        }
        res = self.client().post('/shower_thoughts',
                                 headers={"Authorization": "Bearer {}".format(self.regular)}, json=req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["message"], "New showerthought created")

    def test_add_new_showerthought_nonexistent_creator(self):
        req = {
            "creator": "nonexistent",
            "content": "Content from a nonexistent user."
        }
        res = self.client().post('/shower_thoughts',
                                 headers={"Authorization": "Bearer {}".format(self.regular)}, json=req)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["message"], "No user with that name exists.")

    def test_add_new_showerthought_duplicate_content(self):
        req = {
            "creator": "okayletsgooo",
            "content": "A bird can fly but a fly cannot bird."
        }

        res = self.client().post('/shower_thoughts',
                                 headers={"Authorization": "Bearer {}".format(self.regular)}, json=req)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            data["message"], "Identical showerthought already exists")

    def test_add_new_showerthought_but_forbidden(self):
        req = {
            "creator": "okayletsgooo",
            "content": "Unnecessary content goes in here."
        }

        res = self.client().post('/shower_thoughts',
                                 headers={"Authorization": "Bearer {}".format(self.admin)}, json=req)

        self.assertEqual(res.status_code, 403)

    def test_add_new_showerthought_while_unauthorized(self):
        req = {
            "creator": "okayletsgooo",
            "content": "Unnecessary content goes in here."
        }

        res = self.client().post('/shower_thoughts', json=req)

        self.assertEqual(res.status_code, 401)

    def test_edit_showerthought(self):
        req = {
            "content": "Nighttime is the natural state of the universe and daytime is only caused by a nearby, radiating ball of flame."
        }

        res = self.client().patch('/shower_thoughts/1',
                                  headers={"Authorization": "Bearer {}".format(self.regular)}, json=req)

        self.assertEqual(res.status_code, 200)

    def test_edit_showerthought_with_bad_request(self):
        req = {
            "data": "The key should not be 'data'"
        }

        res = self.client().patch('/shower_thoughts/1',
                                  headers={"Authorization": "Bearer {}".format(self.regular)}, json=req)

        self.assertEqual(res.status_code, 400)

    def test_edit_showerthought_on_nonexistent_uri(self):
        req = {
            "content": "This URI is not going to work."
        }

        res = self.client().patch('/shower_thoughts/100',
                                  headers={"Authorization": "Bearer {}".format(self.regular)}, json=req)

        self.assertEqual(res.status_code, 404)

    def test_edit_showerthought_with_wrong_credentials(self):
        req = {
            "content": "This is not going to work."
        }

        res = self.client().patch('/shower_thoughts/100',
                                  headers={"Authorization": "Bearer {}".format(self.admin)}, json=req)

        self.assertEqual(res.status_code, 403)

    def test_deleting_showerthought(self):
        res = self.client().delete('/shower_thoughts/2',
                                   headers={"Authorization": "Bearer {}".format(self.admin)})

        self.assertEqual(res.status_code, 200)

    def test_deleting_nonexistent_showerthought(self):
        res = self.client().delete('/shower_thoughts/100',
                                   headers={"Authorization": "Bearer {}".format(self.admin)})

        self.assertEqual(res.status_code, 404)

    def test_add_new_user(self):
        req = {
            "name": "youveHeardAboutMe"
        }

        res = self.client().post(
            '/users', headers={"Authorization": "Bearer {}".format(self.regular)}, json=req)

        self.assertEqual(res.status_code, 201)

    def test_add_new_user_but_username_already_exists(self):
        req = {
            "name": "okayletsgooo"
        }

        res = self.client().post(
            '/users', headers={"Authorization": "Bearer {}".format(self.regular)}, json=req)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["message"], "User with that name already exists")

    def test_add_new_user_forbidden(self):
        req = {
            "name": "name"
        }

        res = self.client().post(
            '/users', headers={"Authorization": "Bearer {}".format(self.admin)}, json=req)

        self.assertEqual(res.status_code, 403)

    def test_getting_user(self):
        res = self.client().get(
            '/users/1', headers={"Authorization": "Bearer {}".format(self.admin)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["name"], "johncena00034")
        self.assertIsInstance(data["shower_thoughts"], list)

    def test_getting_nonexistent_user(self):
        res = self.client().get(
            '/users/100', headers={"Authorization": "Bearer {}".format(self.admin)})

        self.assertEqual(res.status_code, 404)

    def test_getting_user_followers(self):
        res = self.client().get(
            '/users/1/followers', headers={"Authorization": "Bearer {}".format(self.admin)})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("followers", data)
        self.assertIn("user_id", data)
        self.assertIn("username", data)

    def test_getting_nonexistent_user_followers(self):
        res = self.client().get(
            '/users/100/followers', headers={"Authorization": "Bearer {}".format(self.admin)})

        self.assertEqual(res.status_code, 404)

    def test_delete_user(self):
        res = self.client().delete('/users/2',
                                   headers={"Authorization": "Bearer {}".format(self.admin)})

        self.assertEqual(res.status_code, 200)

    def test_delete_user_that_doesnt_exist(self):
        res = self.client().delete('/users/100',
                                   headers={"Authorization": "Bearer {}".format(self.admin)})

        self.assertEqual(res.status_code, 404)

    def test_delete_user_without_appropriate_credentials(self):
        res = self.client().delete('/users/2',
                                   headers={"Authorization": "Bearer {}".format(self.regular)})

        self.assertEqual(res.status_code, 403)

    def test_get_all_users(self):
        res = self.client().get('/users',
                                headers={"Authorization": "Bearer {}".format(self.admin)})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("users", data)
        self.assertIsInstance(data["users"], list)

    def test_get_all_users_without_permission(self):
        res = self.client().get('/users')

        self.assertEqual(res.status_code, 401)

    def tearDown(self):
        """Resets db"""
        insert_mock_data()
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
