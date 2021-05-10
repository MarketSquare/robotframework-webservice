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


@app.get('/set_polling_intervall/{seconds}')
def set_polling_intervall(seconds: int):
    if seconds < 1:
        raise fastapi.HTTPException(
            status_code=400,
            detail='Polling  interval must be at least 1 second'
        )
    POLLING_THREAD.set_polling_intervall_seconds(seconds)
    return seconds


@app.get('/get_polling_intervall/')
def get_polling_intervall():
    return POLLING_THREAD.get_polling_intervall_seconds()


@app.get('/stop_polling/')
def stop_polling():
    return POLLING_THREAD.stop()


@app.get('/set_poll_task/{task}')
def set_poll_task(task: str):
    return POLLING_THREAD.set_robot_task(task)


@app.get('/set_topic/{topic}')
def set_topic(topic: str):
    POLLING_THREAD.set_topic(topic)
    return topic


@app.get('/get_topic/')
def get_topic():
    return POLLING_THREAD.get_topic()


@app.get('/start_camunda_polling/')
def start_polling():
    return POLLING_THREAD.run()


@app.get('/set_camunda_poll_url/')
def set_poll_url_for_camunda(poll_url: str):
    POLLING_THREAD.set_poll_url(poll_url)
    return poll_url


@app.get('/get_camunda_poll_url/')
def get_poll_url_for_camunda():
    return POLLING_THREAD.get_poll_url()


def ask_for_work(topic: str, poll_url: str):
    response = requests.get(f"{poll_url}/engine-rest/external-task/count?topicName={topic}")
    response.raise_for_status()
    content = json.loads(response.content.decode())
    return content


def start_robot_task(task: str, variables: list = None) -> int:
    result: int = robot.run(
        'tasks',
        task=task,
        outputdir=f'robotlog/{task}',
        variables=variables,
        consolewidth=120
    )
    return result


class CamundaPollThread(threading.Thread):

    def __init__(self, seconds: int = 1800, robot_task: str = "default_task", topic: str ="default_topic", poll_url: str = "default_url") -> None:
        threading.Thread.__init__(self)
        self.polling = True
        self.robot_task = robot_task
        self.topic = topic
        self.poll_url = poll_url
        self.work_present = ask_for_work(self.topic, self.poll_url)
        self.polling_intervall_seconds = seconds
        self.stopping_event = threading.Event()

    def run(self) -> None:
        if self.work_present:
            while self.polling:
                self.work()
                self.stopping_event.wait(self.polling_intervall_seconds)
                self.stopping_event.clear()

    def set_robot_task(self, var_robot_task: str) -> None:
        self.robot_task = var_robot_task

    def set_polling_intervall_seconds(self, seconds: int) -> None:
        self.polling_intervall_seconds = seconds
        self.stopping_event.set()

    def get_polling_intervall_seconds(self) -> int:
        return self.polling_intervall_seconds

    def set_topic(self, topic: str) -> None:
        self.topic = topic

    def get_topic(self) -> str:
        return self.topic

    def set_poll_url(self, poll_url: str) -> None:
        self.poll_url = poll_url

    def get_poll_url(self) -> str:
        return self.poll_url

    def work(self) -> None:
        robot.run(
            self.robot_task,
            outputdir=f'robotlog/{self.robot_task}',
            variables='variables.yaml'
            )

    def stop(self) -> None:
        self.polling = False
        self.stopping_event.set()


POLLING_THREAD = CamundaPollThread(seconds=1800, robot_task='default_task')
POLLING_THREAD.start()
