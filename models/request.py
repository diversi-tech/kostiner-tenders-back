class Request:
    def __init__(self , request_id, approved=None, date=None, userID=None, tender_name=None, tender_id=None):
        self.request_id = request_id
        self.approved = approved
        self.date = date
        self.userID = userID
        self.tender_name = tender_name
        self.tenser_id = tender_id


