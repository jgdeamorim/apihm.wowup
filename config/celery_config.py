import os
from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery(
    "hubmercado_tasks",
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=["services.produto_service", "services.bling_service"]
)

celery_app.conf.update(
    task_routes={
        "services.produto_service.*": {"queue": "produto_queue"},
        "services.bling_service.*": {"queue": "bling_queue"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Sao_Paulo",
)

if __name__ == "__main__":
    celery_app.start()
