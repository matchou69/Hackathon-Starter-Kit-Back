FROM python:3.11.4-bookworm

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y postgresql-client vim
WORKDIR /code

ENV PYTHONPATH=/code/app

COPY ./app/requirements-dev.txt ./app/requirements.txt
RUN CPUCOUNT=1 pip install -r ./app/requirements.txt

EXPOSE 5001

ENTRYPOINT [ "bash", "-cl", "./envs/dev/back/back-start.sh" ]