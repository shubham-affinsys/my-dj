import os
from django.shortcuts import render
from django.conf import settings

def view_logs(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'djgo.log')  # Adjust the path if necessary
    logs = []

    # Read the log file
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()

    return render(request, 'view_logs.html', {'logs': logs})
