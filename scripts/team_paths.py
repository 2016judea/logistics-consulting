#!/usr/bin/env python3
"""Try common leadership/team/contact paths on a domain and print any address found with nearby text."""
import html, re, subprocess, sys, concurrent.futures as cf
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
PATHS = ["", "/about", "/about-us", "/leadership", "/our-team", "/team", "/about/leadership", "/about-us/leadership", "/management", "/contact", "/contact-us", "/locations", "/about/our-team", "/company/leadership", "/who-we-are", "/our-people"]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
def get(u): return subprocess.run(["curl", "-sL", "-k", "-m", "15", "-A", UA, u], capture_output=True).stdout.decode("utf-8", "replace")
def scan(dom):
    out = {}
    for p in PATHS:
        u = f"https://{dom}{p}"
        h = get(u)
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", " ", h))))
        for m in EMAIL.finditer(h):
            e = m.group(0).lower().rstrip(".")
            if dom.split(".")[-2] not in e.split("@")[1] or re.search(r"\.(png|jpg|gif|svg|webp|css|js)$", e): continue
            if e in out: continue
            i = t.lower().find(e)
            out[e] = (u, t[max(0, i - 120):i] if i >= 0 else "")
    return dom, out
with cf.ThreadPoolExecutor(10) as ex:
    for dom, out in ex.map(scan, sys.argv[1:]):
        for e, (u, c) in out.items():
            print(dom, "|", e, "|", u, "|", c[-110:], flush=True)
        if not out: print(dom, "| -", flush=True)
