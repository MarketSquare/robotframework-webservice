import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import robotframework
from .version import get_version


APP_NAME = 'Robot Task Server'
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



