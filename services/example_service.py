from dal.example_repo import dataDAL

class dataService:
    def __init__(self):
        self.dal = dataDAL()

    def get_all_datas(self):
        return self.dal.get_all_datas()

    def get_data_by_id(self, data_id):
        return self.dal.get_data_by_id(data_id)

    def create_data(self, data):
        return self.dal.create_data(data)

    def update_data(self, data_id, data):
       return self.dal.update_data(self,id())

    def delete_data(self, data_id):
        return self.dal.delete_data(id)
    # Other service methods
