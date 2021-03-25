FROM alpine

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

RUN apk update \
    && apk upgrade \
    && apk add \
    bash \
    jq \
    ca-certificates \
    python3 \
    py3-pip \
    && pip install -r requirements.txt \
    && chmod +x /entrypoint.sh \
    && rm -rf /var/cache/apk/*

COPY *.py /

ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "python3", "main.py" ]