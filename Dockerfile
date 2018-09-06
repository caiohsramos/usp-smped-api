FROM python:3.6
COPY . /app
WORKDIR /app

RUN pip install -r src/requirements.txt
EXPOSE 5000
CMD ["python","src/app.py"]