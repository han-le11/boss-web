import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


class RunHelper:
    def __init__(self) -> None:
        self.file = None
        self.data = None
        self.bo_has_run = False

    def update_has_run(self):
        if self.bo_has_run:
            self.bo_has_run = False

    def upload_file(self) -> pd.DataFrame:
        """
        Widget to upload a file, which is read into a dataframe.
        Display the "help" tip when hovering the mouse over the question mark icon.
        """
        self.file = st.file_uploader(
            label="Restart by uploading a csv file",
            type=["csv"],
            help="Your file should contain data for input variables and target variable",
        )
        if isinstance(self.file, UploadedFile):
            try:
                df = pd.read_csv(self.file, sep=":|;|,")
                return df
            except ValueError as err:
                st.error(
                    "Error: "
                    + str(err)
                    + ". Please check the file contents and re-upload."
                )

    @staticmethod
    def download(df) -> None:
        st.download_button(
            label="Download",
            data=df.to_csv(index=False).encode("utf-8"),
            mime="text/csv",
            key="download_acq",
        )
