import streamlit as st
from ui.page_config import PageConfig, customize_footer, remove_toggles


page_config = PageConfig(
    main_title="Tutorial", tab_title="Tutorial", header="Tutorial", icon="📝"
)

page_config.set_page()
page_config.set_main_title()
page_config.set_header()
customize_footer()

st.warning(
    "As the app is underdevelopment, it will sleep after about 30 minutes of inactivity. Reload the page if this "
    "happens.",
    icon="⚠️",
)
