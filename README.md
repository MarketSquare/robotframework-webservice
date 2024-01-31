[![PyPi license](https://badgen.net/github/license/Marketsquare/robotframework-webservice/)](https://pypi.com/project/robotframework-webservice/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/robotframework-webservice.svg)](https://pypi.python.org/pypi/robotframework-webservice/) [![PyPI download month](https://img.shields.io/pypi/dm/robotframework-webservice.svg)](https://pypi.python.org/pypi/robotframework-webservice/) 

# Robot Task Webservice

A web service managing Robot Framework tasks/tests.

# Goal

This web service shall start Robot Framework tasks/tests and return and cache the according reports.

# Installation and Execution

## Docker
You can run the image and map your test cases into the webservice with a volume :
```
docker run --rm --publish 5003:5003 \
           --volume <host directory of test cases>:/robot/tests \
           --env SUITE_FOLDER=tests \
           ghcr.io/marketsquare/robotframework-webservice:master
```
You can also run the image and map your test cases and your variable files (separated by spaces) into the webservice with volumes :
```
docker run --rm --publish 5003:5003 \
           --volume <host directory of test cases>:/robot/tests \
           --volume <host directory of variable files>:/robot/variables \
           --env SUITE_FOLDER=tests \
           --env "VARIABLE_FILES=variables/variables.py variables/variables2.py" \
           ghcr.io/marketsquare/robotframework-webservice:master
```

## Podman
Almost as Docker, but you might need to attach the webservice to the host network:
```
podman run --network host -v ./examples:/robot/tasks --env SUITE_FOLDER=tasks rf-webservice:latest
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
Endpoints that trigger execution of a robot task/test, for instance:

Call robot task/test:

    http://localhost:5003/robotframework/run/mytask

Call robot task/test with variables:

    http://localhost:5003/robotframework/run/mytask?myVariable1=42&anotherVariable=Mustermann

Response contains a header field `x-request-id` that can be used to retrieve logs and reports of this execution asynchronously (see reporting endpoints)

There are endpoints for synchronous and asynchronous request:

```
# connection remains open for duration of my task/test
http://localhost:5003/robotframework/run/mytask

# connection closes immediately - result must be requested with the x-request-id
http://localhost:5003/robotframework/run/mytask/async
```

**There is no limitation on executed Robot processes! It is easy to push the webservice in DOS with too many requests at once**

## Reporting
Endpoints that provide `log.html` and `report.html` for a specific task execution. You require the `x-request-id` from a previous response that triggered the execution.


# Start web service

The web service starts automatically with uvicorn inside. Simply call:

    python -m RobotFrameworkService.main

You can check available options with

    python -m RobotFrameworkService.main --help

## Example:

    python -m RobotFrameworkService.main -p 5003 -t path_to_my_taskfolder

## Example - Variablefiles:

You can provide variable files that are passed to all robot suites on execution:

    python -m RobotFrameworkService.main -p 5003 -t path_to_my_taskfolder --variablefiles config/env/test.py

# Custom WSGI server

You can start RobotFrameworkService with bare WSGI servers:
    
    uvicorn RobotFrameworkService.main:app --port 5003

Or start web service with other WSGI server, i.e waitress:

    waitress-serve --port 5003 RotbotFrameworkService.main:app

# SwaggerUi
Swagger-UI is available under `http://localhost:5003/docs`


# Demo-Tasks

This project contains some tasks, tests and variables for demonstration. They are located in ``examples`` folder. You may add
your own task/test suites in that directory, if you like.

# Task name with spaces in URL

Tasks may contain spaces, URL must not. Luckily, Robot Framework supports CamelCase as well as snake_case syntax.
Meaning: "Another Task" can be trigger in url with parameter `AnotherTask` or ``another_task``
