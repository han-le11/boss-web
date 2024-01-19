import numpy as np
import pandas as pd
import streamlit as st


# TODO
def _check_bounds(lower_bound, upper_bound):
    if not lower_bound < upper_bound:
        st.error("⚠️ Warning: lower bound has to be smaller than upper bound.")


def _return_bounds(X_names, d) -> (float, float):
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


def input_x_bounds(X_names) -> np.ndarray:
    """
    Display the number input widgets based on the dimension and input variable names.
    :param X_names: list(str)
        Input variable names
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


def set_y_range(y_values, y_name) -> (float, float):
    """
    Find and display min value and max value of the target variable.
    These values are given to BOSS.
    """
    y_min, y_max = None, None
    if y_name and y_values.size != 0 or not np.isnan(y_values).any:
        y_min = np.amin(y_values)
        y_max = np.amax(y_values)
    # else:
    #     st.error("Please check that target values are filled.")
    return y_min, y_max


# TODO
def set_optional_params():
    """
    Set advanced, optional parameters
    :return:
    """
    pass


def dummy_function(_):
    pass


def parse_data_and_bounds(df, dim):
    """
    If there's a dataframe of initial points in the session state, then parse input variables as X, target variables
    as Y.
    :param df:
    :param dim:
    :return:
    """
    n_columns = df.shape[1]
    X_vals = df.iloc[:, 0:dim].to_numpy()
    Y_vals = df.iloc[:, dim].to_numpy()
    X_names = list(df.columns.values)[0:dim]
    y_name = list(df.columns.values)[dim]

    inputs, outputs = st.columns(2)
    with inputs:
        st.write("Input variables", X_vals)
    with outputs:
        st.write("Target variable", Y_vals)

    y_min, y_max = set_y_range(Y_vals, y_name)
    X_bounds = df.iloc[0:2, dim + 1:n_columns].to_numpy()
    st.write("Bounds", X_bounds)
    X_bounds = np.transpose(X_bounds)

    return X_vals, X_names, Y_vals, X_bounds, y_min, y_max
