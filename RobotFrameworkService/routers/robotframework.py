from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response, RedirectResponse

import robot


router = APIRouter(
    prefix="/robotframework",
    tags=["robotframework"],
    responses={404: {"description": "Not found"}},
)


@router.get('/run/{task}')
def run_task(task):
    """
    Run a given task.
    """
    result: int = start_robot_task(task)
    if result == 0:
        result_page = 'PASS'
    elif 250 >= result >= 1:
        result_page = f'FAIL: {result} tasks failed'
    else:
        result_page = f'FAIL: Errorcode {result}'
    result_page += f'<p><a href="/robotlog/{task}/log.html">Go to log</a></p>'
    return Response(content=result_page, media_type="text/html")


@router.get('/run_and_show/{task}', response_class=HTMLResponse)
def start_robot_task_and_show_log(task: str, arguments: Request):
    """
    Run a given task with variables and return log.html
    """
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    start_robot_task(task, variables)
    return RedirectResponse(f"/robotlog/{task}/log.html")


@router.get('/run_and_show_report/{task}', response_class=HTMLResponse)
def start_robot_task_and_show_report(task: str, arguments: Request):
    """
    Run a given task with variables and return report.html
    """
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    start_robot_task(task, variables)
    return RedirectResponse(f"/robotlog/{task}/report.html")


@router.get('/show_log/{task}', response_class=HTMLResponse)
def show_log(task: str):
    """
    Show most recent log.html of given task
    """
    return RedirectResponse(f'/robotlog/{task}/log.html')


@router.get('/show_report/{task}', response_class=HTMLResponse)
def show_report(task: str):
    """
    Show most recent report.html of given task
    """
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
