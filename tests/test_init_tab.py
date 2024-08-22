import numpy as np
import pandas as pd
import pytest
import unittest
import streamlit as st
from unittest.mock import patch
from src.tabs.init_manager_tab import InitManagerTab, set_names_bounds


class TestAddVarNames(unittest.TestCase):
    def setUp(self) -> None:
        self.init = InitManagerTab()
        self.init.dim = 2
        self.arr = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

    def test_return_df(self):
        st.session_state["init_vars"] = {"x": (0, 10), "y": (0, 20), "z": None}
        df = self.init.add_var_names(self.arr, st.session_state["init_vars"])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (3, 3))
        pd.testing.assert_frame_equal(df.iloc[:, :-1], pd.DataFrame(self.arr, columns=['x', 'y']))

    def test_add_var_names_exception(self):
        st.session_state["init_vars"] = {"x": (0, 10), "x": (0, 20), "y": None}
        with pytest.raises(ValueError):
            self.init.add_var_names(self.arr, st.session_state["init_vars"])


class TestSetNamesBounds(unittest.TestCase):
    def setUp(self) -> None:
        if "input_key" not in st.session_state:
            st.session_state.input_key = 0
        if "init_vars" not in st.session_state:
            st.session_state["init_vars"] = dict()

    def test_2d(self):
        with patch('streamlit.session_state') as mock_st:
            mock_st.session_state["init_vars"].return_value = [{
                "input-var x": np.array([1., 5.]),
                "input-var y": np.array([2., 10.]),
                "output-var z": None
            }]
        bounds = set_names_bounds(dimension=2)
        self.assertEqual(bounds.shape, (2, 2))
        self.assertEqual(len(st.session_state["init_vars"]), 2)

    def test_output_variable(self):
        with patch('streamlit.columns') as mock_columns:
            mock_columns.return_value = ["x", "y", "z"]
        with patch('streamlit.number_input') as mock_number_input:
            mock_number_input.return_value = np.array([[1.0, 2.0], [3.0, 4.0]])
        bounds = set_names_bounds(2)
        self.assertEqual(bounds.shape, (2, 2))
        self.assertEqual(len(st.session_state["init_vars"]), 2)
        self.assertIn("output-var ", st.session_state["init_vars"].keys())

    # TODO: Fix test for 3D
    def test_3d(self):
        with patch('streamlit.session_state') as mock_st:
            # dictionary of variable names (key) and bounds (value)
            mock_st.session_state["init_vars"].return_value = [{
                "input-var x": np.array([1., 5.]),
                "input-var y": np.array([2., 10.]),
                "input-var z": np.array([0., 25.]),
                "output-var t": None
            }]
        dimension = 3
        bounds = set_names_bounds(dimension)
        print(len(st.session_state["init_vars"]))
        # Test for the correct shape of the bounds array
        self.assertEqual(bounds.shape, (dimension, 2))
        # Test if variable names and bounds are correctly stored in the dictionary
        self.assertIn('input-var x', list(st.session_state["init_vars"].keys()))
        self.assertIn("output-var t", st.session_state["init_vars"].keys())
        self.assertEqual(len(st.session_state["init_vars"]), dimension)


if __name__ == '__main__':
    unittest.main()
