import logging
import streamlit as st
from boss.bo.bo_main import BOMain
from boss.pp.pp_main import PPMain
from tabs.postprocessing_tab import PostprocessingTab
from ui.page_config import PageConfig, customize_footer, remove_toggles
from ui.boss_run_params import input_x_bounds, set_y_range
from ui.file_handler import upload_file, choose_inputs_and_outputs
from ui.result_displayer import display_result, display_next_acq

# Initialization
if "bo_result" not in st.session_state:
    st.session_state["bo_result"] = None
for k, v in st.session_state.items():
    st.session_state[k] = v

page_config = PageConfig(
    main_title="🏃‍♀️ Run BOSS and Post-processing",
    tab_title="Run BOSS",
    header="Run BO on this page",
    icon="🏃‍♀️",
)
page_config.set_page()
page_config.set_main_title()
page_config.set_header()
customize_footer()
remove_toggles()

run_tab, postprocess_tab = st.tabs(
    ["Run BOSS", "Post-processing"]
)
logger = logging.getLogger("boss_server")


def dummy_function(_):
    pass


def run_boss():
    bo = BOMain(
        dummy_function,
        bounds=bounds,
        yrange=[y_min, y_max],
        kernel="rbf",
        noise=noise_variance,
        iterpts=0,
    )
    if min_or_max == "Minimize":
        result = bo.run(X_vals, Y_vals)
    else:
        result = bo.run(X_vals, -Y_vals)
    st.session_state["bo_result"] = result  # write to session state
    return result


with run_tab:
    st.markdown(
        "#### BOSS optimizes using your input data and suggests the next acquisition."
    )

    uploaded_file = upload_file()
    X_vals, Y_vals, X_names, Y_name = choose_inputs_and_outputs(uploaded_file)
    y_min, y_max = set_y_range(y_values=Y_vals, y_name=Y_name)
    bounds = input_x_bounds(X_names)

    col1, col2 = st.columns(2)
    with col1:
        min_or_max = st.selectbox(
            "Minimize or maximize the target value?", options=("Minimize", "Maximize")
        )
    with col2:
        noise_variance = st.number_input(
            "Noise variance",
            min_value=0.0,
            format="%.7f",
            help="Estimated variance for the Gaussian noise",
        )

    if st.button("Run BOSS"):
        try:
            res = run_boss()
            display_result(res, min_or_max, X_names)
            display_next_acq(res, X_names)
        # except AssertionError:
        #     st.error(
        #         "Error: Have you input all required fields? "
        #         "Make sure that the lower bound of a variable is smaller than its upper bound."
        #     )
        except ValueError:
            st.error("Error: Have you input all required fields?")

with postprocess_tab:
    st.markdown("#### Get plots and data files after optimizing with BOSS.")

    if st.session_state["bo_result"] is not None:
        display_result(st.session_state["bo_result"], min_or_max, X_names)
        pp = PostprocessingTab(st.session_state["bo_result"], X_names)

        col1, col2 = st.columns(2)
        with col1:
            pp_iters = pp.input_pp_iters()

        pp_acq_funcs, pp_slice = pp.plot_acqfn_or_slice()

        if st.button("Run post-processing"):
            try:
                post = PPMain(
                    st.session_state["bo_result"],
                    pp_models=True,
                    pp_model_slice=pp_slice,
                    pp_acq_funcs=pp_acq_funcs,
                )
                post.run()
                pp.display_model_and_uncertainty()
                pp.display_acqfns()
            except AttributeError:
                st.error("Have you run BOSS first in the tab Run BOSS?")
    else:
        st.warning(
            "⚠️ No optimization results available. Please optimize first in the tab Run BOSS."
        )
