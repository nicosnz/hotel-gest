FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runner

WORKDIR /app
ENV PYTHONPATH=/app
RUN apt-get update && apt-get install -y curl

COPY --from=builder /install /usr/local
COPY . .

EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 CMD [ "curl","-f","http://localhost:8000/api/v1/health" ]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]