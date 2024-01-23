# Bayesian Optimization Structure Search (BOSS) web app

Prototype development of the web interface for Bayesian Optimization Structure Search (BOSS). 
This repository currently has two main branches:
```
main        <- Stable version
develop     <- For development
```
The other branches are for specific features.

## Main structure
```
├── src                     <- Source code of the project
│   ├── pages               <- Other pages 
│   ├── tabs                <- Tabs for the run page   
│   ├── ui                  <- UI functions
│   └── home.py             <- Home page that acts as the entry point
├── tests                   <- Tests
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



