import pandas as pd
import streamlit as st
from pandas.errors import ParserError
from streamlit.runtime.uploaded_file_manager import UploadedFile


def reset():
    st.session_state.input_key += 1
    st.session_state["bo_run"] = None
    st.session_state["init_names_and_bounds"] = None
    st.session_state["init_pts"] = None


class RunHelper:
    def __init__(self) -> None:
        self.file = None

    def upload_file(self) -> pd.DataFrame:
        """
        Widget to upload a file, which is read into a dataframe.
        Display the "help" tip when hovering the mouse over the question mark icon.
        """
        self.file = st.file_uploader(
            label="Restart by uploading a csv file",
            type=["csv"],
            help="Your file should contain data for input variables and target variable",
            key=f"uploader_{st.session_state.input_key}"
        )

        if isinstance(self.file, UploadedFile):
            try:
                df = pd.read_csv(self.file, sep=";|,")
                return df
            except ParserError as err:
                st.error(
                    "Error: "
                    + str(err)
                    + " Please check the file contents and re-upload."
                )

    @st.experimental_dialog("Are you sure you want to clear all data?")
    def clear_data(self) -> None:
        """
        Clear all input data and BOSS optimization results.
        """
        # Make 2 placeholders to display the buttons.
        left, right = st.columns([1, 5])
        with left:
            if st.button("Yes", on_click=reset):
                # rerun to close the dialog programmatically
                st.rerun()
        with right:
            if st.button("No", type="primary"):
                st.rerun()
