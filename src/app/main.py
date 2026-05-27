from fastapi import FastAPI, HTTPException
from mangum import Mangum

from .environments import Environments

from .errors.entity_errors import ParamNotValidated


app = FastAPI()
user_repo = Environments.get_user_repo()()


@app.get("/")
def get_user():
    return user_repo.get_first_user().to_dict()


@app.get("/history")
def get_history():
    transactions = user_repo.get_all_transactions()
    return{
        "all_transactions": [transaction.to_dict() for transaction in transactions]
    }


handler = Mangum(app, lifespan="off")
