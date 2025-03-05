# Bayesian Optimization Structure Search (BOSS) web app

## Overview 
Prototype development of a multipage web app for Bayesian Optimization Structure Search (BOSS), a general-purpose Bayesian Optimization code. It is designed to facilitate machine learning in computational and experimental natural sciences.

Demo version of the web app is available [here](https://boss-demo.streamlit.app/). Please note that this version is a work in progress and for demo purposes only—it is *not* for production use.

Code documentation of BOSS as Python API can be found [here](https://cest-group.gitlab.io/boss/).

## Features
Current features include:
- Bayesian Optimization: Perform Bayesian optimization, for example, to optimize materials properties or parameters of experiments for the optimal design. 
- Data Input: Upload your own CSV data or use the app's built-in data generation capabilities
- Visualization: Visualize your data and optimization results using interactive plots
- Post-processing: Perform post-processing tasks, such as generating plots for the surrogate model and acquisition function

## Main structure

This web app repository currently has two main branches:
```
main        <- Stable version for (future) production
develop     <- For development and demo
```
The other feature branches are for specific features.

```
├── src                     <- Source code of the project
│   ├── pages               <- Pages other than the homepage
│   ├── tabs                <- Tabs for the run page   
│   ├── ui                  <- UI functions
│   └── home.py             <- Homepage that acts as the entry point
├── tests                   <- Tests
├── doc                     <- Documentation
```

## How To Run
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command:
```
$ .\env\Scripts\activate
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally, start the web app on local host:
```
$ (env) streamlit run src/home.py
```

## Known Issues
- **Database**: Database connection is not yet implemented in the demo version
- **Result files**: The result files obtained after running one iteration needs to be downloadable. 



