FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --default-timeout=1000 -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]