# Bayesian Optimization Structure Search (BOSS) web app

Prototype development of the web interface for Bayesian Optimization Structure Search (BOSS). 
This repo currently has two main branches:
```
main        <- Stable version
develop     <- For development
```
There are other small feature branches.

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