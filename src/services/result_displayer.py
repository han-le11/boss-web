from pathlib import Path
import numpy as np
import streamlit as st


def show_progress_bar():
    progress_text = "Operation in progress. Please wait."
    prog_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        prog_bar.progress(percent_complete + 1, text=progress_text)


def display_result(res, min_or_max, x_names):
    """
    Display the global optimal location and prediction.
    :param res:
    :param min_or_max:
    :param x_names: string list of variable names
    :return:
    """
    x_glmin = res.select("x_glmin", -1)  # global min location prediction
    x_glmin = np.around(x_glmin, decimals=3).tolist()

    mu_glmin = res.select("mu_glmin", -1)  # global min prediction from the last iteration
    mu_glmin = np.around(mu_glmin, decimals=4)

    if x_names:
        if min_or_max == "Maximize":
            st.success(f"Predicted global maximum: {-mu_glmin} at {x_names} = {x_glmin}", icon="✅")
        else:
            st.success(f"Predicted global minimum: {mu_glmin} at {x_names} = {x_glmin}", icon="✅")


def display_next_acq(res, X_names):
    x_next = res.get_next_acq(-1)
    if X_names:
        for i in range(len(X_names)):
            st.success("Next acquisition: {} for {}".format(np.around(x_next[i], decimals=4),
                                                            X_names[i]), icon="🔍")
    return None


def download_boss_out():
    out_path = Path("./boss.out")
    if 'boss_out' not in st.session_state:
        st.session_state.boss_out = out_path
    if out_path.is_file:
        st.download_button(label="Download summary", data=out_path)
    else:
        st.error("Result summary file does not exist.")






