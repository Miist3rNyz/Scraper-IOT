FROM python:alpine3.19

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "main.py", "import", "--cves"]

