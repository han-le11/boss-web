import numpy as np
import streamlit as st


class ParamsService:
    @staticmethod
    def set_optional_params():
        initpts, iterpts = st.columns(2)
        with initpts:
            init_points = st.number_input("Number of initial Sobol points", min_value=0, step=1)
        with iterpts:
            iters = st.number_input("Number of iterations", min_value=0, step=1)
            # st.selectbox('Choose parameter values that you want to specify, otherwise the default values will be used.',
            #              options=param_keys)
        pass

    @staticmethod
    def input_x_bounds(X_names):
        dimension = len(X_names)
        bounds = np.empty(shape=(dimension, 2))
        if X_names:
            st.write("Dimension of the search space is", dimension)
            for d in range(dimension):
                left_col, right_col = st.columns(2)
                with left_col:
                    lower_bound = st.number_input("Lower bound of {var} *".format(var=X_names[d]))
                    bounds[d, 0] = lower_bound
                with right_col:
                    upper_bound = st.number_input("Upper bound of {var} *".format(var=X_names[d]))
                    bounds[d, 1] = upper_bound
        return bounds

    @staticmethod
    def set_y_range(y_values, y_name):
        y_min, y_max = None, None
        if y_name and y_values.size != 0:
            y_min = np.amin(y_values)
            y_max = np.amax(y_values)
            st.info(f"In the uploaded data, "
                    f"{y_name[0]} has a min value of {y_min} and max value of {y_max}")
        return y_min, y_max
