import streamlit as st


class Config:
    def __init__(self):
        pass

    @classmethod
    def set_page(cls):
        st.set_page_config(
            page_title="Bayesian Optimization Structure Search (BOSS)",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.boss.ai/help'
            }
        )

    @classmethod
    def set_main_title(cls):
        st.title('Bayesian Optimization Structure Search (BOSS)')
