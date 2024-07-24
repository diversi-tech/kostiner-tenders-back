from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask_restx import abort

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
            data['subscriptions']['end_date'] = datetime.strptime(data['subscriptions']['start_date'],
                                                                  '%Y-%m-%d') + relativedelta(years=1)
        if data['subscriptions']['plan-type'] == 'Monthly report':
            data['subscriptions']['end_date'] = datetime.strptime(data['subscriptions']['start_date'],
                                                                  '%Y-%m-%d') + relativedelta(months=1)
        if data['subscriptions']['plan-type'] == 'One-time report':
            data['subscriptions']['end_date'] = str(
                datetime.strptime(data['subscriptions']['start_date'], '%Y-%m-%d') + relativedelta(days=1))
        return super().create(data)

    def validate_date(self, date_str):
        """ Validate if the string is in a valid date format (YYYY-MM-DD) """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_user(self, user):
        date_fields = ['purchase_date', 'start_date', 'end_date']

        for field in date_fields:
            if field in user:
                if not self.validate_date(user[field]):
                    abort(400, f"{field} must be in the format YYYY-MM-DD.")

        if 'purchase_history' in user:
            for item in user['purchase_history']:
                for field in ['purchase_date']:
                    if field in item:
                        if not self.validate_date(item[field]):
                            abort(400, f"purchase_history item field {field} must be in the format YYYY-MM-DD.")

        if 'subscriptions' in user:
            for field in ['start_date', 'end_date']:
                if field in user['subscriptions']:
                    if not self.validate_date(user['subscriptions'][field]):
                        abort(400, f"subscriptions field {field} must be in the format YYYY-MM-DD.")

