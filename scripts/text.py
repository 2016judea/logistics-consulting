#!/usr/bin/env python3
"""Print a page's visible text. text.py URL [regex] [width] -> whole text (first 3000 chars) or each regex hit with context."""
import html, re, subprocess, sys
u = sys.argv[1]; pat = sys.argv[2] if len(sys.argv) > 2 else None; w = int(sys.argv[3]) if len(sys.argv) > 3 else 200
h = subprocess.run(["curl", "-sL", "-k", "-m", "25", "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36", u], capture_output=True).stdout.decode("utf-8", "replace")
t = re.sub(r"(?s)<(script|style|noscript).*?</\1>", " ", h)
t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
if not pat:
    print(t[:3000])
else:
    for m in list(re.finditer(pat, t, re.I))[:8]:
        print("...", t[max(0, m.start() - w):m.end() + w])
