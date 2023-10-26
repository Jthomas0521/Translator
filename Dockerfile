FROM python:3.10.12 as build

WORKDIR /

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENV NAME World

CMD [ "python", "app/app.py" ]


FROM build as dev
RUN pip3 install -r requirements-dev.txt
RUN useradd -ms /bin/bash vscode && chown -R vscode:vscode /app && chmod 755 -R /app
USER vscode
CMD ["sleep","infinity"]