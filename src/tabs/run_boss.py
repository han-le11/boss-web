import numpy as np
import pandas as pd
import streamlit as st
from boss.bo.bo_main import BOMain
from boss.bo.results import BOResults
from streamlit.runtime.uploaded_file_manager import UploadedFile


def dummy_func(_):
    pass


class RunBOSS:
    """
    Class for running BOSS in the Run BOSS tab.
    """

    def __init__(
            self,
            data=None,
            bounds=None,
            bounds_exist=False,
            X_vals=None,
            Y_vals=None,
            X_names=None,
            min_or_max=None,
            noise=None,
            res=None,
    ):
        self.data = data
        self.bounds = bounds
        self.bounds_exist = bounds_exist
        self.X_vals = X_vals
        self.X_names = X_names
        self.Y_vals = Y_vals
        self.kernel = "rbf"
        self.min_or_max = min_or_max
        self.noise = noise
        self.res = res  # type: BOResults or None
        self.X_next = None
        self.arr_next_acq = None

    def upload_file(self):
        """
        Widget to upload a file, which is read into a dataframe.
        Display the "help" tip when hovering the mouse over the question mark icon.
        """
        if st.session_state["init_pts"] is None:
            message = "Please upload a csv file first"
        else:
            message = "Restart by uploading a csv file"

        self.data = st.file_uploader(
            label=message,
            type=["csv"],
            help="Your file should contain data for input variables and target variable",
        )
        if isinstance(self.data, UploadedFile):
            try:
                df = pd.read_csv(self.data, sep=":|;|,")
                return df
            except ValueError as err:
                st.error("Error: " + str(err) + ". Please check the file contents and re-upload.")

    def set_opt_params(self):
        """
        Set parameters for minimization/maximization choice and noise variance.
        :return:
        """
        col1, col2 = st.columns(2)
        with col1:
            self.min_or_max = st.selectbox(
                "Minimize or maximize the target value?",
                options=("Minimize", "Maximize"),
            )
        with col2:
            self.noise = st.number_input(
                "Noise variance",
                min_value=0.0,
                format="%.5f",
                help="Estimated variance for the Gaussian noise",
            )

    def run_boss(self):
        bo = BOMain(
            f=dummy_func,
            bounds=self.bounds,
            kernel=self.kernel,
            noise=self.noise,
            iterpts=0,
        )
        if self.min_or_max == "Minimize":
            self.res = bo.run(self.X_vals, self.Y_vals)
        else:
            self.res = bo.run(self.X_vals, -self.Y_vals)
        st.session_state["bo_result"] = self.res  # write BO result to session state
        return self.res

    def display_result(self) -> None:
        """
        Display the global optimal location and prediction returned by BOSS.
        """
        if self.res is not None:
            x_glmin = self.res.select("x_glmin", -1)  # global min location prediction
            x_glmin = np.around(x_glmin, decimals=3)
            x_glmin = x_glmin.tolist()

            # global min prediction from the last iteration
            mu_glmin = self.res.select("mu_glmin", -1)
            mu_glmin = np.around(mu_glmin, decimals=3)

            if self.X_names is not None:
                if self.min_or_max == "Maximize":
                    st.success(
                        f"Predicted global maximum: {-mu_glmin} at {self.X_names} = {x_glmin}",
                        icon="✅",
                    )
                else:
                    st.success(
                        f"Predicted global minimum: {mu_glmin} at {self.X_names} = {x_glmin}",
                        icon="✅",
                    )

    def display_next_acq(self) -> None:
        """
        Get and display the next acquisition location suggested by BOSS.
        """
        self.X_next = self.res.get_next_acq(-1)
        self.X_next = np.around(self.X_next, decimals=4)
        if self.X_names:
            pairs = dict(zip(self.X_names, self.X_next))
            for key, value in pairs.items():
                st.success(
                    f"Next acquisition: \n" f"{key} at {value}",
                    icon="🔍",
                )

    def get_next_acq(self):
        if self.res is not None:
            self.X_next = self.res.get_next_acq(-1)
            Y_val = np.ones(shape=(self.X_next.shape[0], 1)) * np.nan
            XY_next = np.concatenate((self.X_next, Y_val), axis=1)
            X_new = np.concatenate((self.data, XY_next), axis=0)
            self.arr_next_acq = st.data_editor(X_new)

    def download_next_acq(self) -> None:
        if self.res is not None and self.arr_next_acq is not None:
            df = pd.DataFrame(self.arr_next_acq)
            st.download_button(
                label="Download",
                data=df.to_csv(index=False).encode("utf-8"),
                mime="text/csv",
            )