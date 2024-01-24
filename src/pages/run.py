import logging
import numpy as np
import pandas as pd
import streamlit as st
from boss.bo.bo_main import BOMain
from boss.pp.pp_main import PPMain
from tabs.init_manager_tab import InitManagerTab, set_input_var_bounds
from tabs.postprocessing_tab import PostprocessingTab
from ui.page_config import PageConfig, customize_footer, remove_toggles
from ui.boss_run_params import input_x_bounds, set_y_range, parse_data_and_bounds
from ui.file_handler import upload_file, choose_inputs_and_outputs
from ui.result_displayer import display_result, display_next_acq

# Initialization of session_state
if "bo_result" not in st.session_state:
    st.session_state["bo_result"] = None
if "names_and_bounds" not in st.session_state:
    st.session_state["names_and_bounds"] = None
if "init_pts" not in st.session_state:
    st.session_state["init_pts"] = None
for k, v in st.session_state.items():
    st.session_state[k] = v

# Set page layout and so on
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

# Create tabs
test_tab, init_data_tab, run_tab, postprocess_tab = st.tabs(
    ["Test tab", "Create initial data", "Run BOSS", "Post-processing"]
)

with test_tab:
    df = pd.DataFrame(
        [
            {"var": "x", "number": 4, "bool": True},
            {"var": "y", "number": 5, "bool": False},
            {"var": "z", "number": 3, "bool": True},
        ]
    )
    edited_df = st.data_editor(df)

with init_data_tab:
    init_tab = InitManagerTab()
    init_tab.add_var_names.clear()
    init_type, initpts, dim = init_tab.set_page()
    init_bounds, st.session_state["names_and_bounds"] = set_input_var_bounds(dim)
    init_manager = init_tab.set_init_manager(
        init_type,
        initpts,
        init_bounds,
    )

    if st.button("Generate points"):
        if np.isnan(init_bounds).any():
            st.error("Error: Please input names and bounds for all variables.")
        else:
            # return init points
            init_pts = init_manager.get_all()
            # concatenate an empty column for target values and save to session state
            st.session_state["init_pts"] = init_tab.add_var_names(
                init_pts, st.session_state["names_and_bounds"]
            )

    if (
        st.session_state["init_pts"] is not None
        and len(st.session_state["init_pts"].columns) == dim + 1
        and not np.isnan(init_bounds).any()
        and "" not in list(st.session_state["names_and_bounds"].keys())
    ):
        # return an editable array
        edited_df = st.data_editor(st.session_state["init_pts"])

        # this df has concatenated bounds which is not shown in UI, only seen when downloaded
        init_with_bounds = init_tab.add_bounds_to_dataframe(
            edited_df, st.session_state["names_and_bounds"]
        )
        init_tab.download_init_points(init_with_bounds)

with run_tab:
    st.markdown(
        "#### BOSS optimizes by using your input data and suggests the next acquisition."
    )

    X_vals = []
    X_names = []
    X_bounds = []
    Y_vals = []
    y_min, y_max = (float, float)

    def dummy_function(_):
        pass

    def run_boss():
        bo = BOMain(
            dummy_function,
            bounds=X_bounds,
            yrange=[y_min, y_max],
            kernel="rbf",
            noise=noise_variance,
            iterpts=0,
        )
        if min_or_max == "Minimize":
            result = bo.run(X_vals, Y_vals)
        else:
            result = bo.run(X_vals, -Y_vals)
        st.session_state["bo_result"] = result  # write BO result to session state
        return result

    if (
        st.session_state["init_pts"] is not None
        and len(st.session_state["init_pts"].columns) == dim + 1
        and not np.isnan(init_bounds).any()
        and "" not in list(st.session_state["names_and_bounds"].keys())
    ):
        X_vals, X_names, Y_vals, X_bounds, y_min, y_max = parse_data_and_bounds(
            init_with_bounds, dim
        )
    else:
        uploaded_file = upload_file()
        X_vals, Y_vals, X_names, Y_name = choose_inputs_and_outputs(uploaded_file)
        y_min, y_max = set_y_range(y_values=Y_vals, y_name=Y_name)
        X_bounds = input_x_bounds(X_names)

    # Input fields for minimize/maximize and noise variance
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
        # Run with generated initial points
        if st.session_state["init_pts"] is not None:
            try:
                res = run_boss()
                display_result(res, min_or_max, X_names)
                display_next_acq(res, X_names)
            except ValueError:
                st.error("Error: Have you input all required fields?")

        # Run with an arbitrary file
        elif st.session_state["init_pts"] is None and not np.isnan(X_bounds).any():
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
        else:
            st.error("Error: Have you input all required fields?")

with postprocess_tab:
    st.markdown("####Get plots and data files after optimizing with BOSS.")

    if st.session_state["bo_result"] is not None:
        display_result(st.session_state["bo_result"], min_or_max, X_names)
        pp = PostprocessingTab(st.session_state["bo_result"], X_names)

        col1, col2 = st.columns(2)
        with col1:
            pp_iters = pp.input_pp_iters()

        # plot_models_or_not = pp.plot_models_or_not()
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
