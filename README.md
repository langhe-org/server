## Installing dependencies
```bash
pip install poetry uvicorn
poetry install
```

## Running the server locally

```bash
poetry run python -m uvicorn main:app --reload --port 8080
```

Open [http://localhost:8080/docs](http://localhost:8080/docs) with your browser to see the docs.


## Building the container
```bash
docker build -t [tag] .
```

## Running the container
```bash
docker run -p 8080:8080 [tag]
```

## Pushing the container
```bash
docker push [registry]
```

## Generate migrations
```bash
python -m alembic revision --autogenerate -m "message"
```

## Run migrations
```bash
python -m alembic upgrade head
```
