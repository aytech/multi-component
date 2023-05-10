FROM python:3.9-slim
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt update
RUN apt -y upgrade

RUN python -m pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY db ./db
COPY errors ./errors
COPY protos ./protos
COPY utilities ./utilities
COPY main.py ./
COPY PostgresStorage.py ./
COPY routes.py ./

CMD [ "gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "main:app" ]