from urllib.parse import urlparse

def validate(data):
    errors = []
    for f in ("name", "title", "url"):
        if not data.get(f, "").strip():
            errors.append(f"{f} is required")
    u = urlparse(data.get("url", "").strip())
    if data.get("url", "").strip() and (u.scheme not in ("http", "https") or not u.netloc):
        errors.append("Invalid submission URL")
    return errors