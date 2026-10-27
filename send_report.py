import os, requests

r = requests.post(
    os.environ["RECEIVER_URL"],
    data=open("report.json").read(),
    headers={"X-Token": os.getenv("REPORT_TOKEN", "secret"),
             "Content-Type": "application/json"},
    timeout=20,
)
print("Receiver responded", r.status_code)