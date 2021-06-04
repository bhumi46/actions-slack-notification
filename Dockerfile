FROM python:3.9.5-slim

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

RUN pip install -r requirements.txt \
    && chmod +x /entrypoint.sh

COPY *.py /src/

ENTRYPOINT [ "/entrypoint.sh" ]