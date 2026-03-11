from fastapi import FastAPI

app = FastAPI()

DATA = {
    "domains": [],
    "assets": []
}


@app.get("/domains")
def get_domains():
    return DATA["domains"]


@app.get("/assets")
def get_assets():
    return DATA["assets"]