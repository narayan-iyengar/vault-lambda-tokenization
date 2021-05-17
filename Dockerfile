FROM amazon/aws-lambda-python:3.8

RUN pip install hvac
COPY app.py ./
COPY payload.json ./
COPY encode.json ./
CMD ["app.handler"]
