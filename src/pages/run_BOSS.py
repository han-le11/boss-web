import streamlit as st
from boss.bo.bo_main import BOMain
from services.file_handler import upload_file, choose_inputs_and_outputs
from services.params_service import ParamsService
from services.run_page_config import RunPageConfig
from services.postprocessing_service import run_post_processing, show_model_and_uncertainty
from services.result_displayer import display_result

for k, v in st.session_state.items():
    st.session_state[k] = v

page_config = RunPageConfig()
page_config.set_page()
page_config.set_main_title()
page_config.hide_toggles()
params = ParamsService()

res = None
st.sidebar.header("Run BO here")


def dummy_function(_):
    pass


run_tab, postprocess_tab = st.tabs(["Run",
                                    "Post-processing"])

with run_tab:
    uploaded_file = upload_file()
    X, Y, X_names, Y_name = choose_inputs_and_outputs(uploaded_file)
    bounds = params.input_x_bounds(X_names)

    opt, noise = st.columns(2)
    with opt:
        min_or_max = st.selectbox('Minimize or maximize the target value?',
                                  options=('Minimize', 'Maximize'))
    with noise:
        noise_variance = st.number_input('Noise variance ', min_value=0.0)

    initpts, iterpts = st.columns(2)
    with initpts:
        init_points = st.number_input('Number of initial Sobol points', min_value=0, step=1)
    with iterpts:
        iters = st.number_input('Number of iterations', min_value=0, step=1)

    y_range_lower_bound, y_range_upper_bound = params.input_y_range(y_name=Y_name)

    if st.button("Run BOSS"):
        bo = BOMain(
            dummy_function,
            bounds=bounds,
            yrange=[y_range_lower_bound, y_range_upper_bound],
            kernel='rbf',
            noise=noise_variance,
            initpts=init_points,
            iterpts=iters
        )

        res = bo.run(X, -Y)
        display_result(res, min_or_max)

    # if st.button('Next acquisition'):
    #     X_next = res.get_next_acq(-1)
    #     st.write(X_next)

with postprocess_tab:
    if res is not None:
        run_post_processing(res)
        show_model_and_uncertainty()
    else:
        st.write("No optimization results. Please run a BOSS run first in tab Run.")
