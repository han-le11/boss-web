import numpy as np
import pandas as pd
import streamlit as st
from boss.bo.initmanager import InitManager


def set_input_var_bounds(dimension: int) -> (np.array, dict):
    """
    Return an array of input bounds and a dictionary of variable names and corresponding bounds.

    :param dimension: int
        dimension of the input values

    :return:
    bounds: ndarray
        An array of input bounds, which is used to generate initial points with InitManager.
    names_and_bounds: dict
        A dictionary of variable names (keys) and corresponding bounds (values).
    """
    bounds = np.ones(shape=(dimension, 2)) * np.nan
    st.session_state["init_vars"] = dict()
    for d in range(dimension):
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            var_name = st.text_input(
                f"Please write the name of variable {d + 1}",
                max_chars=50,
                help="A descriptive name will be great!",
                key=f"var_{d}_{st.session_state.input_key}",
            )

            if var_name:
                var_name = "input-var " + var_name
                with col2:
                    bounds[d, 0] = st.number_input(
                        f"Lower bound of {var_name} *",
                        format="%.3f",
                        key=f"lower {d}",
                        value=None,
                    )
                with col3:
                    bounds[d, 1] = st.number_input(
                        f"Upper bound of {var_name} *",
                        format="%.3f",
                        key=f"upper {d}",
                        value=None,
                    )
                st.session_state["init_vars"].update({var_name: bounds[d, :]})

    # Make one widget to input target variable name
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        y_name = st.text_input(
            f"Write the name of the target variable",
            max_chars=50,
            help="A descriptive name will be great!",
            key=f"target_{st.session_state.input_key}",
        )
        y_name = "output-var " + y_name
    st.session_state["init_vars"][y_name] = None  # for target values, bounds are assigned None
    return bounds


class InitManagerTab:
    def __init__(self):
        self.dim = None

    def set_page(self):
        st.markdown(
            "#### If you don't have any data, create initial data points here."
        )
        st.markdown(
            "Please set the parameters below. Type in variable names and bounds. "
            "Then, click on Create initial data. "
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
            initpts = st.number_input(
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
        return init_type, initpts

    def set_init_manager(self, init_type: str, initpts: int, bounds) -> InitManager:
        """
        Return an InitManager instance of the InitManager class (from BOSS library).

        :param init_type: str
            The method of generating initial points.
        :param initpts: int
            The number of initial data points.
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
                                   initpts=initpts,
                                   bounds=bounds,)

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

    def add_var_names(self, init_arr, names_and_bounds) -> pd.DataFrame:
        """
        Return a dataframe with tabulated variable names and corresponding bounds.

        :param init_arr: ndarray
            An array of initial points.
        :param names_and_bounds: dict
            A dictionary of variable names (key) and bounds (value).

        :return df: pd.DataFrame
            A dataframe containing initial points and an empty column for recording the target variable.
        """
        if len(list(st.session_state["init_vars"].keys())) != self.dim + 1:
            st.error("⚠️ Please give a distinct name for each variable.")
        else:
            var_names = list(names_and_bounds.keys())
            empty_y_vals_col = np.ones(shape=(init_arr.shape[0], 1)) * np.nan
            # concatenate an empty column to record the target values
            xy_data = np.concatenate((init_arr, empty_y_vals_col), axis=1)
            df = pd.DataFrame(data=xy_data, columns=var_names)
            return df

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
