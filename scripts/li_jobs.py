#!/usr/bin/env python3
"""Search LinkedIn's logged-out job search (jobs-guest API) and print date | company | title | location | url.

    python3 scripts/li_jobs.py "3PL automation" "fulfillment operations manager" --location "United States" --pages 3
Only postings from the last 30 days (f_TPR=r2592000). The /jobs/view/ URL is a public page.
"""
import argparse, html, re, subprocess, time, urllib.parse
ap = argparse.ArgumentParser(); ap.add_argument("q", nargs="+"); ap.add_argument("--location", default="United States"); ap.add_argument("--pages", type=int, default=2)
a = ap.parse_args()
seen = set()
for q in a.q:
    for p in range(a.pages):
        u = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + urllib.parse.urlencode({"keywords": q, "location": a.location, "f_TPR": "r2592000", "start": p * 10})
        t = subprocess.run(["curl", "-s", "-m", "20", "-A", "Mozilla/5.0 (Macintosh) Chrome/130", u], capture_output=True).stdout.decode("utf-8", "replace")
        cards = t.split("<li>")[1:]
        if not cards: break
        for c in cards:
            g = lambda pat: (m := re.search(pat, c, re.S)) and html.unescape(m.group(1)).strip()
            url = g(r'href="(https://www\.linkedin\.com/jobs/view/[^"?]+)')
            if not url or url in seen: continue
            seen.add(url)
            print(g(r'datetime="([^"]+)"'), g(r'base-search-card__subtitle">.*?>\s*(.*?)\s*<'), g(r'base-search-card__title">\s*(.*?)\s*<'), g(r'job-search-card__location">\s*(.*?)\s*<'), url, sep=" | ", flush=True)
        time.sleep(1)
