FROM python:3.11-slim
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt update
RUN apt -y upgrade

RUN python -m pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY enums ./enums
COPY models ./models
COPY protos ./protos
COPY services ./services
COPY main.py ./

CMD [ "python", "main.py" ]
