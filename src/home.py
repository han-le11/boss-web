import streamlit as st
from page_config.page_config import PageConfig

page_config = PageConfig("🙌 Welcome to BOSS!",
                         "Home - Bayesian Optimization Structure Search",
                         "Home",
                         "🏠")

page_config.set_page()
page_config.set_main_title()
page_config.set_header()
page_config.remove_toggles()
page_config.customize_watermark()

st.markdown(
    "Bayesian Optimization Structure Search (BOSS) is a general-purpose Bayesian Optimization code. \n"
    "It is designed to facilitate machine learning in computational and experimental natural sciences.\n"
    "For a more detailed description of the code and tutorials, please consult the user guide."
)
