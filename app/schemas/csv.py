from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, validator, Field


class Row(BaseModel):
    client_name: str
    client_org: str
    number: int = Field(alias="№")
    money_sum: int | float = Field(alias="sum")
    date: date
    service: str

    @validator("client_name")
    def name_cannot_be_empty(cls, v):
        if len(v) < 2:
            raise ValueError("name cannot be empty")
        return v

    @validator("client_org")
    def org_cannot_be_empty(cls, v):
        if len(v) < 2:
            raise ValueError("org cannot be empty")
        return v

    @validator("number", pre=True)
    def number_must_be_int(cls, v):
        try:
            number = int(v)
        except Exception as e:
            raise ValueError("№ must be int") from e
        return number

    @validator("money_sum", pre=True)
    def money_sum_must_be_num(cls, v: str):
        try:
            if "," in v:
                v = v.replace(",", ".")
            return float(v)
        except Exception as e:
            raise ValueError("money sum must be int or float") from e

    @validator("date", pre=True)
    def date_format(cls, v):
        try:
            return datetime.strptime(v, "%d.%m.%Y").date()
        except Exception as e:
            raise ValueError("bad date format") from e

    @validator("service")
    def service_cannot_be_empty(cls, v):
        if len(v) < 2 or v == "-":
            raise ValueError("service cannot be empty")
        return v
