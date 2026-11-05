"""Round 1: parse drafts, round-robin segments, fit into Zoho cap slots
(~/.claude/hooks/zoho_send_cap.py: 10/h, 25/24h, 90s gap), weekdays 08:30-15:30 CT."""
import csv, json, os, time, datetime, re
from zoneinfo import ZoneInfo
R = os.path.expanduser('~/Desktop/workspace/logistics-consulting/outreach/round1')
tz = ZoneInfo('America/Chicago')
rows = list(csv.DictReader(open(f'{R}/recipients.csv')))
def parse(r):
    txt = open(f"{R}/{r['draft_file']}").read()
    subj = re.search(r'^Subject: (.+)$', txt, re.M).group(1).strip()
    body = txt.split('\n', txt.split('\n').index(next(l for l in txt.split('\n') if l.startswith('Subject:'))) + 1)[-1].lstrip('\n')
    return {'segment': r['segment'], 'company': r['company'], 'to': r['email'].strip(), 'subject': subj, 'content': body}
by = {}
for r in rows: by.setdefault(r['segment'], []).append(parse(r))
order = []
while any(by.values()):
    for s in sorted(by):
        if by[s]: order.append(by[s].pop(0))
taken = [json.loads(l)['t'] for l in open(os.path.expanduser('~/.claude/state/zoho_sends.jsonl'))]
def ok(t):
    if any(abs(t - x) < 240 for x in taken): return False
    if sum(1 for x in taken if t - 3600 < x <= t + 0) >= 9: return False
    if any(sum(1 for x in taken if w <= x < w + 86400) >= 24 for w in (t - 86400 + 1, t)): return False
    return True
now = time.time()
slots, t = [], now + 600
TODAY_MAX = int(os.environ.get('TODAY_MAX', 6))
today = datetime.datetime.fromtimestamp(now, tz).date()
while len(slots) < len(order):
    d = datetime.datetime.fromtimestamp(t, tz)
    in_hours = d.weekday() < 5 and (8, 30) <= (d.hour, d.minute) <= (15, 30)
    if d.date() == today: in_hours = d.hour < 17 and sum(1 for s in slots if datetime.datetime.fromtimestamp(s, tz).date() == today) < TODAY_MAX
    if in_hours and ok(t): slots.append(t); taken.append(t); t += 480
    else: t += 120
for q, s in zip(order, slots):
    q['when'] = datetime.datetime.fromtimestamp(s, tz).strftime('%m/%d/%Y %H:%M:%S')
json.dump(order, open(f'{R}/queue.json', 'w'), indent=1)
from collections import Counter
print(len(order), Counter(q['when'][:10] for q in order))
