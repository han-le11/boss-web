import numpy as np
import unittest
from unittest.mock import patch
from src.ui.boss_run_params import input_x_bounds, return_bounds


class TestReturnBounds(unittest.TestCase):

    @patch('streamlit.number_input')
    def test_return_bounds_prompt_messages(self, mock_number_input):
        mock_number_input.return_value = 5.0
        X_names = ['x', 'y', 'z']
        dim = 2
        _, _ = return_bounds(X_names, dim)
        lower_bound_args, low_bound_kwargs = mock_number_input.call_args_list[0]
        upper_bound_args, upper_bound_kwargs = mock_number_input.call_args_list[1]
        self.assertIn('Lower bound of ', lower_bound_args[0])
        self.assertIn('Upper bound of ', upper_bound_args[0])

    @patch('streamlit.number_input')
    def test_return_bounds_valid_input(self, mock_number_input):
        X_names = ['x', 'y', 'z']
        dim = 2
        mock_number_input.side_effect = [3.0, 5.0]
        lower_bound, upper_bound = return_bounds(X_names, dim)
        self.assertEqual(lower_bound, 3.0)
        self.assertEqual(upper_bound, 5.0)


if __name__ == '__main__':
    unittest.main()


class TestInputXBounds(unittest.TestCase):

    def test_empty_input_names(self):
        X_names = []
        result = input_x_bounds(X_names)
        self.assertTrue(np.array_equal(a1=result, a2=np.empty(shape=(0, 2))))

    def test_single_input_name(self):
        X_names = ['x1']
        with patch(target='src.ui.boss_run_params.return_bounds', return_value=(0, 1)):
            result = input_x_bounds(X_names)
        self.assertTrue(np.array_equal(a1=result, a2=np.array([[0, 1]])))

    def test_multiple_input_names(self):
        X_names = ['x1', 'x2', 'x3']
        with patch(target='src.ui.boss_run_params.return_bounds', side_effect=[(0, 1), (-1, 1), (2, 1)]):
            result = input_x_bounds(X_names)
        self.assertTrue(np.array_equal(a1=result, a2=np.array([[0, 1], [-1, 1], [2, 1]])))


if __name__ == '__main__':
    unittest.main()
