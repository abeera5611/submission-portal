# Assignment Submission Portal

A simple Flask app where students submit their name, registration number, assignment title and a submission URL. Every push is tested automatically by GitHub Actions (running on a self-hosted runner on my own PC), and the test report is sent to a local receiver that saves it as `test-report.json`.

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
Open http://localhost:5000, fill in the form and submit. Valid submissions are saved to `submissions.json` and shown in the table below the form. Missing fields or an invalid URL are rejected with a validation message and are not saved.

## Run the tests
```
python -m pytest
```
This runs three tests (valid submission, missing registration number, invalid URL) and writes `report.json` in the project folder.

## Start the local report receiver
```
python receiver.py
```
The receiver listens on `http://localhost:8000` and saves every report it receives to `test-report.json`. Keep it running during the demo.

## Start the self-hosted CI runner
The CI runs on a GitHub Actions self-hosted runner on this computer, so the runner's `localhost` is the same machine as the receiver (no tunnel needed).

1. In the GitHub repo go to Settings > Actions > Runners > New self-hosted runner (Windows) and follow the download and `config.cmd` steps once.
2. Start the runner and keep the window open during the demo:
   ```
   cd C:\actions-runner
   ./run.cmd
   ```
   It should print `Listening for Jobs`.
3. In Settings > Secrets and variables > Actions add:
   - `RECEIVER_URL` = `http://localhost:8000`
   - `REPORT_TOKEN` = `secret` (must match the receiver's token; set the `REPORT_TOKEN` environment variable to change it)

## CI pipeline
`.github/workflows/ci.yml` runs on every push:
1. Checks out the pushed revision
2. Installs dependencies
3. Runs `python -m pytest` (generates `report.json` from the real test results)
4. Sends `report.json` to the receiver, for both passing and failing runs
5. Fails the pipeline if any test failed

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

Repository: https://github.com/abeera5611/submission-portal
