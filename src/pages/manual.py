import pandas as pd
import streamlit as st
from ui.page_config import PageConfig, customize_footer

page_config = PageConfig(
    main_title="Tutorial",
    tab_title="Tutorial",
    header="Tutorial",
    icon=None,
)
run_url = "https://boss-demo.streamlit.app/run"
lignin_url = "https://drive.google.com/file/d/1LMe2GnJ65t3rnPv4uHOhX_bAyKMiW7nB/view?usp=sharing"
data_with_bounds = "https://drive.google.com/file/d/174q6BNjXOtaetMFZ0pj8jfwhse11rqn8/view?usp=sharing"

df_with_bounds = pd.read_csv("doc/data/withbounds.csv")
df_params = pd.read_csv("doc/data/params_demo.csv")
page_config.set_page()
customize_footer()

st.warning("⚠️ BOSS web app currently does not save your data once you leave the Run page or reload the browser. "
           "Please download your data before leaving the Run page.")

# st.subheader("✅ Overview")
# st.markdown(f"The [Run]({run_url}) page is where you will run BOSS optimization and post-processing.")


st.subheader("✅ Use cases of BOSS optimization")
st.subheader("1. If you use an arbitrary csv file: \n")
st.markdown("Currently, only csv file format is supported. "
            "The uploaded csv file must use colon or semicolon as separator.")
st.markdown(f"As a toy dataset, experimental data of lignin valorization can be downloaded from [here]({lignin_url}). "
            f"You can test the BOSS web app with it.\n")

st.markdown(f"Go to page [Run]({run_url}) then upload the csv file in the tab Run BOSS. "
            "Choose input and output variables and set valid bounds for input variables. "
            "Then, click on Run BOSS. You will see the results.")

st.subheader("2. If you use a csv file containing bounds: \n")
st.markdown(
    "As a current solution, the csv file should have column names like below so that the app can recognize and "
    "parse the bounds and other parameters correctly.\n")
st.dataframe(df_with_bounds)
st.markdown("The purpose of using such file is that you do not have to type in the bounds again for an iteration.")
st.markdown(
    f"You can download the csv file with bounds from [here]({data_with_bounds}) and test the parsing feature of "
    f"the BOSS web app with it.")

st.markdown("Optionally, it is possible to add the columns for noise variance and whether to minimize or maximize in "
            "the csv file (like the example below). ")
st.dataframe(df_params)

st.subheader("3. If you have no initial data: \n")
st.markdown(f"Go to page [Run]({run_url}), then go to the tab Create initial data. ")
st.markdown(
    f"Please set all required parameters. Type in variable names and bounds. "
    "Then, click on Create initial data. "
    "The initial data points will be shown in a table.")
st.markdown(
    "You can take these initial data point values and, for example, run experiments with them and record values "
    "of the target variable."
    "Then, you can optimize with this dataset in tab Run BOSS as usual.")

st.subheader("✅ Restart")
st.markdown(f"If you want to clear all data and start a new optimization round, please reload your browser or click "
            f"the Clear all button in page [Run]({run_url}).")

st.subheader("✅ Post-processing")
st.markdown("After getting BOSS optimization results, you can get some model plots and acquisition function plot. ")
st.markdown(f"Go to page [Run]({run_url}), then go to tab Post-processing and run post-processing. "
            f"The plots will appear here and you can save them.")

st.subheader("✅ Bug report")
st.markdown("As the BOSS web app is under development, if you run into a bug, please report it. We appreciate all "
            "feedback, thank you! Please contact us via Slack or email: ")
st.markdown("Han Le: han.le@aalto.fi")
st.markdown("Joakim Löfgren: joakim.lofgren@aalto.fi")
st.markdown("Matthias Stosiek: matthias.stosiek@aalto.fi or matthias.stosiek@tum.de")