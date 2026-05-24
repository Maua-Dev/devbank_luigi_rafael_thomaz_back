import pytest
import time

from src.app.entities.transaction import Transaction
from src.app.enums.transaction_type_enum import TransactionTypeEnum
from src.app.errors.entity_errors import ParamNotValidated

class Test_Transaction:

    def test_transaction(self):
        transaction = Transaction(
            transaction_type=TransactionTypeEnum.WITHDRAW,
            value=100.0,
            current_balance=1000.0,
            timestamp=123456789.0
        )
        assert transaction.transaction_type == TransactionTypeEnum.WITHDRAW
        assert transaction.value == 100.0
        assert transaction.current_balance == 1000.0
        assert transaction.timestamp == 123456789.0


    def test_transaction_type_null(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=None,
                value=100.0,
                current_balance=1000.0,
                timestamp=123456789.0
            )


    def test_transaction_type_not_enum(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type="WITHDRAW",
                value=100.0,
                current_balance=1000.0,
                timestamp=123456789.0
            )

    
    def test_value_null(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=TransactionTypeEnum.WITHDRAW,
                value=None,
                current_balance=1000.0,
                timestamp=123456789.0
            )


    def test_value_not_float(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=TransactionTypeEnum.WITHDRAW,
                value=100,
                current_balance=1000.0,
                timestamp=123456789.0
            )


    def test_value_zero(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=TransactionTypeEnum.WITHDRAW,
                value=0.0,
                current_balance=1000.0,
                timestamp=123456789.0
            )


    def test_value_negative(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=TransactionTypeEnum.WITHDRAW,
                value=-100.0,
                current_balance=1000.0,
                timestamp=123456789.0
            )


    def test_current_balance_null(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=TransactionTypeEnum.WITHDRAW,
                value=100.0,
                current_balance=None,
                timestamp=123456789.0
            )


    def test_current_balance_not_float(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=TransactionTypeEnum.WITHDRAW,
                value=100.0,
                current_balance=1000,
                timestamp=123456789.0
            )


    def test_current_balance_negative(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=TransactionTypeEnum.WITHDRAW,
                value=100.0,
                current_balance=-1000.0,
                timestamp=123456789.0
            )


    def test_current_balance_zero(self):
        transaction = Transaction(
            transaction_type=TransactionTypeEnum.WITHDRAW,
            value=1000.0,
            current_balance=0.0,
            timestamp=123456789.0
        )
        assert transaction.current_balance == 0.0


    def test_timestamp_not_float(self):
        with pytest.raises(ParamNotValidated):
            Transaction(
                transaction_type=TransactionTypeEnum.DEPOSIT,
                value=100.0,
                current_balance=1000.0,
                timestamp=123456789
            )
