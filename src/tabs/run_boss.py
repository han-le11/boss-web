import numpy as np
import pandas as pd
import tomli_w
import streamlit as st
from boss.bo.bo_main import BOMain


def dummy_func(_):
    pass


class RunBOSS:
    """
    Class for running BOSS.
    """

    def __init__(
            self,
            run_help=None,
            data=None,
            bounds=None,
            X_names=None,
            noise=0.0,
            res=None,
    ):
        self.dim = run_help.dim if run_help is not None else None
        self.data = data
        self.bounds = bounds
        self.has_metadata = False
        self.X_names = X_names or []
        self.Y_names = None
        self.kernel = "rbf"
        self.min = True  # True if minimize, False if maximize
        self.noise = noise
        self.num_init = 0  # number of points that can be treated as initial points
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
        return self.data[self.Y_names].to_numpy()

    def strip_white_spaces(self) -> None:
        """
        Remove leading, trailing, and in-between whitespace in variable names (X_name and Y_name) if there is any.
        """
        for x in self.X_names:
            x.strip().replace(" ", "")
        for y in self.Y_names:
            y.strip().replace(" ", "")

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
                help="Do not use empty space in variable names."
            )
        with out_col:
            self.Y_names = st.multiselect(
                "Choose one output variable *",
                options=list(self.data.columns),
                default=None,
                max_selections=1,
                help="Do not use empty space in variable names."
            )
        self.strip_white_spaces()
        self.dim = len(self.X_names)
        self.data = self.data[self.X_names + self.Y_names]

    def parse_params(self, metadata) -> None:
        """
        Return the variable names and bounds to run with BOMain object.

        :param metadata: dict
            Metadata obtained from the uploaded file.

        :return: None
        """
        self.num_init = metadata.get('num-init')
        self.noise = metadata.get('noise', 0)
        self.min = metadata.get('min', True)
        self.data.columns = [c.strip().replace(" ", "") for c in self.data.columns]
        # Input vars are the ones that have bounds in the metadata
        self.X_names = [c for c in self.data.columns if c in metadata.keys()]
        # Output vars are the ones that do not have bounds in the metadata, as their [min, max] is used as default
        self.Y_names = [c for c in self.data.columns if c not in metadata.keys()]
        self.bounds = np.array([metadata.get(x, None) for x in self.X_names])
        self.dim = self.bounds.shape[0]

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

        # Display None if uploaded file doesn't contain bounds. Otherwise, use the bounds from file.
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

    def input_X_bounds(self, defaults: str | None = None) -> None:
        """
        Display the number input widgets accordingly to the set dimension and input variable names.
        If the uploaded file contains the bounds of input variables, prefill widgets with those bounds.

        :param defaults: ndarray or None
            Default values of lower and upper bounds in input widgets when they first render.
        :return: None
        """
        # if input/output variables have been selected we can
        # ask/display bounds and other keywords
        if len(self.X_names) > 0 and len(self.Y_names) >= 1:
            if not self.has_metadata:
                self.bounds = np.empty(shape=(self.dim, 2))  # array size: dim by 2 (lower bound and upper bound)
            for d in range(self.dim):
                cur_bounds = None if not self.has_metadata else defaults[d]
                lower_b, upper_b = self._display_input_widgets(d, cur_bounds)
                self.bounds[d, 0] = lower_b
                self.bounds[d, 1] = upper_b

    def set_opt_params(self) -> None:
        """
        Display the widgets for choosing minimization/maximization and noise variance.
        If the uploaded file contains these hyperparameters, prefill widgets with those information.

        :return: None
        """
        col1, col2 = st.columns(2)
        with col1:
            self.min = st.selectbox(
                "Minimize the output value?",
                options=(True, False),
                disabled=self.has_run,
                index=0 if self.min is True else 1,
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

    def verify_data(self) -> bool:
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
        if self.min:
            self.results = bo.run(self.X_vals, self.Y_vals)
        else:
            self.results = bo.run(self.X_vals, -self.Y_vals)
        # tell BOSS how many of our batches/data points to treat as initial points
        self.results.set_num_init_batches(self.num_init)
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
                if self.min is False:
                    st.success(
                        f"Predicted global maximum: {self.Y_names[0]} = {-mu_glmin} at \n {res}.",
                        icon="✅",
                    )
                else:
                    st.success(
                        f"Predicted global minimum: {self.Y_names[0]} = {mu_glmin} at \n {res}.",
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

        :return: None
        """
        if self.results is not None:
            X_next = self.results.get_next_acq(-1)
            if X_next is not None:
                XY_next = np.concatenate((X_next, np.ones(shape=(X_next.shape[0], 1)) * np.nan), axis=1)
                acq = pd.DataFrame(data=XY_next, columns=self.X_names + self.Y_names)
                self.data = pd.concat([self.data, acq], ignore_index=True)

    def add_metadata(self) -> None:
        """
        Add the metadata as comment lines (indicated by a hash '#' at the beginning of a line).
        Display a download button for data with the metadata.

        :return: None
        """
        metadata = {
            'noise': self.noise,
            'min': self.min,
            'num-init': self.num_init,
        }
        for d in range(0, self.dim):
            metadata[self.X_names[d]] = str(self.bounds[d].tolist())
        metadata_str = tomli_w.dumps(metadata)

        # remove double quotes
        metadata_str = metadata_str.replace('"', "")
        # remove any whitespaces (leading, trailing, in-between words)
        self.strip_white_spaces()

        # add hash at the beginning of each line
        metadata_str = "\n".join(["#" + line for line in metadata_str[:-1].split("\n")])
        self.dload_data = metadata_str + "\n" + self.data.to_csv(index=False)

    def download_data(self, widget_key: str) -> None:
        """
        Display a download button for data, with the metadata.

        :param widget_key: The key to make the download button widget unique.

        :return: None
        """
        st.download_button(
            label="Download",
            data=self.dload_data,
            file_name="boss_data.csv",
            mime="text/csv",
            key=widget_key,
        )


