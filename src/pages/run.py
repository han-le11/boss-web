import numpy as np
import streamlit as st
from boss.pp.pp_main import PPMain
from tabs.init_manager_tab import InitManagerTab, set_input_var_bounds
from tabs.postprocessing_tab import PostprocessingTab
from tabs.run_boss import RunBOSS
from tabs.run_helper import RunHelper
from ui.file_handler import find_bounds
from ui.page_config import PageConfig, customize_footer, remove_toggles

# Set page layout and settings
config = PageConfig(
    main_title="Run BOSS and Post-processing",
    tab_title="Run BOSS",
    header="Run BO on this page",
    icon=None,
)
config.set_page()
config.init_states()
customize_footer()
remove_toggles()

# Initialize a session state for RunBOSS if there isn't one
if st.session_state["bo_run"] is None:
    st.session_state["bo_run"] = RunBOSS()

# Initialize a session state for RunHelper if there isn't one
bo_run: RunBOSS = st.session_state["bo_run"]
run_help: RunHelper = RunHelper()

st.warning("⚠️ Please download your data before leaving. ")
if st.button("Clear all"):
    run_help.clear_data()

init_data_tab, run_tab, postprocess_tab = st.tabs(
    ["Create initial data", "Run BOSS", "Post-processing"]
)

with init_data_tab:
    init = InitManagerTab()
    init_type, initpts = init.set_page()
    init_bounds = set_input_var_bounds(init.dim)

    if st.button("Generate points"):
        if bo_run.verify_bounds(init_bounds):
            init_manager = init.set_init_manager(
                init_type,
                initpts,
                init_bounds,
            )
            init_pts = init_manager.get_all()
            # concatenate an empty column for target values to df and save to session state
            st.session_state["init_pts"] = init.add_var_names(
                init_pts, st.session_state["init_vars"]
            )

    # Display an editable df for initial points
    if (
            st.session_state["init_pts"] is not None
            and len(st.session_state["init_pts"].columns) == init.dim + 1
            and not np.isnan(init_bounds).any()
            and "" not in list(st.session_state["init_vars"].keys())
            and not bo_run.has_run
    ):
        bo_run.data = st.data_editor(st.session_state["init_pts"])
        # df with bounds, only seen when downloaded, not shown in UI
        bo_run.data = init.add_bounds_to_dataframe(
            bo_run.data, st.session_state["init_vars"]
        )
        init.download_init_points(bo_run.data)

with run_tab:
    if not bo_run.has_run:
        # Use init points if they exist. Otherwise, use uploaded file.
        if st.session_state["init_pts"] is None:
            bo_run.data = run_help.upload_file()

        # Only continue if some data exists
        if bo_run.data is not None:
            bo_run.bounds_exist = find_bounds(bo_run.data)
            # File doesn't have any bounds.
            if not bo_run.bounds_exist:
                bo_run.choose_inputs_and_outputs()

            # Parse parameters from uploaded file or initial data points
            else:
                bo_run.X_names = [c for c in bo_run.data.columns if "input-var" in c]
                bo_run.Y_name = [c for c in bo_run.data.columns if "output-var" in c]
                bo_run.dim = bo_run.X_vals.shape[1]
                bo_run.parse_params(bo_run.data)
                bo_run.data = bo_run.data[bo_run.X_names + bo_run.Y_name]

            # if input/output variables have been selected we can
            # ask/display bounds and other keywords
            if len(bo_run.X_names) > 0 and len(bo_run.Y_name) == 1:
                bo_run.input_X_bounds(bo_run.bounds)
                bo_run.set_opt_params()

    # BO has been run: disable input widgets and only display results
    elif bo_run.has_run:
        bo_run.input_X_bounds(bo_run.bounds)
        bo_run.set_opt_params()
        bo_run.display_result()
        bo_run.display_next_acq()

    # Display an editable dataframe
    if bo_run.data is not None and len(bo_run.X_names) > 0 and len(bo_run.Y_name) == 1:
        bo_run.data = st.data_editor(bo_run.data, key="edit_data")
        bo_run.download()

    # regardless of whether BO has been run we want to display the run button
    if bo_run.data is not None:
        if st.button("Run BOSS", type="primary"):
            if bo_run.verify_bounds(bo_run.bounds):
                try:
                    bo_run.run_boss()
                    bo_run.concat_next_acq()
                    # call rerun to redraw everything so next acq is visible in data_editor
                    st.rerun()
                except TypeError:
                    st.error("Please make sure that all data points are of valid format. "
                             "Fill in the empty cells or download the data if you want to continue later.")

with postprocess_tab:
    if bo_run.results is not None:
        bo_run.display_result()
        pp = PostprocessingTab(bo_run.results, bo_run.X_names)
        col1, col2 = st.columns(2)
        with col1:
            pp_iters = pp.input_pp_iters()

        pp_acq_funcs, pp_slice = pp.plot_acqfn_or_slice()
        if st.button("Run post-processing"):
            post = PPMain(
                bo_run.results,
                pp_models=True,
                pp_model_slice=pp_slice,
                pp_acq_funcs=pp_acq_funcs,
            )
            post.run()
            pp.display_model_and_uncertainty()
            pp.display_acqfns()
    else:
        st.warning(
            "⚠️ No optimization results available. Please optimize first in the tab Run BOSS."
        )
