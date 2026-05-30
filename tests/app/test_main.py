import pytest
from fastapi.exceptions import HTTPException

import src.app.main as main_module
from src.app.main import get_user, get_history, post_deposit, post_withdraw
from src.app.repo.user_repository_mock import UserRepositoryMock
from src.app.entities.transaction import Transaction
from src.app.enums.transaction_type_enum import TransactionTypeEnum


class Test_Main:

    def setup_method(self):
        main_module.user_repo = UserRepositoryMock()


    def test_get_user(self):
        response = get_user()
        assert response.get("name", None) == "Vitor Soller"


    def test_get_history_empty(self):
        response = get_history()
        assert response == {"all_transactions": []}

    
    def test_get_history_one_transaction(self):
        repo = main_module.user_repo
        #using the UserRepositoryMock() was throwing index error
        transaction = Transaction(
            transaction_type = TransactionTypeEnum.deposit,
            value = 100.0,
            current_balance = 1100.0,
            timestamp = 123456789.0
        )
        repo.add_transaction(transaction)

        response = get_history()
        assert response["all_transactions"][0] == transaction.to_dict()
        assert len(response["all_transactions"]) == 1


    def test_get_history_many_transactions(self):
        repo = main_module.user_repo
        #using the UserRepositoryMock() was throwing index error
        response = get_history()
        transaction1 = Transaction(
            transaction_type = TransactionTypeEnum.deposit,
            value = 100.0,
            current_balance = 1100.0,
            timestamp = 123456789.0
        )
        transaction2 = Transaction(
            transaction_type = TransactionTypeEnum.withdraw,
            value = 150.0,
            current_balance = 950.0,
            timestamp = 246813579.0
        )
        repo.add_transaction(transaction1)
        repo.add_transaction(transaction2)

        response = get_history()
        assert response["all_transactions"][0] == transaction1.to_dict()
        assert response["all_transactions"][1] == transaction2.to_dict()
        assert len(response["all_transactions"]) == 2


    def test_post_deposit(self):
        request = {"100": 1}
        response = post_deposit(request=request)

        assert response["current_balance"] == 1100.0
        assert type(response["timestamp"]) == float
        assert response["timestamp"] > 0


    def test_post_deposit_multiple_notes(self):
        request = {
            "2": 50,
            "5": 20,
            "10": 10,
            "20": 5,
            "50": 2,
            "100": 1,
            "200": 1,
        } #sum = 800
        
        response = post_deposit(request=request)
        assert response["current_balance"] == 1800.0

    
    def test_post_deposit_updates_balance(self):
        request = {"50": 2}
        post_deposit(request=request)

        user = main_module.user_repo.get_first_user()
        assert user.current_balance == 1100.0


    def test_post_deposit_updates_history(self):
        request = {"100": 1}
        post_deposit(request=request)

        history = get_history()
        assert len(history["all_transactions"]) == 1
        assert history["all_transactions"][0]["type"] == "deposit"
        assert history["all_transactions"][0]["value"] == 100.0
        assert history["all_transactions"][0]["current_balance"] == 1100.0


    def test_post_deposit_suspicious(self):
        request = {"200": 10}
    
        with pytest.raises(HTTPException) as err:
            post_deposit(request=request)

        assert err.value.status_code == 403


    def test_post_deposit_empty_request(self):
        with pytest.raises(HTTPException) as err:
            post_deposit(request={})

        assert err.value.status_code == 400


    def test_post_deposit_all_zeros(self):
        request = {"2": 0} #main creates the other notes as 0

        with pytest.raises(HTTPException) as err:
            post_deposit(request=request)
        assert err.value.status_code == 400
        assert err.value.detail == "Sem notas selecionadas"


    def test_post_deposit_invalid_note(self):
        request = {"1": 1, "2": 2}
        
        with pytest.raises(HTTPException) as err:
            post_deposit(request=request)
        assert err.value.status_code == 400


    def test_post_deposit_invalid_note_string(self):
        request = {"2": 1, "string": 1}

        with pytest.raises(HTTPException) as err:
            post_deposit(request=request)
        assert err.value.status_code == 400

    
    def test_post_deposit_negative_quantity(self):
        request = {"2": -1}

        with pytest.raises(HTTPException) as err:
            post_deposit(request=request)
        assert err.value.status_code == 400


    def test_post_deposit_quantity_not_int(self):
        request = {"2": 1.5}
        
        with pytest.raises(HTTPException) as err:
            post_deposit(request=request)
        assert err.value.status_code == 400


    def test_post_withdraw(self):
        request = {"100": 1}
        response = post_withdraw(request=request)

        assert response["current_balance"] == 900.0
        assert type(response["timestamp"]) == float
        assert response["timestamp"] > 0


    def test_post_withdraw_multiple_notes(self):
        request = {
            "2": 50,
            "5": 20,
            "10": 10,
            "20": 5,
            "50": 2,
            "100": 1,
            "200": 1,
        } #sum = 800
        
        response = post_withdraw(request=request)
        assert response["current_balance"] == 200.0

    
    def test_post_withdraw_updates_balance(self):
        request = {"50": 2}
        post_withdraw(request=request)

        user = main_module.user_repo.get_first_user()
        assert user.current_balance == 900.0


    def test_post_withdraw_updates_history(self):
        request = {"100": 1}
        post_withdraw(request=request)

        history = get_history()
        assert len(history["all_transactions"]) == 1
        assert history["all_transactions"][0]["type"] == "withdraw"
        assert history["all_transactions"][0]["value"] == 100.0
        assert history["all_transactions"][0]["current_balance"] == 900.0


    def test_post_withdraw_greater_than_balance(self):
        request = {"200": 10}
    
        with pytest.raises(HTTPException) as err:
            post_withdraw(request=request)

        assert err.value.status_code == 403


    def test_post_withdraw_empty_request(self):
        with pytest.raises(HTTPException) as err:
            post_withdraw(request={})

        assert err.value.status_code == 400


    def test_post_withdraw_all_zeros(self):
        request = {"2": 0} #main creates the other notes as 0

        with pytest.raises(HTTPException) as err:
            post_withdraw(request=request)
        assert err.value.status_code == 400
        assert err.value.detail == "Sem notas selecionadas"


    def test_post_withdraw_invalid_note(self):
        request = {"1": 1, "2": 2}
        
        with pytest.raises(HTTPException) as err:
            post_withdraw(request=request)
        assert err.value.status_code == 400


    def test_post_withdraw_invalid_note_string(self):
        request = {"2": 1, "string": 1}

        with pytest.raises(HTTPException) as err:
            post_withdraw(request=request)
        assert err.value.status_code == 400

    
    def test_post_withdraw_negative_quantity(self):
        request = {"2": -1}

        with pytest.raises(HTTPException) as err:
            post_withdraw(request=request)
        assert err.value.status_code == 400


    def test_post_withdraw_quantity_not_int(self):
        request = {"2": 1.5}
        
        with pytest.raises(HTTPException) as err:
            post_withdraw(request=request)
        assert err.value.status_code == 400


    def test_post_withdraw_exact_balance(self):
        request = {"200": 5}
        response = post_withdraw(request=request)
        
        assert response["current_balance"] == 0.0