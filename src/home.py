import streamlit as st
from ui.page_config import PageConfig, customize_footer

page_config = PageConfig(
    main_title="BOSS web app",
    tab_title="Home - Bayesian Optimization Structure Search",
    header="Home",
    icon="🏠",
)
page_config.set_page()
header_img = "doc/img/boss_main_page.png"
st.image(header_img)
customize_footer()
boss_url = "https://sites.utu.fi/boss/"

st.markdown(
    "Bayesian Optimization Structure Search (BOSS) is a general-purpose Bayesian Optimization tool that can facilitate "
    "machine learning in computational and experimental natural sciences.\n"
)
st.markdown(f"You are on the BOSS web app, which is a spin-off of the Python library [BOSS]({boss_url}).")
st.markdown(f"Visit the [BOSS website]({boss_url}) for more information about features of the library and research use "
            f"cases.")

st.title("Contact")
st.markdown("If you have any problems, questions, bug reports, or suggestions for the BOSS web app, please contact us "
            "via Slack or email: \n")
st.markdown("Han Le: han.le@aalto.fi")
st.markdown("Joakim Löfgren: joakim.lofgren@aalto.fi")
st.markdown("Matthias Stosiek: matthias.stosiek@aalto.fi or matthias.stosiek@tum.de")
