from fastapi import FastAPI

app = FastAPI()


@app.post("/login")

def login(email: str, password: str):

    return {
        "token": "jwt_token_example"
    }