[![PyPi license](https://badgen.net/github/license/Marketsquare/robotframework-webservice/)](https://pypi.com/project/robotframework-webservice/) [![PyPi version](https://badgen.net/pypi/v/robotframework-webservice/)](https://pypi.org/project/robotframework-webservice) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/robotframework-webservice.svg)](https://pypi.python.org/pypi/robotframework-webservice/) [![PyPI download month](https://img.shields.io/pypi/dm/robotframework-webservice.svg)](https://pypi.python.org/pypi/robotframework-webservice/) 

# Robot Task Webservice

A web service managing Robot Framework tasks.

**Status: Prototype**

# Goal

This web service shall start Robot Framework tasks and return and cache the according reports.

# Installation and Execution
*Default docker image does not support variable files, yet*

## Docker
```
docker pull ghcr.io/marketsquare/robotframework-webservice:master
```
After that you can run the image and map your test cases in to the webservice with a volumen:
```
docker run -v <host directory of test cases>:/robot/tests --env SUITE_FOLDER=tests rf-webservice:latest
```

## Podman
Almost as Docker, but you might need to attach the webservice to the host network:
```
podman run --network host -v ./tasks:/robot/tasks --env SUITE_FOLDER=tasks rf-webservice:latest
```

## Local
```
pip install robotframework-webservice
```

and execute from command line:

```
python -m RobotFrameworkService.main -p 5003 -t path_to_my_taskfolder
```

# Usage
There are 2 types of endpoints: 
1. Execution
2. Reporting

## Execution
Endpoints that trigger execution of a robot task, for instance:

Call robot task:

    http://localhost:5003/robotframework/run/mytask

Call robot task with variables:

    http://localhost:5003/robotframework/run/mytask?myVariable1=42&anotherVariable=Mustermann

Response contains a header field `x-request-id` that can be used to retrieve logs and reports of this execution asynchronously.

## Reporting
Endpoints that provide `log.html` and `report.html` for a specific task execution. You require the `x-request-id` from a previous response that triggered the execution.


## Start web service

The web service starts automatically with uvicorn inside. Simply call:

    python -m RobotFrameworkService.main

You can check available options with

    python -m RobotFrameworkService.main --help

### Example:

    python -m RobotFrameworkService.main -p 5003 -t path_to_my_taskfolder

### Example - Variablefiles:

You can provide variable files that are passed to all robot suites on execution:

    python -m RobotFrameworkService.main -p 5003 -t path_to_my_taskfolder --variablefiles config/env/test.py

## Custom WSGI server

You can start RobotFrameworkService with bare WSGI servers:
    
    uvicorn RobotFrameworkService.main:app --port 5003

Or start web service with other WSGI server, i.e waitress:

    waitress-serve --port 5003 RotbotFrameworkService.main:app

## SwaggerUi
Swagger-UI is available under `http://localhost:5003/docs`


## Demo-Tasks

This project contains some tasks for demonstration. They are located in ``tasks`` folder. You may add
your own task suites in that directory, if you like.

## Task name with spaces in URL

Tasks may contain spaces, URL must not. Luckily, Robot Framework supports CamelCase as well as snake_case syntax.
Meaning: "Another Task" can be trigger in url with parameter `AnotherTask` or ``another_task``
