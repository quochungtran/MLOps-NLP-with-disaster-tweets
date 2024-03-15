FROM python:3.9-slim

WORKDIR /mlflow/

RUN pip install --no-cache-dir mlflow==2.3.2

EXPOSE 5000

CMD mlflow server \
    --backend-store-uri sqlite:////mlflow/mlflow.db \
    --serve-artifacts \
    --host 0.0.0.0 \
    --port 5000