FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

RUN python -m pip uninstall -y pip \
    && useradd -u 1001 appuser \
    && mkdir -p /data \
    && chown appuser:appuser /data

COPY --from=builder /install /usr/local
COPY app.py .

USER appuser
EXPOSE 8080
CMD ["python", "app.py"]
