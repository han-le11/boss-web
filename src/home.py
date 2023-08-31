import streamlit as st
from ui.page_config import PageConfig, customize_footer

page_config = PageConfig(
    main_title="🙌 Welcome to BOSS!",
    tab_title="Home - Bayesian Optimization Structure Search",
    header="Home",
    icon="🏠",
)

page_config.set_page()
page_config.set_main_title()
page_config.set_header()
customize_footer()

st.markdown(
    "Bayesian Optimization Structure Search (BOSS) is a general-purpose Bayesian Optimization tool. \n"
    "It is designed to facilitate machine learning in computational and experimental natural sciences.\n"
)

st.markdown(
    "Please consult the manual page for more detailed documentation and tutorials."
)
