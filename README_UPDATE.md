# FastAPI-XKit Examples Update Pack

This ZIP contains:
- docker-compose.yml (Redis + Postgres + Jaeger)
- examples/app_full.py (JWT + RBAC + Rate Limit + Audit DB + OpenTelemetry)
- examples/run.sh

## How to use

1. Extract this ZIP into your FastAPI-XKit repo root.
2. Run:

```bash
docker compose up -d
```

3. Install optional dependencies:

```bash
pip install psycopg2-binary sqlalchemy
```

4. Run example app:

```bash
bash examples/run.sh
```

Open:
- API: http://localhost:8000
- Jaeger UI: http://localhost:16686
