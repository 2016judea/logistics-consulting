#!/usr/bin/env python3
"""Pull 3PL profiles from fulfill.com state pages -> name, website. Writes data/fulfill_sites.tsv"""
import re, subprocess, sys, concurrent.futures as cf
UA = "Mozilla/5.0 Chrome/130"
def get(u): return subprocess.run(["curl", "-sL", "-m", "20", "-A", UA, u], capture_output=True).stdout.decode("utf-8", "replace")
states = sys.argv[1:]
profiles = set()
for s in states:
    for p in set(re.findall(r'href="(/3pl/profile/[a-z0-9-]+)"', get(f"https://www.fulfill.com/3pl/location/{s}"))):
        profiles.add((s, p))
def site(sp):
    s, p = sp
    h = get("https://www.fulfill.com" + p)
    m = [u for u in re.findall(r'href="(https?://[^"]+)"', h) if not re.search(r"fulfill\.com|supabase|google|facebook|linkedin|twitter|instagram|youtube|schema|w3\.org|x\.com|tiktok|pinterest", u)]
    return s, p.split("/")[-1], (m[0] if m else "")
with cf.ThreadPoolExecutor(12) as ex, open("data/fulfill_sites.tsv", "a") as f:
    for s, n, u in ex.map(site, sorted(profiles)):
        f.write(f"{s}\t{n}\t{u}\n")
print(len(profiles))
