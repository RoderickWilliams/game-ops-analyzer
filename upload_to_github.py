import os
import base64
import json
import urllib.request
import urllib.error
import sys
import time

TOKEN = os.environ.get("GH_TOKEN", "")
OWNER = "RoderickWilliams"
REPO = "game-ops-analyzer"
API = "https://api.github.com"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Files to upload (relative path -> content)
def collect_files():
    files = {}
    for root, dirs, filenames in os.walk(PROJECT_DIR):
        # Skip .git, __pycache__, and example output html files
        if ".git" in root or "__pycache__" in root:
            continue
        for fn in filenames:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, PROJECT_DIR).replace("\\", "/")
            # Skip generated html, temp scripts
            if rel.endswith((".html",)) and "examples" in rel:
                continue
            if rel in ("check_github.py", "create_and_push.py", "git_push.py"):
                continue
            files[rel] = full
    return files

def upload_file(path, content_b64, token):
    url = f"{API}/repos/{OWNER}/{REPO}/contents/{path}"
    data = json.dumps({
        "message": f"Add {path}",
        "content": content_b64,
        "branch": "main",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PUT", headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        return True, result.get("content", {}).get("html_url", "")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 422 and "already exists" in body:
            return True, "already exists, skipped"
        return False, f"HTTP {e.code}: {body[:200]}"
    except Exception as e:
        return False, str(e)

def main():
    if not TOKEN:
        print("ERROR: GH_TOKEN environment variable not set")
        sys.exit(1)

    files = collect_files()
    print(f"Found {len(files)} files to upload")

    success = 0
    failed = 0
    for path, full_path in sorted(files.items()):
        with open(full_path, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode("utf-8")

        ok, msg = upload_file(path, content_b64, TOKEN)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {path} - {msg}")
        if ok:
            success += 1
        else:
            failed += 1
        time.sleep(0.5)  # rate limit

    print(f"\nDone: {success} uploaded, {failed} failed")
    if failed == 0:
        print(f"\nRepository: https://github.com/{OWNER}/{REPO}")

if __name__ == "__main__":
    main()
