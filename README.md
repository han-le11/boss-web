# Bayesian Optimization Structure Search (BOSS) web app

Prototype development of the web interface for Bayesian Optimization Structure Search (BOSS). 
This repo currently has two branches:
```
main        <- Stable version
develop     <- For development of new features 
```
## Jira board links
[Tasks to do, in progress, in review, and done](https://cest-boss.atlassian.net/jira/software/c/projects/BOSS/boards/1?selectedIssue=BOSS-5)\
[Project Backlog](https://cest-boss.atlassian.net/jira/software/c/projects/BOSS/boards/1/backlog?atlOrigin=eyJpIjoiMGUyZjlmNmI0ZTUxNDY0NThhMWE0YTdmMWEyNjkxZmUiLCJwIjoiaiJ9)

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
$ (env) streamlit run src/app.py
```