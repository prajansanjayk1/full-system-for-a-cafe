from celery import shared_task

from apps.payments.services import process_webhook_event


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True, max_retries=8)
def process_payment_webhook(self, event_id):
    process_webhook_event(event_id=event_id)
