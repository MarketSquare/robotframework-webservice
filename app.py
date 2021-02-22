import robot
import sys
from fastapi import FastAPI, Request
from fastapi.responses import *
from fastapi.staticfiles import StaticFiles



APP_NAME= 'Robot-Webserver zum Starten von RobotTasks'
app = FastAPI(title=APP_NAME)
app.mount("/robotlog", StaticFiles(directory="robotlog"), name="robotlog")



@app.get('/')
def greetings():
    return 'Webserver zum Starten von RobotTasks'


@app.get('/status/')
def server_status():
    status = {'Python Version': sys.version,
              'Platform': sys.platform,
              'Arguments': sys.argv,
              'Application': APP_NAME}
    return status


@app.get('/robotlog/{path}')
def browse_robot_log(path):
    return RedirectResponse(path)
    #return send_from_directory('robotlog', path)


@app.get('/run/{task}')
def do_some_work(task):
    #app.logger.info(f'Incoming request for task {task}')
    result: int = here_comes_work(task)
    if result == 0:
        result_page = 'PASS'
    elif 250 >= result >= 1:
        result_page = f'FAIL: {result} tasks failed'
    else:
        result_page = f'FAIL: Errorcode {result}'
    result_page += '<p><a href="../robotlog/log.html">Go to log</a></p>'
    return Response(content=result_page, media_type="application/xml")


@app.get('/run_and_show/{task}', response_class=HTMLResponse)
def do_some_work_and_show_log(task: str, arguments: Request):
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    here_comes_work(task, variables)
    return RedirectResponse(f"/robotlog/{task}/log.html")


@app.get('/run_and_show_report/{task}', response_class=HTMLResponse)
def do_some_work_and_show_report(task: str, arguments: Request):
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    here_comes_work(task, variables)
    return RedirectResponse(f"/robotlog/{task}/report.html")


def here_comes_work(task: str, variables: list = None) -> int:
    result: int = robot.run(
        'tasks',
        task=task,
        outputdir=f'robotlog/{task}',
        variables=variables,
        consolewidth=120
    )
    return result