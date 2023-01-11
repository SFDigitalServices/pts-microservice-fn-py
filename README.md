# pts-microservice-fn-py [![CircleCI](https://badgen.net/circleci/github/SFDigitalServices/pts-microservice-fn-py/main)](https://circleci.com/gh/SFDigitalServices/pts-microservice-fn-py) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/pts-microservice-fn-py/badge.svg?branch=main)](https://coveralls.io/github/SFDigitalServices/pts-microservice-fn-py?branch=main)
Permit Tracking System (PTS) microservice with Azure serverless python function

## `api/status/http`
Query http status of the serverless function.

### Query
Example
```
$ curl https://<host>/api/status/http

{"status": "success", "data": {"message": "200 OK"}}
```

## `api/status/pts`
Query status of PTS connection

### Query
Example
```
$ curl https://<host>/api/status/pts
--header 'ACCESS_KEY: 111111'

{"status": "success", "data": {"message": "200 OK"}}
```


## `api/permit`

POST permit information to PTS
```
$ curl --location --request POST 'https://<host>/api/permit'
--header 'ACCESS_KEY: 111111'
--header 'Content-Type: application/json'
--data-raw '{
    "P_AVS_ADDRESS_ID": 100000,
    "P_SCOPE_OF_WORK": "TEST",
    "P_VALUATION": 0,
    "P_APPLICANT_FIRST_NAME": "FIRST",
    "P_APPLICANT_LASTINNAME": "LAST",
    "P_APPLICANT_EMAIL_ADDRESS": "TEST@TEST.TEST",
    "P_APPLICANT_PHONE_NUMBER": 4151111111,
    "P_APPLICANT_LICENSE_NUMBER": "000001",
    "P_APPLICANT_ROLE": "CONTRACTOR",
    "P_CONTACT1_FIRST_NAME": "FIRST",
    "P_CONTACT1_LASTINNAME": "LAST",
    "P_CONTACT1_EMAIL_ADDRESS": "TEST@TEST.TEST",
    "P_CONTACT1_PHONE_NUMBER": 4151111111,
    "P_CONTACT1_LICENSE_NUMBER": "ABC",
    "P_FORMIO": "111111111"
}'

{ "status": "success", "data": { "out": { "P_STATUS": "OKAY", "P_MSG": null, "P_APP_NUM": "1234567890" } }
```

### External Reference Data
External references can be pass through by using EXT_ prefix, such as EXT_ID.
```
$ curl --location --request POST 'https://<host>/api/permit'
--header 'ACCESS_KEY: 111111'
--header 'Content-Type: application/json'
--data-raw '{
    ...,
    EXT_ID: "1234"
}'

{ "status": "success", "data": { "out": { ..., EXT_ID: "1234" } }
```


## `/api/permit/bluebeam`
PUT Blubeam Project ID into Permit Application
```
$ curl --request PUT 'https://<host>/api/permit/bluebeam'
--header 'ACCESS_KEY: 111111'
--header 'Content-Type: application/json' 
--data-raw '{
    "P_APPLICATION_NUMBER": 1234567890,
    "P_BLUEBEAM_PROJ_NO": "111-111-111"
}'

{"status": "success", "data": {"out": {"P_STATUS": "SUCCESS", "P_MSG": "Application has been updated"}}}
```


## `api/complaint`
GET complaint based on AVS address id

### Query
OKAY
```
$ curl --request GET 'https://<host>/api/complaint?avs_address_id=12345'
--header 'ACCESS_KEY: 111111'

{"status": "success", "data": {"out": {"P_STATUS": "OKAY", "P_MSG": "No Active Complaints Found"}}}
```
ERROR
```
$ curl --request GET 'https://<host>/api/complaint?avs_address_id=12345' 

{"status": "success", "data": {"out": {"P_STATUS": "ERROR", "P_MSG": "|Active complaint found 100000001|Active complaint found 100000002|Active complaint found 100000003"}}}
```

## Deployment notes

### Oracle Instant Client 

#### driver download
`https://www.oracle.com/cis/database/technologies/instant-client/downloads.html`

