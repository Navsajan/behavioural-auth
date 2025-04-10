# views.py in biometrics app

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv
import os
from django.conf import settings
from django.shortcuts import render

# Optional: Create a directory to store CSVs if not exists
CSV_DIR = os.path.join(settings.BASE_DIR, 'biometric_data')
os.makedirs(CSV_DIR, exist_ok=True)

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

            return JsonResponse({'status': 'success', 'message': 'Data saved successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)