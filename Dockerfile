FROM python:3.9 as base

ENV PYTHONUNBUFFERED=1

ENV FASTAPI_DIR=/api_fast_api

WORKDIR $FASTAPI_DIR

RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    python3-gdal \
    && rm -rf /var/lib/apt/lists/*

COPY . $FASTAPI_DIR/

RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
