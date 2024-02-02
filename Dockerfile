FROM python:alpine3.19

WORKDIR /app

RUN mkdir logs

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "main.py", "import", "--cves"]

