FROM python:3.14-slim

ENV SUITE_FOLDER .
ENV VARIABLE_FILES ""
ENV PORT 5003

WORKDIR /robot

RUN mkdir logs
RUN pip install robotframework-webservice

EXPOSE ${PORT}

COPY docker-entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/robot/entrypoint.sh"]