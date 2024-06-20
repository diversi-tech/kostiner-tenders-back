# from dal.auth_repo import  AuthRepo
#
# class aythService:
#     def __init__(self):
#         self.dal = AuthRepo()
#
#     def create_user(self):
#         return self.dal.create_user(self,username,password)
#
#     def delete_data(self, data_id):
#         return self.dal.verify_user(self,username,password)
#     # Other service methods
from dal.auth_repo import AuthRepo

class AuthService:
    def __init__(self):
        self.auth_repo = AuthRepo()

    def create_user(self, username, password):
        return self.auth_repo.create_user(username, password)

    def verify_user(self, username, password):
        return self.auth_repo.verify_user(username, password)
