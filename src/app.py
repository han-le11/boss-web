import streamlit as st
from boss.bo.bo_main import BOMain
from page_config import Config
from file_reader import FileUploader

Config.set_page()
Config.set_main_title()


def dummy_function(_):
    pass


home, input_data, run, postprocessing, tutorial = st.tabs(["🏠 Home",
                                                           "Input data",
                                                           "Run BOSS",
                                                           "Post-processing",
                                                           "Tutorial"])
with input_data:
    uploaded_file = FileUploader.upload_file()
    X, Y, X_names, Y_name = FileUploader.choose_inputs_and_outputs(uploaded_file)

with run:
    noise = st.number_input('Data noise', min_value=0.0)

    lower1, upper1 = st.columns(2)
    with lower1:
        lower_bound_1 = st.number_input('Lower bound of input variable 1')
    with upper1:
        upper_bound_1 = st.number_input('Upper bound of input variable 1')

    lower2, upper2 = st.columns(2)
    with lower2:
        lower_bound_2 = st.number_input('Lower bound of input variable 2')
    with upper2:
        upper_bound_2 = st.number_input('Upper bound of input variable 2')

    y_range_lower, y_range_upper = st.columns(2)
    with y_range_lower:
        y_range_lower_bound = st.number_input('Estimated lower value of output')
    with y_range_upper:
        y_range_upper_bound = st.number_input('Estimated upper value of output')

    initpts, iterpts = st.columns(2)
    with initpts:
        init_points = st.number_input('Number of initial Sobol points', min_value=0, step=1)
    with iterpts:
        iters = st.number_input('Number of iterations', min_value=0, step=1)

    if st.button("Run BOSS"):
        bo = BOMain(
            dummy_function,
            bounds=[[lower_bound_1, upper_bound_1], [lower_bound_2, upper_bound_2]],
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

