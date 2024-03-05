FROM python:3.9 as requirements-stage

WORKDIR /app

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

WORKDIR /app

COPY --from=requirements-stage /app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]