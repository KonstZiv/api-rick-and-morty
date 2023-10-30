from celery import shared_task

from characters.scraper import sync_characters_with_api


@shared_task
def sync_db():
    return sync_characters_with_api()
