FROM python:3.11-slim as builder

RUN pip install poetry

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN poetry config virtualenvs.in-project true --local && poetry install --without dev,test


FROM python:3.11-slim

RUN apt-get update

COPY --from=builder /usr/src/app /usr/src/app

WORKDIR /usr/src/app

EXPOSE 8000

ENV PATH="/usr/src/app/.venv/bin:$PATH"

CMD ["uvicorn", "src.asgi:application", "--host", "0.0.0.0", "--port", "8000"]