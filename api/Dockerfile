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

COPY dao.py ./
COPY main.py ./
COPY models.py ./
COPY PostgresStorage.py ./

CMD [ "gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "main:app" ]