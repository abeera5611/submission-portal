# Assignment Submission Portal

A simple Flask app where students submit their name, registration number, assignment title and a submission URL. Every push is tested automatically by GitHub Actions, and the test report is sent to a local receiver that saves it as `test-report.json`.

## Requirements
- Python 3.10+
- Git

## Setup
```
pip install -r requirements.txt
```

## Run the application
```
python app.py
```
Open http://localhost:5000, fill in the form and submit. Valid submissions are saved to `submissions.json` and shown in the table below the form.

## Run the tests
```
pytest
```
This runs three tests (valid submission, missing registration number, invalid URL) and writes `report.json` in the project folder.

## Start the local report receiver
```
python receiver.py
```
The receiver listens on port 8000 and saves every report it receives to `test-report.json`.

Keep it running during the demo. To let GitHub Actions reach it:

1. In a second terminal, start a tunnel:
   ```
   cloudflared tunnel --url http://localhost:8000
   ```
   (or `ngrok http 8000`)
2. Copy the public URL the tunnel prints.
3. In the GitHub repo go to Settings > Secrets and variables > Actions and add:
   - `RECEIVER_URL`: the tunnel URL
   - `REPORT_TOKEN`: the same token used by `receiver.py` (default is `secret`; set the `REPORT_TOKEN` environment variable to change it)

Quick tunnel URLs change on every restart, so update `RECEIVER_URL` before each demo.

## CI pipeline
`.github/workflows/ci.yml` runs on every push:
1. Installs dependencies
2. Runs `pytest` (generates `report.json` from the real test results)
3. Sends `report.json` to the receiver, for passing and failing runs
4. Fails the pipeline if any test failed

## Report format
`test-report.json` contains: repository, branch, commit SHA, run ID, timestamp, each test's name/result/failure message, total/passed/failed counts, and the overall status.

## Project structure
```
app.py              Flask app
validators.py       Input validation
templates/          HTML template
test_submissions.py Automated tests
conftest.py         Generates report.json from test results
send_report.py      Sends the report to the receiver (used in CI)
receiver.py         Local HTTP receiver, saves test-report.json
.github/workflows/  CI pipeline
```

Repository: https://github.com/<your-username>/submission-portal