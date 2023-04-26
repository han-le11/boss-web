import streamlit as st
import numpy as np
import pandas as pd
from boss.bo.bo_main import BOMain

st.title('BOSS Web App')
features = st.container()

uploaded_file = st.file_uploader("Choose a csv or excel file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)


def func_2d(X):
    x = X[0, 0]
    y = X[0, 1]
    z = 0.01 * ((x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2 + 20 * (x + y))
    return z


@st.cache_data()
def get_data(df):
    return df


# obj function
st.write('The toy objective function is')
st.latex(r'''
        0.01\cdot((x^2 + y - 11)^2 + (x + y^2 - 7)^2 + 20 \cdot(x + y))
        ''')
st.write('True global minimum')
st.latex(r'''
        z = -1.4633, x_{min} = (-4.00035, -3.5542).
        ''')

lower_bound = st.number_input('Lower bound')
st.write('The lower bound is ', lower_bound)
upper_bound = st.number_input('Upper bound')
st.write('The upper bound is ', upper_bound)
y_range_lower_bound = st.number_input('Lower bound of the dependent variable')
y_range_upper_bound = st.number_input('Upper bound of the dependent variable')
init_points = st.number_input('Number of initial Sobol points', min_value=1, step=1)
iters = st.number_input('Number of iterations', min_value=1, step=1)

# if st.button("Save parameters"):
#     get_data(df).append({"lower_bound": lower_bound, "upper_bound": upper_bound,
#                          "y_range_lower_bound": y_range_lower_bound,
#                          "y_range_upper_bound": y_range_upper_bound,
#                          "init_points": init_points,
#                          "iters": iters})
#     st.write(pd.DataFrame(get_data()))

if st.button("Run BOSS"):
    bo = BOMain(
        func_2d,
        bounds=[[lower_bound, upper_bound], [lower_bound, upper_bound]],
        yrange=[y_range_lower_bound, y_range_upper_bound],
        kernel='rbf',
        initpts=init_points,
        iterpts=iters
        )

    res = bo.run()
    mu_glmin = res.select('mu_glmin', -1)  # global min prediction from the last iteration
    x_glmin = res.select('x_glmin', -1)  # global min location prediction

    st.write('Predicted global min: {} at x = {}'.format(mu_glmin, x_glmin))
