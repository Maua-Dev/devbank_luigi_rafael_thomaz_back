
from typing import Tuple
from ..errors.entity_errors import ParamNotValidated
import re


class User:
    
    name: str
    agency: str
    account: str
    current_balance: float

    def __init__(
        self,
        name: str = None,
        agency: str = None,
        account: str = None,
        current_balance: float = 1000.0
    ):
        
        validation_name = self.validate_name(name)
        if validation_name[0] is False:
            raise ParamNotValidated("name", validation_name[1])
        self.name = name

        validation_agency = self.validate_agency(agency)
        if validation_agency[0] is False:
            raise ParamNotValidated("agency", validation_agency[1])
        self.agency = agency

        validation_account = self.validate_account(account)
        if validation_account[0] is False:
            raise ParamNotValidated("account", validation_account[1])
        self.account = account

        validation_current_balance = self.validate_current_balance(current_balance)
        if validation_current_balance[0] is False:
            raise ParamNotValidated("current_balance", validation_current_balance[1])
        self.current_balance = current_balance


    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        if name is None:
            return(False, "Name is required")
        if type(name) != str:
            return(False, "Name must be a string")
        if len(name) < 3 or len(name) > 40:
            return(False, "Name must be between 3 and 40 characters long")
        return(True, "")
    

    @staticmethod
    def validate_agency(agency: str) -> Tuple[bool, str]:
        if agency is None:
            return(False, "Agency is required")
        if type(agency) != str:
            return(False, "Agency must be a string")
        if not re.fullmatch(r"\d{4}", agency): 
            #using regex to validate both length and if there's non-numbers
            return(False, "Agency must be 4 digits")
        return(True, "")
    

    @staticmethod
    def validate_account(account: str) -> Tuple[bool, str]:
        if account is None:
            return(False, "Account is required")
        if type(account) != str:
            return(False, "Account must be a string")
        if not re.fullmatch(r"\d{5}-\d", account): 
            #using regex to validate both format and if there's non-numbers
            return(False, "Account must follow the scheme 00000-0")
        return(True, "")
    

    @staticmethod
    def validate_current_balance(current_balance: float) -> Tuple[bool, str]:
        if current_balance is None:
            return(False, "Current Balance is required")
        if type(current_balance) != float:
            return(False, "Current Balance must be a float")
        if current_balance < 0:
            return(False, "Current Balance can't be negative")
        return(True, "")
    

    def to_dict(self):
        return{
            "name": self.name,
            "agency": self.agency,
            "account": self.account,
            "current_balance": self.current_balance
        }
    

    def __eq__(self,other):
        return(
            self.name == other.name and 
            self.agency == other.agency and 
            self.account == other.account and 
            self.current_balance == other.current_balance
        )
    

    def __repr__(self):
        return f"""
            User(name={self.name}, 
            agency={self.agency}, 
            account={self.account}, 
            current_balance={self.current_balance})
        """
