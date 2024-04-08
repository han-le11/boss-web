import pandas as pd
import numpy as np
import unittest
from src.ui.file_handler import check_if_there_are_bounds, extract_col_data, parse_bounds


class TestCheckIfThereAreBounds(unittest.TestCase):
    def test_none_df(self):
        df = None
        self.assertFalse(check_if_there_are_bounds(df))

    def test_no_bounds(self):
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        self.assertFalse(check_if_there_are_bounds(df))

    def test_with_bounds(self):
        df = pd.DataFrame({'boss-bound-x': [1, 2, 3], 'col2': [4, 5, 6]})
        self.assertTrue(check_if_there_are_bounds(df))


class TestParseBounds(unittest.TestCase):
    def test_parse_bounds_not_none(self):
        df = pd.DataFrame({
            'boss-bound1': [1, 2],
            'boss-bound2': [3, 4],
            'boss-bound3': [5, 6]
        })
        expected_output = np.array([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(parse_bounds(df).all(), expected_output.all())

    def test_parse_bounds_none(self):
        df = None
        self.assertIsNone(parse_bounds(df))


class TestExtractColData(unittest.TestCase):
    def test_single_matching_column(self):
        df = pd.DataFrame({'test_col_1': [1, 2, 3], 'other_col': [4, 5, 6]})
        keyword = 'test'
        result = extract_col_data(df, keyword)
        self.assertTrue(np.array_equal(result, np.array([[1], [2], [3]])))

    def test_multiple_matching_columns(self):
        df = pd.DataFrame({'test_col_1': [1, 2, 3], 'test_col_2': [4, 5, 6]})
        keyword = 'test'
        result = extract_col_data(df, keyword)
        self.assertTrue(np.array_equal(result, np.array([[1, 4], [2, 5], [3, 6]])))

    def test_no_matching_columns(self):
        df = pd.DataFrame({'col_a': [1, 2, 3], 'col_b': [4, 5, 6]})
        keyword = 'test'
        result = extract_col_data(df, keyword)
        self.assertTrue(np.array_equal(result, np.array([])))


if __name__ == '__main__':
    unittest.main()
