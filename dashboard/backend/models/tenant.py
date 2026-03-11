from pydantic import BaseModel


class Tenant(BaseModel):

    id: str
    name: str
    domains: list
    plan: str