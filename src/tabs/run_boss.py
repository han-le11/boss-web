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
            min_or_max='Minimize',
            noise=None,
            res=None,
    ):
        self.data = data
        self.bounds = bounds
        self.bounds_exist = bounds_exist
        self.X_names = X_names or []
        self.Y_name = None
        self.dim = None
        self.kernel = "rbf"
        self.min_or_max = min_or_max
        self.noise = noise
        self.X_next = None
        self.arr_next_acq = None
        self.results = res
        self.has_run = False

    @property
    def X_vals(self):
        return self.data[self.X_names].to_numpy()

    @property
    def Y_vals(self):
        return self.data[self.Y_name].to_numpy()

    def upload_file(self) -> pd.DataFrame:
        """
        Widget to upload a file, which is read into a dataframe.
        Display the "help" tip when hovering the mouse over the question mark icon.
        """
        self.data = st.file_uploader(
            label="Restart by uploading a csv file",
            type=["csv"],
            help="Your file should contain data for input variables and target variable",
        )
        if isinstance(self.data, UploadedFile):
            try:
                df = pd.read_csv(self.data, sep=":|;|,")
                return df
            except ValueError as err:
                st.error(
                    "Error: "
                    + str(err)
                    + ". Please check the file contents and re-upload."
                )

    def choose_inputs_and_outputs(self):
        """
        Display widgets that let users choose at least one column for input variable(s) and
        only one column for target variable.
        :param df:
            Dataframe read from the UploadedFile object (file uploaded by a user).
        """
        in_col, out_col = st.columns(2)

        with in_col:
            self.X_names = st.multiselect(
                "Choose input variables *",
                options=list(self.data.columns),
                default=None,
            )
        with out_col:
            self.Y_name = st.multiselect(
                "Choose one target variable *",
                options=list(self.data.columns),
                default=None,
                max_selections=1,
            )
        self.dim = len(self.X_names)
        self.data = self.data[self.X_names + self.Y_name]

    def extract_col_data(self, keyword: str) -> np.array:
        """
        Get the data where column name contains the given keyword.
        :param keyword: The keyword that the column name should contain.
        :return:
        array: np.array
            An array of the column(s) whose name contains the given keyword.
        """
        array = self.data.filter(regex=keyword).to_numpy()
        if array.size == 0:
            array = np.array([])
        return array

    def parse_bounds(self, df):
        """
        Return the variable names and bounds to run with BOMain object.
        :param df: Uploaded file, which is read into a dataframe.
        :return:
            tp_bounds_array: numpy array of the bounds
        """
        if self.bounds_exist:
            bounds_array = df.filter(regex="boss-bound").dropna().to_numpy()
            self.bounds = np.transpose(bounds_array)
            self.dim = self.bounds.shape[0]

    # TODO
    def _check_bounds(self, lower_bound, upper_bound):
        """
        Check if the lower bound is smaller than the upper bound.
        :param lower_bound:
        :param upper_bound:
        :return:
        """
        if not lower_bound < upper_bound:
            st.error("⚠️ Warning: lower bound has to be smaller than upper bound.")
        pass

    def _display_input_widgets(
            self, d, cur_bounds: np.ndarray = None
    ) -> (float, float):
        """
        Function to prompt the user to input lower and upper bounds for a variable.

        :param d: Current dimension of the variable being considered.
        :param cur_bounds: Default values of lower and upper bounds in input widgets when they first render.
        :return:
        lower_bound, upper_bound: Lower and upper bounds set by the user.
        """
        left_col, right_col = st.columns(2)
        cur_bounds = np.array([0.0, 0.0]) if cur_bounds is None else cur_bounds
        with left_col:
            lower_bound = st.number_input(
                "Lower bound of {var}".format(var=self.X_names[d]),
                format="%.5f",
                help="Minimum value of the variable that defines the search space",
                value=cur_bounds[0],
            )
        with right_col:
            upper_bound = st.number_input(
                "Upper bound of {var}".format(var=self.X_names[d]),
                format="%.5f",
                help="Maximum value of the variable that defines the search space",
                value=cur_bounds[1],
            )
        return lower_bound, upper_bound

    def input_X_bounds(self, defaults: np.ndarray = None):
        """
        Display the number input widgets based on the dimension and input variable names.

        :param defaults: Default values of lower and upper bounds in input widgets when they first render.
        """
        if self.bounds is None:
            self.bounds = np.empty(shape=(self.dim, 2))
        else:
            if not self.X_names:
                self.X_names = list(self.data)[: self.dim]
            if not self.Y_name:
                self.Y_name = [self.data.columns[self.dim]]
        self.dim = len(self.X_names)
        for d in range(self.dim):
            lower_and_upper = np.array([0.0, 0.0]) if defaults is None else defaults[d]
            lower_b, upper_b = self._display_input_widgets(d, lower_and_upper)
            self.bounds[d, 0] = lower_b
            self.bounds[d, 1] = upper_b

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

    # TODO
    def set_adv_params(self):
        """
        Set advanced, optional parameters.
        :return:
        """
        pass

    def run_boss(self):
        bo = BOMain(
            f=dummy_func,
            bounds=self.bounds,
            kernel=self.kernel,
            noise=self.noise,
            iterpts=0,
        )
        # st.write(f"y min: {self.Y_vals.min()}, y max {self.Y_vals.max()}")
        
        if self.min_or_max == "Minimize":
            self.results = bo.run(self.X_vals, self.Y_vals)
        else:
            self.results = bo.run(self.X_vals, -self.Y_vals)

        return self.results

    def display_result(self) -> None:
        """
        Display the global optimal location and prediction returned by BOSS.
        """
        if self.results is not None:
            x_glmin = self.results.select("x_glmin", -1)  # global min location prediction
            x_glmin = np.around(x_glmin, decimals=3)
            x_glmin = x_glmin.tolist()

            # global min prediction from the last iteration
            mu_glmin = self.results.select("mu_glmin", -1)
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
        if self.results is not None:
            X_next = self.results.get_next_acq(-1)
            X_next = np.around(X_next, decimals=4)
            if self.X_names:
                pairs = dict(zip(self.X_names, X_next))
                for key, value in pairs.items():
                    st.success(
                        f"Next acquisition: \n" f"{key} at {value}",
                        icon="🔍",
                    )

    def concat_next_acq(self):
        X_next = self.results.get_next_acq(-1)
        if X_next is not None:
            XY_next = np.concatenate(
                (X_next, np.ones(shape=(X_next.shape[0], 1)) * np.nan), axis=1
            )
            acq = pd.DataFrame(data=XY_next, columns=self.X_names + self.Y_name)
            self.data = pd.concat([self.data, acq], ignore_index=True)

    def download_next_acq(self) -> None:
        if self.results is not None:
            df = pd.DataFrame(self.data)
            st.download_button(
                label="Download",
                data=df.to_csv(index=False).encode("utf-8"),
                mime="text/csv",
            )
