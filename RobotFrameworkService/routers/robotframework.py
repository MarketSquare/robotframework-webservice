import pathlib

from fastapi import APIRouter, Request, Path
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from starlette.responses import JSONResponse

from RobotFrameworkService.Config import Config as RFS_Config
from ..constants import LOGS

import robot

import multiprocessing as mp

router = APIRouter(
    prefix="/robotframework",
    responses={404: {"description": "Not found: Webservice is either busy or requested endpoint is not supported."}},
)

async def run_robot_in_brackground(func, args=[], kwargs={}):
    p = mp.Process(target=func, args=args, kwargs=kwargs)
    p.start()
    return p

async def run_robot_and_wait(func, args=[], kwargs={}):
    # this is still blocking
    result: int = func(*args, **kwargs)
    if result == 0:
        result_page = 'PASS'
        result_page += f'<p><a href="/logs/{id}/log.html">Go to log</a></p>'
        status_code = 200
    elif 250 >= result >= 1:
        result_page = f'FAIL: {result} tasks failed'
        result_page += f'<p><a href="/logs/{id}/log.html">Go to log</a></p>'
        status_code = 400
    else:
        result_page = f'FAIL: Errorcode {result}'
        status_code = 500
    
    return Response(content=result_page, media_type="text/html", status_code=status_code)


@router.get('/run/all', tags=["execution"])
async def run_all(request: Request):
    """
    Run all task available.
    """
    id = request.headers["request-id"]
    response = await run_robot_and_wait(func=_start_all_robot_tasks, args=[id])
    
    return response


@router.get('/run/all/async', tags=["execution"])
async def run_all_async(request: Request):
    """
    Starts all Robot tasks. Returns execution id and continures to run Robot tasks in background.
    """
    id = request.headers["request-id"]
    await run_robot_in_brackground(func=_start_all_robot_tasks, args=[id])
    return id


@router.get('/run/{task}', tags=["execution"])
async def run_task(task, request: Request):
    """
    Run a given task.
    """
    id = request.headers["request-id"]
    variables = RequestHelper.parse_variables_from_query(request)   
    response = await run_robot_and_wait(func=_start_specific_robot_task, kwargs={'id': id, 'task':task, 'variables':variables})
    return response


@router.get('/run/{task}/async', tags=["execution"])
async def run_task_async(task, request: Request):
    """
    Start a given task. Returns execution id and continues to run Robot task in background.
    """
    id = request.headers["request-id"]
    variables = RequestHelper.parse_variables_from_query(request)   
    await run_robot_in_brackground(func=_start_specific_robot_task, kwargs={'task':task, 'variables':variables})
    return id

@router.get('/run/suite/{suite}', tags=["execution"])
async def run_suite(suite, request: Request):
    """
    Run a given suite.
    """
    id = request.headers["request-id"]
    variables = RequestHelper.parse_variables_from_query(request)
    response = await run_robot_and_wait(func=_start_specific_robot_suite, kwargs={'id': id, 'suite':suite, 'variables':variables})
    return response

@router.get('/run/suite/{suite}/async', tags=["execution"])
async def run_suite_async(suite, request: Request):
    """
    Start a given suite. Returns execution id and continues to run Robot suite in background.
    """
    id = request.headers["request-id"]
    variables = RequestHelper.parse_variables_from_query(request)
    await run_robot_in_brackground(func=_start_specific_robot_suite, kwargs={'suite':suite, 'variables':variables})
    return id


@router.get('/run_and_show/{task}', tags=["execution"], response_class=HTMLResponse)
async def start_robot_task_and_show_log(task: str, request: Request):
    """
    Run a given task with variables and return log.html
    """
    id = request.headers["request-id"]
    variables = RequestHelper.parse_variables_from_query(request)
    await run_robot_and_wait(func=_start_specific_robot_task, kwargs={'id':id, 'task':task, 'variables':variables})
    return RedirectResponse(f"/logs/{id}/log.html")


@router.get('/run_and_show_report/{task}', tags=["execution"], response_class=HTMLResponse)
async def start_robot_task_and_show_report(task: str, request: Request):
    """
    Run a given task with variables and return report.html
    """
    id = request.headers["request-id"]
    variables = RequestHelper.parse_variables_from_query(request)
    await run_robot_and_wait(func=_start_specific_robot_task, kwargs={'id':id, 'task':task, 'variables':variables})
    return RedirectResponse(f"/logs/{id}/report.html")


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


@router.get('/show_output/{executionid}', tags=["reporting"], response_class=HTMLResponse)
async def show_raw_output(executionid: str = Path(
    title="ID of a previous request",
    description="Insert here the value of a previous response header field 'x-request-id'"
)
):
    """
    Show most recent report.html from a given execution
    """
    return RedirectResponse(f'/logs/{executionid}/output.xml')


@router.get('/executions', tags=["execution"], response_class=JSONResponse)
async def show_execution_ids():
    """
    get all execution ids for the finished tasks
    """
    logs = pathlib.Path(f'./{LOGS}')
    is_execution_finished = (lambda x:
                             x.is_dir()
                             and (x / 'report.html').exists()
                             and (x / 'log.html').exists())
    return [log.stem for log in logs.iterdir() if is_execution_finished(log)]


def _start_all_robot_tasks(id: str, variables: list = None) -> int:
    config = RFS_Config().cmd_args
    if variables is None:
        variables = []
    if config.variablefiles is None:
        variablefiles = []
    else:
        variablefiles = config.variablefiles

    return robot.run(
        config.taskfolder,
        outputdir=f'logs/{id}',
        debugfile=config.debugfile,
        variable=variables,
        variablefile=variablefiles,
        consolewidth=120
    )

def _start_specific_robot_suite(id: str, suite: str, variables: list=None) -> int:
    config = RFS_Config().cmd_args
    if variables is None:
        variables = []
    if config.variablefiles is None:
        variablefiles = []
    else:
        variablefiles = config.variablefiles

    return robot.run(
        config.taskfolder,
        suite=suite,
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
        variablefiles = []
    else:
        variablefiles = config.variablefiles

    return robot.run(
        config.taskfolder,
        task=task,
        outputdir=f'logs/{id}',
        debugfile=config.debugfile,
        variable=variables,
        variablefile=variablefiles,
        consolewidth=120
    )


class RequestHelper:
    @staticmethod
    def parse_variables_from_query(arguments: Request) -> list:
        return [f'{k}:{v}' for k, v in arguments.query_params.items()]
