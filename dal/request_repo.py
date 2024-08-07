from idlelib.iomenu import errors

from bson import ObjectId

from models.request import Request

from dal.base_repo import base_repo
class request_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner','requests')
        print('in __init__ in request_repo')

    def get_obj_id(self):
        return 'request_id'


    def get_all_users_request(self ,user_id):
        result = self.collection.find({'userID': user_id})
        return list(result)

    def get_unapproved_requests(self):
        unapproved_requests_cursor = self.collection.find({'approved': False})
        unapproved_requests = []

        for request_data in unapproved_requests_cursor:
            request = Request(
                request_id=str(request_data.get('request_id')),
                approved=request_data.get('approved'),
                date=request_data.get('date'),
                userID=request_data.get('userID'),
                tender_name=request_data.get('tender_name'),
                tender_id=request_data.get('tender_id')
            )
            unapproved_requests.append(request)

        return unapproved_requests

    def approve_request(self, request_id):
        try:
            # יצירת ObjectId מה-ID שניתן לפונקציה
            obj_id = ObjectId(request_id)

            # ביצוע העדכון במסד הנתונים
            result = self.collection.update_one({'request_id': obj_id, 'approved': False}, {'$set': {'approved': True}})

            print("result-repo", result)
            # החזרת תוצאת העדכון
            if result.matched_count == 0:
                print(f"No matching request found or request is already approved for ID: {request_id}")
                return False

            if result.modified_count > 0:
                print(f"Request with ID: {request_id} was successfully approved.")
                return True

            return False
        except errors.InvalidId as e:
            print(f"Invalid ID: {e}")
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None











