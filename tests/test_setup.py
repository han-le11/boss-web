import unittest
import numpy as np
import pandas as pd
import streamlit as st
from src.tabs.setup import SetUp

class TestSetUp(unittest.TestCase):

    def setUp(self):
        self.setup = SetUp()
        st.session_state.input_key = 0

    def test_set_init_bounds(self):
        dimension = 2
        bounds = self.setup.set_init_bounds(dimension)
        self.assertEqual(bounds.shape, (dimension, 2))
        self.assertTrue(np.isnan(bounds).all())

    def test_upload_file_no_file(self):
        self.setup.file = None
        result = self.setup.upload_file()
        self.assertIsNone(result)

    def test_upload_file_with_metadata(self):
        csv_content = "#noise: 0.1\n#min: True\n#num-init: 5\nvar1;var2;target\n1;2;3\n4;5;6"
        self.setup.file = st.file_uploader.UploadedFile("test.csv", "text/csv", csv_content.encode())
        result = self.setup.upload_file()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(self.setup.has_metadata)
        self.assertEqual(self.setup.metadata['noise'], 0.1)
        self.assertEqual(self.setup.metadata['min'], True)
        self.assertEqual(self.setup.metadata['num-init'], 5)

    def test_upload_file_no_metadata(self):
        csv_content = "var1;var2;target\n1;2;3\n4;5;6"
        self.setup.file = st.file_uploader.UploadedFile("test.csv", "text/csv", csv_content.encode())
        result = self.setup.upload_file()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(self.setup.has_metadata)

    def test_clear_data(self):
        st.session_state["bo_run"] = "some_value"
        st.session_state["init_names_and_bounds"] = "some_value"
        st.session_state["init_pts"] = "some_value"
        self.setup.clear_data()
        self.assertIsNone(st.session_state["bo_run"])
        self.assertIsNone(st.session_state["init_names_and_bounds"])
        self.assertIsNone(st.session_state["init_pts"])

if __name__ == '__main__':
    unittest.main()