from fastapi import FastAPI

app = FastAPI()

DATA = {
    "domains": [],
    "assets": [],
    "endpoints": []
}


@app.get("/domains")
def get_domains():
    return DATA["domains"]


@app.get("/assets")
def get_assets():
    return DATA["assets"]


@app.get("/endpoints")
def get_endpoints():
    return DATA["endpoints"]