from celery import Celery
from config.celery_config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["services.produto_service"]
)

if __name__ == "__main__":
    celery_app.start()
