import numpy as np
import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


class RunHelper:
    def __init__(self) -> None:
        self.data = None

    def download(self) -> None:
        st.download_button(
            label="Download",
            data=self.data.to_csv(index=False).encode("utf-8"),
            mime="text/csv",
            key="download_acq",
        )




