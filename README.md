# pubmed-scraper-shyamsai

A command-line Python tool to fetch and filter research papers from PubMed based on a user query. It specifically identifies papers where at least one author is affiliated with a **pharmaceutical** or **biotech company**, and outputs the results as a CSV file.

---

## 🚀 Features

- 🔎 Query PubMed using its full query syntax.
- 🧠 Automatically detects **non-academic author affiliations** using heuristics.
- 📁 Outputs results as a CSV file or prints to console.
- 🐍 Fully typed Python code, modular, and easy to extend.
- ✅ Built using [Poetry](https://python-poetry.org/) for packaging and dependency management.

---

## 📦 Installation

### ➤ From TestPyPI (after publishing):

```
pip install -i https://test.pypi.org/simple/ pubmed-scraper-shyamsai
```
or
```
pip install --extra-index-url https://test.pypi.org/simple/ pubmed-scraper-shyamsai
```

## ➤ From source (local development):

```
git clone https://github.com/shyamsai0611/pubmed-scraper-shyamsai.git
cd pubmed-scraper-shyamsai
poetry install

```


## 🛠 Usage
### Basic CLI:

```
get-papers-list "covid vaccine"
```
### Save results to a file:

```
get-papers-list "covid vaccine" -f results.csv
```
### Enable debug mode (prints matched paper titles):

```
get-papers-list "cancer immunotherapy" -d
```

## 📊 Output Format (CSV)
| Column                       | Description                                                |
| ---------------------------- | ---------------------------------------------------------- |
| `PubmedID`                   | Unique identifier of the paper in PubMed                   |
| `Title`                      | Title of the research paper                                |
| `Publication Date`           | Date the paper was published                               |
| `Non-academicAuthor(s)`      | Authors affiliated with non-academic (pharma/biotech) orgs |
| `CompanyAffiliation(s)`      | Names of those organizations                               |
| `Corresponding Author Email` | Email address found in the author affiliations             |

## 🧠 Heuristics for Non-Academic Authors

An author is considered non-academic if:

Their affiliation contains keywords like pharma, biotech, therapeutics, labs, inc, ltd, gmbh, etc.

AND it does not contain academic terms like university, institute, hospital, etc.

## 📁 Project Structure
```
pubmed-scraper-shyamsai/
├── pubmed_scraper_shyamsai/
│   ├── __init__.py
│   ├── scraper.py      # Core logic for querying and filtering
│   └── cli.py          # Command-line interface
├── pyproject.toml       # Poetry configuration
├── README.md
└── result.csv           # Example output (if saved)
```

## 🧪 Running Locally (Dev Mode)
```
poetry run get-papers-list "cancer" -f cancer_papers.csv -d
```

## 👨‍💻 Author
Shyam Sai Manohar K
📧 munna06112003@gmail.com
