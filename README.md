# Robot Task Webservice

A web service managing Robot Framework tasks.

**Status: Prototype**

# Goal

This web service shall start Robot Framework tasks and return and cache the according reports.

# Install
```
pip install robotframework-webservice
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
