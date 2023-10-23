FROM python3.10.12

WORKDIR /

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV NAME World

CMD [ "python", "app.py" ]