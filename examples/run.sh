#!/bin/bash
export JWT_SECRET="supersecret"
export REDIS_URL="redis://localhost:6379/0"
export DATABASE_URL="postgresql+psycopg2://fastapixkit:fastapixkit@localhost:5432/fastapixkit_db"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"

uvicorn examples.app_full:app --reload --port 8000
