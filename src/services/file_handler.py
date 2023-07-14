import streamlit as st
import pandas as pd


def upload_file():
    file = st.file_uploader("Please upload a csv or excel file first", type=["csv", "xlsx"])
    if 'file' not in st.session_state:
        st.session_state['file'] = file
    return file


def display_placeholder_text_in_multiselect_box():
    pass


def choose_inputs_and_outputs(uploaded_file):
    input_names = []
    output_name = []
    x = []
    y = []

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        in_col, out_col = st.columns(2)
        with in_col:
            input_names = st.multiselect(
                "Choose input columns", options=list(df.columns), default=None,
            )
        with out_col:
            output_name = st.multiselect(
                "Choose output column", options=list(df.columns), default=None
            )
        x = df[input_names].to_numpy()
        y = df[output_name].to_numpy()

        with st.expander("See chosen data"):
            if x.size != 0:
                ins, outs = st.columns(2)
                with ins:
                    st.write("Input variable", x)
                if y.size != 0:
                    with outs:
                        st.write("Target variable", y)
    return x, y, input_names, output_name

