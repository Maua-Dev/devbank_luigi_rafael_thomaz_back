from src.app.entities.user import User
from src.app.entities.transaction import Transaction
from src.app.enums.transaction_type_enum import TransactionTypeEnum

from src.app.repo.user_repository_mock import UserRepositoryMock

class Test_UserRepositoryMock:

    def test_get_all_users(self):
        repo = UserRepositoryMock()
        users = repo.get_all_users()

        assert len(users) == 2
        assert users[0].name == "Vitor Soller"
        assert users[0].agency == "1234"
        assert users[0].account == "00000-1"
        assert users[0].current_balance == 1000.0

    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_first_user()

        assert type(user) == User
        assert user.name == "Vitor Soller"
        assert user.account == "00000-1"

    def test_add_transaction(self):
        repo = UserRepositoryMock()

        transaction = Transaction(
            transaction_type=TransactionTypeEnum.DEPOSIT,
            value=100.0,
            current_balance=1100.0,
            timestamp=1.0
        )

        repo.add_transaction(transaction)

        assert len(repo._transactions) == 1
        assert repo._transactions[0] == transaction

    def test_get_all_transactions(self):
        repo = UserRepositoryMock()

        transaction = Transaction(
            transaction_type=TransactionTypeEnum.WITHDRAW,
            value=50.0,
            current_balance=950.0,
            timestamp=1.0
        )

        repo.add_transaction(transaction)

        transactions = repo.get_all_transactions()

        assert len(transactions) == 1
        assert transactions[0].transaction_type == TransactionTypeEnum.WITHDRAW
        assert transactions[0].value == 50.0

    def test_update_balance(self):
        repo = UserRepositoryMock()
        user = repo.update_balance(1500.0)

        assert user.current_balance == 1500.0
        assert repo.get_first_user().current_balance == 1500.0