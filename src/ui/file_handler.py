import logging
import streamlit as st
import pandas as pd
from dateutil.parser import ParserError


def upload_file():
    """
    Widget to upload a file.
    Display the "help" tip when hovering the mouse over the question mark icon.
    """
    file = st.file_uploader(
        "Please upload a csv file first",
        type=["csv"],
        help="Your file should contain data for input variables and target variable",
    )
    return file


# TODO
def display_placeholder_text_in_multiselect_box():
    pass


def choose_inputs_and_outputs(uploaded_file):
    """
    Let users choose at least one column for input variable(s) and only one column for target variable.
    :param uploaded_file:
        A file (either csv or excel) uploaded by a user
    """
    input_names = []
    output_name = []
    x = []
    y = []

    if uploaded_file is not None:
        df = None
        try:
            df = pd.read_csv(uploaded_file, sep=":|;|,")
        except ValueError as err:
            st.error("Error: " + str(err) + " Please check and upload the file again.")

        if df is not None:  # successful
            in_col, out_col = st.columns(2)
            with in_col:
                input_names = st.multiselect(
                    "Choose input variables *", options=list(df.columns), default=None
                )
            with out_col:
                output_name = st.multiselect(
                    "Choose one target variable *",
                    options=list(df.columns),
                    default=None,
                    max_selections=1,
                )
            x = df[input_names]
            y = df[output_name]

            with st.expander("See chosen data"):
                ins, outs = st.columns(2)
                if x.size != 0:
                    with ins:
                        st.write("Input variables", x)
                if y.size != 0:
                    with outs:
                        st.write("Target variable", y)
            x = x.to_numpy()
            y = y.to_numpy()

    return x, y, input_names, output_name
