import asyncio
from typing import Tuple, Optional, List

import aiohttp
from django.conf import settings
from django.db import IntegrityError
from dataclasses import dataclass, asdict

from characters.models import Character


@dataclass
class UpdateResult:
    updated: int
    created: int


async def scrape_page(
    session: aiohttp.ClientSession,
    page: int = 1,
    url_graph: str = settings.GRAPHQL_RICK_AND_MORTY_URL,
) -> Tuple[List[dict], int]:
    query = f"""{{
  characters(page: {page}) {{
    info {{
      pages
    }}
    results {{
      api_id: id
      name
      status
      species
      gender
      image
    }}
  }}
}}"""
    response_api = await session.post(url_graph, json={"query": query})
    response_api_dict = await response_api.json()
    pages = response_api_dict["data"]["characters"]["info"]["pages"]
    return response_api_dict["data"]["characters"]["results"], pages


async def save_or_update_characters(
    characters_api_list: List[dict],
    results: Optional[UpdateResult] = None,
) -> dict:
    if not results:
        results = UpdateResult(0, 0)
    characters_api = [
        Character(**character_dict) for character_dict in characters_api_list
    ]
    characters_db = set()
    async for character_db in Character.objects.all():
        characters_db.add(character_db)
    characters_diff = set(characters_api) - set(characters_db)

    for character in characters_diff:
        try:
            await character.asave()
            results.created += 1
        except IntegrityError:
            await Character.objects.filter(api_id=character.api_id).aupdate(
                name=character.name,
                status=character.status,
                species=character.species,
                gender=character.gender,
                image=character.image,
            )
            results.updated += 1

    return asdict(results)


async def scrape_all_pages(
    url_graph: str = settings.GRAPHQL_RICK_AND_MORTY_URL,
) -> dict:
    async with aiohttp.ClientSession() as session:
        characters_api_list, pages = await scrape_page(session=session, page=0)
        async with asyncio.TaskGroup() as tg:
            page_results = [
                tg.create_task(
                    scrape_page(session=session, page=page, url_graph=url_graph)
                )
                for page in range(2, pages + 1)
            ]
    for page_result in page_results:
        characters_api_list += page_result.result()[0]
    return await save_or_update_characters(characters_api_list)
