FROM python:3.10.12

WORKDIR /

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENV NAME World

CMD [ "python", "app/app.py" ]