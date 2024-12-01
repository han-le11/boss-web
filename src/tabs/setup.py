import numpy as np
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


class SetUp:
    """
    Helper class for running BOSS optimization.
    """

    def __init__(self) -> None:
        self.file = None
        self.bounds = None
        self.dim = None
        self.has_metadata = False  # whether the file contains metadata
        self.metadata = None  # dictionary of metadata of BOSS parameters

    def set_init_bounds(self, dimension: int) -> np.array:
        """
        Return an array of input bounds and a dictionary of variable names and corresponding bounds.

        :param dimension: int
            dimension of the search space of input variables.

        :return:
        bounds: ndarray
            An array of input bounds, which is used to generate initial points with InitManager.
        """
        self.bounds = np.ones(shape=(dimension, 2)) * np.nan
        st.session_state["init_vars"] = dict()
        for d in range(dimension):
            col1, col2, col3 = st.columns(3, gap="large")
            with col1:
                var_name = st.text_input(
                    f"Name of variable {d + 1}",
                    max_chars=50,
                    help="A descriptive name will be great!",
                    key=f"var_{d}_{st.session_state.input_key}",
                )

                if var_name:
                    with col2:
                        self.bounds[d, 0] = st.number_input(
                            f"Lower bound of {var_name}",
                            format="%.3f",
                            key=f"lower {d}",
                            value=None,
                        )
                    with col3:
                        self.bounds[d, 1] = st.number_input(
                            f"Upper bound of {var_name}",
                            format="%.3f",
                            key=f"upper {d}",
                            value=None,
                        )
                st.session_state["init_vars"][var_name] = self.bounds[d, :]

        # Make one widget to input target variable name
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            y_name = st.text_input(
                f"Name of the output variable",
                max_chars=50,
                help="A descriptive name will be great!",
                key=f"target_{st.session_state.input_key}",
            )
        st.session_state["init_vars"][y_name] = None  # for target values, bounds are assigned None
        return self.bounds

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
            key=f"uploader_{st.session_state.input_key}",
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
        # Make 2 placeholders to display the yes and no buttons.
        left, right = st.columns([1, 5])
        with left:
            if st.button("Yes", on_click=reset):
                # rerun to close the dialog programmatically
                st.rerun()
        with right:
            if st.button("No", type="primary"):
                st.rerun()
