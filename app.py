import robot
import sys
from flask import Flask, send_from_directory, jsonify, redirect, url_for, request

app = Flask(__name__, static_url_path='')


@app.route('/')
def greetings():
    return 'Webserver zum Starten von RobotTasks'


@app.route('/status/')
def server_status():
    app.logger.info(f'Incoming status request...')
    status = {'Python Version': sys.version,
              'Platform': sys.platform,
              'Arguments': sys.argv}
    return jsonify(status)


@app.route('/robotlog/<path:path>')
def browse_robot_log(path):
    return send_from_directory('robotlog', path)


@app.route('/run/<path:task>')
def do_some_work(task):
    app.logger.info(f'Incoming request for task {task}')
    result: int = here_comes_work(task)
    if result == 0:
        result_page = 'PASS'
    elif 250 >= result >= 1:
        result_page = f'FAIL: {result} tasks failed'
    else:
        result_page = f'FAIL: Errorcode {result}'
    result_page += '<p><a href="../robotlog/log.html">Go to log</a></p>'
    return result_page


@app.route('/run_and_show/<path:task>')
def do_some_work_and_show_log(task):
    here_comes_work(task)
    return redirect(url_for('browse_robot_log', path='log.html'))


def here_comes_work(task: str) -> int:
    robot_variables: list = [f'{k}:{v}' for k, v in request.args.to_dict().items()]
    result: int = robot.run(
        'tasks',
        task=task,
        variable=robot_variables,
        outputdir='robotlog',
        consolewidth=120
    )
    return result
