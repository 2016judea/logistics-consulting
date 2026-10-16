#!/usr/bin/env python3
"""Find a company's careers page and print the job titles/lines it lists right now.
    python3 scripts/careers.py https://example.com ...
"""
import html, re, subprocess, sys
from urllib.parse import urljoin, urlparse
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
def get(u): return subprocess.run(["curl", "-sL", "-k", "-m", "20", "-A", UA, u], capture_output=True).stdout.decode("utf-8", "replace")
def text(h):
    h = re.sub(r"(?s)<(script|style|noscript).*?</\1>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " | ", h)))
JOB = re.compile(r"[^|]{0,60}\b(driver|associate|manager|supervisor|lead|operator|dispatcher|handler|coordinator|technician|engineer|picker|packer|forklift|director|specialist|mechanic|clerk)s?\b[^|]{0,80}", re.I)
for site in sys.argv[1:]:
    h = get(site)
    links = []
    for href in re.findall(r'href=["\']([^"\'#]+)["\']', h, re.I):
        u = urljoin(site, href)
        if re.search(r"career|jobs?\b|employment|join|hiring|opportunit|work-with|workwithus|apply", u, re.I) and u not in links:
            links.append(u)
    print(f"## {site}  links: {links[:5]}")
    for u in links[:3]:
        t = text(get(u))
        hits = []
        for m in JOB.finditer(t):
            s = m.group(0).strip(" |")
            if 6 < len(s) < 140 and s not in hits: hits.append(s)
        print(f"  -> {u}: {len(hits)}")
        for s in hits[:10]: print("     ", s)
