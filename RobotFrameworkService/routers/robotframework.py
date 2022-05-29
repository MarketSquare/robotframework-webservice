import time

from fastapi import APIRouter, Request, Path
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from RobotFrameworkService.Config import Config as RFS_Config

import robot


router = APIRouter(
    prefix="/robotframework",
    responses={404: {"description": "Not found"}},
)


@router.get('/run/all', tags=["execution"])
async def run(request: Request):
    """
    Run all task available.
    """
    id = request.headers["request-id"]
    result: int = _start_all_robot_tasks(id)
    if result == 0:
        result_page = 'PASS'
        status_code = 200
    elif 250 >= result >= 1:
        result_page = f'FAIL: {result} tasks failed'
        status_code = 400
    else:
        result_page = f'FAIL: Errorcode {result}'
        status_code = 500
    result_page += f'<p><a href="/logs/{id}/log.html">Go to log</a></p>'
    return Response(content=result_page, media_type="text/html", status_code=status_code)


@router.get('/run/{task}', tags=["execution"])
async def run_task(task, request: Request):
    """
    Run a given task.
    """
    id = request.headers["request-id"]
    result: int = _start_specific_robot_task(id, task)
    if result == 0:
        result_page = 'PASS'
    elif 250 >= result >= 1:
        result_page = f'FAIL: {result} tasks failed'
    else:
        result_page = f'FAIL: Errorcode {result}'
    result_page += f'<p><a href="/logs/{task}/log.html">Go to log</a></p>'
    return Response(content=result_page, media_type="text/html")


@router.get('/run_and_show/{task}', tags=["execution"], response_class=HTMLResponse)
async def start_robot_task_and_show_log(task: str, arguments: Request):
    """
    Run a given task with variables and return log.html
    """
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    _start_specific_robot_task(task, variables)
    return RedirectResponse(f"/logs/{task}/log.html")


@router.get('/run_and_show_report/{task}', tags=["execution"], response_class=HTMLResponse)
async def start_robot_task_and_show_report(task: str, arguments: Request):
    """
    Run a given task with variables and return report.html
    """
    variables = [f'{k}:{v}' for k, v in arguments.query_params.items()]
    _start_specific_robot_task(task, variables)
    return RedirectResponse(f"/logs/{task}/report.html")


@router.get('/show_log/{executionid}', tags=["reporting"], response_class=HTMLResponse)
async def show_log(executionid: str = Path(
    title="ID of a previous request",
    description="Insert here the value of a previous response header field 'x-request-id'"
    )
    ):
    """
    Show most recent log.html from a given execution
    """
    return RedirectResponse(f'/logs/{executionid}/log.html')


@router.get('/show_report/{executionid}', tags=["reporting"], response_class=HTMLResponse)
async def show_report(executionid: str = Path(
    title="ID of a previous request",
    description="Insert here the value of a previous response header field 'x-request-id'"
    )
    ):
    """
    Show most recent report.html from a given execution
    """
    return RedirectResponse(f'/logs/{executionid}/report.html')


def _start_all_robot_tasks(id: str, variables: list = None) -> int:
    config = RFS_Config().cmd_args
    if variables is None:
        variables = []
    if config.variablefiles is None:
        variablefiles=[]
    else:
        variablefiles=config.variablefiles

    return robot.run(
        config.taskfolder,
        outputdir=f'logs/{id}',
        debugfile=config.debugfile,
        variable=variables,
        variablefile=variablefiles,
        consolewidth=120
    )


def _start_specific_robot_task(id: str, task: str, variables: list = None) -> int:
    config = RFS_Config().cmd_args
    if variables is None:
        variables = []
    if config.variablefiles is None:
        variablefiles=[]
    else:
        variablefiles=config.variablefiles

    return robot.run(
            config.taskfolder,
            task=task,
            outputdir=f'logs/{id}',
            debugfile=config.debugfile,
            variable=variables,
            variablefile=variablefiles,
            consolewidth=120
        )
