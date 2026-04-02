#!/usr/bin/env python3
"""
AEIDSS — Data Processing Script
================================
Converts raw JHU CSSE COVID-19 CSV files into the
optimised JSON format embedded in aeidss_dashboard.html

USAGE:
    python scripts/process_data.py

INPUT:  data/*.csv  (JHU CSSE time-series files)
OUTPUT: Prints JSON to stdout (redirect to a file if needed)

The output JSON is already embedded in aeidss_dashboard.html.
Run this script only if you want to update the data.
"""

import csv
import json
import sys
import os

# Paths (relative to repo root)
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

FILES = {
    'confirmed': 'time_series_covid19_confirmed_global.csv',
    'deaths':    'time_series_covid19_deaths_global.csv',
}


def parse_csv(path):
    """Parse a JHU time-series CSV into (dates, records)."""
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    header  = rows[0]
    dates   = header[4:]
    records = []
    for row in rows[1:]:
        if len(row) < 5:
            continue
        records.append({
            'province': row[0],
            'country':  row[1],
            'lat':      row[2],
            'lon':      row[3],
            'values':   [int(float(v)) if v else 0 for v in row[4:]],
        })
    return dates, records


def aggregate_by_country(records):
    """Sum province-level data up to country level."""
    agg = {}
    for r in records:
        c = r['country']
        if c not in agg:
            agg[c] = [0] * len(r['values'])
        for i, v in enumerate(r['values']):
            agg[c][i] += v
    return agg


def get_subregions(records):
    """Build dict of country → list of sub-regions."""
    subs = {}
    for r in records:
        c, p = r['country'], r['province']
        if c not in subs:
            subs[c] = []
        if p and p != c and p not in subs[c]:
            subs[c].append(p)
    return subs


def compute_risk(country, conf, deaths, dates):
    """Compute composite risk score for a country."""
    lc  = conf[-1]
    ld  = deaths[-1]
    cfr = round(ld / lc * 100, 2) if lc > 0 else 0
    prev    = conf[-3] if len(conf) >= 3 else conf[0]
    growth  = round((lc - prev) / max(1, prev) * 100, 2)
    weekly  = max(0, lc - conf[-2]) if len(conf) >= 2 else 0
    risk    = min(100, abs(growth) * 0.5 + cfr * 5 + min(20, weekly / 500000))
    risk_cat = 'High' if risk > 20 else ('Medium' if risk > 10 else 'Low')
    return dict(cfr=cfr, gr=growth, wn=weekly, rs=round(risk, 1), rc=risk_cat)


def main():
    print("Loading CSV files…", file=sys.stderr)

    conf_path   = os.path.join(DATA_DIR, FILES['confirmed'])
    deaths_path = os.path.join(DATA_DIR, FILES['deaths'])

    for path in [conf_path, deaths_path]:
        if not os.path.exists(path):
            print(f"ERROR: {path} not found.", file=sys.stderr)
            print("Download the JHU CSSE dataset into the /data folder.", file=sys.stderr)
            sys.exit(1)

    dates_c, conf_records   = parse_csv(conf_path)
    dates_d, deaths_records = parse_csv(deaths_path)

    conf_agg   = aggregate_by_country(conf_records)
    deaths_agg = aggregate_by_country(deaths_records)
    subregions = get_subregions(conf_records)

    # Sample every 14th date to reduce file size
    sample_idx    = list(range(0, len(dates_c), 14))
    sampled_dates = [dates_c[i] for i in sample_idx]

    all_countries = sorted(
        conf_agg.keys(),
        key=lambda c: conf_agg[c][-1],
        reverse=True
    )

    print(f"Countries found: {len(all_countries)}", file=sys.stderr)
    print(f"Date range: {dates_c[0]} → {dates_c[-1]}", file=sys.stderr)
    print(f"Sampled dates: {len(sampled_dates)}", file=sys.stderr)

    countries_data = {}
    for c in all_countries:
        conf   = conf_agg[c]
        deaths = deaths_agg.get(c, [0] * len(dates_c))
        risk   = compute_risk(c, conf, deaths, dates_c)
        countries_data[c] = {
            'tc': conf[-1],
            'td': deaths[-1],
            'sr': subregions.get(c, []),
            'cs': [conf[i] for i in sample_idx],
            'ds': [deaths[i] for i in sample_idx],
            **risk
        }

    # Global totals (sampled)
    global_conf   = [sum(conf_agg[c][i] for c in all_countries if i < len(conf_agg[c]))
                     for i in sample_idx]
    global_deaths = [sum(deaths_agg.get(c, [0] * len(dates_c))[i] for c in all_countries)
                     for i in sample_idx]

    output = {
        'dates':     sampled_dates,
        'names':     all_countries,
        'countries': countries_data,
        'global':    {'c': global_conf, 'd': global_deaths},
    }

    size = len(json.dumps(output, separators=(',', ':')))
    print(f"Output size: {size / 1024:.0f} KB", file=sys.stderr)
    print("Done! Paste the JSON below into aeidss_dashboard.html", file=sys.stderr)
    print()

    print(json.dumps(output, separators=(',', ':')))


if __name__ == '__main__':
    main()
