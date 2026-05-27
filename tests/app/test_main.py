from fastapi.exceptions import HTTPException
import pytest
import src.app.main as main_module
from src.app.main import get_user, get_history
from src.app.repo.item_repository_mock import ItemRepositoryMock
from src.app.repo.user_repository_mock import UserRepositoryMock


class Test_Main:
    
    def test_get_user(self):
        repo = UserRepositoryMock()
        response = get_user()
        print(response.get("name", None))

        assert response.get("name", None) == "Vitor Soller"


    def test_get_history(self):
        repo = UserRepositoryMock()
        response = get_history()
        
