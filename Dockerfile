FROM python:3.10.12 as build

WORKDIR /

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV NAME World
WORKDIR /app
RUN useradd -ms /bin/bash vscode && chown -R vscode:vscode /app && chmod 755 -R /app
USER vscode
COPY ./ /app

CMD [ "python", "/app/src/app.py" ]


FROM build as dev
WORKDIR /app
COPY requirements-dev.txt ./requirements-dev.txt
RUN pip3 install -r requirements-dev.txt
