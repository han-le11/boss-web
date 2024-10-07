import numpy as np
import pandas as pd
import tomli_w
import streamlit as st
from boss.bo.bo_main import BOMain


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
            X_names=None,
            noise=0.0,
            res=None,
    ):
        self.data = data
        self.bounds = bounds
        self.bounds_exist = False
        self.X_names = X_names or []
        self.Y_name = None
        self.dim = None
        self.kernel = "rbf"
        self.min = "yes"  # yes if minimize, no if maximize
        self.noise = noise
        self.X_next = None
        self.results = res
        self.has_run = False
        self.dload_data = None  # data format only for download, not displayed in UI

    @property
    def X_vals(self):
        """
        Return the input values.

        :return:
        X_vals: ndarray
            Numpy array of the X values.
        """
        return self.data[self.X_names].to_numpy()

    @property
    def Y_vals(self):
        """
        Return the output values.

        :return:
        Y_vals: ndarray
            Numpy array of the Y values.
        """
        return self.data[self.Y_name].to_numpy()

    def choose_inputs_and_outputs(self) -> None:
        """
        If there is no bounds in the uploaded file, display widgets that let users choose at least one column
        for input variable(s) and only one column for target variable.

        :return: None
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
                "Choose one output variable *",
                options=list(self.data.columns),
                default=None,
                max_selections=1,
            )
        self.dim = len(self.X_names)
        self.data = self.data[self.X_names + self.Y_name]

    def parse_params(self, df) -> None:
        """
        Return the variable names and bounds to run with BOMain object.

        :param df:
            Uploaded file, which is read into a dataframe.

        :return: None
        """
        bounds_array = df.filter(regex="boss-bound").dropna().to_numpy()
        self.bounds = np.transpose(bounds_array)
        self.dim = self.bounds.shape[0]
        if "noise variance" in df.columns:
            self.noise = df["noise variance"][0]
        if "noise" in df.columns:
            self.noise = df["noise"][0]
        if "minimize" in df.columns:
            self.min = df["minimize"][0].lower()

    def _display_input_widgets(
            self, d: int, cur_bounds: np.ndarray = None
    ) -> (float, float):
        """
        Function to prompt the user to input lower and upper bounds for a variable.

        :param d: int
            Current dimension of the variable being considered.
        :param cur_bounds: ndarray
            Default values of lower and upper bounds in input widgets when they first render.

        :return:
        lower_bound, upper_bound: (float, float)
            The lower and upper bounds set by the user.
        """
        left, right = st.columns(2)

        # Display None if file doesn't contain bounds. Otherwise, use the bounds from file.
        with left:
            lower = st.number_input(
                "Lower bound of {var}".format(var=self.X_names[d]),
                format="%.3f",
                help="Minimum value of the variable that defines the search space",
                value=None if cur_bounds is None else cur_bounds[0],
                disabled=self.has_run,
            )
        with right:
            upper = st.number_input(
                "Upper bound of {var}".format(var=self.X_names[d]),
                format="%.3f",
                help="Maximum value of the variable that defines the search space",
                value=None if cur_bounds is None else cur_bounds[1],
                disabled=self.has_run,
            )
        return lower, upper

    def input_X_bounds(self, defaults=None) -> None:
        """
        Display the number input widgets based on the dimension and input variable names.

        :param defaults: None or ndarray
            Default values of lower and upper bounds in input widgets when they first render.

        :return: None
        """
        if not self.bounds_exist:
            self.bounds = np.empty(shape=(self.dim, 2))
        for d in range(self.dim):
            cur_bounds = None if not self.bounds_exist else defaults[d]
            lower_b, upper_b = self._display_input_widgets(d, cur_bounds)
            self.bounds[d, 0] = lower_b
            self.bounds[d, 1] = upper_b

    def set_opt_params(self) -> None:
        """
        Set parameters for minimization/maximization choice and noise variance.

        :return: None
        """
        col1, col2 = st.columns(2)
        with col1:
            self.min = st.selectbox(
                "Minimize the output value?",
                options=("yes", "no"),
                disabled=self.has_run,
                index=0 if self.min.lower() == "yes" else 1,
                help="Choose yes if you want to minimize the output variable value. If you want to maximize it, "
                     "choose no."
            )
        with col2:
            self.noise = st.number_input(
                "Noise variance",
                min_value=0.0,
                value=self.noise,
                format="%.5f",
                help="Estimated variance for the Gaussian noise",
                disabled=self.has_run,
            )

    @staticmethod
    def verify_bounds(bounds) -> bool:
        """
        For each variable, check if the lower bound is smaller than the upper bound.

        :return: bool
        """
        if bounds is None:
            st.error("⚠️ Please choose bounds for all variables.")
            return False
        else:
            if np.isnan(bounds).any():
                st.error("⚠️ Please set valid bounds for all variables.")
            if not np.all(bounds[:, 0] < bounds[:, 1]):
                st.error("⚠️ Lower bound has to be smaller than upper bound.")
                return False
            if not np.isnan(bounds).any() and np.all(bounds[:, 0] < bounds[:, 1]):
                return True

    def verify_data(self):
        st.write("current data \n", self.data)
        if self.data.isnull().values.any():
            st.error("⚠️ Please fill in the empty cells or download the data if you want to continue later.")
            return False
        else:
            return True

    def run_boss(self) -> None:
        """
        Run BOSS with the given parameters.

        :return: None
        """
        bo = BOMain(
            f=dummy_func,
            bounds=self.bounds,
            kernel=self.kernel,
            noise=self.noise,
            iterpts=0,
        )
        if self.min.lower() == "yes":
            self.results = bo.run(self.X_vals, self.Y_vals)
        elif self.min.lower() == "no":
            self.results = bo.run(self.X_vals, -self.Y_vals)
        self.has_run = True

    def display_result(self) -> None:
        """
        Display the global optimal location and prediction returned by BOSS.

        :return: None
        """
        if self.results is not None:
            x_glmin = self.results.select("x_glmin", -1)  # global min
            x_glmin = np.around(x_glmin, decimals=3)

            # global min prediction from the last iteration
            mu_glmin = self.results.select("mu_glmin", -1)
            mu_glmin = np.around(mu_glmin, decimals=3)
            glmin = {}
            for key, val in zip(self.X_names, x_glmin):
                glmin[key] = val
            res = ", ".join(str(key) + " = " + str(val) for key, val in glmin.items())
            if self.X_names is not None:
                if self.min.lower() == "no":
                    st.success(
                        f"Predicted global maximum: {self.Y_name[0]} = {-mu_glmin} at \n {res}.",
                        icon="✅",
                    )
                else:
                    st.success(
                        f"Predicted global minimum: {self.Y_name[0]} = {mu_glmin} at \n {res}.",
                        icon="✅",
                    )

    def display_next_acq(self) -> None:
        """
        Get and display the next acquisition location suggested by BOSS.

        :return: None
        """
        if self.results is not None:
            X_next = np.transpose(np.around(self.results.get_next_acq(-1), decimals=4))
            next_acq = {}
            for key, val in zip(self.X_names, X_next):
                next_acq[key] = val
            res = ", ".join(str(key) + " = " + str(val[0]) for key, val in next_acq.items())
            st.success(
                f"Next acquisition:  \n {res}",
                icon="✅",
            )

    def concat_next_acq(self) -> None:
        """
        Concatenate the next acquisition location to the data table.
        """
        if self.results is not None:
            X_next = self.results.get_next_acq(-1)
            if X_next is not None:
                XY_next = np.concatenate((X_next, np.ones(shape=(X_next.shape[0], 1)) * np.nan), axis=1)
                acq = pd.DataFrame(data=XY_next, columns=self.X_names + self.Y_name)
                self.data = pd.concat([self.data, acq], ignore_index=True)

    # TODO: Will be obsolete when we have the new csv format.
    def add_bounds(self) -> None:
        """
        Add the bounds to the data table, only used when downloading data.

        :return: None
        """
        var_names = self.X_names + self.Y_name  # store column names for the final df

        # Add "output-var " in front of output name so the file will be parsed correctly later
        if not self.bounds_exist:
            var_names[-1] = "output-var " + self.Y_name[0]

        bounds_arr = np.zeros(shape=(self.data.shape[0], self.dim)) * np.nan
        for d in range(self.dim):
            # filling the bounds array
            bounds_arr[0, d] = self.bounds[d][0]
            bounds_arr[1, d] = self.bounds[d][1]
            if not self.bounds_exist:
                var_names[d] = "input-var " + self.X_names[d]
            bound_name = self.X_names[d].removeprefix("input-var ")
            var_names.append(f"#boss-bound {bound_name}")  # store column names for the returned df

        data = np.concatenate((self.data, bounds_arr), axis=1)
        self.dload_data = pd.DataFrame(data=data, columns=var_names)

    def add_params(self) -> None:
        """
        Add the noise variance and to the dataframe. This function is only used for downloaded data.

        :return: None
        """
        self.dload_data["#noise variance"] = None
        self.dload_data["#noise variance"][0] = self.noise
        self.dload_data["#minimize"] = None
        self.dload_data["#minimize"][0] = self.min  # whether to minimize or maximize

    def data_to_str(self):
        """
        Write the metadata as comment lines (indicated by a hash at the start of a line).
        the data to string.
        """
        metadata = {
            'noise': self.noise,
            'min': self.min,
        }
        for d in range(self.dim):
            metadata['lower ' + self.X_names[d]] = self.bounds[d][0]
            metadata['upper ' + self.X_names[d]] = self.bounds[d][1]
        metadata_str = tomli_w.dumps(metadata)
        # remove double quotes
        metadata_str = metadata_str.replace('"', "")
        # add hash at the beginning of each line
        metadata_str = "\n".join(["#" + line for line in metadata_str[:-1].split("\n")])

        self.dload_data = metadata_str + "\n" + self.data.to_csv(index=False)
        st.download_button(
            label="Download new",
            data=self.dload_data,
            file_name="new_data.csv",
            mime="text/csv",
            key="new",
        )

    def download(self) -> None:
        """
        Make a download button for the dataset with bounds and other parameters.

        :return: None
        """
        self.add_bounds()
        # self.add_params()
        st.download_button(
            label="Download",
            data=self.dload_data.to_csv(index=False, encoding="utf-8"),
            file_name="boss_data.csv",
            mime="text/csv",
            key="download_data",
        )
