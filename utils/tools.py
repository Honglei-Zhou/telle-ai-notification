import os
from datetime import timezone
import pytz


local_tz = pytz.timezone('America/Chicago')

dirpath = os.path.dirname(os.path.realpath(__file__))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(local_tz)
