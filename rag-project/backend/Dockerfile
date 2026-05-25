FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --default-timeout=1000 -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]