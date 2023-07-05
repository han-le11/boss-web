import os
import streamlit as st
from boss.pp.pp_main import PPMain
from PIL import Image


def run_post_processing(res):
    pp = PPMain(res, pp_models=True, pp_acq_funcs=True)
    pp.run()


def show_model_and_uncertainty():
    pp_dir = './postprocessing/graphs_models'
    for path, directories, files in os.walk(pp_dir):
        for file in files:
            if file.endswith(("png", "jpg")):
                img_path = os.path.join(path, file)
                img = Image.open(img_path)
                if "uncert" in img_path:
                    st.image(img, caption='Uncertainty over the search space.')
                else:
                    st.image(img, caption='Acquisitions, next acquisition point, and global minimum.')
