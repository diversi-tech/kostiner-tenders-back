from dal.user_repo import user_repo

class userService:
    def __init__(self):
        self.dal = user_repo()

    def get(self):
        return self.dal.get()

    def get_by_id(self, user_id):
        print('userService //def get_by_id(self, user_id):')
        return self.dal.get_by_id(user_id)

    def insert(self, data):
        print('post in user_service')
        return self.dal.insert(data)

    def update(self, user_id, data):
        print('userSevice //def def update(self, user_id, data)')
        return self.dal.update(user_id, data)

    def delete(self, user_id):
        return self.dal.delete(user_id)

    # Other service methods
