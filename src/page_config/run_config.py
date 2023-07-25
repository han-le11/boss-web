import streamlit as st


class RunPageConfig:
    @staticmethod
    def set_page():
        st.set_page_config(
            page_title="Run BOSS", layout="centered", initial_sidebar_state="collapsed"
        )
        css = '''
            <style>
                section.main > div {max-width:75rem}
            </style>
            '''
        st.markdown(css, unsafe_allow_html=True)

    @staticmethod
    def set_main_title():
        st.title("🏃‍♀️ Run BOSS")

    @staticmethod
    def remove_toggles():
        st.markdown("""
                    <style>
                        button.step-up {display: none;}
                        button.step-down {display: none;}
                        div[data-baseweb] {border-radius: 4px;}
                    </style>""",
                    unsafe_allow_html=True
                    )



