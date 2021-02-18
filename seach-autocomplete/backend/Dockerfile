FROM python:3.7-alpine

WORKDIR /home/backtend/

ENV FLASK_APP api.py 

ENV FLASK_RUN_HOST 0.0.0.0

ENV FLASK_RUN_PORT 4000

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run"]