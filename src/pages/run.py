import numpy as np
import streamlit as st
from boss.bo.bo_main import BOMain
from boss.pp.pp_main import PPMain
from tabs.postprocessing_tab import PostprocessingTab
from ui.boss_run_params import input_X_bounds
from ui.file_handler import (
    upload_file,
    check_if_there_are_bounds,
    parse_bounds,
    choose_inputs_and_outputs,
    extract_col_data,
)
from ui.page_config import PageConfig, customize_footer, remove_toggles
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
    st.markdown(
        "#### BOSS optimizes by using your input data and suggests the next acquisition."
    )


    def dummy_function(_):
        pass


    def run_boss(func, X_ranges, in_vals, out_vals, kernel, noise_var):
        bo = BOMain(
            f=func,
            bounds=X_ranges,
            kernel=kernel,
            noise=noise_var,
            iterpts=0,
        )
        if min_or_max == "Minimize":
            result = bo.run(in_vals, out_vals)
        else:
            result = bo.run(in_vals, -out_vals)
        st.session_state["bo_result"] = result  # write BO result to session state
        return result


    # Parse data immediately from generated initial points
    if (
            st.session_state["init_pts"] is not None
            and len(st.session_state["init_pts"].columns) == dim + 1
            and not np.isnan(init_bounds).any()
            and "" not in list(st.session_state["names_and_bounds"].keys())
    ):
        X_bounds = parse_bounds(init_with_bounds)
        X_vals = extract_col_data(df=init_with_bounds, keyword="input-var")
        Y_vals = extract_col_data(df=init_with_bounds, keyword="output-var")
        X_names = list(init_with_bounds.columns)[:dim]

    # Display file uploader widget
    else:
        df_file = upload_file()
        bounds_exist = check_if_there_are_bounds(df_file)

        # Parse bounds from the uploaded file
        if bounds_exist:
            X_names = list(df_file.columns)[:dim]
            data = df_file.iloc[:, :-2]
            st.write(data)
            X_bounds_from_file = parse_bounds(df_file)
            X_bounds = input_X_bounds(X_names, X_bounds_from_file)
            X_vals = extract_col_data(df=df_file, keyword="input-var")
            Y_vals = extract_col_data(df=df_file, keyword="output-var")
        else:
            # Manually set variable names and bounds
            X_vals, Y_vals, X_names, Y_name = choose_inputs_and_outputs(df_file)
            X_bounds = input_X_bounds(X_names)

    # Choose minimize/maximize and noise variance
    col1, col2 = st.columns(2)
    with col1:
        min_or_max = st.selectbox(
            "Minimize or maximize the target value?", options=("Minimize", "Maximize")
        )
    with col2:
        noise_variance = st.number_input(
            "Noise variance",
            min_value=0.0,
            format="%.5f",
            help="Estimated variance for the Gaussian noise",
        )

    if st.button("Run BOSS"):
        # Run with generated initial points or uploaded file
        # if st.session_state["init_pts"] is not None:
        try:
            res = run_boss(
                func=dummy_function,
                X_ranges=X_bounds,
                in_vals=X_vals,
                out_vals=Y_vals,
                kernel="rbf",
                noise_var=noise_variance,
            )
            display_result(res, min_or_max, X_names)
            display_next_acq(res, X_names)
        except ValueError:
            st.error("Error: Have you input all required fields?")

with postprocess_tab:
    st.markdown("Get plots and data files after optimizing with BOSS.")

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
