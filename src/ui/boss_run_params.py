import numpy as np
import streamlit as st


# TODO
def _check_bounds(lower_bound, upper_bound):
    """
    Check if the lower bound is smaller than the upper bound.
    :param lower_bound:
    :param upper_bound:
    :return:
    """
    if not lower_bound < upper_bound:
        st.error("⚠️ Warning: lower bound has to be smaller than upper bound.")


def _display_input_widgets_X_bounds(X_names: list[str], dim: int, lower_and_upper_bounds=None) -> (float, float):
    """
    Function to prompt the user to input lower and upper bounds for a variable.

    :param X_names: List of variable names.
    :param dim: Dimension of the search space.
    :param lower_and_upper_bounds: Default values of input widgets when they first render.
    :return: Lower and upper bounds set by the user.
    """
    left_col, right_col = st.columns(2)
    lower_and_upper_bounds = np.array([0.0, 0.0]) if lower_and_upper_bounds is None else lower_and_upper_bounds
    with left_col:
        lower_bound = st.number_input(
            "Lower bound of {var}".format(var=X_names[dim]),
            format="%.5f",
            help="Minimum value of the variable that defines the search space",
            value=lower_and_upper_bounds[0],
        )
    with right_col:
        upper_bound = st.number_input(
            "Upper bound of {var}".format(var=X_names[dim]),
            format="%.5f",
            help="Maximum value of the variable that defines the search space",
            value=lower_and_upper_bounds[1],
        )
    return lower_bound, upper_bound


def input_X_bounds(X_names: list[str], lower_and_upper_bounds=None) -> np.ndarray:
    """
    Display the number input widgets based on the dimension and input variable names.

    :param X_names: Input variable names
    :param lower_and_upper_bounds: Default value of input widgets when they first render.
    :return: Lower and upper bounds set by the user.
    """
    dimension = len(X_names)
    bounds = np.empty(shape=(dimension, 2))
    if X_names:
        for d in range(dimension):
            lower_and_upper = np.array([0.0, 0.0]) if lower_and_upper_bounds is None else lower_and_upper_bounds[d]
            lower_bound, upper_bound = _display_input_widgets_X_bounds(X_names, d, lower_and_upper)
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
