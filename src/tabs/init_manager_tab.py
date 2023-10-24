import streamlit as st
import numpy as np
import pandas as pd
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


def set_input_var_bounds(dimension):
    bounds = np.ones(shape=(dimension, 2)) * np.nan
    names_and_bounds = dict()
    for d in range(dimension):
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            var_name = st.text_input(
                f"Please write the name of variable {d + 1}",
                max_chars=50,
                help="A descriptive name will be great!",
            )

            if var_name:
                with col2:
                    bounds[d, 0] = st.number_input(
                        f"Lower bound of {var_name} *",
                        format="%.4f",
                    )
                with col3:
                    bounds[d, 1] = st.number_input(
                        f"Upper bound of {var_name} *",
                        format="%.4f",
                    )

                names_and_bounds.update({var_name: bounds[d, :]})
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        y_val_name = st.text_input(
                                f"Write the name of the target variable",
                                max_chars=50,
                                help="A descriptive name will be great!",
                                )
    names_and_bounds[y_val_name] = None
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
        st.info(f"Info: Now dimension of the search space is set to {dimension}.")
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

    def record_generated_init_points(self, points):
        self.init_pts = points

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
        xy_data = np.concatenate((bounds, y_vals), axis=1)  # concatenate to a new column
        return xy_data

    @staticmethod
    def add_fields_for_y_vals(init_array, names_and_bounds):
        names = names_and_bounds.keys()
        # st.write("test col names: ", names)
        y_vals = np.ones(shape=(init_array.shape[0], 1)) * np.nan
        xy_data = np.concatenate((init_array, y_vals), axis=1)  # concatenate a new column
        df = pd.DataFrame(data=xy_data,
                          columns=names
                          )
        return df
