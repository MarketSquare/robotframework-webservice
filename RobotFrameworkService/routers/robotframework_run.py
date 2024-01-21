import asyncio
import multiprocessing as mp
from concurrent.futures import Executor
from typing import Optional

import robot
from fastapi import Body, APIRouter, Request, status
from fastapi.responses import Response
from typing_extensions import Annotated

from RobotFrameworkService.Config import Config as RFS_Config
from RobotFrameworkService.requests.RobotOptions import RobotOptions

router = APIRouter(
    prefix="/robotframework",
    responses={
        404: {
            "description": "Not found: Webservice is either busy or requested endpoint is not supported."
        }
    },
)

run_examples = {
    "Suite run": {
        "value": {
            "paths": ["examples"],
            "suite": "tasks"
        },
    },
    "Test run": {
        "value": {
            "paths": ["examples"],
            "test": "Demonstration Test"
        },
    },
    "Task run": {
        "value": {
            "paths": ["examples"],
            "task": "Demonstration Task"
        },
    },
    "Task sync run": {
        "value": {
            "paths": ["examples"],
            "task": "Demonstration Task",
            "sync": True
        },
    },
    "Tests run with included tags": {
        "value": {
            "paths": ["examples"],
            "include_tags": ["tag"]
        },
    },
    "Tests run with TRACE log level": {
        "value": {
            "paths": ["examples"],
            "test": "Log With Levels",
            "loglevel": "TRACE"
        },
    },
    "Task run with variables": {
        "value": {
            "paths": ["examples"],
            "task": "Task with more variables",
            "variables": {"firstname": "Max", "lastname": "Mustermann"}
        },
    }
}


def validate_robot_options(body: RobotOptions) -> Optional[str]:
    if body.test and body.suite:
        return "Options test and suite cannot be both specified"
    if body.task and body.suite:
        return "Options task and suite cannot be both specified"
    if body.test and body.task:
        return "Options test and task cannot be both specified"


def build_robot_options(id: str, body: RobotOptions) -> (list, dict):
    config = RFS_Config().cmd_args

    options = {
        "outputdir": f"logs/{id}",
        "rpa": body.rpa,
        "consolewidth": 120,
        "loglevel": body.loglevel
    }

    if body.test:
        options["test"] = body.test

    if body.task:
        options["task"] = body.task

    if body.suite:
        options["suite"] = body.suite

    if body.variables:
        variables = [f"{k}:{v}" for k, v in body.variables.items()]
        options["variable"] = variables

    if body.include_tags:
        options["include"] = body.include_tags
    if body.exclude_tags:
        options["exclude"] = body.exclude_tags

    if config.variablefiles:
        options["variablefile"] = config.variablefiles

    if config.debugfile:
        options["debugfile"] = config.debugfile

    return body.paths or [config.taskfolder], options


@router.post("/run", tags=["execution"])
async def run(robot_options: Annotated[RobotOptions, Body(openapi_examples=run_examples)], request: Request):
    errors = validate_robot_options(robot_options)
    if errors:
        return Response(
            content=errors, media_type="text/html", status_code=status.HTTP_400_BAD_REQUEST
        )
    id = request.headers["request-id"]
    tests, options = build_robot_options(id, robot_options)
    if robot_options.sync:
        response = await run_robot_and_wait(
            request.app.state.executor,
            id,
            func=_run_robot,
            args=[tests, options],
        )
        return response
    else:
        await run_robot_in_background(
            func=_run_robot,
            args=[tests, options],
        )
        return id


async def run_robot_in_background(func, args: list):
    p = mp.Process(target=func, args=args)
    p.start()
    return p


async def run_robot_and_wait(executor: Executor, id, func, args: list):
    loop = asyncio.get_event_loop()
    result: int = await loop.run_in_executor(executor, func, *args)
    if result == 0:
        result_page = "PASS"
        result_page += f'<p><a href="/logs/{id}/log.html">Go to log</a></p>'
        status_code = status.HTTP_200_OK
    elif 250 >= result >= 1:
        result_page = f"FAIL: {result} tasks failed"
        result_page += f'<p><a href="/logs/{id}/log.html">Go to log</a></p>'
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        result_page = f"FAIL: Errorcode {result}"
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return Response(
        content=result_page, media_type="text/html", status_code=status_code
    )


def _run_robot(tests: list, options: dict) -> int:
    return robot.run(
        *tests,
        **options
    )
