#!/usr/bin/env python3
"""For each company name, print its live LinkedIn job posts (last 30 days) whose company field matches.
    python3 scripts/li_company_jobs.py "KSP Fulfillment" "Citi-Cargo" ...
"""
import html, re, subprocess, sys, time, urllib.parse
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
for name in sys.argv[1:]:
    key = norm(name)[:8]
    hits = []
    for start in (0, 10):
        u = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + urllib.parse.urlencode({"keywords": name, "location": "United States", "f_TPR": "r2592000", "start": start})
        t = subprocess.run(["curl", "-s", "-m", "20", "-A", "Mozilla/5.0 (Macintosh) Chrome/130", u], capture_output=True).stdout.decode("utf-8", "replace")
        for c in t.split("<li>")[1:]:
            g = lambda pat: (m := re.search(pat, c, re.S)) and html.unescape(m.group(1)).strip()
            co = g(r'base-search-card__subtitle">.*?>\s*(.*?)\s*<') or ""
            if key in norm(co):
                hits.append((g(r'datetime="([^"]+)"'), co, g(r'base-search-card__title">\s*(.*?)\s*<'), g(r'job-search-card__location">\s*(.*?)\s*<'), g(r'href="(https://www\.linkedin\.com/jobs/view/[^"?]+)')))
        time.sleep(0.7)
    print(f"## {name}: {len(hits)}")
    for h in sorted(set(hits), reverse=True)[:6]:
        print("  ", " | ".join(str(x) for x in h))
