import asyncio

from celery import shared_task

from characters.async_scraper import scrape_all_pages
from characters.scraper import sync_characters_with_api


@shared_task
def sync_db():
    return sync_characters_with_api()


@shared_task
def async_sync_db():
    return asyncio.run(scrape_all_pages())
