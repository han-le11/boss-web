import numpy as np
import unittest
from src.tabs.run_boss import RunBOSS


class TestAddBounds(unittest.TestCase):

    def setUp(self):
        self.obj = RunBOSS()  # Instantiate your class here
        self.obj.X_names = ["X1", "X2"]
        self.obj.Y_name = ["Y"]
        self.obj.data = np.array([[1, 2, 3], [3, 4, 6], [5, 7, 9], [2, 8, 6]])
        self.obj.bounds_exist = False
        self.obj.dim = 2
        self.obj.bounds = [(0, 1), (0, 1)]

    def test_shape_file_without_bounds(self):
        self.obj.add_bounds()
        print(self.obj.dload_data.shape)
        self.assertEqual(self.obj.dload_data.shape,
                         (self.obj.data.shape[0], self.obj.dim + 3))  # 3 original columns + 2 columns for bounds

    def test_col_names_file_without_bounds(self):
        """
        Test that the column names of bounds are correctly named,
        if the uploaded file does not have bounds.
        """
        self.obj.add_bounds()
        self.assertIn("boss-bound X1", self.obj.dload_data.columns)
        self.assertIn("boss-bound X2", self.obj.dload_data.columns)
        self.assertIn("output-var Y", self.obj.dload_data.columns)


if __name__ == '__main__':
    unittest.main()

