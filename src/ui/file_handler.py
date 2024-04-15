import numpy as np
import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def upload_file():
    """
    Widget to upload a file, which is read into a dataframe.
    Display the "help" tip when hovering the mouse over the question mark icon.
    """
    file = st.file_uploader(
        "Please upload a csv file first",
        type=["csv"],
        help="Your file should contain data for input variables and target variable",
    )
    if isinstance(file, UploadedFile):
        try:
            df = pd.read_csv(file, sep=":|;|,")
            return df
        except ValueError as err:
            st.error("Error: " + str(err) + ". Please check the file contents and re-upload.")


def check_if_there_are_bounds(df) -> bool:
    """
    Returns True if there are bounds in the uploaded file; otherwise False.
    :param df: data from the uploaded file that is read into a dataframe.
    :return:
    """
    bounds_exist = False
    if df is not None:
        x = df.filter(regex='boss-bound').dropna().to_numpy()
        if x.size != 0:
            # get a list of bound names
            bound_names = [k for k in list(df.columns) if 'boss-bound' in k]
            if len(bound_names) != 0:
                bounds_exist = True
    return bounds_exist


def parse_bounds(df):
    """
    Return the variable names and bounds to run with BOMain object.
    :param df: Uploaded file, which is read into a dataframe.
    :return: numpy array of the bounds
    """
    if df is not None:
        bounds_array = df.filter(regex="boss-bound").dropna().to_numpy()
        tp_bounds_array = np.transpose(bounds_array)
        return tp_bounds_array


def extract_col_data(df: pd.DataFrame, keyword: str) -> np.array:
    """
    Get the column(s) whose name contains the given keyword.
    :param df: Uploaded file, which is read into a dataframe.
    :param keyword: the keyword that the column name should contain.
    :return: numpy array of the column(s) whose name contains the given keyword.
    """
    array = df.filter(regex=keyword).to_numpy()
    if array.size == 0:
        array = np.array([])
    return array


def choose_inputs_and_outputs(df):
    """
    Display widgets that let users choose at least one column for input variable(s) and
    only one column for target variable.
    :param df:
        Dataframe read from the UploadedFile object (file uploaded by a user).
    """
    X_names = []
    Y_name = []
    X_vals = []
    Y_vals = []

    if df is not None:
        in_col, out_col = st.columns(2)
        with in_col:
            X_names = st.multiselect(
                "Choose input variables *", options=list(df.columns), default=None
            )
        with out_col:
            Y_name = st.multiselect(
                "Choose one target variable *",
                options=list(df.columns),
                default=None,
                max_selections=1,
            )
        X_vals = df[X_names]
        Y_vals = df[Y_name]

        with st.expander("See chosen data"):
            ins, outs = st.columns(2)
            if X_vals.size != 0:
                with ins:
                    st.write("Input variables", X_vals)
            if Y_vals.size != 0:
                with outs:
                    st.write("Target variable", Y_vals)
        X_vals = X_vals.to_numpy()
        Y_vals = Y_vals.to_numpy()
    return X_vals, Y_vals, X_names, Y_name
