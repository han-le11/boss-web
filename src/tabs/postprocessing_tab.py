import numpy as np
import os
import streamlit as st
from PIL import Image


class PostprocessingTab:
    def __init__(self, bo_results, X_names: list) -> None:
        """
        Initialize the PostprocessingTab class.

        :param bo_results: BO results object.
        :param X_names: List of X-axis names.

        """
        self.bo_results = bo_results
        self.X_names: list = X_names
        self.model_plots: list[Image] = []
        self.uncert_plots: list[Image] = []
        self.model_slice: list = [None, None, None]
        self.fixed_vars: dict[str, float] = {}
        self.slider_value: int = st.session_state.cur_iter

    @property
    def fixed_keys(self):
        # fixed variable names are X_names excluding the variables in model slice
        return [self.X_names[i] for i in range(len(self.X_names)) if i+1 not in self.model_slice]

    @property
    def fixed_values(self):
        return {var: self.fixed_vars.get(var, 0.0) for var in self.fixed_keys}

    # TODO: write unit test
    def set_var_default(self):
        """
        Set default values for fixed variables.
        """
        # for each fixed variable name, make a number input field
        for var in self.fixed_keys:
            self.fixed_vars[var] = st.number_input(label="Fixed value for " + var, value=0.0, key="fixed_" + var)

    # TODO: write unit test
    def set_model_slice(self) -> None:
        """
        Let users choose axes for the 2d cross-section to plot, how many points per edge in the plot grid.
        This setting is passed to use in output and plots.
        """
        # x and y define the cross-section and z is number of points per axis
        st.write("Which axes (max 2D) of the objective function to plot?")
        col1, col2, col3 = st.columns(3)
        with col1:
            x1: str = st.selectbox("X1-axis", options=self.X_names)
        with col2:
            x2: str = st.selectbox("X2-axis", options=self.X_names, index=1)
        with col3:
            self.model_slice[2] = st.number_input(
                "Number of points per axis in the grid", value=50, step=1, min_value=1
            )
        # Access index of x1 and x2 in X_names
        self.model_slice[0] = self.X_names.index(x1) + 1
        self.model_slice[1] = self.X_names.index(x2) + 1
        if self.model_slice[0] == self.model_slice[1]:
            st.warning("Please select different axes to display contour plots.")

    # TODO: refactor this to display model plots of n-interations and make it cleaner
    def _show_plots(self, path, warning: str = None) -> None:
        """
        Internal function used to display plots.

        :param path: str
            The path of the plots.
        :param warning: str
            The warning text if no plots are found.
        """
        if os.path.isdir(path):
            for path, directories, files in os.walk(path):
                for i, file in enumerate(files):
                    img_path = os.path.join(path, file)
                    # Load image from path and append to list of either model or uncertainty plots
                    img = Image.open(img_path)
                    if "uncert" not in img_path:
                        self.model_plots.append(img)
                    else:
                        self.uncert_plots.append(img)
        else:
            st.warning(warning)

    def next_image(self):
        """
        Move to the next image.
        """
        if st.session_state.cur_iter < len(self.model_plots) - 1:
            st.session_state.cur_iter += 1

    @staticmethod
    def prev_image():
        """
        Move to the previous image.
        """
        if st.session_state.cur_iter > 0:
            st.session_state.cur_iter -= 1

    def load_plots(self) -> None:
        """
        Load model and uncertainty plots from the local folder.
        """
        model_dir = "./postprocessing/graphs_models"
        if os.path.isdir(model_dir):
            self._show_plots(path=model_dir, warning=None)

    def update_slider_value(self):
        """
        Update the slider value.
        """
        st.session_state.cur_iter = self.slider_value
        st.rerun()

