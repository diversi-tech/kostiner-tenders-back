from flask import request
import jwt, os
from dotenv import load_dotenv
from dal.base_repo import base_repo

load_dotenv()

class user_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner', 'users')
        print('in __init__ in user_repo')

    def get_obj_id(self):
        return 'user_id'
