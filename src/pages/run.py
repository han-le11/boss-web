import numpy as np
import streamlit as st
from boss.pp.pp_main import PPMain
from tabs.init_manager_tab import InitManagerTab, set_input_var_bounds
from tabs.postprocessing_tab import PostprocessingTab
from tabs.run_boss import RunBOSS
from ui.boss_run_params import input_X_bounds
from ui.file_handler import (
    upload_file,
    find_bounds,
    parse_bounds,
    choose_inputs_and_outputs,
    extract_col_data,
)
from ui.page_config import PageConfig, customize_footer, remove_toggles

# Initialization of session states
if "data" not in st.session_state:
    st.session_state["data"] = None
if "bo_result" not in st.session_state:
    st.session_state["bo_result"] = None
if "names_and_bounds" not in st.session_state:
    st.session_state["names_and_bounds"] = None
if "init_pts" not in st.session_state:
    st.session_state["init_pts"] = None
for k, v in st.session_state.items():
    st.session_state[k] = v

# Set page layout and settings
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
init_data_tab, run_tab, postprocess_tab = st.tabs(
    ["Create initial data", "Run BOSS", "Post-processing"]
)

with init_data_tab:
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
        # return an editable array
        edited_df = st.data_editor(st.session_state["init_pts"])

        # this df has concatenated bounds which is not shown in UI, only seen when downloaded
        init_with_bounds = init_tab.add_bounds_to_dataframe(
            edited_df, st.session_state["names_and_bounds"]
        )
        init_tab.download_init_points(init_with_bounds)


with run_tab:
    data = upload_file()  # uploaded file
    data_with_bounds = None
    bo_run = RunBOSS()

    if st.session_state["init_pts"] is not None:
        bo_run.bounds_exist = True
    else:
        bo_run.bounds_exist = find_bounds(data)

    # Special case: File doesn't have bounds. Manually choose variables and their names
    if data is not None and not bo_run.bounds_exist:
        bo_run.X_names = list(data.columns)[:dim]
        bo_run.X_vals, bo_run.Y_vals, bo_run.X_names, bo_run.Y_name = choose_inputs_and_outputs(data)
        bo_run.data = data[bo_run.X_names + bo_run.Y_name]

    else:
        # Parse data immediately from generated initial points
        if (
            st.session_state["init_pts"] is not None
            and len(st.session_state["init_pts"].columns) == dim + 1
            and not np.isnan(init_bounds).any()
            and "" not in list(st.session_state["names_and_bounds"].keys())
        ):
            data_with_bounds = init_with_bounds
            # bo_run.data = init_with_bounds
            # bo_run.X_names = list(init_with_bounds.columns)[:dim]
            # bo_run.X_vals = extract_col_data(df=init_with_bounds, keyword="input-var")
            # bo_run.Y_vals = extract_col_data(df=init_with_bounds, keyword="output-var")

        elif st.session_state["init_pts"] is None and data is not None:
            # Parse bounds from the uploaded file
            data_with_bounds = data
            # bo_run.X_names = list(data.columns)[:dim]
            # bo_run.data = data.iloc[:, :-2]
            # bo_run.X_vals = extract_col_data(df=data, keyword="input-var")
            # bo_run.Y_vals = extract_col_data(df=data, keyword="output-var")

        bo_run.data = data_with_bounds.copy(deep=True).iloc[:, :-2]
        bo_run.X_names = list(data_with_bounds.columns)[:dim]
        bo_run.X_vals = extract_col_data(df=data_with_bounds, keyword="input-var")
        bo_run.Y_vals = extract_col_data(df=data_with_bounds, keyword="output-var")

    if bo_run.data is not None:
        st.write(bo_run.data)
        bounds_from_file = parse_bounds(data_with_bounds)
        bo_run.bounds = input_X_bounds(bo_run.X_names, bounds_from_file)

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
        if st.session_state["init_pts"] is not None or data is not None:
            bo_run.res = bo_run.run_boss()
            bo_run.display_result()
            bo_run.display_next_acq()

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
