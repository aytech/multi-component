FROM python:3.11-slim
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt update
RUN apt -y upgrade

RUN python -m pip install --upgrade pip
COPY ./storage-connector/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./storage-connector/enums ./enums
COPY ./storage-connector/models ./models
COPY ./protobuf/proto ./proto
COPY ./storage-connector/services ./services
COPY ./storage-connector/main.py ./

RUN python -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. ./proto/*.proto
RUN pip uninstall -y grpcio-tools

CMD [ "python", "main.py" ]
