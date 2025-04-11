# views.py in biometrics app

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv
import os
from django.conf import settings
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


# Optional: Create a directory to store CSVs if not exists
CSV_DIR = os.path.join(settings.BASE_DIR, 'biometric_data')
os.makedirs(CSV_DIR, exist_ok=True)
firebase_json = os.getenv("FIREBASE_KEY")

if firebase_json is None:
    raise Exception("FIREBASE_KEY environment variable not set")

firebase_dict = json.loads(firebase_json)
cred = credentials.Certificate(firebase_dict)


firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://behavioural-auth-default-rtdb.firebaseio.com/'
})


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def save_behavior(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user = data.get('user', 'user1')
            gender = data.get('gender', 'M')

            filename = f"{user}.csv"
            filepath = os.path.join(CSV_DIR, filename)

            # Check if file exists to write header
            file_exists = os.path.isfile(filepath)

            with open(filepath, 'a', newline='') as csvfile:
                fieldnames = [
                    'cpm', 'error_rate', 'dwell_avg', 'dwell_std',
                    'flight_avg', 'flight_std', 'click_dwell_avg',
                    'click_flight_avg', 'pressure_touch', 'scroll_x',
                    'scroll_y', 'double_click', 'swipe_speed_avg',
                    'tilt_angle_avg', 'gender'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                data['gender'] = gender
                writer.writerow({field: data.get(field, '') for field in fieldnames})
            store_behavioral_data_to_firebase(user, gender, data)    

            return JsonResponse({'status': 'success', 'message': 'Data saved to CSV and Firebase successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def store_behavioral_data_to_firebase(user_id, gender, data_dict):
    """
    Push data to Firebase under each user.
    """
    ref = db.reference(f"/users/{user_id}")
    ref.push({
        "gender": gender,
        "data": data_dict
    })
    
