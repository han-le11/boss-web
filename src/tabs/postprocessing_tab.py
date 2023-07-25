import numpy as np
import os
import streamlit as st
from PIL import Image


class PostprocessingTab:
    def __init__(self, bo_results, x_names) -> None:
        self.bo_results = bo_results
        self.x_names = x_names
        self.expander = None

    @staticmethod
    def plot_models_or_not() -> bool:
        pp_models = st.checkbox("Plot GP models and uncertainty.", value=True)
        return pp_models

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
        model_slice = [1, 2, 50]
        if not plot_acqfns and self.x_names is not None:
            x, y, z = self.input_model_slice()
            model_slice[0] = self.x_names.index(x) + 1
            model_slice[1] = self.x_names.index(y) + 1
            model_slice[2] = z
        return plot_acqfns, model_slice

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
                "Number of points per edge in the grid", value=50, step=1, min_value=1
            )
        return x, y, z

    def display_model_and_uncertainty(self) -> None:
        pp_dir = "./postprocessing/graphs_models"
        self._show_plots(
            pp_dir,
            "Model plots",
            "No model plots to display. Make sure that you have chosen to plot something.",
        )

    def display_acqfns(self) -> None:
        path = "./postprocessing/graphs_acqfns"
        self._show_plots(
            path, "Acquisition function", "No other plots for acquisition functions."
        )

    def _show_plots(self, path, title, warning_text) -> None:
        if os.path.isdir(path):
            self.expander = st.expander(title, expanded=True)
            for path, directories, files in os.walk(path):
                columns = self.expander.columns(2, gap="medium")
                for i, file in enumerate(files):
                    if file.endswith(("png", "jpg")):
                        with columns[i]:
                            img_path = os.path.join(path, file)
                            img = Image.open(img_path)
                            if "uncert" in img_path:
                                st.image(
                                    img, caption="Uncertainty over the search space"
                                )
                            else:
                                st.image(
                                    img,
                                    caption="Acquisitions, next acquisition, and global minimum",
                                )
        else:
            st.warning(warning_text)
