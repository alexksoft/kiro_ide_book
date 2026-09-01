"""Verify every URL in the AI+Python catalogue; record results to ai_link_status.json."""

import concurrent.futures as cf
import json
import ssl
import urllib.error
import urllib.request
from datetime import date

from ai_python_data import ROWS
from ai_python_snippets import SNIPPETS

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
BOT_BLOCK = {401, 403, 429}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def check(url):
    last = None
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
                return url, r.status, "ok"
        except urllib.error.HTTPError as e:
            last = e.code
            if method == "GET":
                return url, e.code, "blocked-to-bots" if e.code in BOT_BLOCK else "broken"
        except Exception as e:  # noqa: BLE001
            last = type(e).__name__
            if method == "GET":
                return url, last, "broken"
    return url, last, "broken"


urls = sorted({r[4] for r in ROWS} | {s[5] for s in SNIPPETS})
print(f"catalogue rows: {len(ROWS)} | unique URLs to check: {len(urls)}")

with cf.ThreadPoolExecutor(max_workers=16) as ex:
    results = list(ex.map(check, urls))

today = date.today().isoformat()
status = {u: {"code": c, "kind": k, "checked": today} for u, c, k in results}
with open("ai_link_status.json", "w") as fh:
    json.dump(status, fh, indent=1, sort_keys=True)

ok = [r for r in results if r[2] == "ok"]
blocked = [r for r in results if r[2] == "blocked-to-bots"]
broken = [r for r in results if r[2] == "broken"]

print(f"\nverified 200 OK      : {len(ok)}")
print(f"blocked to bots      : {len(blocked)}")
print(f"BROKEN - needs fixing: {len(broken)}")
for u, c, _ in broken:
    print(f"   {c}  {u}")
print("\nblocked-to-bots detail:")
for u, c, _ in blocked:
    print(f"   {c}  {u}")
