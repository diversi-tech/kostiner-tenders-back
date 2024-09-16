import ast
from datetime import datetime
from bson import ObjectId
import pandas as pd
from dateutil.relativedelta import relativedelta
from werkzeug.exceptions import NotFound

from flask_restx import abort
# from flask import abort

from dal.tender_repo import tender_repo, DataAlreadyExistsError
from services.base_service import base_service
from services.product_service import product_service as product_service1

product_service = product_service1()


def parse_date(date):
    print(f'parse_date date: {date}')
    if not date:
        raise TypeError('missing data')
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError) as e:
        print(f'err in parse_date: {str(e)}')
        raise e


class tender_service(base_service):
    def __init__(self):
        self.repo = tender_repo()
        super().__init__(self.repo)
        print('in __init__ in tender_service')

    def get_id_by_name(self, tender_name):
        print(f'tender service get id by name')
        return self.repo.get_id_by_name(tender_name)


    def get_all(self, user, search_date):
        list_all_tender = tender_history = tender_current = None
        role = user.get('role')
        subscription = user.get('subscriptions')
        history = user.get('purchase_history')

        # what can happen?
        if role not in ['admin', 'user', 'subscriber']:
            print("if role not in ['admin', 'user', 'subscriber']:")
            raise ValueError('the user invalid')

        if role != 'admin' and not subscription and not history:
            print("if role != 'admin' and not subscription and not history:")
            raise NotFound('no tenders for user')

        # subscription
        if role == 'user':
            print(subscription)
            if subscription:
                print(' if subscription:')
                if not subscription.get('start_date') or not subscription.get('end_date'):
                    print("if not subscription.get('start_date') or not subscription.get('end_date'):")
                    raise ValueError('missing data for subscription')

                # Parse subscription dates
                start_date = parse_date(subscription['start_date'])
                end_date = parse_date(subscription['end_date'])
                new_search_date = parse_date(search_date) if search_date else start_date
                categories = subscription.get('categories')

                if new_search_date and (start_date > new_search_date or new_search_date > end_date):
                    new_search_date = start_date
                tender_current = {}
                for category in categories:
                    tender_current[category] = []
                    print(f'tender_service get all category {category}')
                    tender_current[category] = self.repo.get_by_category(category, new_search_date, start_date, end_date)

            # purchase history
            tender_history = {}
            if history:
                for purchase in history:
                    if not (purchase and purchase.get('purchase_start_date') and purchase.get('purchase_end_date') and purchase.get(
                            'categories')):
                        print(f'invalid purchase')

                    else:
                        start_date = parse_date(purchase['purchase_start_date'])
                        end_date = parse_date(purchase['purchase_end_date'])
                        new_search_date = parse_date(search_date) if search_date else start_date
                        print(
                            f'type(start_date): {type(start_date)}, type(end_date): {type(end_date)}, type(new_search_date): {type(new_search_date)}')
                        categories = purchase.get('categories')
                        if new_search_date and (start_date > new_search_date or new_search_date > end_date):
                            new_search_date = start_date

                        for category in categories:
                            print(f'tender_service get all category {category}')
                            tender_history[category] = self.repo.get_by_category(category, new_search_date, start_date,
                                                                                 end_date)
                            # print(f' tender_service get all tender_history: {tender_history}')
        # admin
        if role == 'admin':
            end_date = parse_date(search_date) if search_date else datetime.now()
            start_date = end_date - relativedelta(months=1)
            products = product_service.get_all()
            categories_name = [category['category'] for category in products]
            print(f'**********tender_service get all categories_name: {categories_name}************')
            list_all_tender = {}
            for category in categories_name:
                print(f'tender_service get all category {category}')
                list_all_tender[category] = self.repo.get_by_category(category, start_date, start_date, end_date)

        result = {}
        if role == 'user':
            if tender_current != {}:
                result['subscriptions'] = tender_current
            if tender_history != {}:
                result['history'] = tender_history
        elif role == 'admin':
            result = list_all_tender

        print(f'tender_service result {result}')
        return result

    def convert_objectid_to_str(self, data):
        if isinstance(data, list):
            return [self.convert_objectid_to_str(item) for item in data]
        elif isinstance(data, dict):
            return {key: self.convert_objectid_to_str(value) for key, value in data.items()}
        elif isinstance(data, tuple):
            return tuple(self.convert_objectid_to_str(item) for item in data)
        elif isinstance(data, ObjectId):
            return str(data)
        else:
            return data

    def convert_datetime_to_str(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self.convert_datetime_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_datetime_to_str(i) for i in obj]
        elif isinstance(obj, tuple):
            return tuple(self.convert_datetime_to_str(i) for i in obj)
        return obj

    def insert_from_csv(self, file):
        return self._insert_from_file(file, 'csv')

    def insert_from_excel(self, file):
        return self._insert_from_file(file, 'excel')

    def _insert_from_file(self, file, file_type):
        df = None
        print('tender service insert_from_file')
        result = []
        try:
            if file_type == 'csv':
                df = pd.read_csv(file, encoding='utf-8')
                print(f'tender service df.head() {df.head()}')
            elif file_type == 'excel':
                df = pd.read_excel(file, engine='openpyxl')
                print(f'tender service df.head() {df.head()}')

            expected_columns = [
                "שם הגוף", "שם ומספר המכרז", "תאריך פרסום", "תאריך הגשה", "קטגוריות", "שם הזוכה ופרטי הזוכה",
                "מידע על הזוכה",
                "מציעים", "סכום ההצעה", "אומדן"
            ]

            actual_columns = df.columns.tolist()

            if not all(col in actual_columns for col in expected_columns):
                print("if not all(col in actual_columns for col in expected_columns):")
                raise ValueError(f"{file_type.upper()} file must contain columns: {', '.join(expected_columns)}")

            data = df.to_dict(orient='records')
            print(f'tender service data: {data}')

            for row in data:
                try:
                    categories = row['קטגוריות'].split(', ')
                    participants = row['מציעים'].split(', ')
                    if isinstance(categories, str):
                        categories = row['קטגוריות'].split(',')
                    if isinstance(participants, str):
                        participants = row['מציעים'].split(',')
                    tender = {
                        'tender_id': ObjectId(),
                        'body_name': row['שם הגוף'],
                        'tender_number_name': row["שם ומספר המכרז"],
                        'published_date': row['תאריך פרסום'],
                        'submission_date': row['תאריך הגשה'],
                        "category": categories,
                        'participants': participants,
                        'winner_name': row["שם הזוכה ופרטי הזוכה"],
                        'details_winner': row['מידע על הזוכה'],
                        'amount_bid': row['סכום ההצעה'],
                        'estimate': row['אומדן']
                    }
                except Exception as e:
                    print(f"Error processing row: {row}. Error: {e}")
                    continue
                result.append(tender)
            print(f'tender service result: {result}')
            return self.repo.insert_csv(result)
        except DataAlreadyExistsError as e:
            print('tender service DataAlreadyExistsError')
            raise e
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            raise e
        except PermissionError as e:
            print(f"Permission error: {e}")
            raise e
        except pd.errors.ParserError as e:
            print(f"Parser error: {e}")
            raise e
        except UnicodeDecodeError as e:
            print(f"Unicode decode error: {e}")
            raise e
        except Exception as e:
            print(f'tender service Exception: {e}')
            raise e

    def search(self, user, criteria):
        print(f'Tender service search with criteria: {criteria}')

        if not user['subscriptions'].get('start_date') or not user['subscriptions'].get('end_date'):
            raise ValueError('אין לך גישה למכרזים האלו')

        # Parse subscription dates
        start_date = datetime.strptime(user['subscriptions']['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(user['subscriptions']['end_date'], '%Y-%m-%d')
        user_categories = set(user['subscriptions']['categories'])
        print(f'tender_service user categories: {user_categories}')
        print(f'tender_service dates: {start_date},{end_date}')

        # Filter categories to include only those in the user's subscription
        if 'category' in criteria:
            print(f' if category in criteria:')
            criteria_categories = set(criteria['category'])
            valid_categories = criteria_categories.intersection(user_categories)
            criteria['category'] = list(valid_categories)
            print(f'Filtered criteria categories: {criteria["category"]}')
        else:
            print(f' else category in criteria:')
            criteria['category'] = list(user_categories)

        if not criteria['category']:
            criteria['category'] = list(user_categories)

        # Ensure 'published_date' is within the allowed date range
        if 'published_date' in criteria:
            print(f'published_date: {criteria["published_date"]}')
            if not (start_date <= criteria['published_date'] <= end_date):
                raise ValueError("No access to tenders with the given published_date")
        else:
            criteria['published_date'] = {'$gte': start_date, '$lte': end_date}
        print(f'Filtered criteria : {criteria}')

        # Call the repository's search method with filtered criteria and date range
        return self.repo.search(criteria)
