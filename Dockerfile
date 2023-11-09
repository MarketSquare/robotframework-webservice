FROM python:3.11

ENV SUITE_FOLDER .
ENV PORT 5003

WORKDIR robot

RUN mkdir logs
RUN pip install robotframework-webservice

EXPOSE ${PORT}

ENTRYPOINT exec python -m RobotFrameworkService.main -p ${PORT} -t ${SUITE_FOLDER}