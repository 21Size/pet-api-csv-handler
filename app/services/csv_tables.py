import csv
import os
from datetime import datetime

from loguru import logger

from app.schemas.csv_tables import Row
from app.schemas.request import BillsFilter


async def build_csv(file: bytes) -> str:
    data = file.decode('utf-8').splitlines()  # конвертируем в нужную кодировку
    rows = csv.DictReader(data, delimiter=",")  # считываем данные в словари
    with open(f"../app/data/bills.csv", "w", encoding="utf-8-sig") as f:  # открываем файл
        writer = csv.DictWriter(f, rows.fieldnames)  # подключаем запись из словарей
        writer.writeheader()  # записываем названия столбцов
        for row in rows:  # итерируемся по строкам
            if len(row) == 6:  # проверяем длину табличной строки
                try:
                    Row(**row)  # валидация строки
                    writer.writerow(row)  # записываем строку
                except Exception as e:
                    logger.error(f"{e} | Row: #{rows.line_num} {row}")  # выводим ошибку валидации
            else:
                logger.error(f"len(row) must be 6 | Row: #{rows.line_num} {row}")  # ошибка о длинне строки
    return os.path.abspath(f.name)  # возвращаем путь к файлу


async def get_filtered_bills_from_csv():
    with open(f"../app/data/bills.csv", "r", encoding="utf-8-sig") as f:  # открываем файл для чтения
        rows = csv.DictReader(f, delimiter=",")  # запускаем считыватель
        for row in rows:  # итерируемся
            yield row  # отдаем объек генератора
