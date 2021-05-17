from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from RobotFrameworkService.Config import Config as RFS_Config

import robot


router = APIRouter(
    prefix="/robotframework",
    tags=["robotframework"],
    responses={404: {"description": "Not found"}},
)


@router.get('/run/{task}')
async def run_task(task):
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
    result_page += f'<p><a href="/logs/{task}/log.html">Go to log</a></p>'
    return Response(content=result_page, media_type="text/html")


@router.get('/run_and_show/{task}', response_class=HTMLResponse)
async def start_robot_task_and_show_log(task: str, arguments: Request):
    """
    Run a given task with variables and return log.html
    """
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    start_robot_task(task, variables)
    return RedirectResponse(f"/logs/{task}/log.html")


@router.get('/run_and_show_report/{task}', response_class=HTMLResponse)
async def start_robot_task_and_show_report(task: str, arguments: Request):
    """
    Run a given task with variables and return report.html
    """
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    start_robot_task(task, variables)
    return RedirectResponse(f"/logs/{task}/report.html")


@router.get('/show_log/{task}', response_class=HTMLResponse)
async def show_log(task: str):
    """
    Show most recent log.html of given task
    """
    return RedirectResponse(f'/logs/{task}/log.html')


@router.get('/show_report/{task}', response_class=HTMLResponse)
async def show_report(task: str):
    """
    Show most recent report.html of given task
    """
    return RedirectResponse(f'/logs/{task}/report.html')


def start_robot_task(task: str, variables: list = None) -> int:
    config = RFS_Config().cmd_args
    result: int = robot.run(
        config.taskfolder,
        task=task,
        outputdir=f'logs/{task}',
        variables=variables,
        consolewidth=120
    )
    return result
