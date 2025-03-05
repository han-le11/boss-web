import numpy as np
import pandas as pd
import pytest
import unittest
import streamlit as st
from boss.bo.initmanager import InitManager
from types import NoneType
from src.tabs.init_manager_setup import InitManagerSetUp

class TestSetInitManager(unittest.TestCase):
    def setUp(self) -> None:
        self.init = InitManagerSetUp()
        self.init.dim = 2
        self.num_init = 5
        self.init_type = "sobol"
        # if "input_key" not in st.session_state:
        #     st.session_state.input_key = 0
        # if "init_vars" not in st.session_state:
        #     st.session_state["init_vars"] = dict()

    def test_set_init_manager(self):
        bounds = np.array([[0, 1], [0, 1]])
        init_manager = self.init.set_init_manager(bounds)
        self.assertIsInstance(init_manager, InitManager)

    def test_set_init_manager_with_none_bounds(self):
        init_type = "sobol"
        bounds = None # example bounds
        init_manager = self.init.set_init_manager(init_type, bounds)
        self.assertIsInstance(init_manager, NoneType)

class TestAddVarNames(unittest.TestCase):
    def setUp(self) -> None:
        self.init = InitManagerSetUp()
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

if __name__ == '__main__':
    unittest.main()
