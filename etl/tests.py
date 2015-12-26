from pathlib import Path
from unittest import TestCase


class BasicDataTest(TestCase):

    def setUp(self):
        data_path = Path('../data/')

    def test(self):
        return True