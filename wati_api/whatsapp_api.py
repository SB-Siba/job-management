import requests
import json

class WatiAPIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def send_message(self, phone_number, template_name, parameters):
        url = f"{self.base_url}/api/v1/sendTemplateMessage"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "phone_number": phone_number,
            "template_name": template_name,
            "parameters": parameters
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
