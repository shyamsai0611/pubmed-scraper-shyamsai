import argparse
import csv
from typing import List, Dict
from pubmed_scraper_shyamsai.scraper import fetch_pubmed_ids, fetch_paper_details

def save_to_csv(data: List[Dict], filename: str):
    fields = ["PubmedID", "Title", "Publication Date", "Non-academicAuthor(s)", "CompanyAffiliation(s)", "Corresponding Author Email"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved {len(data)} results to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic pharma/biotech author affiliations.")
    parser.add_argument("query", help="PubMed query string")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logs")
    parser.add_argument("-f", "--file", type=str, help="CSV output filename")

    args = parser.parse_args()

    try:
        ids = fetch_pubmed_ids(args.query)
        if not ids:
            print("❌ No results found.")
            return

        results = fetch_paper_details(ids, debug=args.debug)
        if not results:
            print("❌ No non-academic pharma/biotech authors found.")
            return

        if args.file:
            save_to_csv(results, args.file)
        else:
            for r in results:
                print("-" * 50)
                for k, v in r.items():
                    print(f"{k}: {v}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
