FROM python:3.12-slim

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY bot/ .

CMD ["python", "main.py"]
