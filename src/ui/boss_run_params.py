import numpy as np
import pandas as pd
import streamlit as st
from dataclasses import dataclass


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


@dataclass
class BOSSRunParams:
    """
    Class for keeping track of BOSS run parameters parsed from dataframe of initial data points.
    """
    X_vals: np.ndarray
    X_names: list[str]
    Y_vals: np.ndarray
    X_bounds: np.ndarray


def parse_data_and_bounds(df: pd.DataFrame, dim: int):
    """
    If there's a dataframe of initial points in the session state, then parse input variables as X, target variables
    as Y.
    :param df: dataframe of initial data points
    :param dim: dimension
    :return: BOSSRunParams
    """
    n_columns = df.shape[1]
    X_vals = df.iloc[:, 0:dim].to_numpy()
    Y_vals = df.iloc[:, dim].to_numpy()
    X_names = df.columns.to_list()[0:dim]

    inputs, outputs = st.columns(2)
    with inputs:
        st.write("Input variables", X_vals)
    with outputs:
        st.write("Target variable", Y_vals)

    X_bounds = df.iloc[0:2, dim + 1:n_columns].to_numpy()
    st.write("Bounds", X_bounds)
    X_bounds = np.transpose(X_bounds)

    return BOSSRunParams(X_vals, X_names, Y_vals, X_bounds)
