from pydantic import BaseModel


class ScanJob(BaseModel):

    id: str
    tenant_id: str
    domain: str
    status: str