#### package dependency
`libaio1` package is required. If needed install via SSH `apt-get install libaio1`

#### :warning: [Linux Consumption] Successful slot swaps automatically reverted after a few minutes :warning:
DO NOT USE "SWAP" option until [issue](https://github.com/Azure/azure-functions-host/issues/7336) is resolved.   
see more at: https://github.com/Azure/azure-functions-host/issues/7336


## Development

### Get started

Install Pipenv (if needed)
> $ pip install --user pipenv

Install included packages
> $ pipenv install

Output virtualenv information
> $ pipenv --venv

### Docker
[Build the container image and test locally](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=in-process%2Cbash%2Cazure-cli&pivots=programming-language-python#build-the-container-image-and-test-locally)

Build
> $ docker build --tag <DOCKER_ID>/azurefunctionsimage:1.0.0 .   

Run 
> $ docker run -p 8080:80 -it <docker_id>/azurefunctionsimage:1.0.0 

Run with .env file
> $ docker run -p 8080:80 --env-file .env -it <docker_id>/azurefunctionsimage:1.0.0 



### Quickstart Reference Guide
[Azure Gov Cloud Container Registry Quick Start](https://sfgovdt.jira.com/wiki/spaces/DSEng/pages/3329622144/Azure+Gov+Cloud+Container+Registry+Quick+Start)
[Create a function in Azure with Python using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)  
[Create a Python function in Azure from the command line](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python)

### Environment variables
[Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python#environment-variables)
In Functions, `application settings`, such as service connection strings, are exposed as environment variables during execution. You can access these settings by declaring `import os` and then using, `setting = os.environ["setting-name"]`. See example of `local.settings.json` file at `local.settings.example.json`.

### Generating requirements.txt
Currently Azure Python Functions [does not support pipenv](https://github.com/Azure/azure-functions-python-worker/issues/417). However we can run `pipenv lock --requirements` to produce a requirements file for the non-dev requirements and `pipenv lock --requirements --dev` to produce one for just the dev requirements.
sample usage:  
production
```
$ pipenv lock --requirements > requirements.txt
```
development
```
pipenv lock --requirements --dev > requirements-dev.txt
```

#### azure-functions-worker
DO NOT include azure-functions-worker in requirements.txt
The Python Worker is managed by Azure Functions platform
Manually managing azure-functions-worker may cause unexpected issues

### Testing and Code Coverage
Code coverage command with missing statement line numbers  
> $ pipenv run python -m pytest --cov --cov-report term-missing

### Prec-commit
Set up git hook scripts with pre-commit
> $ pipenv run pre-commit install

### Continuous integration
* Setup `.env`
    1. Setup environmental variables from `local.settings.json`
* Setup coveralls.
    1. Log into coveralls.io to obtain the coverall token for your repo.
    2. Create an environment variable in CircleCI with the name `COVERALLS_REPO_TOKEN` and the coverall token value.

## How to fork in own repo (SFDigitalServices use only)
reference: [How to fork your own repo in Github](http://kroltech.com/2014/01/01/quick-tip-how-to-fork-your-own-repo-in-github/)

### Create a new blank repo
First, create a new blank repo that you want to ultimately be a fork of your existing repo. We will call this new repo "my-awesome-microservice-py".

### Clone that new repo on your local machine
Next, make a clone of that new blank repo on your machine:
> $ git clone https://github.com/SFDigitalServices/my-awesome-microservice-fn-py.git

### Add an upstream remote to your original repo
While this technically isn’t forking, its basically the same thing. What you want to do is add a remote upstream to this new empty repo that points to your original repo you want to fork:
> $ git remote add upstream https://github.com/SFDigitalServices/microservice-fn-py.git

### Pull down a copy of the original repo to your new repo
The last step is to pull down a complete copy of the original repo:
> $ git fetch upstream

> $ git merge upstream/main

Or, an easier way:
> $ git pull upstream main

Now, you can work on your new repo to your hearts content. If any changes are made to the original repo, simply execute a `git pull upstream main` and your new repo will receive the updates that were made to the original!

Psst: Don't forget to upload the fresh copy of your new repo back up to git:

> $ git push origin main


