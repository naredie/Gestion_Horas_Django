FROM python:3.9

ENV PYTHONUNBUFFERED=1

ARG UID=1000
ENV UID=${UID}
ARG GID=1000
ENV GID=${GID}

ENV PATH="/home/docker/.local/bin:$PATH"

RUN groupadd -g ${GID} -o docker && useradd -r -u ${UID} -g ${GID} docker
RUN mkdir /home/docker && chown -R ${UID}:${GID} /home/docker
USER docker

WORKDIR /code

COPY requirements.txt /code/
COPY requirements-dev.txt /code/
RUN python -m pip install --upgrade pip && python -m pip install --no-cache --user -r requirements-dev.txt
# COPY . /code/
