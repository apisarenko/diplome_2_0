import unittest
from modules.db_file import DB_Mongo


db = DB_Mongo()
dict_test = {'id': 1234567, 'first_name': 'Маркел', 'last_name': 'Маркел', 'is_closed': False,
             'can_access_closed': True, 'sex': 2, 'bdate': '21.11.1977',
             'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'relation': 6, 'interests': ''}


class TestDB(unittest.TestCase):
    def test_import(self):
        db.import_data(dict_test)
        self.assertEqual(db.get_basic_id()[0], dict_test['id'])

    def test_drop(self):
        db.drop()
        self.assertEqual(db.item_count(), 0)


if __name__ == '__main__':
    unittest.main()
