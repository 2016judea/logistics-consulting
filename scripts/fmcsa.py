#!/usr/bin/env python3
"""fmcsa.py <dot|name-like> ... -> dot, name, city, power units, drivers, mileage(year), officers, filed email, MCS-150 date, SAFER url"""
import json, subprocess, sys, urllib.parse
for a in sys.argv[1:]:
    where = f"dot_number='{a}'" if a.isdigit() else f"status_code='A' AND upper(legal_name) like '%{a.upper()}%'"
    u = "https://data.transportation.gov/resource/az4n-8mr2.json?" + urllib.parse.urlencode({"$where": where, "$limit": 8})
    for r in json.loads(subprocess.run(["curl", "-s", u], capture_output=True).stdout):
        d = r["dot_number"]
        print(d, "|", r.get("legal_name"), "|", r.get("dba_name", ""), "|", r.get("phy_city"), r.get("phy_state"), "| PU", r.get("power_units"), "| drv", r.get("total_drivers"), "| mi", r.get("mcs150_mileage"), r.get("mcs150_mileage_year"), "|", r.get("company_officer_1", ""), "/", r.get("company_officer_2", ""), "|", r.get("email_address", ""), "|", r.get("mcs150_date"), f"| https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string={d}")
