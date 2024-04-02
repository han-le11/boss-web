import numpy as np
import streamlit as st


# TODO
def _check_bounds(lower_bound, upper_bound):
    if not lower_bound < upper_bound:
        st.error("⚠️ Warning: lower bound has to be smaller than upper bound.")


def _return_bounds(X_names: list[str], d: int) -> (float, float):
    left_col, right_col = st.columns(2)
    with left_col:
        lower_bound = st.number_input(
            "Lower bound of {var} *".format(var=X_names[d]),
            format="%.5f",
            help="Minimum value of the variable that defines the search space",
        )
    with right_col:
        upper_bound = st.number_input(
            "Upper bound of {var} *".format(var=X_names[d]),
            format="%.5f",
            help="Maximum value of the variable that defines the search space",
        )
    return lower_bound, upper_bound


def input_x_bounds(X_names: list[str]) -> np.ndarray:
    """
    Display the number input widgets based on the dimension and input variable names.
    :param X_names: Input variable names
    """
    dimension = len(X_names)
    bounds = np.empty(shape=(dimension, 2))
    if X_names:
        st.write("Dimension of the search space is", dimension)
        for d in range(dimension):
            lower_bound, upper_bound = _return_bounds(X_names, d)
            bounds[d, 0] = lower_bound
            bounds[d, 1] = upper_bound
    return bounds


# TODO
def set_optional_params():
    """
    Set advanced, optional parameters.
    :return:
    """
    pass

