import requests
from datetime import datetime
import os

APP_ID = os.environ["APP"]
API_KEY = os.environ["API"]

endpoint="https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET"]
exercise_text=input("Tell me which exercise you did? ")

GENDER = "male"
WEIGHT_KG = 85
HEIGHT_CM = 165
AGE = 23

headers={
"x-app-id":APP_ID,
"x-app-key":API_KEY
}

parameters={
"query" : exercise_text,
"gender" : GENDER,
"weight_kg":WEIGHT_KG,
"height_cm":HEIGHT_CM,
"age": AGE

}

response = requests.post(url=endpoint,json=parameters,headers=headers)
response.raise_for_status()
result = response.json()

today = datetime.today()

bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
}

for exercise in result['exercises']:
    g_parameters = {
        'workout':{
            'date':today.strftime('%d/%m/%Y'),
            'time':today.strftime('%H:%M:%S'),
            'exercise':exercise['name'].title(),
            'duration':exercise['duration_min'],
            'calories':exercise['nf_calories']
        }
    }

    sheet_response=requests.post(url=sheet_endpoint,json=g_parameters,headers=bearer_headers)
    print(sheet_response.text)




