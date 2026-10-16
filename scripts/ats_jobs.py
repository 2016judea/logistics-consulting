#!/usr/bin/env python3
"""Probe public ATS job boards (Greenhouse, Lever, Ashby, Workable) for a company slug and
print ops/automation roles with their posted/updated date and URL.

    python3 scripts/ats_jobs.py shipmonk redstagfulfillment ...
"""
import json, re, subprocess, sys
UA = "Mozilla/5.0 Chrome/130"
ROLE = re.compile(r"automat|operation|general manager|site (lead|manager|director)|engineer|continuous improvement|industrial|process|warehouse manager|director|robot|labor|workforce|dc manager|fulfillment manager", re.I)

def get(u, data=None):
    cmd = ["curl", "-s", "-m", "15", "-A", UA, u]
    if data:
        cmd += ["-H", "Content-Type: application/json", "-d", data]
    return subprocess.run(cmd, capture_output=True).stdout.decode("utf-8", "replace")

def gh(s):
    try: j = json.loads(get(f"https://boards-api.greenhouse.io/v1/boards/{s}/jobs"))
    except Exception: return []
    return [(x.get("updated_at", "")[:10], x["title"], x.get("location", {}).get("name", ""), x["absolute_url"]) for x in j.get("jobs", [])]

def lever(s):
    try: j = json.loads(get(f"https://api.lever.co/v0/postings/{s}?mode=json"))
    except Exception: return []
    if not isinstance(j, list): return []
    import datetime
    return [(datetime.datetime.utcfromtimestamp(x.get("createdAt", 0) / 1000).strftime("%Y-%m-%d"), x["text"], x.get("categories", {}).get("location", ""), x["hostedUrl"]) for x in j]

def ashby(s):
    try: j = json.loads(get(f"https://api.ashbyhq.com/posting-api/job-board/{s}"))
    except Exception: return []
    return [(x.get("publishedAt", "")[:10], x["title"], x.get("location", ""), x["jobUrl"]) for x in j.get("jobs", [])]

def workable(s):
    try: j = json.loads(get(f"https://apply.workable.com/api/v3/accounts/{s}/jobs", data='{"query":""}'))
    except Exception: return []
    return [(x.get("published", "")[:10], x["title"], (x.get("location") or {}).get("city", ""), f"https://apply.workable.com/{s}/j/{x['shortcode']}/") for x in j.get("results", [])]

for s in sys.argv[1:]:
    for name, fn in (("greenhouse", gh), ("lever", lever), ("ashby", ashby), ("workable", workable)):
        rows = fn(s)
        if rows:
            hits = [r for r in rows if ROLE.search(r[1])]
            print(f"## {s} [{name}] {len(rows)} jobs, {len(hits)} ops/automation")
            for r in sorted(hits, reverse=True)[:12]:
                print("  ", *r, sep=" | ")
