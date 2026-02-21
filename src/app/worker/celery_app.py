from celery import Celery

from app.config import settings

celery_app = Celery(
    __name__,
    broker=str(settings.celery.broker_url),
    backend=str(settings.celery.result_backend),
)

celery_app.conf.update(**settings.celery.model_dump(exclude={'broker_url', 'result_backend'}))
