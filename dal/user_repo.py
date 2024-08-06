from dal.base_repo import base_repo
from flask_restx import abort


class user_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner', 'users')
        print('in __init__ in user_repo')

    def get_obj_id(self):
        return 'user_id'


    def insert(self, data):
        if self.collection.find_one({'user_name': data['user_name']}):
            abort(400, "user name exist in the system")
        super().insert(data)
