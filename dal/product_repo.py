from idlelib.iomenu import errors
from os import abort
from pymongo import errors
from flask import abort


from dal.base_repo import base_repo

class product_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner','products')
        print('in __init__ in base_repo')
    # def get_obj_id(self):

    def get_by_category(self, category):
        try:
            return self.collection.find_one({"category": category})
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None

    def update_by_category(self, category, data):
        try:
            # בדיקה אם המוצר עם הקטגוריה הנוכחית קיים
            current_product = self.get_by_category(category)
            if not current_product:
                abort(404, f"Product with category '{category}' doesn't exist.")

            # בדיקה אם יש שינוי בשם הקטגוריה
            if "category" in data and data["category"] != category:
                # בדיקה אם קיימת כבר קטגוריה עם השם החדש
                existing_category = self.collection.find_one({"category": data["category"]})
                if existing_category:
                    abort(400, "Product with this category already exists.")

            # ביצוע העדכון במסמך לפי הקטגוריה הנתונה
            result = self.collection.update_one({"category": category}, {'$set': data})

            return result
        except ValueError as ve:
            print(f"ValueError: {ve}")
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


    def delete_by_category(self, category):
        try:
            # מחיקת המסמך לפי הקטגוריה
            result = self.collection.delete_one({"category": category})

            # אם נמחק מסמך, result.deleted_count יהיה שווה ל-1
            if result.deleted_count == 1:
                return True
            else:
                print(f"Category '{category}' not found.")
                return False
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False


    def insert(self, data):
        try:
            # Check if product with same category already exists
            if self.collection.find_one({"category": data["category"]}):
                abort(400, "Product with this category already exists.")
            # Insert new product into database
            result = self.collection.insert_one(data)
            # Return the newly inserted product
            return data
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None, "An error occurred while inserting the product."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, "An unexpected error occurred."