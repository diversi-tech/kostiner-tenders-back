from datetime import datetime

from bson import ObjectId
from pymongo.errors import PyMongoError

from config.config import mail
from flask_mail import Message
from services.base_service import base_service
from dal.request_repo import request_repo



class request_service(base_service):
    def __init__(self, user_repo, tender_repo):
        self.repo = request_repo()
        self.user_repo = user_repo()
        self.tender_repo = tender_repo()

        # קריאה לקונסטרקטור של מחלקת הבסיס
        super().__init__(self.repo)
        print('in __init__ in request_service')

    def get_all_users_request(self, user_id):
        return self.repo.get_all_users_request(user_id)

    def create(self, name, user_id):
        print('in crate ')
        try:
            tender_id = self.tender_repo.get_id_by_name(name)
        except ValueError as ve:
            print(f"Error: {ve}")
            # מחזירה הודעת שגיאה וקוד סטטוס 404 במקרה של ValueError
            return {'message': str(ve)}, 404
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            # מחזירה הודעת שגיאה וקוד סטטוס 500 במקרה של PyMongoError
            return {'message': f'An error occurred: {str(e)}'}, 500

        data = {
            'request_id': 'string',
            'tender_id': tender_id,
            'tender_name': name,
            'userID': user_id,
            'approved': False,
            'date': datetime.utcnow()
        }

        print(f'request_service create data')
        result = self.repo.insert(data)
        print("result", result)
        if result:
            email = 'ariellakostiner@gmail.com'
            if email:
                msg = Message(f'בקשה לצפייה במכרז ממתינה לאישור', recipients=[email])
                msg.html = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <h2 style="text-align: center; color: #333333;">בקשה לצפייה במכרז</h2>
                            <p style="color: #333333;">היי אריאלה,</p>
                            <p style="color: #333333;">יש בקשה לצפייה במכרז שממתינה לאישורך.</p>
                            <p style="color: #333333;">קישור לאישור:</p>
                            <p style="text-align: center;">
                                <a href="https://kostiner-tenders.onrender.com/" style="color: #1a73e8; text-decoration: none; font-weight: bold;">לאישור לחץ כאן</a>
                            </p>
                        </div>
                    </body>
                </html>
                """

                print(f"Approval email sent to {email}")
                try:
                    mail.send(msg)
                    print('Email sent successfully')
                except Exception as e:
                    print(f'Failed to send email: {e}')
                    return {'message': f'Failed to send email: {str(e)}'}, 500
                return data, 201

    def get_unapproved_requests(self):
        return self.repo.get_unapproved_requests()

    def approve_request(self, request_id):
        try:
            # אישור הבקשה
            result = self.repo.approve_request(request_id)
            print("result", result)
            if result:
                # מציאת המשתמש ושליחת מייל
                request_data = self.repo.collection.find_one({'request_id': ObjectId(request_id)})
                print("request_data", request_data)
                if request_data:
                    user_id = request_data.get('userID')
                    user = self.user_repo.get_by_id(user_id)
                    if user:
                        email = user.get('email')
                        if email:
                            msg = Message(f'בקשתך לצפייה במכרז אושרה וממתינה לתשלום', recipients=[email])
                            msg.html = f"""
                            <html>
                                <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                                    <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                                        <h2 style="text-align: center; color: #333333;">אישור בקשתך לצפייה במכרז</h2>
                                        <p style="color: #333333;">היי, {user['user_name']}</p>
                                        <p style="color: #333333;">בקשתך אושרה וממתינה לתשלום. תודה על סבלנותך.</p>
                                        <p style="color: #333333;">קישור לתשלום:</p>
                                        <p style="text-align: center;">
                                            <a href="https://kostiner-tenders.onrender.com/" style="color: #1a73e8; text-decoration: none; font-weight: bold;">לתשלום לחץ כאן</a>
                                        </p>
                                    </div>
                                </body>
                            </html>
                            """
                            print(f"Approval email sent to {email}")
                            try:
                                mail.send(msg)
                                print('Email sent successfully')
                            except Exception as e:
                                print(f'Failed to send email: {e}')
                                return {'message': f'Failed to send email: {str(e)}'}, 500

            return result
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def paid_up(self, request_id):
        try:
            request_data = self.repo.collection.find_one({'request_id': ObjectId(request_id)})
            if not request_data:
                return {'message': 'Request not found'}, 404

            if not request_data.get('approved', False):
                return {'message': 'בקשתך עדיין לא אושרה'}, 400

            tender = self.tender_repo.get_by_id(request_data['tender_id'])
            if not tender:
                return {'message': 'Tender not found'}, 404

            print(f'tender {tender}')
            print("request_data", request_data)

            user_id = request_data.get('userID')
            user = self.user_repo.get_by_id(user_id)
            if not user:
                return {'message': 'User not found'}, 404

            email = user.get('email')
            if not email:
                return {'message': 'User email not found'}, 404

            msg = Message(f'בהמשך לבקשתך לצפייה במכרז', recipients=[email])
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                        <h2 style="text-align: center; color: #333333;">פרטי המכרז</h2>
                        <p style="color: #333333;">היי, {user['user_name']}</p>
                        <p style="color: #333333;">בקשתך לצפיה במכרז {request_data['tender_name']}</p>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>שם המכרז:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['body_name']}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>תאריך:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['published_date']}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>קטגוריות:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['category']}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>שם הזוכה:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['winner_name']}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>פרטי הזוכה:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['details_winner']}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>שמות הזוכים:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['participants']}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>מספר מכרז:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['tender_number_name']}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>הערכה:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['estimate']}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #dddddd; padding: 8px;"><strong>סכום הגוב:</strong></td>
                                <td style="border: 1px solid #dddddd; padding: 8px;">{tender['amount_bid']}</td>
                            </tr>
                        </table>
                        <p style="color: #333333;">קישור לצפייה:</p>
                        <p><a href="https://kostiner-tenders.onrender.com/" style="color: #1a73e8;">https://kostiner-tenders.onrender.com/</a></p>
                    </div>
                </body>
            </html>
            """
            print(f"Approval email sent to {email}")
            try:
                mail.send(msg)
                print('Email sent successfully')
            except Exception as e:
                print(f'Failed to send email: {e}')
                return {'message': f'Failed to send email: {str(e)}'}, 500

            self.repo.delete(request_id)
            return {'message': 'Request processed successfully'}, 200

        except Exception as e:
            print(f"Unexpected error: {e}")
            return {'message': 'An unexpected error occurred'}, 500





