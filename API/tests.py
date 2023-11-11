from django.test import TestCase

# Create your tests here.

import requests


data = {
    "full_name": "Ram",
    "phone_number": "+998950202311",
    "organization_name": "SOFF",
    "amount": 10000,
    "type": "physical"
}

response = requests.post(
    url = "http://127.0.0.1:8000/api/v1/sponsor-create/",
    data=data
)

print(response.status_code)