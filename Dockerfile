FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888

CMD ["python", "newproject/manage.py", "runserver", "0.0.0.0:8888"]
