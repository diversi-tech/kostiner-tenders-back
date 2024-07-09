from dal.base_repo import base_repo

class user_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner', 'users')
        print('in __init__ in base_repo')

    def get_obj_id(self):
        return 'user_id'
