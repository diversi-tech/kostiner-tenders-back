from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask_restx import abort
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo.errors import PyMongoError
import logging

from dal.user_repo import user_repo
from services.base_service import base_service


class user_service(base_service):
    def __init__(self):
        super().__init__(user_repo())
        self.repo = user_repo()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        print('in __init__ in user_service')

    def create(self, data):
        print(f'user_service create')
        if 'subscriptions' in data and data['subscriptions']['plan_type'] == 'Subscription':
            data['subscriptions']['end_date'] = str(datetime.strptime(data['subscriptions']['start_date'],
                                                                  '%Y-%m-%d') + relativedelta(years=1))
        if 'subscriptions' in data and data['subscriptions']['plan_type'] == 'Monthly report':
            data['subscriptions']['end_date'] = str(datetime.strptime(data['subscriptions']['start_date'],
                                                                  '%Y-%m-%d') + relativedelta(months=1))
        if 'subscriptions' in data and data['subscriptions']['plan_type'] == 'One-time report':
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
        except Exception:
            return False

    def validate_user(self, user):
        date_fields = ['purchase_date', 'start_date', 'end_date']

        if not user:
            abort(400, "user is null")

        for field in date_fields:
            if field in user:
                if not self.validate_date(user[field]):
                    abort(400, f"'{field}' must be in the format YYYY-MM-DD. user: {user['first_name']}")

        if 'purchase_history' in user:
            for item in user['purchase_history']:
                for field in ['purchase_date']:
                    if field in item:
                        if not self.validate_date(item[field]):
                            abort(400, f"purchase_history item field '{field}' must be in the format YYYY-MM-DD. user: {user['first_name']}")

        if 'subscriptions' in user and user['subscriptions'] is not None:
            for field in ['start_date', 'end_date']:
                if field in user['subscriptions']:
                    if not self.validate_date(user['subscriptions'][field]):
                        abort(400, f"subscriptions field '{field}' must be in the format YYYY-MM-DD. user: {user['first_name']}")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_and_transfer_subscriptions():
    repo = user_repo()
    logger.info("Running subscription check and transfer")
    try:
        users = repo.get()
        logger.info(f"Fetched {len(users)} users from database")
    except PyMongoError as e:
        logger.error(f"Error fetching users from database: {e}")
        return

    current_date = datetime.now().date()
    for user in users:
        try:
            subscription = user.get('subscriptions')
            if subscription:
                end_date = subscription['end_date']
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                elif isinstance(end_date, datetime):
                    end_date = end_date.date()

                if end_date < current_date:
                    logger.info(f"Transferring subscription for user {user['user_id']}")
                    purchase = {
                        'plan_type': user['subscriptions']['plan_type'],
                        'purchase_start_date': user['subscriptions']['start_date'],
                        'purchase_end_date': user['subscriptions']['end_date'],
                        'categories': user['subscriptions']['categories'],
                        'amount': user['subscriptions']['amount']
                    }
                    user['purchase_history'].append(purchase)
                    user['subscriptions'] = None
                    repo.update(user['user_id'], user)
                    logger.info(f"User {user['user_id']} subscription transferred")
        except PyMongoError as e:
            logger.error(f"Error updating user {user['user_id']}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for user {user['user_id']}: {e}")


scheduler = BackgroundScheduler()
scheduler.add_job(check_and_transfer_subscriptions, 'interval', days=1)
scheduler.start()

logger.info("Scheduler started, job will run every 1 day")
