import streamlit as st
from ui.page_config import PageConfig, customize_footer


page_config = PageConfig(
    main_title="Tutorial",
    tab_title="Tutorial",
    header="Tutorial",
)

page_config.set_page()
customize_footer()

st.warning(
    "As the app is underdevelopment, it will sleep after about 30 minutes of inactivity. Reload the page if this "
    "happens.",
    icon="⚠️",
)
