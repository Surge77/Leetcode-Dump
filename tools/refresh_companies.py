"""Rebuild tools/companies.json from a clone of liquidslr/leetcode-company-wise-problems.

    git clone --depth 1 https://github.com/liquidslr/leetcode-company-wise-problems <dir>
    python tools/refresh_companies.py <dir>
    python tools/build_index.py          # regenerates COMPANIES.md

Only problem slugs and titles are kept (no frequencies or other columns): for each company its TOP most frequent
problems overall and those asked in the last six months. The source is community-reported and changes every few
months; re-run this when it has been updated. Companies are the curated list below.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "companies.json"
SOURCE = "https://github.com/liquidslr/leetcode-company-wise-problems"
TOP, RECENT = 120, 60
COMPANIES = {  # display name: folder name in the source repo
    "Google": "Google", "Amazon": "Amazon", "Microsoft": "Microsoft", "Meta": "Meta", "Apple": "Apple",
    "Adobe": "Adobe", "Uber": "Uber", "Atlassian": "Atlassian", "Bloomberg": "Bloomberg", "Salesforce": "Salesforce",
    "LinkedIn": "LinkedIn", "Oracle": "Oracle", "Nvidia": "Nvidia", "Netflix": "Netflix", "Intuit": "Intuit",
    "PayPal": "PayPal", "Visa": "Visa", "American Express": "American Express", "Goldman Sachs": "Goldman Sachs",
    "J.P. Morgan": "J.P. Morgan", "Morgan Stanley": "Morgan Stanley", "DE Shaw": "DE Shaw", "Walmart Labs": "Walmart Labs",
    "Cisco": "Cisco", "IBM": "IBM", "Samsung": "Samsung", "Qualcomm": "Qualcomm", "ServiceNow": "ServiceNow",
    "Nutanix": "Nutanix", "Databricks": "Databricks", "Snowflake": "Snowflake", "Airbnb": "Airbnb",
    "DoorDash": "DoorDash", "eBay": "eBay", "Expedia": "Expedia", "Tesla": "Tesla", "Yahoo": "Yahoo",
    "Rubrik": "Rubrik", "Flipkart": "Flipkart", "PhonePe": "PhonePe", "Paytm": "Paytm", "Swiggy": "Swiggy",
    "Zomato": "Zomato", "Meesho": "Meesho", "Zoho": "Zoho", "Zeta": "Zeta", "Media.net": "Media.net",
    "Sprinklr": "Sprinklr", "Infosys": "Infosys", "TCS": "tcs", "Accenture": "Accenture", "Cognizant": "Cognizant",
    "Capgemini": "Capgemini", "Deloitte": "Deloitte",
}


def slugs(csv_path, limit):
    """[(slug, title, difficulty)] from one list file, most frequent first."""
    if not csv_path.exists():
        return []
    with csv_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: -float(r.get("Frequency") or 0))
    out = []
    for r in rows[:limit]:
        slug = r["Link"].rstrip("/").rsplit("/problems/", 1)[-1].strip()
        out.append((slug, r["Title"].strip(), r["Difficulty"].strip().title()))
    return out


def build(source_dir, as_of):
    companies, titles = {}, {}
    for name, folder in COMPANIES.items():
        top = slugs(source_dir / folder / "5. All.csv", TOP)
        recent = slugs(source_dir / folder / "3. Six Months.csv", RECENT)
        if not top:
            print(f"skipping {name}: no list in the source", file=sys.stderr)
            continue
        for slug, title, difficulty in top + recent:
            titles[slug] = [title, difficulty]
        companies[name] = {"all": [s for s, _, _ in top], "recent": [s for s, _, _ in recent]}
    return {"source": SOURCE, "as_of": as_of, "companies": companies, "titles": dict(sorted(titles.items()))}


def dumps(data):
    lines = ["{", f' "source": {json.dumps(data["source"])},', f' "as_of": {json.dumps(data["as_of"])},', ' "companies": {']
    lines.append(",\n".join(f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in data["companies"].items()))
    lines += [" },", ' "titles": {']
    lines.append(",\n".join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in data["titles"].items()))
    lines += [" }", "}"]
    return "\n".join(lines) + "\n"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit(__doc__)
    source = Path(argv[0])
    as_of = subprocess.run(["git", "-C", str(source), "log", "-1", "--format=%cs"], capture_output=True, text=True,
                           check=True).stdout.strip()
    data = build(source, as_of)
    OUT.write_text(dumps(data), encoding="utf-8", newline="\n")
    print(f"wrote {OUT.name}: {len(data['companies'])} companies, {len(data['titles'])} problems, as of {as_of}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
