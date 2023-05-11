# BOSS WEB APP

Prototype development of the web interface for BOSS. 
This repo currently has two branches:
```
main        <- Stable version
develop     <- For development of small features 
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
$ (env) streamlit run app.py
```