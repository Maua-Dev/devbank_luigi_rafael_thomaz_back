from ..entities.user import User
from ..entities.transaction import Transaction
from .user_repository_interface import IUserRepository

from typing import List

class UserRepositoryMock(IUserRepository):

    def __init__(self) -> None:
        self._users: List[User] = [
            User(
                name="Vitor Soller",
                agency="1234",
                account="00000-1",
                current_balance=1000.0
            ),
            User(
                name="Leo Lorio",
                agency="1234",
                account="00000-2",
                current_balance=500.0
            )
        ]
        self._transactions: List[Transaction] = []

    def get_all_users(self) -> List[User]:
        return self._users

    def get_first_user(self) -> User:
        return self._users[0]

    def add_transaction(self, transaction: Transaction) -> Transaction:
        self._transactions.append(transaction)
        return transaction

    def get_all_transactions(self) -> List[Transaction]:
        return self._transactions

    def update_balance(self, new_balance: float) -> User:
        self._users[0].current_balance = new_balance
        return self._users[0]