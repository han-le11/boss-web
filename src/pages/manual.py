import pandas as pd
import streamlit as st
from ui.page_config import PageConfig, customize_footer

page_config = PageConfig(
    main_title="Manual",
    tab_title="Manual",
    header="Tutorial",
    icon=None,
)
page_config.set_page()
customize_footer()

run_url = "https://boss-demo.streamlit.app/run"
lignin_url = (
    "https://drive.google.com/file/d/1LMe2GnJ65t3rnPv4uHOhX_bAyKMiW7nB/view?usp=sharing"
)
data_with_bounds = (
    "https://drive.google.com/file/d/174q6BNjXOtaetMFZ0pj8jfwhse11rqn8/view?usp=sharing"
)
df_with_bounds = pd.read_csv("doc/data/data_with_bounds.csv")
df_params = pd.read_csv("doc/data/params_demo.csv")

st.warning(
    "⚠️ BOSS web app currently does not save your data once you leave the Run page or reload the browser. "
    "Please download your data before leaving the Run page."
)

st.subheader("✅ Overview")
st.write(
    "The goal is to perform Bayesian Optimization (BO) by running one BOSS iteration at a time. The cycle is "
    "started with manual data input from the user. Data can then be communicated to and from the app using "
    "automatically generated CSV files.  \n\n"
    f"The [Run]({run_url}) page has all the main features, i.e., creating initial data points, running BOSS, "
    "and post-processing. As you progress through the workflow, the web app will show instructions and guide "
    "you. In addition, you can find more detailed information in this manual."
)

st.subheader("✅ Workflow")
st.write(
    "The main steps in the workflow are as follows. For more details, please check the annotation below the "
    "graph. \n"
)
st.image("doc/img/workflow.png", width=650)

st.subheader(":green[Step 1.1. Upload a pre-defined CSV file in the Run BOSS tab]")
st.write(
    "**1. If the CSV file does not contain metadata (i.e., bounds and other parameters for BOSS run):**"
    "\n \n"
    f"In this case, the CSV file should be in proper tabular format. You can try out the BOSS web app using the "
    f"experimental data of lignin valorization as a toy dataset, which can be downloaded from [here]({lignin_url}).  "
    f"\n\n"
    f"On page [Run]({run_url}), navigate to the tab “Run BOSS” and upload a CSV file there. Choose input and "
    f"output variables and set valid bounds for input variables. Choose to minimize or maximize the output value "
    f"(BOSS runs minimization by default) and set the noise variance. Then, click on Run BOSS. "
)
st.image("doc/screenshots/run/case 1.1.1.png", width=650)

st.write(
    "**2. If you use a csv file containing bounds and other parameters for BOSS run:**"
    "\n\n We use an internal file format to store metadata, e.g., the bounds and the noise variance, together with"
    "the data for successive BOSS iterations.  \n\n"
    "Please note that as a user, you do not have to create such a file "
    "containing metadata; you can use the normal tabular data file format to initialize the BO cycle and then "
    "continue with further BOSS iterations using the file that is provided to you by the web app.  \n\n"
)
st.dataframe(df_with_bounds)
st.write(
    "For completeness, we explain our internal data format in the following:  \n\n"
    "The CSV file contains column names in the first row, as in the example above, so that the app can correctly "
    "recognize and parse the relevant data and metadata. "
)
st.markdown(
    """
    - Column names for the input variables have the text “input-var” in their names. For example, “input-var x” 
    and “input-var y”, etc. 
    - Column name for the output variable has “output-var” and the column names for bounds 
    have “boss-bound”. 
    - The noise variance and a flag determining minimization or maximization are in separate 
    columns in the CSV file (like in the example below)
    """
)

st.write(
    f"You can download such a CSV file with metadata from [here]({data_with_bounds}). You can and test the "
    "parsing feature of the web app with it. After running one iteration, any downloaded file contains all such "
    "metadata, so that the user can reupload it and run a new BOSS iteration without having to re-enter "
    "information."
)

st.subheader(":green[Step 1.2 and Step 2. If you have no initial data:]")
st.write(
    f"If you want to start the data acquisition process without any pre-existing data, go to the page [Run]({run_url}), "
    f"then go to the “Create initial data” tab. Set all the required parameters and type in variable names and "
    f"bounds. Then, click on the button “Create initial data”.  \n\n"
    f"A dataset of initial points in the search space generated by BOSS will be shown in a table.")
st.image("doc/screenshots/init/case 1.2 init.png", width=650)
st.write(
    "Now, if you switch to the “Run BOSS” tab, you can see that the dataset of initial points and chosen bounds have "
    "been transferred automatically from the “Create initial data” tab to the “Run BOSS” tab.")
st.image("doc/screenshots/init/case 1.2 run.png", width=650)
st.write("You can continue with the BO cycle, as in step 1.1., after typing in the target values (under the "
         "“output-var” column). If you want to continue at a later time, please do not forget to download the CSV "
         "file (via the Download button) with which you can restart the BO cycle.")

st.subheader(":green[Step 3, 4.1, and 4.2. Run BOSS and record the output value of the new acquisition]")
st.write("When clicking the red “Run BOSS” button (i.e., running one BOSS iteration), you will see the new "
         "acquisition point, as suggested by BOSS. This acquisition will also be automatically appended to your "
         "original dataset.  \n\n"
         "Please note that after clicking “Run BOSS”, the parameters for BOSS are not editable "
         "anymore (as seen in the screenshot below). If you want to start a new BOSS run with different parameter "
         "values, please click the “Clear all” button to clear all data in your current iteration.")
st.image("doc/screenshots/run/step 3-4.png", width=650)
st.write("The value of the output variable needs to be obtained manually, e.g., by running experiments, and entered "
         "directly into the table in the browser. Since the web app does not save your dataset, please download it "
         "before leaving or reloading your browser.")

st.subheader("✅ Post-processing")
st.write(
    "After getting BOSS optimization results, you can produce certain plots for the surrogate model and acquisition "
    "function. \n\n"
    f"Go to page [Run]({run_url}), click “Run post-processing”. The plots will appear here and you can save them.")
st.image("doc/screenshots/pp/ppplots.png", width=650)


st.subheader("✅ Start a new BOSS run")
st.write("If you want to clear all data and start a completely new optimization round, please click the “Clear all” "
         "button on the page Run or reload your browser. There will be a pop-up dialog asking if you are sure about "
         "clearing all your current data. ")
st.image("doc/screenshots/clear.png", width=700)


st.subheader("✅ Bug report and question")
st.write(
    "As the BOSS web app is under development, if you run into a bug or have any questions, please reach out to us on "
    "Slack or email. We appreciate all feedback! Please contact:  \n\n"
    "Han Le: han.le@aalto.fi  \n "
    "Joakim Löfgren: joakim.lofgren@aalto.fi  \n "
    "Matthias Stosiek: matthias.stosiek@aalto.fi or matthias.stosiek@tum.de"
)
