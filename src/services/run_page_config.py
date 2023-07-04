import streamlit as st


class RunPageConfig:
    @staticmethod
    def set_page():
        st.set_page_config(
            page_title="Bayesian Optimization Structure Search (BOSS)",
            layout="centered",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.boss.ai/help'
            }
        )

    @staticmethod
    def set_main_title():
        st.title('Bayesian Optimization Structure Search (BOSS)')
