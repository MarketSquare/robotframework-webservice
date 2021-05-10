import threading
import fastapi
import robot
import sys
import requests
import json
from fastapi import FastAPI, Request
from fastapi.responses import *
from fastapi.staticfiles import StaticFiles


APP_NAME = 'Robot Task Server'
app = FastAPI(title=APP_NAME)
app.mount("/robotlog", StaticFiles(directory="robotlog"), name="robotlog")


@app.get('/')
def greetings():
    return 'web service for starting robot tasks'


@app.get('/status/')
def server_status():
    status = {'python version': sys.version,
              'platform': sys.platform,
              'arguments': sys.argv,
              'application': APP_NAME}
    return status


@app.get('/run/{task}')
def do_some_work(task):
    result: int = start_robot_task(task)
    if result == 0:
        result_page = 'PASS'
    elif 250 >= result >= 1:
        result_page = f'FAIL: {result} tasks failed'
    else:
        result_page = f'FAIL: Errorcode {result}'
    result_page += '<p><a href="../robotlog/log.html">Go to log</a></p>'
    return Response(content=result_page, media_type="application/xml")


@app.get('/run_and_show/{task}', response_class=HTMLResponse)
def start_robot_task_and_show_log(task: str, arguments: Request):
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    start_robot_task(task, variables)
    return RedirectResponse(f"/robotlog/{task}/log.html")


@app.get('/run_and_show_report/{task}', response_class=HTMLResponse)
def start_robot_task_and_show_report(task: str, arguments: Request):
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    start_robot_task(task, variables)
    return RedirectResponse(f"/robotlog/{task}/report.html")


@app.get('/show_log/{task}', response_class=HTMLResponse)
def show_logs(task: str):
    return RedirectResponse(f'/robotlog/{task}/log.html')


@app.get('/show_report/{task}', response_class=HTMLResponse)
def show_report(task: str):
    return RedirectResponse(f'/robotlog/{task}/report.html')


def start_robot_task(task: str, variables: list = None) -> int:
    result: int = robot.run(
        'tasks',
        task=task,
        outputdir=f'robotlog/{task}',
        variables=variables,
        consolewidth=120
    )
    return result