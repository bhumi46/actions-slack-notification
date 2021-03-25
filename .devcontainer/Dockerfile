ARG ARG_DOCKER_CLIENT_VERSION=19.03.8
FROM belldata/docker-client:${ARG_DOCKER_CLIENT_VERSION} as client

FROM python:3
ENV TZ=Asia/Tokyo
ARG ARG_DOCKER_CLIENT_VERSION=19.03.8

ENV DOCKER_CLIENT_VERSION=${ARG_DOCKER_CLIENT_VERSION}
ENV DOCKER_API_VERSION=1.40
COPY --from=client docker-${DOCKER_CLIENT_VERSION}.tgz .

RUN mkdir /src \
    && apt-get update \
    && apt-get install -y tzdata git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && tar xzvf docker-${DOCKER_CLIENT_VERSION}.tgz \
    && mv docker/* /usr/bin/ \
    && rm -rf docker-${DOCKER_CLIENT_VERSION}.tgz \
    && cd /tmp \
    && git clone https://github.com/awslabs/git-secrets.git \
    && cd git-secrets \
    && make install \
    && git secrets --register-aws --global \
    && cd ../ \
    && rm -rf git-secrets

WORKDIR /src/

CMD [ "bash" ]