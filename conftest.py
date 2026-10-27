import json, os, datetime

results = []

def pytest_runtest_logreport(report):
    if report.when == "call" or (report.when == "setup" and report.failed):
        results.append({
            "name": report.nodeid,
            "result": "passed" if report.passed else "failed",
            "failure_message": str(report.longrepr).splitlines()[-1] if report.failed else None,
        })

def pytest_sessionfinish(session, exitstatus):
    passed = sum(r["result"] == "passed" for r in results)
    report = {
        "repository": os.getenv("GITHUB_REPOSITORY", "local"),
        "branch": os.getenv("GITHUB_REF_NAME", "local"),
        "commit_sha": os.getenv("GITHUB_SHA", "local"),
        "run_id": os.getenv("GITHUB_RUN_ID", "local"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tests": results,
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "status": "passed" if exitstatus == 0 else "failed",
    }
    json.dump(report, open("report.json", "w"), indent=2)