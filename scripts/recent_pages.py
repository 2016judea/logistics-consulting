#!/usr/bin/env python3
"""List a company site's pages modified in the last ~6 months, from its sitemap.

    python3 scripts/recent_pages.py https://example.com [--all]

Reads robots.txt for Sitemap: lines (falls back to /sitemap.xml, /sitemap_index.xml,
/wp-sitemap.xml), follows nested sitemaps one level, and prints lastmod + URL for
pages since 2026-04-16 whose path looks like news/blog/press/careers/jobs
(--all drops that filter). This is where an opener comes from: a page THEY
published recently about their own operation.
"""
import re, subprocess, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
SINCE = "2026-04-16"
WANT = re.compile(r"news|blog|press|career|job|announc|expan|facility|warehouse|location|update|post", re.I)


def get(u):
    return subprocess.run(["curl", "-sL", "-k", "--max-time", "20", "-A", UA, u], capture_output=True).stdout.decode("utf-8", "replace")


def entries(xml):
    for block in re.findall(r"<(?:url|sitemap)>(.*?)</(?:url|sitemap)>", xml, re.S):
        loc = re.search(r"<loc>\s*(.*?)\s*</loc>", block, re.S)
        mod = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", block, re.S)
        if loc:
            yield loc.group(1).replace("&amp;", "&"), (mod.group(1)[:10] if mod else "")


def main(site, all_pages):
    site = site.rstrip("/")
    maps = re.findall(r"(?im)^sitemap:\s*(\S+)", get(site + "/robots.txt"))
    maps += [site + p for p in ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml")]
    seen, out = set(), []
    for m in maps:
        if m in seen:
            continue
        seen.add(m)
        xml = get(m)
        for loc, mod in entries(xml):
            if loc.endswith(".xml") or "sitemap" in loc.split("/")[-1]:
                if loc not in seen and len(seen) < 25:
                    seen.add(loc)
                    for l2, m2 in entries(get(loc)):
                        out.append((m2, l2))
            else:
                out.append((mod, loc))
        if out:
            break
    for mod, loc in sorted(set(out), reverse=True):
        if mod >= SINCE and (all_pages or WANT.search(loc)):
            print(mod, loc)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for s in args:
        print("##", s)
        main(s, "--all" in sys.argv)
