FROM nexus.dpag.io:18078/python:3.9-buster

COPY . /app
WORKDIR /app
RUN pip install -U -r requirements.txt -i https://nexus.dpag.io:8443/nexus/repository/pypi-all/simple

ENTRYPOINT [ "uvicorn", "app:app", "--port","8080" ]

EXPOSE 8080