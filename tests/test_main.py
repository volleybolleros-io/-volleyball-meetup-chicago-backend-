import unittest
from main import app

class DBTestCase(unittest.TestCase):

    def test_main(self):
        self.assertIsNotNone(app)
