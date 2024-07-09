from dal.user_repo import user_repo
from services.base_service import base_service

class user_service(base_service):
    def __init__(self):
        repo = user_repo()
        print(f'in __init__ in user_service')
        super().__init__(repo)
