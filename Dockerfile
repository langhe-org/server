FROM python:3.10

WORKDIR /app

RUN pip install poetry uvicorn
RUN poetry init

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry install

COPY . .

EXPOSE 8080

CMD [ "poetry", "run", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080" ]
