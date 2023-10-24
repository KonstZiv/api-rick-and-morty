from typing import Callable

import requests
from django.conf import settings

from characters.models import Character


def scrape_page(response_api_dict: dict) -> list[Character]:
    characters = []
    for character_api_dict in response_api_dict["results"]:
        characters.append(
            Character(
                api_id=character_api_dict["id"],
                name=character_api_dict["name"],
                status=character_api_dict["status"],
                species=character_api_dict["species"],
                gender=character_api_dict["gender"],
                image=character_api_dict["image"],
            )
        )
    return characters


def scrape_all_pages(
    url: str = settings.API_RICK_AND_MORTY_URL,
    scrape_page_func: Callable = scrape_page,
) -> list[Character]:
    characters_all = []
    next_page = url
    while next_page:
        response_api_dict = requests.get(next_page).json()
        characters_page = scrape_page_func(response_api_dict)
        characters_all.extend(characters_page)
        next_page = response_api_dict["info"]["next"]

    return characters_all


def save_characters(characters: list[Character]):
    objs = Character.objects.bulk_create(characters)
    return objs


def sync_characters_with_api(url: str = settings.API_RICK_AND_MORTY_URL) -> None:
    characters = scrape_all_pages(url, scrape_page)
    save_characters(characters)
