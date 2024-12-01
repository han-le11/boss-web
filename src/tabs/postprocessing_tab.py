import numpy as np
import os
import re  # Regular expression operations
import streamlit as st
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class PostprocessingTab:
    def __init__(self, bo_results, x_names) -> None:
        self.bo_results = bo_results
        self.x_names = x_names
        self.expander = None
        self.model_plots = []
        self.uncert_plots = []

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
            "Select an iteration to display the model and uncertainty plots.",
            "No model plots to display. Make sure that you have chosen to plot something.",
        )

    def display_acqfns(self) -> None:
        path = "./postprocessing/graphs_models"
        self._show_plots(
            path, "Acquisition function", "No other plots for acquisition functions."
        )

    # TODO: refactor this to display model plots of n-interations and make it cleaner
    def _show_plots(self, path, title, warning_text) -> None:
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
            st.warning(warning_text)

        # display plots
        with col1:
            model_iter = st.slider("Select an iteration to display a model plot",
                                   min_value=0, max_value=len(self.model_plots), key="model")
            st.image(self.model_plots[model_iter-1], width=500)
        with col2:
            uncert_iter = st.slider("Select an iteration to display an uncertainty plot",
                                    min_value=0, max_value=len(self.uncert_plots), key="uncert")
            st.image(self.uncert_plots[uncert_iter-1], width=500)

    def load_model_plots(self):
        """
        Finds and sorts all model graphs, then returns them as PIL images.
        """
        basedir = Path.cwd() / "postprocessing/graphs_models"
        # The number following npts is captured in a group (\d+) for sorting later.
        rgx = re.compile(r"\w+npts(\d+).png")
        uncert_rgx = re.compile(r"\w+npts(\d+)+_uncert.png")

        # Find model plots
        model_matches = [re.search(rgx, str(f)) for f in basedir.iterdir()]
        model_matches = [m for m in model_matches if m]  # remove null matches
        model_matches.sort(key=lambda m: int(m.group(1)))
        model_paths = [basedir / m.group(0) for m in model_matches]
        # Load images and display initial image
        self.model_plots = [Image.open(path) for path in model_paths]
        st.select_slider(label="Select an iteration",
                         options=self.model_plots,)


