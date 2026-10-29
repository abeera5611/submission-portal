import json

r = json.load(open("report.json"))
lines = [
    f"Repository: {r['repository']}",
    f"Branch: {r['branch']}",
    f"Commit: {r['commit_sha']}",
    f"Run ID: {r['run_id']}",
    f"Overall result: {r['status'].upper()}",
    f"Total: {r['total']}  Passed: {r['passed']}  Failed: {r['failed']}",
    "",
    "Individual results:",
]
for t in r["tests"]:
    line = f"- [{t['result'].upper()}] {t['name']}"
    if t.get("failure_message"):
        line += f"  -> {t['failure_message']}"
    lines.append(line)

open("email_body.txt", "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))