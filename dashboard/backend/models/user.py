from pydantic import BaseModel


class User(BaseModel):

    id: str
    email: str
    tenant_id: str
    role: str