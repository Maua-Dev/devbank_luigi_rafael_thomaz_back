import pytest

from src.app.entities.user import User
from src.app.errors.entity_errors import ParamNotValidated

class Test_User:

    def test_user(self):
        user = User(
            name="Vitor Soller",
            agency="1234",
            account="00000-1",
            current_balance=1000.0
        )

        assert user.name == "Vitor Soller"
        assert user.agency == "1234"
        assert user.account == "00000-1"
        assert user.current_balance == 1000.0


    def test_name_null(self):
        with pytest.raises(ParamNotValidated):
            User(
                name=None,
                agency="1234",
                account="00000-1",
                current_balance=1000.0                
            )

    
    def test_name_not_string(self):
        with pytest.raises(ParamNotValidated):
            User(
                name=True,
                agency="1234",
                account="00000-1",
                current_balance=1000.0                
            )


    def test_name_too_short(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="a",
                agency="1234",
                account="00000-1",
                current_balance=1000.0
            )


    def test_name_too_long(self):
        with pytest.raises(ParamNotValidated): 
            User(
                name="abcdefghi abcdefghi abcdefghi abcdefghi max reached",
                agency="1234",
                account="00000-1",
                current_balance=1000.0
            )
    

    def test_name_with_invalid_characters(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="My_Name!",
                agency="1234",
                account="00000-1",
                current_balance=1000.0
            )


    def test_name_with_invalid_space(self):
        with pytest.raises(ParamNotValidated):
            User(
                name=" Spaces ",
                agency="1234",
                account="00000-1",
                current_balance=1000.0
            )


    def test_name_with_double_spaces(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Double  Spaces",
                agency="1234",
                account="00000-1",
                current_balance=1000.0
            )


    def test_name_with_diacritics(self):
        #diacritics are letters with accent or such
        user = User(
            name="Cição de Sá",
            agency="1234",
            account="00000-1",
            current_balance=1000.0
        )

        assert user.name == "Cição de Sá"

    
    def test_agency_null(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency=None,
                account="00000-1",
                current_balance=1000.0
            )
    
    
    def test_agency_not_string(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency=1234,
                account="00000-1",
                current_balance=1000.0
            )
    
    
    def test_agency_too_long(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="123456",
                account="00000-1",
                current_balance=1000.0
            )
    
    
    def test_agency_too_short(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="12",
                account="00000-1",
                current_balance=1000.0
            )
    
    
    def test_agency_not_numbers(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="1a!4",
                account="00000-1",
                current_balance=1000.0
            )

    
    def test_account_null(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="1234",
                account=None,
                current_balance=1000.0
            )

    
    def test_account_not_string(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="1234",
                account=111111,
                current_balance=1000.0
            )
            
    
    def test_account_not_numbers(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="1234",
                account="a!000-b",
                current_balance=1000.0
            )
            
    
    def test_account_format_not_matching(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="1234",
                account="0-00001",
                current_balance=1000.0
            )
    
    
    def test_current_balance_null(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="1234",
                account="00000-1",
                current_balance=None
            )


    def test_current_balance_not_float(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="1234",
                account="00000-1",
                current_balance=1000
            )


    def test_current_balance_negative(self):
        with pytest.raises(ParamNotValidated):
            User(
                name="Vitor Soller",
                agency="1234",
                account="00000-1",
                current_balance=-1000.0
            )


    def test_current_balance_zero(self):
        user = User(
            name="Vitor Soller",
            agency="1234",
            account="00000-1",
            current_balance=0.0
        )
