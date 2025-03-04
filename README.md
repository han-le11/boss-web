# Bayesian Optimization Structure Search (BOSS) web app

Prototype development of a multipage web app for Bayesian Optimization Structure Search (BOSS). 
Code documentation of BOSS can be found [here](https://cest-group.gitlab.io/boss/).

This web app repository currently has two main branches:
```
main        <- Stable version for (future) production
develop     <- For development and demo
```
The other feature branches are for specific features.

## Main structure
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



