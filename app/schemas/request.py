from pydantic import BaseModel


class BillsFilter(BaseModel):
    client_name: str | None
    client_org: str | None