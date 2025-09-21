# monitoring/metrics.py
# Este archivo define las métricas que deberías exponer en /metrics usando prometheus_client.
from prometheus_client import Counter, Histogram, Gauge

# Prefijo fashion_
REQUESTS = Counter("fashion_requests_total", "Total requests", ["method", "endpoint", "status"])
RESPONSE_TIME = Histogram("fashion_response_duration_seconds", "Response duration seconds", ["method", "endpoint"])
STOCK_LEVEL = Gauge("fashion_stock_level", "Stock level per product/talla", ["product_id", "talla"])
LOW_STOCK_ALERTS = Counter("fashion_low_stock_alerts_total", "Low stock alerts triggered", ["product_id"])
