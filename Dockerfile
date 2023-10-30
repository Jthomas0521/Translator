FROM python:3.10.12 as build

WORKDIR /

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENV NAME World
WORKDIR /src
RUN useradd -ms /bin/bash vscode && chown -R vscode:vscode /src && chmod 755 -R /src
USER vscode

CMD [ "python", "/src/app.py" ]


FROM build as dev
WORKDIR /src
COPY requirements-dev.txt ./requirements-dev.txt
RUN pip3 install -r requirements-dev.txt
