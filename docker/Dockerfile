# Dockerfile for Python whisk docker action
FROM openwhisk/action-python-v3.6-ai:c5f4cfe

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

