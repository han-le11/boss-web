import numpy as np
import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


class RunHelper:
    def __init__(self) -> None:
        self.res = None

    def download_data(self) -> None:
        if self.res is not None:
            new_data = self.res.copy(deep=True)
            st.download_button(
                label="Download",
                data=new_data.to_csv(index=False).encode("utf-8"),
                mime="text/csv",
                key="download_acq",
            )
