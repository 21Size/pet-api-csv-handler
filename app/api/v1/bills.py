from loguru import logger

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.csv_tables import Row
from app.schemas.request import BillsFilter
from app.services.csv_tables import build_csv, get_filtered_bills_from_csv

bills_router = APIRouter(prefix="/bills")


@bills_router.post("/import")
async def post_data(file: UploadFile = File(...)):
    if file.filename[-4:] == ".csv": # проверка формата файла
        b_file = file.file.read()  # чтение файла в байты
        new_file_path = await build_csv(b_file)  # сбор csv
        logger.info("New data recorded")
        # чтобы не блокировать поток
        # bg.add_task(build_csv, b_file)
    else:
        raise HTTPException(400, "file must be .csv")
    return {"new_file_path": new_file_path}


@bills_router.post("/export")
async def get_data(f: BillsFilter):
    data = []
    if f.client_name and f.client_org:  # проверка на наличие фильтров
        async for row in get_filtered_bills_from_csv():  # проходимся по генератору со строками
            if row["client_name"] == f.client_name and row["client_org"] == f.client_org:  # проверяем строку
                data.append(Row(**row))  # добавляем строку в результат

    if f.client_name and not f.client_org:  # проверка на наличие фильтров
        async for row in get_filtered_bills_from_csv():  # проходимся по генератору со строками
            if row["client_name"] == f.client_name:  # проверяем строку
                data.append(Row(**row))

    if not f.client_name and f.client_org:  # проверка на наличие фильтров
        async for row in get_filtered_bills_from_csv():  # проходимся по генератору со строками
            if row["client_org"] == f.client_org:  # проверяем строку
                data.append(Row(**row))  # добавляем строку в результат
    return {"bills": data}  # отдаем результат
