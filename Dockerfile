FROM python:3.8-slim

WORKDIR /dir

COPY . ./

EXPOSE 8000

RUN pip install --requirement requirements.txt

CMD gunicorn --bind 0.0.0.0:8000 server:app --timeout 20000 --workers=1 --capture-output
