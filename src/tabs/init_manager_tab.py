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
    # When this widget first renders, the default value is 5
    initpts = st.number_input(
        "How many initial data points to generate?",
        min_value=1,
        value=5,
        step=1,
        help="The number of initial data points to create",
    )
    return initpts


def set_input_var_bounds(dimension) -> np.ndarray:
    bounds = np.empty(shape=(dimension, 2))
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
    # st.write(bounds)
    return bounds


class InitManagerTab:

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
                value=2,
                min_value=1,
                step=1,
            )
        st.info(f"Info: Now dimension of the search space is set to {dimension}.")
        return init_type, initpts, dimension

    @staticmethod
    def set_init_manager(init_type, initpts, bounds):
        init_manager = None
        if bounds.size != 0:
            init_manager = InitManager(
                inittype=init_type,
                initpts=initpts,
                bounds=bounds,
            )
        else:
            st.warning("Error: Please input variable names and bounds.")
        return init_manager

    @staticmethod
    def download_init_points(init_points):
        df = pd.DataFrame(init_points)
        data = df.to_csv().encode("utf-8")
        st.download_button(
            label="Download",
            data=data,
            mime="text/csv",
        )
