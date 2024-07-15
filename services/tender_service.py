import json
from bson import ObjectId
import pandas as pd
from werkzeug.datastructures import FileStorage
import io

from dal.tender_repo import tender_repo, DataAlreadyExistsError
from services.base_service import base_service


class tender_service(base_service):
    def __init__(self):
        self.repo = tender_repo()
        super().__init__(self.repo)
        print('in __init__ in tender_service')

    def get_all(self, query):
        return self.repo.get(query)

    def insert_from_csv(self, file):
        return self._insert_from_file(file, 'csv')

    def insert_from_excel(self, file):
        return self._insert_from_file(file, 'excel')

    def _insert_from_file(self, file, file_type):
        print('tender service insert_from_file')
        result = []
        try:
            if file_type == 'csv':
                df = pd.read_csv(file, encoding='utf-8')
                print(f'tender service df.head() {df.head()}')
            elif file_type == 'excel':
                df = pd.read_excel(file, engine='openpyxl')
                print(f'tender service df.head() {df.head()}')

            expected_columns = ["שם הגוף", "מספר מכרז", "שם מכרז", "תאריך פרסום", "תאריך הגשה", "מציעים", "קטגוריות", "שם הזוכה", "מידע על הזוכה"
                                , "סכום ההצעה", "אומדן"
                                ]

            actual_columns = df.columns.tolist()

            if not all(col in actual_columns for col in expected_columns):
                raise ValueError(f"{file_type.upper()} file must contain columns: {', '.join(expected_columns)}")

            data = df.to_dict(orient='records')
            print(f'tender service data: {data}')
            for row in data:
                try:
                    tender = {
                        'tender_id': ObjectId(),
                        'body_name': row['שם הגוף'],
                        'tender_number': row['מספר מכרז'],
                        'tender_name': row['שם מכרז'],
                        'published_date': row['תאריך פרסום'],
                        'submission_date': row['תאריך הגשה'],
                        "category": row['קטגוריות'],
                        'participants': row['מציעים'],
                        'winner_name': row['שם הזוכה'],
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
