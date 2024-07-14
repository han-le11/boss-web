import pandas as pd
import unittest
from src.ui.file_handler import find_bounds


class TestFindBounds(unittest.TestCase):
    def test_none_df(self):
        df = None
        self.assertFalse(find_bounds(df))

    def test_no_bounds(self):
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        self.assertFalse(find_bounds(df))

    def test_with_bounds(self):
        df = pd.DataFrame({'boss-bound-x': [1, 2, 3], 'col2': [4, 5, 6]})
        self.assertTrue(find_bounds(df))


if __name__ == '__main__':
    unittest.main()
