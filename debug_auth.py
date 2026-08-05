import io, csv, urllib.request, ssl
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from server import get_device_id

AUTH_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5F36AagduDVC-x31fdwm4jcrhv1Fk8NIzifJrEJs4COc-VGMpTcbtKpLWfj-3PfLtpXWWCJ4pgsuX/pub?gid=0&single=true&output=csv"
current_device_id = get_device_id()
print("CURRENT DEVICE ID:", repr(current_device_id))

req = urllib.request.Request(AUTH_URL, headers={'User-Agent': 'Mozilla/5.0'})
context = ssl._create_unverified_context()
with urllib.request.urlopen(req, context=context) as response:
    csv_data = response.read().decode('utf-8')

print("RAW CSV:", repr(csv_data))
reader = list(csv.reader(io.StringIO(csv_data)))
print("READER:", reader)

for row in reader:
    if len(row) >= 2:
        print(f"Comparing '{repr(row[1].strip())}' == '{repr(current_device_id)}' ->", row[1].strip() == current_device_id)
