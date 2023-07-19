import streamlit as st


class PageConfig:
    def __init__(self, main_title, tab_title, header, icon):
        """
        Set layout for a certain page.
        :param main_title: str
            Page title in the main area
        :param tab_title: str
            Page title showed on the browser tab
        :param header: str
            Page header
        :param icon: str
            Page icon
        """
        self.main_title = main_title
        self.tab_title = tab_title
        self.header = header
        self.icon = icon

    def set_page(self):
        """
        Set the page layout.
        Temporarily customize the max width with css.
        :return: None
        """
        st.set_page_config(
            page_title=self.tab_title,
            page_icon=self.icon,
            layout="centered",
            initial_sidebar_state="collapsed",
        )
        set_width = """
                    <style>
                        section.main > div {max-width:60rem}
                    </style>
                    """
        st.markdown(set_width, unsafe_allow_html=True)

    def set_main_title(self):
        st.title(self.main_title)

    def set_header(self):
        st.sidebar.header(self.header)

    @staticmethod
    def customize_watermark():
        hide_streamlit_style = """
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
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
