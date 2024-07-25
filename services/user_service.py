import json
from functools import wraps
from dal.user_repo import user_repo
from services.base_service import base_service

class user_service(base_service):
    def __init__(self):
        super().__init__(user_repo())
        self.repo = user_repo()
        print('in __init__ in user_service')

    # def get_by_id(self, user_id):
    #     return self.repo.get_by_id(self,user_id)



