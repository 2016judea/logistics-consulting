#!/usr/bin/env python3
"""Print every email address a company's own site publishes, and the page it is on.

    python3 scripts/site_emails.py https://example.com [more sites...]

Fetches the homepage, then any same-site link whose path looks like
contact/about/team/leadership/staff, and greps each page for addresses
(plain text, mailto:, and Cloudflare's data-cfemail obfuscation). Output is
tab-separated: site, address, page_url. An address only counts as published
if this script, or a re-fetch, finds it on the page named.
"""
import html as html_mod, re, subprocess, sys
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
LINK = re.compile(r'href=["\']([^"\'#]+)["\']', re.I)
WANT = re.compile(r"contact|about|team|leader|staff|people|management|our-?company|who-we-are", re.I)
BAD = re.compile(r"\.(png|jpe?g|gif|svg|webp|css|js)$|sentry|wixpress|example\.com|domain\.com|godaddy|yourdomain|@2x", re.I)


def get(url):
    r = subprocess.run(["curl", "-sL", "-k", "--max-time", "20", "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", errors="replace")


def cf_decode(hexstr):
    k = int(hexstr[:2], 16)
    return "".join(chr(int(hexstr[i:i + 2], 16) ^ k) for i in range(2, len(hexstr), 2))


def emails_in(html):
    found = set(m.group(0).rstrip(".") for m in EMAIL.finditer(html))
    found |= {cf_decode(h) for h in re.findall(r'data-cfemail="([0-9a-f]+)"', html)}
    return {e for e in found if not BAD.search(e)}


def crawl(site):
    host = urlparse(site).netloc.replace("www.", "")
    html = get(site)
    pages = [(site, html)]
    links = []
    for href in LINK.findall(html):
        u = urljoin(site, href)
        if host in urlparse(u).netloc and WANT.search(urlparse(u).path) and u not in links:
            links.append(u)
    for u in links[:8]:
        pages.append((u, get(u)))
    seen = {}
    for u, h in pages:
        text = re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", h))))
        for e in emails_in(h):
            i = text.lower().find(e.lower())
            if i < 0:
                j = h.lower().find(e.lower())
                raw = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h[max(0, j - 1500):j]))
                ctx = raw[-140:].strip()
            else:
                ctx = text[max(0, i - 140):i].strip()
            seen.setdefault(e.lower(), (u, ctx[-140:]))
    return seen


if __name__ == "__main__":
    for site in sys.argv[1:]:
        res = crawl(site)
        if not res:
            print(f"{site}\t-\t-", flush=True)
        for e, (u, ctx) in sorted(res.items()):
            print(f"{site}\t{e}\t{u}\t{ctx}", flush=True)
