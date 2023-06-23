import streamlit as st
import pandas as pd


class FileUploader:
    @classmethod
    def upload_file(cls):
        file = st.file_uploader("Choose a csv or excel file", type=['csv', 'xlsx'])
        return file

    @classmethod
    def choose_inputs_and_outputs(cls, uploaded_file):
        input_names = []
        output_name = []
        x = []
        y = []
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            in_col, out_col = st.columns(2)
            with in_col:
                input_names = st.multiselect("Choose input columns", options=list(df.columns), default=None)
            with out_col:
                output_name = st.multiselect("Choose output column", options=list(df.columns), default=None)
            x = df[input_names]
            y = df[output_name]

            if x.size != 0:
                ins, outs = st.columns(2)
                with ins:
                    st.write("Input data", x)
                if y.size != 0:
                    with outs:
                        st.write("Y range", y)
        return x, y, input_names, output_name