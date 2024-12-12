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
        self.cur_iter = 0

    def input_pp_iters(self):
        pp_iters = st.multiselect(
            "Which iterations to run post-processing?",
            help="Can't be chosen if there is no iteration.",
            options=np.arange(0, np.arange(0, self.bo_results.num_iters)),
            default=None,
        )
        return pp_iters

    def plot_acqfn_or_slice(self):
        # By default, when this checkbox first renders, it is selected.
        plot_acqfns = st.checkbox(
            "Plot the acquisition functions in first and second axes. "
            "If not selected, you can customize which axes to plot.",
            value=True,
        )
        model_slice = [1, 2, 50]  # x axis, y axis, number of points per axis
        if not plot_acqfns and self.x_names is not None:
            x, y, z = self.input_model_slice()
            model_slice[0] = self.x_names.index(x) + 1
            model_slice[1] = self.x_names.index(y) + 1
            model_slice[2] = z
        return plot_acqfns, model_slice

    # TODO: refactor for the new postprocessing structure
    def input_model_slice(self) -> (int, int, int):
        # pp_models_slice = [x,y,z]
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

    # TODO: check if refactor is needed
    def display_acqfns(self) -> None:
        path = "./postprocessing/graphs_models"
        self._show_plots(
            path, "Acquisition function", "No other plots for acquisition functions."
        )

    # TODO: refactor this to display model plots of n-interations and make it cleaner
    def _show_plots(self, path, title, warning) -> None:  # obj_1, obj_2, slider
        """
        Internal function to display plots.

        :param path: str
            The path of the plots.
        :param title: str
            The title of the plots.
        :param warning: str
            The warning text if no plots are found.
        """
        col1, col2 = st.columns(2)
        if os.path.isdir(path):
            # self.expander = st.expander(title, expanded=True)
            for path, directories, files in os.walk(path):
                for i, file in enumerate(files):
                    img_path = os.path.join(path, file)
                    img = Image.open(img_path)
                    if "uncert" not in img_path:
                        self.model_plots.append(img)
                    else:
                        self.uncert_plots.append(img)
        else:
            st.warning(warning)

        self.cur_iter = st.slider(label="Next iteration", min_value=0, max_value=len(self.model_plots) - 1, key="iter")
        with col1:
            st.image(self.model_plots[self.cur_iter], width=500)
        with col2:
            st.write("")  # blank line to align the plots
            st.image(self.uncert_plots[self.cur_iter], width=500)

    def next_iter(self):
        """
        Move to the next iteration.
        """
        self.cur_iter += 1

    def display_model_and_uncertainty(self) -> None:
        pp_dir = "./postprocessing/graphs_models"
        if st.button(label="Next iteration", on_click=self.next_iter, key="show_next"):
            st.write("cur_iter: ", self.cur_iter)
        self._show_plots(
            path=pp_dir,
            title="Select an iteration to display the model and uncertainty plots.",
            warning="No model plots to display. Make sure that you have chosen to plot something.",
        )

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
