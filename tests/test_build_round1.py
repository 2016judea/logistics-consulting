"""scripts/build_round1.py is the source of truth for outreach/round1/recipients.csv, and the CSV is also
the ledger (status, scheduled_ct, reply_kind, reply_on, filled by hand after the 10/16 scheduling).
A rebuild must regenerate the drafts without wiping the ledger columns."""
import csv
import re

import build_round1 as B


def test_a_rebuild_keeps_the_hand_filled_ledger_columns(tmp_path):
    B.main(str(tmp_path))
    rows = list(csv.DictReader(open(tmp_path / "recipients.csv", newline="")))
    assert len(rows) == len(B.R)
    rows[0]["status"] = "scheduled"; rows[0]["scheduled_ct"] = "10/22/2026 08:30"; rows[1]["reply_kind"] = "yes"
    with open(tmp_path / "recipients.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=B.COLS + ["status", "scheduled_ct", "reply_kind", "reply_on"])
        w.writeheader(); [w.writerow({**{"status": "", "scheduled_ct": "", "reply_kind": "", "reply_on": ""}, **r}) for r in rows]
    B.main(str(tmp_path))
    again = list(csv.DictReader(open(tmp_path / "recipients.csv", newline="")))
    assert again[0]["status"] == "scheduled" and again[0]["scheduled_ct"] == "10/22/2026 08:30"
    assert again[1]["reply_kind"] == "yes" and again[2]["status"] == ""
    assert again[0]["company"] == rows[0]["company"]


def test_every_recipient_has_a_verified_address_and_a_draft_with_both_links(tmp_path):
    B.main(str(tmp_path))
    for r in csv.DictReader(open(tmp_path / "recipients.csv", newline="")):
        assert re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]+", r["email"]), r["email"]
        assert r["email_method"] in ("published", "FMCSA-filed")
        draft = (tmp_path / r["draft_file"]).read_text()
        assert draft.startswith("DRAFT - NOT SENT")
        assert B.LINKEDIN in draft and B.SUBSTACK in draft and f"Subject: {r['subject']}" in draft
