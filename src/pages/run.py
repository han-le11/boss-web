import numpy as np
import streamlit as st
from boss.pp.pp_main import PPMain
from tabs.init_manager_tab import InitManagerTab, set_input_var_bounds
from tabs.postprocessing_tab import PostprocessingTab
from tabs.run_boss import RunBOSS
from ui.file_handler import (
    find_bounds,
    choose_inputs_and_outputs,
    extract_col_data
)
from ui.page_config import PageConfig, customize_footer, remove_toggles

# Set page layout and settings
config = PageConfig(
    main_title="Run BOSS and Post-processing",
    tab_title="Run BOSS",
    header="Run BO on this page",
    icon=None,
)
config.init_states()
config.set_page()
config.set_main_title()
config.set_header()
customize_footer()
remove_toggles()

init_data_tab, run_tab, postprocess_tab = st.tabs(
    ["Create initial data", "Run BOSS", "Post-processing"]
)

with init_data_tab:
    bo_run = RunBOSS()
    init_tab = InitManagerTab()
    init_type, initpts, dim = init_tab.set_page()
    init_bounds, st.session_state["names_and_bounds"] = set_input_var_bounds(dim)

    if st.button("Generate points"):
        if np.isnan(init_bounds).any():
            st.error("Error: Please input names and bounds for all variables.")
        if len(list(st.session_state["names_and_bounds"].keys())) != dim + 1:
            st.error("Error: Please give a distinct name for each variable.")
        else:
            init_manager = init_tab.set_init_manager(
                init_type,
                initpts,
                init_bounds,
            )
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
        bo_run.data = st.data_editor(st.session_state["init_pts"])

        # df with bounds, only seen when downloaded, not shown in UI
        init_with_bounds = init_tab.add_bounds_to_dataframe(
            bo_run.data, st.session_state["names_and_bounds"]
        )
        init_tab.download_init_points(init_with_bounds)


with (run_tab):
    df_with_bounds = None
    bo_run.data = bo_run.upload_file()  # uploaded file
    if st.session_state["init_pts"] is not None:
        bo_run.bounds_exist = True
    else:
        bo_run.bounds_exist = find_bounds(bo_run.data)

    # THREE USE CASES:
    # Case 1. File doesn't have any bounds.
    if bo_run.data is not None and not bo_run.bounds_exist:
        (
            bo_run.X_vals,
            bo_run.Y_vals,
            bo_run.X_names,
            bo_run.Y_name,
        ) = choose_inputs_and_outputs(bo_run.data)
        bo_run.data = bo_run.data[bo_run.X_names + bo_run.Y_name]

    elif bo_run.bounds_exist:
        # Case 2. Parse bounds from generated initial points
        if (
                st.session_state["init_pts"] is not None
                and len(st.session_state["init_pts"].columns) == dim + 1
                and not np.isnan(init_bounds).any()
                and "" not in list(st.session_state["names_and_bounds"].keys())
        ):
            df_with_bounds = init_with_bounds

        # Case 3. Parse bounds from the uploaded file
        elif st.session_state["init_pts"] is None and bo_run.data is not None:
            df_with_bounds = bo_run.data

        # Parsing data from uploaded file
        if df_with_bounds is not None or bo_run.data is not None:
            bo_run.X_vals = extract_col_data(df=bo_run.data, keyword="input-var")
            bo_run.Y_vals = extract_col_data(df=bo_run.data, keyword="output-var")
            bo_run.dim = len(bo_run.X_vals[0])
            st.write("dimension: ", bo_run.dim)
            bo_run.data = df_with_bounds.copy(deep=False).iloc[:, :-bo_run.dim]

    if bo_run.data is not None and not bo_run.data.isnull().values.all():
        bo_run.data = st.data_editor(bo_run.data)
        bo_run.parse_bounds(df_with_bounds)
        bo_run.input_X_bounds(bo_run.bounds)
        st.write("x next: ", bo_run.X_next)

    # Choose minimize/maximize and noise variance
    col1, col2 = st.columns(2)
    with col1:
        bo_run.min_or_max = st.selectbox(
            "Minimize or maximize the target value?", options=("Minimize", "Maximize")
        )
    with col2:
        bo_run.noise = st.number_input(
            "Noise variance",
            min_value=0.0,
            format="%.5f",
            help="Estimated variance for the Gaussian noise",
        )

    if st.button("Run BOSS"):
        if st.session_state["init_pts"] is not None or bo_run.data is not None:
            bo_run.res = bo_run.run_boss()
            st.write(f"y min: {bo_run.Y_vals.min()}, y max {bo_run.Y_vals.max()}")
            bo_run.display_result()
            bo_run.display_next_acq()

    if bo_run.data is not None and bo_run.X_next is not None:
        bo_run.concat_next_acq()
        bo_run.data = st.data_editor(bo_run.data)
        bo_run.download_next_acq(bo_run.data)

with postprocess_tab:
    if st.session_state["bo_result"] is not None:
        bo_run.display_result()
        pp = PostprocessingTab(st.session_state["bo_result"], bo_run.X_names)
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
