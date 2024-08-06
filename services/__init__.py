from dal.user_repo import user_repo
from dal.tender_repo import tender_repo

from services.user_service import user_service as user_service1
from services.tender_service import tender_service as tender_service1
from services.auth_service import AuthService as auth_service1
from services.product_service import product_service as product_service1
from services.request_service import request_service as request_service1


user_service = user_service1()
tender_service = tender_service1()
auth_service = auth_service1()
product_service = product_service1()
request_service = request_service1(user_repo, tender_repo)