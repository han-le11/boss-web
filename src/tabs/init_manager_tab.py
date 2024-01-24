import numpy as np
import pandas as pd
import streamlit as st
from boss.bo.initmanager import InitManager


def choose_init_type() -> str:
    init_type = st.selectbox(
        "Select the type of initial points",
        options=("sobol", "random", "grid"),
        help="Select method for creating the initial sampling locations",
    )
    return init_type


def input_init_points() -> int:
    initpts = st.number_input(
        "How many initial data points to generate?",
        min_value=1,
        value=5,  # When this widget first renders, its value is 5
        step=1,
        help="The number of initial data points to create",
    )
    return initpts


def set_input_var_bounds(dimension) -> (np.array, dict):
    """
    Return an array of input bounds and a dictionary of variable names and corresponding bounds.
    :param dimension:
    :return:
    bounds: input bounds, which is used to generate initial points with InitManager.
    names_and_bounds: a dictionary of variable names and corresponding bounds.
    """
    bounds = np.ones(shape=(dimension, 2)) * np.nan
    names_and_bounds = dict()
    for d in range(dimension):
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            var_name = st.text_input(
                f"Please write the name of variable {d + 1}",
                max_chars=50,
                help="A descriptive name will be great!",
                key=f"var {d}",
            )

            if var_name:
                with col2:
                    bounds[d, 0] = st.number_input(
                        f"Lower bound of {var_name} *",
                        format="%.4f",
                        key=f"lower {d}",
                        value=None,
                    )
                with col3:
                    bounds[d, 1] = st.number_input(
                        f"Upper bound of {var_name} *",
                        format="%.4f",
                        key=f"upper {d}",
                        value=None,
                    )
                names_and_bounds.update({var_name: bounds[d, :]})

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        y_val_name = st.text_input(
            f"Write the name of the target variable",
            max_chars=50,
            help="A descriptive name will be great!",
        )
    names_and_bounds[y_val_name] = None  # for target values, bounds are assigned None
    return bounds, names_and_bounds


class InitManagerTab:
    def __init__(self):
        self.init_pts = []
        self.var_names = []
        self.points_dict = dict

    @staticmethod
    def set_page():
        st.warning("This tab is under development.", icon="⚠️")
        st.markdown(
            "#### If you have not had any data, create initial data points here."
        )
        st.markdown(
            "You can take these initial data point values and, for example, run experiments with them and record "
            "values of the target variable. "
            "Then, you can optimize with this data in tab Run BOSS."
        )
        right, centre, left = st.columns(3, gap="large")
        with right:
            init_type = choose_init_type()
        with centre:
            initpts = input_init_points()
        with left:
            dimension = st.number_input(
                "Choose the dimension of the search space",
                value=2,  # When this widget first renders, its value is 2.
                min_value=1,
                step=1,
            )
        return init_type, initpts, dimension

    @staticmethod
    def set_init_manager(init_type, initpts, bounds) -> InitManager:
        """
        Return an InitManager object of the BOSS package.
        :param init_type:
        :param initpts:
        :param bounds:
        :return:
        """
        # init_manager = None
        # if np.isnan(bounds).any():
        #     st.warning("Error: Please input variable names and bounds.")
        # else:
        init_manager = InitManager(
            inittype=init_type,
            initpts=initpts,
            bounds=bounds,
        )
        return init_manager

    @staticmethod
    def download_init_points(points_array):
        df = pd.DataFrame(points_array)
        data = df.to_csv().encode("utf-8")
        st.download_button(
            label="Download",
            data=data,
            mime="text/csv",
        )

    @staticmethod
    def input_target_value(bounds):
        y_vals = np.full_like(a=bounds.size, fill_value=1) * np.nan
        if bounds.size != 0:
            for b in bounds:
                y_vals[b] = st.number_input(f"Target value for {b}")
        # concatenate to a new column
        xy_data = np.concatenate((bounds, y_vals), axis=1)
        return xy_data

    @staticmethod
    @st.cache_data(show_spinner=False)
    def add_var_names(init_arr, names_and_bounds):
        """
        Return a dataframe with tabulated variable names and corresponding bounds.
        :param init_arr: numpy array of initial points.
        :param names_and_bounds: dictionary
        :return:
        """
        var_names = list(names_and_bounds.keys())
        if "" in var_names:
            st.error("Please give a name for each variable.")
        else:
            y_vals = np.ones(shape=(init_arr.shape[0], 1)) * np.nan
            # concatenate a column to record y_vals
            xy_data = np.concatenate((init_arr, y_vals), axis=1)
            df = pd.DataFrame(data=xy_data, columns=var_names)
            return df

    @staticmethod
    def add_bounds_to_dataframe(init_df, names_and_bounds):
        """
        This dataframe is not shown to the user. It's only used for running BOSS:
        save generated initial points and target value as data,
        and input bounds.
        :param init_df: dataframe of initial points and recorded target values
        :param names_and_bounds: dictionary of variable names (key) and bounds (value)
        :return:
        """
        if init_df is None:
            st.warning("Error: Please input variable names and bounds.")
        elif "" in list(names_and_bounds.keys()):
            st.error("Please give a name for each variable.")

        # first, get variable names given by the user
        var_names = list(names_and_bounds.keys())

        # store column names for the final df
        df_col_names = list(names_and_bounds.keys())

        num_init_points = init_df.shape[0]  # number of generated init points
        dimension = len(var_names) - 1

        # make an empty array of size num_init_points x dimension
        bounds = np.zeros(shape=(num_init_points, dimension)) * np.nan

        for n in range(dimension):
            df_col_names.append(
                f"bound {var_names[n]}"
            )  # store column names for the returned df
            bound_n = names_and_bounds.get(var_names[n])
            bounds[0, n] = bound_n[0]
            bounds[1, n] = bound_n[1]

        # concatenate the column containing bounds
        final_array = np.concatenate((init_df, bounds), axis=1)
        final_df = pd.DataFrame(data=final_array, columns=df_col_names)
        return final_df
