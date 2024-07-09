class base_service:
    def __init__(self, repo):
        self.repo = repo
        print(f'in __init__ base_service implements {self.repo}')

    def get_all(self):
        print('in service in get method')
        return self.repo.get()

    def get_by_id(self, object_id):
        return self.repo.get_by_id(object_id)

    def create(self, data):
        return self.repo.insert(data)

    def update(self, object_id, data):
        return self.repo.update(object_id, data)

    def delete(self, object_id):
        return self.repo.delete(object_id)

