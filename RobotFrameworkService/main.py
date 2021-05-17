import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uvicorn import Server
from uvicorn.config import Config

from RobotFrameworkService.Config import Config as RFS_Config
from RobotFrameworkService.routers import robotframework
from RobotFrameworkService.version import get_version


APP_NAME = 'Robot Framework Server'
app = FastAPI(title=APP_NAME, version=get_version())
app.include_router(robotframework.router)
robotlog = StaticFiles(directory="logs")
app.mount("/logs", robotlog, name="robotlog")


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


def get_config():
    return args


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--taskfolder", default='tasks', help="Folder with tasks service will executed")
    parser.add_argument('--version', action='version', version=f'Robot Framework Webservice {get_version()}')
    parser.add_argument("-p", "--port", default=os.environ.get('RFS_PORT', default=5003), type=int, help="Port of Robot Framework Webservice")
    args = parser.parse_args()

    RFS_Config().cmd_args=args

    server = Server(config=(Config(app=app, loop="asyncio", host="0.0.0.0", port=args.port)))
    server.run()


