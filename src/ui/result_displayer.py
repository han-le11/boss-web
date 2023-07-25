import numpy as np
import streamlit as st


def display_result(res, min_or_max, x_names) -> None:
    """
    Display the global optimal location and prediction returned by BOSS.
    """
    x_glmin = res.select("x_glmin", -1)  # global min location prediction
    x_glmin = np.around(x_glmin, decimals=3)
    x_glmin = x_glmin.tolist()

    # global min prediction from the last iteration
    mu_glmin = res.select("mu_glmin", -1)
    mu_glmin = np.around(mu_glmin, decimals=3)

    if x_names:
        if min_or_max == "Maximize":
            st.success(
                f"Predicted global maximum: {-mu_glmin} at {x_names} = {x_glmin}",
                icon="✅",
            )
        else:
            st.success(
                f"Predicted global minimum: {mu_glmin} at {x_names} = {x_glmin}",
                icon="✅",
            )


def _get_next_acq(res):
    x_next = res.get_next_acq(-1)
    x_next = np.around(x_next, decimals=4)
    return x_next


def display_next_acq(res, X_names) -> None:
    """
    Get and display the next acquisition location suggested by BOSS.
    """
    x_next = res.get_next_acq(-1)
    x_next = np.around(x_next, decimals=4)
    if X_names:
        pairs = dict(zip(X_names, x_next))
        for key, value in pairs.items():
            st.success(
                f"Next acquisition: \n" f"{key} at {value}",
                icon="🔍",
            )


# TODO
def concatenate_next_acq_to_data():
    pass
