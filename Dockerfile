FROM python:3.12-slim

WORKDIR /app
RUN pip install pipenv
COPY app/Pipfile app/Pipfile.lock /app/
RUN pipenv sync --system

COPY app/ /app/

ENTRYPOINT ["python", "app.py"]
