import numpy as np
from boss import keywords
import streamlit as st


class ParamsService:
    @staticmethod
    def select_params():
        print(keywords.get_copied_categories())
        # categories[(int, 0)]
        # categories[(float, 0)] for noise
        for cat, cat_dict in keywords.categories.items():
            print('category dict', cat_dict)

            # param_type = cat.index(0)
            # param_keys = cat_dict.keys()
            # print(param_type)
            # st.selectbox('Choose parameter values that you want to specify, otherwise the default values will be used.',
            #              options=param_keys)
        pass

    @staticmethod
    def input_x_bounds(X_names):
        dimension = len(X_names)
        bounds = np.empty(shape=(dimension, 2))
        if X_names:
            st.write('Dimension of the search space is', dimension)
            for d in range(dimension):
                left_col, right_col = st.columns(2)
                with left_col:
                    lower_bound = st.number_input('Lower bound of {var}'.format(var=X_names[d]))
                    bounds[d, 0] = lower_bound
                with right_col:
                    upper_bound = st.number_input('Upper bound of {var}'.format(var=X_names[d]))
                    bounds[d, 1] = upper_bound
        return bounds

    @staticmethod
    def input_y_range():
        left_col, right_col = st.columns(2)
        with left_col:
            y_range_lower_bound = st.number_input('Estimated lower value of output')
        with right_col:
            y_range_upper_bound = st.number_input('Estimated upper value of output')
        return y_range_lower_bound, y_range_upper_bound
