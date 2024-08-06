class Request:
    def __init__(self , request_id ,approved=None , date=None , userID=None , tenderName=None ):
        self.request_id = request_id
        self.approved = approved
        self.date = date
        self.userID = userID
        self.tenderName = tenderName


