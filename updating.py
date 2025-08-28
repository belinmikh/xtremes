import asyncio
import json
import logging
import os.path
import time
from random import randint

import requests

from database.interfaces import IDatabase
from datafile.interfaces import IFileSchema


def save_file(url: str, filename: str) -> bool:
    # I failed to do that async for some reason
    session = requests.Session()

    session.headers.update({
        'User-Agent': f'Mozilla/4.{randint(0, 9)} (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    })

    response = session.get(url, verify=False, timeout=30)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        logging.info(f"File saved as {filename}")
        return True
    logging.error(f"Failed to save {filename}")
    return False


async def update(hours_period: float, db: IDatabase, file_schema: IFileSchema, url: str, filename: str):
    while True:
        if not os.path.exists(filename) or time.time() - os.path.getctime(filename) > hours_period * 60 * 60:
            logging.info(f"Saving {filename}...")
            updated = save_file(url, filename)
        else:
            logging.info(f"{filename} is up to date")
            updated = True
        if updated:
            try:
                with open("keywords.json", "r", encoding="utf-8") as file:
                    include = json.load(file)
            except RuntimeError:
                logging.warn("Missing / broken keywords.json")
                include = ["содерж", "изобр", "начин"]
            file_schema.read_from(filename, include)
            await db.fill(file_schema.data)
        await asyncio.sleep(hours_period)
