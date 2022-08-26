## Running the server

```bash
python -m uvicorn main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) with your browser to see the docs.


## Deploying
```bash
poetry export -f requirements.txt -o requirements.txt
gcloud app deploy
```

## Generate migrations
```bash
python -m alembic revision --autogenerate -m "message"
```

## Run migrations
```bash
python -m alembic upgrade head
```