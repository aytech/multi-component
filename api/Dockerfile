FROM python:3.9-slim
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt update
RUN apt -y upgrade

RUN python -m pip install --upgrade pip
COPY ./api/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./protobuf/proto ./proto
COPY ./api/utilities ./utilities
COPY ./api/main.py ./
COPY ./api/routes.py ./

RUN python -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. ./proto/*.proto
RUN pip uninstall -y grpcio-tools

CMD [ "gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "main:app" ]