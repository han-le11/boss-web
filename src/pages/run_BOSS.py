import streamlit as st
from boss.bo.bo_main import BOMain
from boss.pp.pp_main import PPMain
from page_config.page_config import PageConfig
from services.file_handler import upload_file, choose_inputs_and_outputs
from services.init_manager import InitManagerTab
from services.boss_run_params import ParamsService
from services.postprocessing_service import PostprocessingService
from services.result_displayer import display_result, display_next_acq

# Initialization
if 'bo_result' not in st.session_state:
    st.session_state.bo_result = None

for k, v in st.session_state.items():
    st.session_state[k] = v

page_config = PageConfig(main_title="🏃‍♀️ Run BOSS and Post-processing",
                         tab_title="Run BOSS",
                         header="Run BO here",
                         icon="🏃‍♀️")
page_config.set_page()
page_config.set_main_title()
page_config.set_header()
page_config.remove_toggles()
page_config.customize_watermark()

params = ParamsService()


def dummy_function(_):
    pass


def run_boss():
    bo = BOMain(
        dummy_function,
        bounds=bounds,
        yrange=[y_min, y_max],
        kernel="rbf",
        noise=noise_variance,
        iterpts=0
    )
    if min_or_max == 'Minimize':
        st.session_state.bo_result = bo.run(X_vals, Y_vals)
    else:
        st.session_state.bo_result = bo.run(X_vals, -Y_vals)
    return st.session_state.bo_result


init_data, run_data_tab, postprocess_tab = st.tabs(["Create initial data",
                                                    "Run",
                                                    "Post-processing"]
                                                   )

with init_data:
    st.markdown("#### If you do not have data, create initial data points here.")
    tab = InitManagerTab()
    tab.set_page()
    init_manager = tab.set_init_manager()
    if st.button("Generate points"):
        points = init_manager.get_all()
        st.write(points)
        file = tab.convert_array_to_csv(points)

        # st.download_button("Download",
        #                    data=file,
        #                    file_name='data.csv',
        #                    mime='text/csv')

with run_data_tab:
    st.markdown("#### BOSS optimizes using your input data and suggests the next acquisition.")

    uploaded_file = upload_file()
    X_vals, Y_vals, X_names, Y_name = choose_inputs_and_outputs(uploaded_file)
    y_min, y_max = params.set_y_range(y_values=Y_vals, y_name=Y_name)
    bounds = params.input_x_bounds(X_names)

    col1, col2 = st.columns(2)
    with col1:
        min_or_max = st.selectbox("Minimize or maximize the target value?", options=("Minimize", "Maximize"))
    with col2:
        noise_variance = st.number_input("Noise variance", min_value=0.0, value=0.01)

    if st.button("Run BOSS"):
        try:
            st.session_state.bo_result = run_boss()
            display_result(st.session_state.bo_result, min_or_max, X_names)
            display_next_acq(st.session_state.bo_result, X_names)
        except AssertionError:
            st.error("Have you input all required fields? "
                     "And make sure that the lower bound of a variable is smaller than its upper bound.")
        except ValueError:
            st.error("Have you input all required fields?")

with postprocess_tab:
    st.markdown("#### Get plots and data files after optimizing with BOSS.")

    if st.session_state.bo_result is not None:
        display_result(st.session_state.bo_result, min_or_max, X_names)
        pp = PostprocessingService(st.session_state.bo_result, X_names)

        col1, col2 = st.columns(2)
        with col1:
            pp_iters = pp.input_pp_iters()

        plot_models_or_not = pp.plot_models_or_not()
        pp_acq_funcs, pp_slice = pp.plot_acqfn_or_slice()

        if st.button("Run post-processing"):
            try:
                post = PPMain(st.session_state.bo_result,
                              pp_models=plot_models_or_not,
                              pp_model_slice=pp_slice,
                              pp_acq_funcs=pp_acq_funcs)
                post.run()
            except AttributeError:
                st.error("Have you run BOSS first in the tab Run?")
            pp.display_model_and_uncertainty()
            pp.display_acqfns()
    else:
        st.warning("No optimization results available. Please run BOSS first in the tab Run.")
