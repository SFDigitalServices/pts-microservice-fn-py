# To enable ssh & remote debugging on app service change the base image to the one below
# Docker Images from https://hub.docker.com/_/microsoft-azure-functions-python
FROM mcr.microsoft.com/azure-functions/python:4-python3.10

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN apt-get install libaio1

COPY . /home/site/wwwroot