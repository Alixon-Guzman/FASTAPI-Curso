# app/middleware/domain_logger.py
import logging
import os
from datetime import datetime

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "fashion_domain.log")

logger = logging.getLogger("fashion_domain")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

def log_stock_change(product_id: int, talla: str, old_stock: int, new_stock: int, user: str = "system"):
    logger.info(f"STOCK_CHANGE product_id={product_id} talla={talla} old={old_stock} new={new_stock} by={user}")
