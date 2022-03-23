import unittest
from main import app

class MainTestCase(unittest.TestCase):

    def test_main(self):
        self.assertIsNotNone(app)
