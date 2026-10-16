# Logistics consulting outreach

Aidan spent five years as a researcher in Amazon Transportation & Fulfillment. He is
not taking traditional employment; he wants short, paid logistics/fulfillment
engagements. This repo holds the outreach for that, built off his public proof asset —
the Substack post *"Directed Staffing of Outbound Dock Doors in Amazon Fulfillment
Centers."*

## Status: all 50 scheduled (2026-10-16)

Aidan said go. All 50 are scheduled in Zoho from aidan@brickandmortar.dev, plaintext,
America/Chicago: 12 on 10/22, 24 on 10/23, 14 on 10/26, fitted under the mailbox cap
(`~/.claude/hooks/zoho_send_cap.py`). One email each, no follow-ups. Per-row status and
send time are in `recipients.csv`; `queue.json` is what was scheduled
(`scripts/build_queue.py`). Read replies with the business-inbox skill and fill
`reply_kind` / `reply_on`.

## What's here

- `outreach/round1/recipients.csv` — 50 verified recipients, ~17 per segment:
  1. Twin Cities (MN 7-county metro) 3PL / warehousing / fulfillment / FBA-prep / courier.
  2. National & regional mid-market 3PLs, most with a live operations hiring signal.
  3. Regional parcel / courier / last-mile operators.
  Each row names the person who runs the dock (VP/Director of Operations, GM, or the
  owner at small shops), their email, how that email was verified, and a sourced,
  dated opener about their own operation.
- `outreach/round1/drafts/<slug>.txt` — one draft email per recipient, written in
  Aidan's voice: the opener line about them, his Amazon credential verbatim, five
  problem lines in generic industry terms (no numbers, no Amazon internals), his close
  ("Ask me anything, I do consulting."), and two links — his LinkedIn and the Substack
  post. No price, no attachment.
- `scripts/` — the tools used to find and verify recipients (FMCSA census lookups,
  on-site email harvesting, careers/job-post scans). `build_round1.py` is the source of
  truth: it writes the CSV and every draft. Edit it, re-run it, don't hand-edit the
  output.

## Address rule

Every address is either **published** on the company's own website, or **FMCSA-filed** —
the email the operator signed into the federal carrier census
(`data.transportation.gov`, dataset `az4n-8mr2`). The method is recorded per row in
`email_method`. No address is a guessed `first.last@` pattern; pattern guesses bounce,
and bounces stop a Mailgun account at 3%.

## Not done / needs Aidan

- He reads and approves (or edits) each draft before any send.
- The send channel and schedule are his call (see the `distribution-channel` skill and
  `BUSINESS.md` rule 4: at least 50 delivered recipients across 3+ segments before a
  result means anything).
