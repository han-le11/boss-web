import streamlit as st
import sys


def customize_footer() -> None:
    """
    Add a footer 'Made by BOSS team' for each page in the app.
    Current solution is with css.
    """
    footer_style = """
                <style>
                footer {visibility: hidden;}
                footer:after {
                    content:'Made by BOSS team'; 
                    visibility: visible;
                    display: block;
                    position: relative;
                    #background-color: red;
                    padding: 5px;
                    top: 2px;
                }
                </style>
                """
    st.markdown(footer_style, unsafe_allow_html=True)


def remove_toggles() -> None:
    """
    Remove +/- toggles that are automatically created with number input widget.
    """
    st.markdown(
        """
        <style>
            button.step-up {display: none;}
            button.step-down {display: none;}
            div[data-baseweb] {border-radius: 4px;}
        </style>""",
        unsafe_allow_html=True,
    )


class PageConfig:
    def __init__(self, *, main_title, tab_title, header, icon) -> None:
        """
        Set layout for a certain page.
        :param main_title: str
            Page title in the main area
        :param tab_title: str
            Page title showed on the browser tab
        :param header: str
            Page header on the sidebar
        :param icon: str
            Page icon
        """
        self.main_title = main_title
        self.tab_title = tab_title
        self.header = header
        self.icon = icon

    def set_page(self) -> None:
        """
        Set the page layout.
        Temporarily customize the max width with css.
        """
        st.set_page_config(
            page_title=self.tab_title,
            page_icon=self.icon,
            layout="centered",
            initial_sidebar_state="expanded",
        )
        set_width = """
                    <style>
                        section.main > div {max-width:60rem}
                    </style>
                    """
        st.markdown(set_width, unsafe_allow_html=True)
        st.title(self.main_title)
        st.sidebar.header(self.header)

    @staticmethod
    def init_states() -> None:
        # session state to clear all data of the current run if restart button is clicked
        if "input_key" not in st.session_state:
            st.session_state.input_key = 0

        if "bo_run" not in st.session_state:
            st.session_state["bo_run"] = None

        # dictionary of variable names (key) and bounds (value)
        if "init_vars" not in st.session_state:
            st.session_state["init_vars"] = None

        # Session state to track dataframe containing initial points
        if "init_pts" not in st.session_state:
            st.session_state["init_pts"] = None

        # Session state to track the current iter index to display in tab post-processing.
        # For cur_iter, min value is 0, max value is number of iterations - 1.
        if "cur_iter" not in st.session_state:
            st.session_state.cur_iter = 0
