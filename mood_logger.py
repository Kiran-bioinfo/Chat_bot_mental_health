import csv
from datetime import datetime
import os

MOOD_LOG_FILE = 'mood_log.csv'

def log_mood(mood):
    file_exists = os.path.isfile(MOOD_LOG_FILE)
    
    # Get current timestamp in IST format (DD-MM-YYYY HH:MM:SS)
    # Python's datetime objects are timezone-naive by default, 
    # but for simplicity and given the 'IST format' requirement without explicit timezone handling,
    # we'll assume local time is sufficient or that the system's timezone is set to IST.
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    with open(MOOD_LOG_FILE, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'mood']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader() # file doesn't exist yet, write a header

        writer.writerow({'timestamp': timestamp, 'mood': mood})
    return True