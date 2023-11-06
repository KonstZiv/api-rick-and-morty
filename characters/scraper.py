from typing import Callable

import requests
from django.conf import settings
from django.db import IntegrityError

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


def save_or_update_characters(characters: list[Character]):
    updated = 0
    created = 0
    characters_api = characters
    characters_db = Character.objects.all()
    characters_diff = set(characters_api) - set(characters_db)
    for character in characters_diff:
        try:
            character.save()
            created += 1
        except IntegrityError:
            Character.objects.filter(api_id=character.api_id).update(
                name=character.name,
                status=character.status,
                species=character.species,
                gender=character.gender,
                image=character.image,
            )
            updated += 1

    return {"updated": updated, "created": created}


def sync_characters_with_api(
    url: str = settings.API_RICK_AND_MORTY_URL,
) -> dict[str, int]:
    characters = scrape_all_pages(url, scrape_page)
    return save_or_update_characters(characters)
