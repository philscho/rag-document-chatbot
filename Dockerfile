FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY app/ ./app/
COPY data/chroma_db ./data/chroma_db

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

CMD [ "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000" ]
