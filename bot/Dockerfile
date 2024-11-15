FROM python:3.12-slim

WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv sync --system

COPY src/ .

ENTRYPOINT ["python", "app.py"]
