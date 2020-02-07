import unittest
from application import Application


class TestGeneration(unittest.TestCase):

    def test_default_content_from_url(self):
        app = Application()
        app.get_data_from_url('https://json.medrating.org/todos', 'https://json.medrating.org/users')
        app.generate_reports(no_file=True)

    def test_default_content_from_file(self):
        app = Application()
        app.get_data_from_file('./data/default_tasks.json', './data/default_users.json')
        app.generate_reports(no_file=True)

    def test_empty_content(self):
        app = Application()
        app.get_data_from_file('./data/empty_tasks.json', './data/default_users.json')
        app.generate_reports(no_file=True)

    def test_broken_content(self):
        app = Application()
        app.get_data_from_file('./data/broken_tasks.json', './data/broken_users.json')
        app.generate_reports(no_file=True)

    def test_user1_has_no_tasks(self):
        app = Application()
        app.get_data_from_file('./data/user1_has_no_tasks.json', './data/default_users.json')
        app.generate_reports(no_file=True)