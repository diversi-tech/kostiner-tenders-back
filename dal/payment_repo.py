from dal.base_repo import base_repo


# load_dotenv()

class payment_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner', 'payments')
        print('in __init__ in payment_repo')
