import pandas as pd
import streamlit as st
import tomli
from io import StringIO
from pandas.errors import ParserError
from streamlit.runtime.uploaded_file_manager import UploadedFile


def reset():
    """
    Helper function for clearing data.
    Reset all session states when clicking the "Yes" button to clear all data.
    """
    st.session_state.input_key += 1
    st.session_state["bo_run"] = None
    st.session_state["init_names_and_bounds"] = None
    st.session_state["init_pts"] = None


class RunHelper:
    """
    Helper class for running BOSS optimization.
    """

    def __init__(self) -> None:
        self.file = None
        self.has_metadata = False  # whether the file contains metadata
        self.metadata = None  # dictionary of metadata of BOSS parameters

    def upload_file(self) -> pd.DataFrame:
        """
        Widget to upload a file, which is read into a dataframe. Check if metadata exists.

        return:
        pd.DataFrame
            The dataframe of data, without metadata.
        """
        self.file = st.file_uploader(
            label="The CSV file must use colons or semicolons as separators",
            type=["csv"],
            help="Your file should contain data for input variables and target variable",
            key=f"uploader_{st.session_state.input_key}"
        )

        if self.file is None:
            pass
        else:
            try:
                # convert to str to look for metadata
                stringio = StringIO(self.file.getvalue().decode("utf-8"))
                lines = stringio.read().split("\n")
                # remove hash and empty last line if it exists
                if lines[-1] == "":
                    lines = lines[:-1]
                metadata = [l[1:] for l in lines if l[0] == "#"]
                self.metadata = tomli.loads("\n".join(metadata))
                if self.metadata:
                    self.has_metadata = True
                st.write(self.metadata)
                return pd.read_csv(self.file, sep=";|,", comment="#")  # ignore comments for hyperparams and metadata
            except ParserError as err:
                st.error(
                    "Error: "
                    + str(err)
                    + " Please check the file contents and re-upload."
                )

    @st.dialog("Are you sure you want to clear all data?")
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
