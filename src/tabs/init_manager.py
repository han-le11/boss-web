import numpy as np
import pandas as pd
import streamlit as st
from boss.bo.initmanager import InitManager


class InitPointsSetUp:
    """
    Class for setting up initial data points.
    Not to be confused with InitManager from BOSS, which is used to generate initial data points.
    """
    def __init__(self):
        self.dim = None
        self.min = True
        self.X_names = []
        self.Y_names = []
        self.data = None
        self.bounds = None
        self.num_init = 0  # number of generated initial points

    def set_init_widgets(self):
        st.markdown(
            "#### If you don't have any data, create initial data points here."
        )
        st.markdown(
            "Please set the parameters below. Type in variable names and bounds. "
            "Then, click on the 'Generate points' button. "
            "The initial data points will be shown in a table."
        )
        left, centre, right = st.columns(3, gap="large")
        with left:
            self.dim = st.number_input(
                "Choose the dimension of the search space",
                value=2,  # When this widget first renders, its value is 2.
                min_value=1,
                step=1,
            )
        with centre:
            self.num_init = st.number_input(
                "How many initial data points to generate?",
                min_value=1,
                value=5,  # When this widget first renders, its value is 5
                step=1,
                help="The number of initial data points to create",
            )
        with right:
            init_type = st.selectbox(
                "Select the type of initial points",
                options=("sobol", "random", "grid"),
                help="Select method for creating the initial sampling locations",
            )
        return init_type

    def set_init_manager(self, init_type: str, bounds) -> InitManager:
        """
        Return an InitManager instance of the InitManager class (from BOSS library).

        :param init_type: str
            The method of generating initial points.
        :param bounds:
            The bounds of all variables.

        :return:
        InitManager
        An instance of the InitManager class
        """
        if bounds is not None:
            if len(list(st.session_state["init_vars"].keys())) != self.dim + 1:
                st.error("⚠️ Please give a distinct name for each variable.")
            if np.isnan(bounds).any():
                st.error("⚠️ Please set bounds for all variables.")
            else:
                return InitManager(inittype=init_type,
                                   initpts=self.num_init,
                                   bounds=bounds,
                                   )

    @staticmethod
    def download_init_points(arr) -> None:
        if not isinstance(arr, pd.DataFrame):
            arr = pd.DataFrame(arr)
        data = arr.to_csv(index=False).encode("utf-8")
        st.warning("⚠️ If you don't record the values of the target variable now, please download this dataset and "
                   "record them later.")
        st.download_button(
            label="Download",
            file_name="boss_init.csv",
            data=data,
            mime="text/csv",
        )

    @staticmethod
    def add_var_names(init_arr, names_and_bounds) -> pd.DataFrame:
        """
        Return a dataframe with tabulated variable names and corresponding bounds.

        :param init_arr: ndarray
            An array of initial points for the input space.
        :param names_and_bounds: dict
            A dictionary of variable names (key) and bounds (value).

        :return df: pd.DataFrame
            A dataframe containing initial points and an empty column for recording the target variable.
        """
        # if len(list(st.session_state["init_vars"].keys())) == self.dim + 1:
        try:
            var_names = list(names_and_bounds.keys())
            empty_y_vals_col = np.ones(shape=(init_arr.shape[0], 1)) * np.nan
            # concatenate an empty column to record the target values
            xy_data = np.concatenate((init_arr, empty_y_vals_col), axis=1)
            df = pd.DataFrame(data=xy_data, columns=var_names)
            return df
        except ValueError:
            raise ValueError("⚠️ Please give a distinct name for each variable.")

    @staticmethod
    def add_bounds_to_dataframe(df, names_and_bounds) -> pd.DataFrame:
        """
        This dataframe is not shown to the user. It's only used to concatenate the
        input bounds to the dataframe of generated initial points.

        :param df: pd.DataFrame
            A dataframe to be concatenated.
        :param names_and_bounds:
            A dictionary of variable names (key) and bounds (value).

        :return final_df: pd.DataFrame
            A dataframe of tabular data and concatenated bounds.
        """
        if df is None:
            st.warning("Please input variable names and bounds.")
        elif "" in list(names_and_bounds.keys()):
            st.error("Please give a name for each variable.")
        else:
            var_names = [s for s in list(names_and_bounds.keys())]
            dimension = len(var_names) - 1
            num_init_points = df.shape[0]
            bounds = np.zeros(shape=(num_init_points, dimension)) * np.nan
            df_col_names = var_names  # store column names for the final df

            for n in range(dimension):
                cur_var = var_names[n].removeprefix("input-var ")
                df_col_names.append(
                    f"boss-bound {cur_var}"
                )  # store column names for the returned df
                bound_n = names_and_bounds.get(var_names[n])
                bounds[0, n] = bound_n[0]
                bounds[1, n] = bound_n[1]

            final_array = np.concatenate((df, bounds), axis=1)
            final_df = pd.DataFrame(data=final_array, columns=df_col_names)
            return final_df
