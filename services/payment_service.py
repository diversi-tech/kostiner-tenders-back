import os

import requests



class payment_service():
    def get_access_token(self):
        client_id = os.getenv('YPAY_CLIENT_ID')
        client_secret = os.getenv('YPAY_SECRET_KEY')
        url = "https://ypay.co.il/api/v1/accessToken"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "client_id": client_id,
            "client_secret": client_secret
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(response.json())
            return response.json()["access_token"]
        else:
            raise Exception("Failed to get access token: " + response.text)

    def purchase_product(self, access_token, payloadData):
        url = "https://ypay.co.il/api/v1/payment"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {access_token}",
            "description": ""
        }
        payload = payloadData
        print(payload)
        response = requests.post(url, headers=headers, json=payload)
        print(response.status_code)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to make payment: " + response.text)

    def create_document(self, access_token, document):
        url = "https://ypay.co.il/api/v1/document"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {access_token}",
            
        }
        response = requests.post(url, headers=headers, json=document)
        print(response.status_code)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to make payment: " + response.text)
