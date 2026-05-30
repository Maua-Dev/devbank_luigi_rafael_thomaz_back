from fastapi import FastAPI, HTTPException
from mangum import Mangum

from .entities.transaction import Transaction
from .enums.transaction_type_enum import TransactionTypeEnum

from .environments import Environments


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


@app.post("/deposit")
def post_deposit(request: dict):
    for note, qty in request.items():
        #check if the note somehow is not a number and if its valid
        if not note.isdigit() or int(note) not in [2, 5, 10, 20, 50, 100, 200]:
            raise HTTPException(status_code=400, detail="Nota inválida")
        
        #check if the note quantity somehow is not int
        if type(qty) != int:
            raise HTTPException(status_code=400, detail="Quantidade de notas deve ser um inteiro")
        
        #check if quantity is somehow less than 0
        if qty < 0:
            raise HTTPException(status_code=400, detail="Quantidade de notas não pode ser negativa")
 
    notes = {
        2: request.get("2", 0),
        5: request.get("5", 0),
        10: request.get("10", 0),
        20: request.get("20", 0),
        50: request.get("50", 0),
        100: request.get("100", 0),
        200: request.get("200", 0)
    }
    value = float(
        sum(note * qty for note, qty in notes.items())
    )

    if value == 0.0:
        raise HTTPException(status_code=400, detail="Sem notas selecionadas")
    
    current_balance = user_repo.get_first_user().current_balance

    #check for suspicious deposit, but if user has 0.0 balance, allow up to $20 deposit
    if value >= 2 * current_balance:
        if current_balance == 0.0 and value <= 20:
            pass
        else:
            raise HTTPException(status_code=403, detail="Depósito suspeito")


    current_balance = user_repo.get_first_user().current_balance
    new_balance = current_balance + value

    user_repo.update_balance(new_balance)

    transaction = Transaction(
            transaction_type=TransactionTypeEnum.DEPOSIT,
            value=value,
            current_balance=new_balance
            #timestamp is generated after the constructor
        )
    user_repo.add_transaction(transaction)

    return{
        "current_balance": new_balance,
        "timestamp": transaction.timestamp
    }


@app.post("/withdraw")
def post_withdraw(request: dict):
    for note, qty in request.items():
        #check if the note somehow is not a number and if its valid
        if not note.isdigit() or int(note) not in [2, 5, 10, 20, 50, 100, 200]:
            raise HTTPException(status_code=400, detail="Nota inválida")
        
        #check if the note quantity somehow is not int
        if type(qty) != int:
            raise HTTPException(status_code=400, detail="Quantidade de notas deve ser um inteiro")
        
        #check if quantity is somehow less than 0
        if qty < 0:
            raise HTTPException(status_code=400, detail="Quantidade de notas não pode ser negativa")

    notes = {
        2: request.get("2", 0),
        5: request.get("5", 0),
        10: request.get("10", 0),
        20: request.get("20", 0),
        50: request.get("50", 0),
        100: request.get("100", 0),
        200: request.get("200", 0)
    }
    value = float(
        sum(note * qty for note, qty in notes.items())
    )

    if value == 0.0:
        raise HTTPException(status_code=400, detail="Sem notas selecionadas")
    
    if value > user_repo.get_first_user().current_balance:
        raise HTTPException(status_code=403, detail="Saldo insuficiente para transação")


    current_balance = user_repo.get_first_user().current_balance
    new_balance = current_balance - value

    user_repo.update_balance(new_balance)

    transaction = Transaction(
            transaction_type=TransactionTypeEnum.WITHDRAW,
            value=value,
            current_balance=new_balance
            #timestamp is generated after the constructor
        )
    user_repo.add_transaction(transaction)

    return{
        "current_balance": new_balance,
        "timestamp": transaction.timestamp
    }


handler = Mangum(app, lifespan="off")
