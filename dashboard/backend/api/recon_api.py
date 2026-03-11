from fastapi import FastAPI
from workers.recon_worker import run_recon

app = FastAPI()


@app.post("/scan")

async def start_scan(domain: str):

    result = await run_recon(domain)

    return result