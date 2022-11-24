from loguru import logger

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.csv_builder import build_csv

bills_router = APIRouter(prefix="/bills")


@bills_router.post("/")
async def post_data(file: UploadFile = File(...)):
    if file.filename[-4:] == ".csv":
        b_file = file.file.read()
        new_file_path = await build_csv(b_file, file.filename)
    else:
        raise HTTPException(400, "file must be .csv")
    return {"new_file_path": new_file_path}


@bills_router.get("/")
async def get_data():
    pass
