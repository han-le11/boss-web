import streamlit as st
from boss.bo.bo_main import BOMain
from params_service import ParamsService
from page_config import PageConfig
from file_handler import upload_file, choose_inputs_and_outputs

page_config = PageConfig
page_config.set_page()
page_config.set_main_title()
params = ParamsService


def dummy_function(_):
    pass


home, run, postprocessing, tutorial = st.tabs(["🏠 Home",
                                               "Run BOSS",
                                               "Post-processing",
                                               "Tutorial"])
with run:
    uploaded_file = upload_file()
    X, Y, X_names, Y_name = choose_inputs_and_outputs(uploaded_file)
    bounds = params.input_x_bounds(X_names)
    noise = st.number_input('Data noise', min_value=0.0)

    initpts, iterpts = st.columns(2)
    with initpts:
        init_points = st.number_input('Number of initial Sobol points', min_value=0, step=1)
    with iterpts:
        iters = st.number_input('Number of iterations', min_value=0, step=1)

    y_range_lower_bound, y_range_upper_bound = params.input_y_range()

    if st.button("Run BOSS"):
        bo = BOMain(
            dummy_function,
            bounds=bounds,
            yrange=[y_range_lower_bound, y_range_upper_bound],
            kernel='rbf',
            noise=noise,
            initpts=init_points,
            iterpts=iters
        )

        res = bo.run(X, -Y)

        mu_glmin = res.select('mu_glmin', -1)  # global min prediction from the last iteration
        x_glmin = res.select('x_glmin', -1)  # global min location prediction
        st.write('Predicted global min: {} at x = {}'.format(mu_glmin, x_glmin))

    # if st.button('Next acquisition'):
    #     X_next = res.get_next_acq(-1)
    #     st.write(X_next)
