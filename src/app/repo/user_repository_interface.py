from abc import ABC, abstractmethod
from typing import List

from ..entities.user import User
from ..entities.transaction import Transaction


class IUserRepository(ABC):

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """
        Return the current user.

        Returns:
            User: The stored user.
        """
        pass


    @abstractmethod
    def get_user(self) -> User:
        """
        Return the current user.

        Returns:
            User: The stored user.
        """
        pass


    @abstractmethod
    def add_transaction(self, transaction: Transaction) -> Transaction:
        """
        Persist a new transaction.

        Args:
            transaction (Transaction): Fully validated transaction entity.

        Returns:
            Transaction: The persisted transaction.
        """
        pass


    @abstractmethod
    def get_all_transactions(self) -> List[Transaction]:
        """
        Return all stored transactions ordered by insertion.

        Returns:
            List[Transaction]: Collection of all transactions.
        """
        pass
    

    @abstractmethod
    def update_balance(self, new_balance: float) -> User:
        """
        Update the user's current balance.

        Args:
            new_balance (float): The new balance to set.

        Returns:
            User: The updated user.
        """
        pass