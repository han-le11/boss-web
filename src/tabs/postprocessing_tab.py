import numpy as np
import os
import streamlit as st
from PIL import Image


class PostprocessingTab:
    def __init__(self, bo_results, x_names) -> None:
        self.bo_results = bo_results
        self.x_names = x_names
        self.expander = None
        self.model_plots = []
        self.uncert_plots = []
        # self.cur_iter = 0  # counter for the current iteration

    # TODO: ensure that this function works with num_iters
    def input_pp_iters(self):
        pp_iters = st.multiselect(
            "Which iterations to run post-processing?",
            help="Can't be chosen if there is no iteration.",
            options=np.arange(0, np.arange(0, self.bo_results.num_iters)),
            default=None,
        )
        return pp_iters

    def plot_acqfn_or_slice(self):
        """
        Return a tuple of plot_acqfns and model_slice
        """
        col1, col2, col3 = st.columns([1, 2, 1], gap="large")
        with col1:
            # By default, when this checkbox first renders, it is selected.
            plot_acqfns = st.selectbox(
                label="Plot the function in the first and second axes?",
                options=(True, False),
                help="If you select 'No', you can manually set which axes to plot.",
            )
        model_slice = [1, 2, 50]  # x axis, y axis, number of points per axis
        if not plot_acqfns and self.x_names is not None:
            x, y, z = self.input_model_slice()
            model_slice[0] = self.x_names.index(x) + 1
            model_slice[1] = self.x_names.index(y) + 1
            model_slice[2] = z
        return plot_acqfns, model_slice

    # TODO: if needed, refactor for the new postprocessing structure. try passing the tuple to pp_model_slice.
    def input_model_slice(self) -> tuple[int, int, int]:
        """
        Returns which (max 2D) cross-section of the objective function domain to use in output and plots. First two
        integers define the cross-section and last determines how many points per edge in the dumped grid.
        """
        # pp_models_slice = [x,y,z]  # keyword in BOSS post-processing
        # x and y define the cross-section and z is grid
        st.write("Which cross-section (max 2D) of the objective function to plot?")
        col1, col2, col3 = st.columns(3)
        with col1:
            x = st.selectbox("First axis of cross-section", options=self.x_names)
        with col2:
            y = st.selectbox("Second axis of cross-section", options=self.x_names)
        with col3:
            z = st.number_input(
                "Number of points per axis in the grid", value=50, step=1, min_value=1
            )
        return x, y, z

    # TODO: refactor this to display model plots of n-interations and make it cleaner
    def _show_plots(self, path, warning: str = None) -> None:
        """
        Internal function used to display plots.

        :param path: str
            The path of the plots.
        :param warning: str
            The warning text if no plots are found.
        """
        col1, col2 = st.columns(2)
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
        # Display one model plot on the left and one uncertainty plot on the right
        with col1:
            st.image(self.model_plots[st.session_state.cur_iter], width=500)
        with col2:
            st.write("")  # temp fix: add a blank line to align 2 plots horizontally
            st.image(self.uncert_plots[st.session_state.cur_iter], width=500)

    def next_image(self):
        if st.session_state.cur_iter < len(self.model_plots) - 1:
            st.session_state.cur_iter += 1

    def prev_image(self):
        if st.session_state.cur_iter > 0:
            st.session_state.cur_iter -= 1

    def display_model_and_uncertainty(self) -> None:
        self._show_plots(path="./postprocessing/graphs_models", warning=None)

    # TODO: implement this to display convergence and hyperparams plot
    def conv_hyperparams_plots(self) -> None:
        """
        Display plots of the convergence measures and hyperparameters.
        """
        col1, col2 = st.columns(2)
        with col1:
            st.image("./postprocessing/graphs_convergence/convergence.png", width=500)
        with col2:
            st.image("./postprocessing/graphs_convergence/hyperparameters.png", width=500)
        pass
