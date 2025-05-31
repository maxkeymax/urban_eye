from celery import Celery

from urban_eye.settings import settings

celery_app = Celery(
    "urban_eye",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["urban_eye.tasks.video_tasks"],
)

celery_app.conf.update(
    task_default_queue="default",
    timezone="UTC",
    enable_utc=True,
    worker_hijack_root_logger=False,
)
