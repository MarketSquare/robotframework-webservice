# Robot Task Webservice

A web service managing Robot Framework tasks.

**Status: Prototype**

#Goal

This web service shall start Robot Framework tasks and return and cache the according reports.

# Usage
Call robot task:

    http://localhost:5003/run/mytask

Call robot task with variables:

    http://localhost:5003/run/mytask?myVariable1=42&anotherVariable=Mustermann

Response contains status and log report.


## Start web service

Start web service on port 5003:
    
    uvicorn app:app --port 5003

Start web service with other WSGI server, i.e waitress:

    waitress-serve --port 5003 app:app


## Demo-Tasks

This project contains some tasks for demonstration. They are located in ``tasks`` folder. You may add
your own task suites in that directory, if you like.


## Task name with spaces in URL

Tasks may contain spaces, URL must not. Luckily, Robot Framework supports CamelCase as well as snake_case syntax.
Meaning: "Another Task" can be trigger in url with parameter `AnotherTask` or ``another_task``


## Variablen

Variables can be passed as url parameters:

    http://localhost:5003/taskWithMoreVariables?firstname=Max&lastname=Mustermann


## Robot Log.html, output.xml und report.hmtl

Latest task reports can be accessed at endpoint ``\robotlog\``.

    http://localhost:5003/robotlog/log.html
    http://localhost:5003/robotlog/output.xml
    http://localhost:5003/robotlog/report.html
