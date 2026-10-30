# Assignment Submission Portal

A simple Flask app where students submit their name, registration number, assignment title and a submission URL. Every push is tested automatically by GitHub Actions (running on a self-hosted runner on my own PC), and the test report is sent to a local receiver that saves it as `test-report.json`. The report is also emailed through Gmail, and the static demo is deployed to GitHub Pages only when all tests pass.

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

## Email report (Gmail)
After every run, passing or failing, the pipeline emails the test report. The email contains the commit identifier, the overall result, the total/passed/failed counts, every test's result, and `report.json` as an attachment.

Setup:
1. In your Google Account turn on 2-Step Verification, then create an **App Password** (Security > App passwords).
2. In the GitHub repo go to Settings > Secrets and variables > Actions and add:
   - `MAIL_USER` = the Gmail address that sends the report
   - `MAIL_APP_PASSWORD` = the 16-character app password (not the normal Gmail password)
   - `REPORT_EMAIL` = the address that receives the report

Credentials are stored only in GitHub secrets, never in the code. The email is built by `make_summary.py` and sent through `smtp.gmail.com` on port 465.

## GitHub Pages deployment
The `deploy` job publishes the static demo from the `public/` folder to GitHub Pages. It uses `needs: test` and runs only on `main`, so it deploys only when all tests pass. If a test fails, the deploy job is skipped and the previously published version stays unchanged.

Setup: Settings > Pages > Source: **GitHub Actions** (the repository must be public).

Live demo: https://abeera5611.github.io/submission-portal/

## CI pipeline
`.github/workflows/ci.yml` runs on every push:
1. Checks out the pushed revision
2. Installs dependencies
3. Runs `python -m pytest` (generates `report.json` from the real test results)
4. Sends `report.json` to the receiver, for both passing and failing runs
5. Builds an email summary and emails the report through Gmail
6. Fails the pipeline if any test failed
7. Deploys the static demo to GitHub Pages (only if all tests passed)

## Report format
`test-report.json` contains: repository, branch, commit SHA, run ID, timestamp, each test's name/result/failure message, total/passed/failed counts, and the overall status.

## Project structure
```
app.py              Flask app
validators.py       Input validation
templates/          HTML template
public/             Static demo deployed to GitHub Pages
test_submissions.py Automated tests
conftest.py         Generates report.json from test results
send_report.py      Sends the report to the receiver (used in CI)
make_summary.py     Builds the email body from report.json
receiver.py         Local HTTP receiver, saves test-report.json
.github/workflows/  CI pipeline
```

Repository: https://github.com/abeera5611/submission-portal
