FROM debian:10 as client

ENV DOCKER_CLIENT_VERSION=19.03.8
ENV DOCKER_API_VERSION=1.40
ADD https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_CLIENT_VERSION}.tgz .

RUN apt-get update \
    && apt-get install -y curl \
    && curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash -s -- v0.2.21

FROM python:3.9.5-slim
ARG ARG_DOCKER_CLIENT_VERSION=19.03.8
ENV TZ=Asia/Tokyo
ENV DOCKER_CLIENT_VERSION=${ARG_DOCKER_CLIENT_VERSION}
ENV DOCKER_API_VERSION=1.40

COPY --from=client docker-${DOCKER_CLIENT_VERSION}.tgz .
COPY --from=client /usr/local/bin/act /usr/local/bin/act
RUN mkdir /src \
    && apt-get update \
    && apt-get install -y tzdata git curl \
    && apt-get clean \
    && tar xzvf docker-${DOCKER_CLIENT_VERSION}.tgz \
    && mv docker/* /usr/bin/ \
    && rm -rf /tmp/* /var/cache/apk/* docker-${DOCKER_CLIENT_VERSION}.tgz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src/

CMD [ "bash" ]