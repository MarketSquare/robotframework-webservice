import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from RobotFrameworkService.routers import robotframework
from RobotFrameworkService.version import get_version


APP_NAME = 'Robot Framework Server'
app = FastAPI(title=APP_NAME, version=get_version())
app.include_router(robotframework.router)
robotlog = StaticFiles(directory="robotlog")
app.mount("/robotlog", robotlog, name="robotlog")


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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--taskfolder", help="Folder with tasks service will executed")
    args = parser.parse_args()


