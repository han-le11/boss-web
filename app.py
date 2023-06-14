import numpy as np
import pandas as pd
import streamlit as st
from boss.bo.bo_main import BOMain

st.title('BOSS Web App')
features = st.container()


def toy_func_2d(X):
    x = X[0, 0]
    y = X[0, 1]
    z = 0.01 * ((x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2 + 20 * (x + y))
    return z


def dummy_function(_):
    pass


input_data, run, postprocessing, tutorial = st.tabs(["Input data",
                                                     "Run BOSS",
                                                     "Post-processing",
                                                     "Tutorial"])
with input_data:
    st.write("Upload a csv file.")

with tutorial:
    st.write("Tutorial")

with run:
    uploaded_file = st.file_uploader("Choose a csv file")

    def upload_file():
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df)
            inputs = df[['P-factor', 'Temperature']].to_numpy()
            outputs = df['lignin yield'].to_numpy()
            # st.write(type(inputs), type(outputs))
        return inputs, outputs


    dimension, noise = st.columns(2)
    with dimension:
        dimension = st.number_input('Dimension', min_value=1, step=1)
    with noise:
        noise = st.number_input('Data noise', min_value=0)

    lower1, upper1 = st.columns(2)
    with lower1:
        lower_bound_1 = st.number_input('Lower bound of input variable 1')
    with upper1:
        upper_bound_1 = st.number_input('Upper bound of input variable 1')

    lower2, upper2 = st.columns(2)
    with lower1:
        lower_bound_2 = st.number_input('Lower bound of input variable 2')
    with upper1:
        upper_bound_2 = st.number_input('Upper bound of input variable 2')

    y_range_lower, y_range_upper = st.columns(2)
    with y_range_lower:
        y_range_lower_bound = st.number_input('Estimated lower value of output')
    with y_range_upper:
        y_range_upper_bound = st.number_input('Estimated upper value of output')

    init_points = st.number_input('Number of initial Sobol points', min_value=0, step=1)
    iters = st.number_input('Number of iterations', min_value=0, step=1)

    # if st.button("Save parameters"):
    #     get_data(df).append({"lower_bound": lower_bound, "upper_bound": upper_bound,
    #                          "y_range_lower_bound": y_range_lower_bound,
    #                          "y_range_upper_bound": y_range_upper_bound,
    #                          "init_points": init_points,
    #                          "iters": iters})
    #     st.write(pd.DataFrame(get_data()))

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

        X, Y = upload_file()
        print("Input data", X)
        print("Y range", Y)
        st.write("Input data", X)
        st.write("Y range", Y)
        st.write(X.shape)
        st.write(Y.shape)
        res = bo.run(X, -Y)

        mu_glmin = res.select('mu_glmin', -1)  # global min prediction from the last iteration
        x_glmin = res.select('x_glmin', -1)  # global min location prediction

        st.write('Predicted global min: {} at x = {}'.format(mu_glmin, x_glmin))

    # if st.button('Next acquisition'):
    #     X_next = res.get_next_acq(-1)
    #     st.write(X_next)
