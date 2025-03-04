import numpy as np
import streamlit as st
from boss.pp.pp_main import PPMain
from tabs.init_manager import InitPointsSetUp
from tabs.postprocessing_tab import PostprocessingTab
from tabs.run_boss import RunBOSS
from tabs.setup import SetUp
from ui.page_config import PageConfig, customize_footer

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
setup = SetUp()

# Initialize a session state for RunBOSS if there isn't one
if st.session_state["bo_run"] is None:
    st.session_state["bo_run"] = RunBOSS()

# Initialize a session state for RunHelper if there isn't one
bo_run: RunBOSS = st.session_state["bo_run"]

if st.button("Restart", help="Clear all data of the current run and start over.", type="primary"):
    setup.clear_data()

# Define tabs
setup_tab, run_tab, postprocess_tab = st.tabs(
    ["Set up BOSS", "Run BOSS", "Post-processing"]
)

with setup_tab:
    st.write("#### Set up input data and parameters for BOSS here.")
    col1, col2 = st.columns([2, 1])
    with col1:
        choice = st.selectbox(
            "Do you want to upload a csv file, or create initial data points?",
            options=("Upload file", "Create data points"),
            help="If you don't have any data, select 'Create data points'. Otherwise, select 'Upload file'.",
            index=None,
            disabled=bo_run.has_run,
        )
    match choice:
        case "Create data points":
            init = InitPointsSetUp()
            init_type = init.set_init_widgets()
            bo_run.bounds = setup.set_init_bounds(init.dim)
            bo_run.dim = init.dim
            bo_run.num_init = init.num_init
            bo_run.set_opt_params()

            if st.button("Generate points") and bo_run.verify_bounds(bo_run.bounds):
                init_manager = init.set_init_manager(
                    init_type,
                    bo_run.bounds,
                )
                init_pts = init_manager.get_all()
                # concatenate an empty column for target values to df and save to session state
                st.session_state["init_pts"] = init.add_var_names(
                    init_pts, st.session_state["init_vars"]
                )
                bo_run.X_names = list(st.session_state["init_vars"].keys())[:-1]
                bo_run.Y_names = [c for c in st.session_state["init_vars"].keys() if c not in bo_run.X_names]

            # TODO: check if this if statement can be simplified
            # Display an editable dataframe that contains initial points
            if (
                    st.session_state["init_pts"] is not None
                    and len(st.session_state["init_pts"].columns) == init.dim + 1
                    and not np.isnan(bo_run.bounds).any()
                    and "" not in list(st.session_state["init_vars"].keys())
                    and not bo_run.has_run
            ):
                bo_run.data = st.data_editor(st.session_state["init_pts"])
                bo_run.add_metadata()
                bo_run.download_data(widget_key="init_points")
                # df with bounds, only seen when downloaded, not shown in UI
                # bo_run.data = init.add_bounds_to_dataframe(
                #     bo_run.data, st.session_state["init_vars"]
                # )
                # init.download_init_points(bo_run.data)

        case "Upload file":
            # If BOSS hasn't been run, display widget to upload file.
            if not bo_run.has_run:
                bo_run.data = setup.upload_file()
                # Only continue if some data exists:
                if bo_run.data is not None:
                    bo_run.has_metadata = setup.has_metadata
                    # TODO: refactor this if-else block to make these 2 cases less divergent
                    # File doesn't have any metadata.
                    if not bo_run.has_metadata:
                        bo_run.choose_inputs_and_outputs()
                        bo_run.num_init = bo_run.data.shape[0]
                    # Parse parameters from uploaded file or initial data points
                    else:
                        bo_run.parse_params(setup.metadata)
                        bo_run.data = bo_run.data[bo_run.X_names + bo_run.Y_names]

                    # if input/output variables have been selected we can
                    # ask/display bounds and other keywords
                    if len(bo_run.X_names) > 0 and len(bo_run.Y_names) >= 1:
                        bo_run.input_X_bounds(bo_run.bounds)
                        bo_run.set_opt_params()
                        st.info("To continue running BOSS, navigate to the 'Run BOSS' tab.")
            # BOSS has been run, disable widgets for hyperparameters, only show them.
            else:
                bo_run.input_X_bounds(bo_run.bounds)
                bo_run.set_opt_params()

with run_tab:
    st.write("#### Run BOSS iterations here.")
    # BO has been run: disable input widgets and only display results
    if bo_run.has_run:
        bo_run.display_result()
        bo_run.display_next_acq()

    # TODO: check if this needs to be refactored because there's new data format
    # Display an editable dataframe for existing data
    if len(bo_run.X_names) > 0 and len(bo_run.Y_names) == 1 and bo_run.data is not None:
        bo_run.data = st.data_editor(bo_run.data, key="edit_data")
        bo_run.add_metadata()
        bo_run.download_data(widget_key="run_tab")

    # TODO: if possible, clean up the if conditions
    # Regardless of whether BO has been run, we want to display the run button.
    if st.button("Run BO iteration", type="primary"):
        if bo_run.verify_bounds(bo_run.bounds) and bo_run.verify_data():
            try:
                bo_run.run_boss()
                bo_run.has_run = True
                bo_run.concat_next_acq()
                # call rerun to redraw everything so next acq is visible in data_editor
                st.rerun()
            except TypeError:
                st.error("Please make sure that all data points are of valid format. "
                         "Fill in the empty cells or download the data if you want to continue later.")

with postprocess_tab:
    st.write("#### Plot the results of the optimization.")
    if bo_run.results is not None:
        bo_run.display_result()
        pp = PostprocessingTab(bo_run.results, bo_run.X_names)
        pp_slice = pp.plot_acqfn_or_slice()
        if st.button("Run post-processing", type="primary"):
            post = PPMain(
                bo_run.results,
                pp_models=True,
                pp_model_slice=pp_slice,
            )
            post.run()

        # Load images of models and uncertainty
        pp.load_plots()

        if len(pp.model_plots) > 1:
            col1, col2, col3 = st.columns([1, 2, 1], gap="large")
            with col1:
                if st.button("Previous"):
                    pp.prev_image()
            with col3:
                if st.button("Next"):
                    pp.next_image()

        img1, img2 = st.columns(2)
        # Display one model plot on the left and one uncertainty plot on the right
        with img1:
            st.image(pp.model_plots[st.session_state.cur_iter], width=500)
        with img2:
            st.write("")  # temp fix: add a blank line to align 2 plots horizontally
            st.image(pp.uncert_plots[st.session_state.cur_iter], width=500)
        st.write("test index before slider: ", st.session_state["cur_iter"])

        # TODO: only display buttons and sliders if there's more than 1 iteration?
        if len(pp.model_plots) > 1:
            # Slider
            st.session_state.cur_iter = st.slider(label="Select iteration",
                                                  min_value=0,
                                                  max_value=len(pp.model_plots) - 1,
                                                  key="iter",
                                                  value=st.session_state.cur_iter,
                                                  )
        st.write("test index after slider: ", st.session_state["cur_iter"])

    else:

        st.warning(
            "⚠️ No optimization results available. Please set up in 'Set up BOSS' tab and run in 'Run BOSS' tab."
        )
