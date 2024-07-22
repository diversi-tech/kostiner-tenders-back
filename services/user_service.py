from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dal.user_repo import user_repo
from services.base_service import base_service


class user_service(base_service):
    def __init__(self):
        super().__init__(user_repo())
        self.repo = user_repo()
        print('in __init__ in user_service')

    def create(self, data):
        print(f'user_service create')
        if data['subscriptions']['plan-type'] == 'Subscription':
            print(
                f'user_service create type(data["subscriptions"]["end_date"]) {type(data['subscriptions']['end_date'])}')
            data['subscriptions']['end_date'] = datetime.strptime(data['subscriptions']['start_date'],
                                                                  '%Y-%m-%d') + relativedelta(years=1)
        if data['subscriptions']['plan-type'] == 'Monthly report':
            data['subscriptions']['end_date'] = datetime.strptime(data['subscriptions']['start_date'],
                                                                  '%Y-%m-%d') + relativedelta(months=1)
        if data['subscriptions']['plan-type'] == 'One-time report':
            data['subscriptions']['end_date'] = str(
                datetime.strptime(data['subscriptions']['start_date'], '%Y-%m-%d') + relativedelta(days=1))
        return super().create(data)
