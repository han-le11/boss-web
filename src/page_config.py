import streamlit as st


class Config:
    def __init__(self):
        pass

    @classmethod
    def set(cls):
        st.set_page_config(
            page_title="BOSS Web App",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.boss.ai/help'
            }
        )
        # return None
