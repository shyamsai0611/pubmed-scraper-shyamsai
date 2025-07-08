from typing import List, Dict
import requests
from xml.etree import ElementTree as ET
import re

PHARMA_KEYWORDS = ["pharma", "biotech", "therapeutics", "labs", "inc", "ltd", "gmbh", "corporation", "healthcare", "biosciences", "med", "clinical"]
ACADEMIC_KEYWORDS = ["university", "college", "institute", "school", "hospital", "centre", "center", "faculty"]

def is_non_academic_affiliation(aff: str) -> bool:
    aff = aff.lower()
    return not any(x in aff for x in ACADEMIC_KEYWORDS) and any(x in aff for x in PHARMA_KEYWORDS)

def fetch_pubmed_ids(query: str, retmax: int = 100) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": retmax}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["esearchresult"]["idlist"]

def fetch_paper_details(ids: List[str], debug: bool = False) -> List[Dict]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    r = requests.get(url, params={"db": "pubmed", "id": ",".join(ids), "retmode": "xml"})
    r.raise_for_status()
    root = ET.fromstring(r.text)
    results = []

    for article in root.findall(".//PubmedArticle"):
        citation = article.find("MedlineCitation")
        article_info = citation.find("Article")
        paper = {
            "PubmedID": citation.findtext("PMID", ""),
            "Title": article_info.findtext("ArticleTitle", "No Title"),
            "Publication Date": "Unknown",
            "Non-academicAuthor(s)": "",
            "CompanyAffiliation(s)": "",
            "Corresponding Author Email": "N/A"
        }

        pub_date = article_info.find(".//PubDate")
        if pub_date is not None:
            y, m, d = pub_date.findtext("Year", ""), pub_date.findtext("Month", ""), pub_date.findtext("Day", "")
            paper["Publication Date"] = f"{y}-{m or '01'}-{d or '01'}"

        authors = article_info.find("AuthorList")
        emails, companies, authors_out = set(), set(), set()

        if authors:
            for a in authors.findall("Author"):
                name = " ".join(filter(None, [a.findtext("ForeName", ""), a.findtext("LastName", "")]))
                for aff in a.findall(".//AffiliationInfo/Affiliation"):
                    if aff is not None and is_non_academic_affiliation(aff.text or ""):
                        authors_out.add(name)
                        companies.add(aff.text.strip())
                        match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", aff.text)
                        if match:
                            emails.add(match.group(0))

        if authors_out:
            paper["Non-academicAuthor(s)"] = "; ".join(authors_out)
            paper["CompanyAffiliation(s)"] = "; ".join(companies)
            paper["Corresponding Author Email"] = next(iter(emails), "N/A")
            results.append(paper)
            if debug:
                print(f"✔ {paper['Title'][:60]}...")

    return results
