import csv
import os
from datetime import datetime

from loguru import logger

from app.schemas.csv import Row


async def build_csv(file: bytes, filename: str):
    data = file.decode('utf-8').splitlines()
    rows = csv.DictReader(data, delimiter=",")
    with open(f"../app/data/{datetime.now().date()}-{filename}", "w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        for row in rows:
            if rows.line_num > 1 and len(row) == 6:
                try:
                    Row(**row)
                    writer.writerow(row.values())
                except Exception as e:
                    logger.error(f"{e} | Row: #{rows.line_num} {row}")
    return os.path.abspath(f.name)
