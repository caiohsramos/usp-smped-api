FROM python:3.6
COPY ./app /app
WORKDIR /app
EXPOSE 5000

RUN pip install -r requirements.txt
CMD ["python", "main.py"]
