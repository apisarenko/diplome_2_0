import requests
import unittest


API_KEY = '5e9a912e73e22d3469b459f74bfdfcfbcaced2e338bd73c9aa2620e3c0b1bc1cf91b88282d71bfc3803e7'
URL = 'https://api.vk.com/method/users.get'


class TestServerFunctionality(unittest.TestCase):
    def setUp(self):
        params = {
            'access_token': API_KEY,
            'user_id': '10799607',
            'v': 5.95,
        }
        self.response = requests.get(URL, params=params)

    def test_status(self):
        self.assertEqual(self.response.json()['response'][0]['id'], 10799607)

    def test_data(self):
        self.assertEqual(self.response.json()['response'][0]['first_name'], 'Андрей')
        self.assertEqual(self.response.json()['response'][0]['last_name'], 'Писаренко')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
