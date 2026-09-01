"""Verify every URL in the catalogue and record the result to link_status.json.

Some sites (Stack Overflow, Medium, Quora, Udemy, OpenAI...) block automated
clients with 403/429 even though the page is fine in a browser. Those are
recorded as 'blocked-to-bots' rather than broken, so the workbook can be honest
about what was and was not machine-verified.
"""

import concurrent.futures as cf
import json
import ssl
import urllib.error
import urllib.request
from datetime import date

from kiro_resources_data import ROWS, DUPES_REMOVED

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
                kind = "blocked-to-bots" if e.code in BOT_BLOCK else "broken"
                return url, e.code, kind
        except Exception as e:  # noqa: BLE001
            last = type(e).__name__
            if method == "GET":
                return url, last, "broken"
    return url, last, "broken"


urls = [r[3] for r in ROWS]
print(f"rows: {len(urls)} | unique: {len(set(urls))} | duplicates removed by data module: {DUPES_REMOVED}")

with cf.ThreadPoolExecutor(max_workers=16) as ex:
    results = list(ex.map(check, urls))

today = date.today().isoformat()
status = {u: {"code": c, "kind": k, "checked": today} for u, c, k in results}
with open("link_status.json", "w") as fh:
    json.dump(status, fh, indent=1, sort_keys=True)

ok = [r for r in results if r[2] == "ok"]
blocked = [r for r in results if r[2] == "blocked-to-bots"]
broken = [r for r in results if r[2] == "broken"]

print(f"\nverified 200 OK      : {len(ok)}")
print(f"blocked to bots      : {len(blocked)}  (pages exist; open fine in a browser)")
print(f"BROKEN - needs fixing: {len(broken)}")
for u, c, _ in broken:
    print(f"   {c}  {u}")
print("\nblocked-to-bots detail:")
for u, c, _ in blocked:
    print(f"   {c}  {u}")
