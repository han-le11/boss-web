import numpy as np
import pandas as pd
import unittest
from src.tabs.run_boss import RunBOSS


class TestParams(unittest.TestCase):
    """
    Test parse_params function and add_bounds function of class RunBOSS.
    """

    def setUp(self):
        self.obj = RunBOSS()
        self.obj.X_names = ["X1", "X2"]
        self.obj.Y_name = ["Y"]
        self.obj.data = np.array([[1, 2, 3], [3, 4, 6], [5, 7, 9], [2, 8, 6]])
        self.obj.bounds_exist = False
        self.obj.dim = 2
        self.obj.bounds = [(0, 1), (0, 1)]
        self.test_df = pd.DataFrame({
            'boss-bound-x': [1, 2, 3],
            'boss-bound-y': [4, 5, 6],
            'noise variance': [0.1, None, None],
            'goal': ['maximize', None, None]
        })

    def test_find_bounds(self):
        self.obj.parse_params(self.test_df)
        self.assertEqual(self.obj.bounds.tolist(), [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(self.obj.bounds.shape, (2, 3))
        self.assertEqual(self.obj.dim, 2)
        self.assertEqual(self.obj.noise, 0.1)

    def test_set_opt_params(self):
        self.obj.parse_params(self.test_df)
        self.assertEqual(self.obj.min_max, 'maximize')

    def test_shape_file_without_bounds(self):
        self.obj.add_bounds()
        # 3 original columns + 2 columns for bounds
        self.assertEqual(self.obj.dload_data.shape,(self.obj.data.shape[0], self.obj.dim + 3))

    def test_col_names_file_without_bounds(self):
        """
        Test that the column names of bounds are correctly named,
        if the uploaded file does not have bounds.
        """
        self.obj.add_bounds()
        self.assertIn("boss-bound X1", self.obj.dload_data.columns)
        self.assertIn("boss-bound X2", self.obj.dload_data.columns)
        self.assertIn("output-var Y", self.obj.dload_data.columns)

    def test_bounds_none(self):
        bounds = None
        self.assertFalse(self.obj.verify_bounds(bounds))

    def test_bounds_with_nan_values(self):
        bounds = np.array([[1, 2], [np.nan, 4]])
        self.assertFalse(self.obj.verify_bounds(bounds))

    def test_lower_bound_not_smaller_than_upper_bound(self):
        bounds = np.array([[2, 1], [3, 4]])
        self.assertFalse(self.obj.verify_bounds(bounds))

    def test_valid_bounds(self):
        bounds = np.array([[1, 2], [3, 4]])
        self.assertTrue(self.obj.verify_bounds(bounds))


class TestDataVerification(unittest.TestCase):
    def test_null_values(self):
        data_with_null = pd.DataFrame({'A': [1, 2, None, 4]})
        obj = RunBOSS(data=data_with_null)
        self.assertFalse(obj.verify_data())

    def test_no_null_values(self):
        data_no_null = pd.DataFrame({'A': [1, 2, 3, 4]})
        obj = RunBOSS(data=data_no_null)
        self.assertTrue(obj.verify_data())


if __name__ == '__main__':
    unittest.main()
