import numpy as np
import streamlit as st
from boss.pp.pp_main import PPMain
from tabs.init_manager_tab import InitManagerTab, set_input_var_bounds
from tabs.postprocessing_tab import PostprocessingTab
from tabs.run_boss import RunBOSS
from ui.file_handler import find_bounds
from ui.page_config import PageConfig, customize_footer, remove_toggles

bo_run = RunBOSS()

# Set page layout and settings
config = PageConfig(
    main_title="Run BOSS and Post-processing",
    tab_title="Run BOSS",
    header="Run BO on this page",
    icon=None,
)
config.init_states()
config.set_page()
customize_footer()
remove_toggles()
if "bo_data" not in st.session_state:
    st.session_state.bo_data = bo_run.data
init_data_tab, run_tab, postprocess_tab = st.tabs(
    ["Create initial data", "Run BOSS", "Post-processing"]
)

with init_data_tab:
    init = InitManagerTab()
    init_type, initpts = init.set_page()
    init_bounds, st.session_state["names_and_bounds"] = set_input_var_bounds(init.dim)

    if st.button("Generate points"):
        if np.isnan(init_bounds).any():
            st.error("Error: Please input valid names and bounds for all variables.")
        if len(list(st.session_state["names_and_bounds"].keys())) != init.dim + 1:
            st.error("Error: Please give a distinct name for each variable.")
        else:
            init_manager = init.set_init_manager(
                init_type,
                initpts,
                init_bounds,
            )
            init_pts = init_manager.get_all()
            # concatenate an empty column for target values to df and save to session state
            st.session_state["init_pts"] = init.add_var_names(
                init_pts, st.session_state["names_and_bounds"]
            )

    if (
        st.session_state["init_pts"] is not None
        and len(st.session_state["init_pts"].columns) == init.dim + 1
        and not np.isnan(init_bounds).any()
        and "" not in list(st.session_state["names_and_bounds"].keys())
    ):
        bo_run.data = st.data_editor(st.session_state["init_pts"])
        # df with bounds, only seen when downloaded, not shown in UI
        bo_run.data = init.add_bounds_to_dataframe(
            bo_run.data, st.session_state["names_and_bounds"]
        )
        init.download_init_points(bo_run.data)
        st.session_state.bo_data = bo_run.data

with run_tab:
    # st.write("updated data: ", st.session_state.bo_data)
    bo_run.data = bo_run.upload_file()
    if st.session_state["init_pts"] is not None:
        # Set init points to None if uploaded file is different from init points
        if bo_run.data is not None and not st.session_state["init_pts"].equals(bo_run.data):
            st.session_state["init_pts"] = None
        else:
            bo_run.data = st.session_state.bo_data   # temporary: give data back to bo_run
    bo_run.bounds_exist = find_bounds(bo_run.data)

    # Case 1. File doesn't have any bounds.
    if bo_run.data is not None and not bo_run.bounds_exist:
        st.session_state.bo_data = bo_run.data
        bo_run.choose_inputs_and_outputs(bo_run.data)

    # Case 2 and 3. Parse bounds from uploaded file or initial data points
    elif bo_run.data is not None:
        bo_run.X_vals = bo_run.extract_col_data(keyword="input-var")
        bo_run.Y_vals = bo_run.extract_col_data(keyword="output-var")
        bo_run.dim = bo_run.X_vals.shape[1]
        st.session_state.bo_data = bo_run.data.copy(deep=True).iloc[:, : -bo_run.dim]

    if bo_run.data is not None and not bo_run.data.isnull().values.all():
        bo_run.parse_bounds(bo_run.data)
        bo_run.input_X_bounds(bo_run.bounds)
        bo_run.set_opt_params()
        if bo_run.bounds_exist:
            bo_run.data = bo_run.data.copy(deep=True).iloc[:, : -bo_run.dim]
        st.session_state.bo_data = st.data_editor(bo_run.data)

    if st.button("Run BOSS"):
        if bo_run.data is not None:
            bo_run.res = bo_run.run_boss()
            bo_run.display_result()
            bo_run.display_next_acq()
            bo_run.concat_next_acq()

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
