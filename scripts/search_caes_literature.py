#!/usr/bin/env python3
"""Search CAES/AA-CAES/TCES literature through public Crossref metadata.

The script intentionally uses only the Python standard library so it can run
inside a fresh Codex environment without API keys.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CROSSREF_API = "https://api.crossref.org/works"

TOPIC_QUERIES = {
    "aa-caes-thermal-storage": (
        "adiabatic compressed air energy storage thermal energy storage packed bed"
    ),
    "aa-caes-dynamic-model": (
        "dynamic simulation adiabatic compressed air energy storage integrated thermal storage"
    ),
    "caes-exergy": (
        "exergy analysis adiabatic compressed air energy storage thermal energy storage"
    ),
    "tces-caes": (
        "thermochemical energy storage compressed air energy storage"
    ),
    "salt-hydrate-tces": (
        "thermochemical energy storage salt hydrates magnesium chloride magnesium sulfate"
    ),
    "zeolite-water-tces": (
        "zeolite 13X water thermochemical energy storage dehydration"
    ),
    "mgoh2-mgo-tces": (
        "modified Mg(OH)2 MgO thermochemical heat storage"
    ),
    "caes-economics": (
        "compressed air energy storage techno economic analysis LCOS"
    ),
}


@dataclass
class Paper:
    title: str
    year: str
    venue: str
    authors: str
    doi: str
    url: str
    abstract: str
    score: int
    quality: int


def clean_text(value: Any) -> str:
    if isinstance(value, list):
        value = " ".join(str(v) for v in value)
    text = str(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def year_from_item(item: dict[str, Any]) -> str:
    for key in ("published-print", "published-online", "published", "issued"):
        parts = item.get(key, {}).get("date-parts")
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def author_string(item: dict[str, Any], max_authors: int = 3) -> str:
    authors = []
    for author in item.get("author", [])[:max_authors]:
        name = " ".join(
            part for part in [author.get("given", ""), author.get("family", "")]
            if part
        ).strip()
        if name:
            authors.append(name)
    if not authors:
        return ""
    if len(item.get("author", [])) > max_authors:
        authors.append("et al.")
    return ", ".join(authors)


def relevance_score(item: dict[str, Any], query_terms: list[str]) -> int:
    title = clean_text(item.get("title", "")).lower()
    abstract = clean_text(item.get("abstract", "")).lower()
    venue = clean_text(item.get("container-title", "")).lower()
    text = f"{title} {abstract} {venue}"
    score = 0
    for term in query_terms:
        if len(term) < 3:
            continue
        if term in title:
            score += 4
        elif term in text:
            score += 1
    if "review" in title:
        score += 2
    if "compressed air energy storage" in text:
        score += 5
    if "thermochemical" in text:
        score += 3
    if "exergy" in text:
        score += 2
    return score


def quality_score(title: str, venue: str, year: str, doi: str) -> int:
    text = f"{title} {venue}".lower()
    score = 0
    high_signal_venues = [
        "applied energy",
        "energy",
        "energy conversion and management",
        "journal of energy storage",
        "renewable energy",
        "applied thermal engineering",
        "international journal of hydrogen energy",
        "energies",
    ]
    for venue_name in high_signal_venues:
        if venue_name in text:
            score += 8
            break
    if "review" in title.lower():
        score += 4
    if doi:
        score += 3
    if year.isdigit() and int(year) >= 2020:
        score += 2
    return score


def crossref_search(query: str, rows: int) -> list[dict[str, Any]]:
    params = {
        "query.bibliographic": query,
        "rows": str(rows),
        "select": ",".join([
            "title",
            "author",
            "published-print",
            "published-online",
            "published",
            "issued",
            "container-title",
            "DOI",
            "URL",
            "abstract",
            "type",
        ]),
        "filter": "type:journal-article",
    }
    url = f"{CROSSREF_API}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "caes-paper-evaluator/1.0 "
                "(mailto:anonymous@example.com)"
            )
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("message", {}).get("items", [])


def item_to_paper(item: dict[str, Any], query_terms: list[str]) -> Paper:
    title = clean_text(item.get("title", ""))
    venue = clean_text(item.get("container-title", ""))
    doi = clean_text(item.get("DOI", ""))
    url = clean_text(item.get("URL", ""))
    abstract = clean_text(item.get("abstract", ""))
    score = relevance_score(item, query_terms)
    quality = quality_score(title, venue, year_from_item(item), doi)
    return Paper(
        title=title,
        year=year_from_item(item),
        venue=venue,
        authors=author_string(item),
        doi=doi,
        url=url,
        abstract=abstract,
        score=score,
        quality=quality,
    )


def dedupe(papers: list[Paper]) -> list[Paper]:
    seen: set[str] = set()
    unique = []
    for paper in papers:
        key = (paper.doi or paper.title).lower()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(paper)
    return unique


def to_markdown(papers: list[Paper]) -> str:
    lines = [
        "| Relevance | Quality | Year | Title | Venue | DOI/URL |",
        "|---:|---:|---:|---|---|---|",
    ]
    for paper in papers:
        link = f"https://doi.org/{paper.doi}" if paper.doi else paper.url
        title = paper.title.replace("|", "\\|")
        venue = paper.venue.replace("|", "\\|")
        lines.append(
            f"| {paper.score} | {paper.quality} | {paper.year} | {title} | {venue} | {link} |"
        )
    return "\n".join(lines)


def bibtex_key(paper: Paper) -> str:
    first_author = "paper"
    if paper.authors:
        first_author = re.sub(r"[^A-Za-z0-9]", "", paper.authors.split(",")[0])
    first_word = "caes"
    for word in re.findall(r"[A-Za-z0-9]+", paper.title):
        if len(word) > 3:
            first_word = word.lower()
            break
    return f"{first_author}{paper.year}{first_word}"


def to_bibtex(papers: list[Paper]) -> str:
    entries = []
    for paper in papers:
        fields = [
            f"  title = {{{paper.title}}}",
            f"  journal = {{{paper.venue}}}",
            f"  year = {{{paper.year}}}",
        ]
        if paper.authors:
            fields.append(f"  author = {{{paper.authors}}}")
        if paper.doi:
            fields.append(f"  doi = {{{paper.doi}}}")
        elif paper.url:
            fields.append(f"  url = {{{paper.url}}}")
        entries.append("@article{" + bibtex_key(paper) + ",\n" + ",\n".join(fields) + "\n}")
    return "\n\n".join(entries)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", choices=sorted(TOPIC_QUERIES), help="Preset CAES topic")
    parser.add_argument("--query", help="Custom Crossref query")
    parser.add_argument("--limit", type=int, default=10, help="Number of results to print")
    parser.add_argument("--from-year", type=int, help="Keep papers from this year onward")
    parser.add_argument("--to-year", type=int, help="Keep papers up to this year")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum relevance score")
    parser.add_argument("--cache", type=Path, help="Optional JSON output path")
    parser.add_argument("--bibtex", type=Path, help="Optional BibTeX output path")
    args = parser.parse_args()

    if not args.topic and not args.query:
        print("Choose --topic or provide --query.\n")
        print("Available topics:")
        for topic, query in TOPIC_QUERIES.items():
            print(f"  {topic}: {query}")
        return 2

    query = args.query or TOPIC_QUERIES[args.topic or ""]
    query_terms = [term.lower() for term in re.findall(r"[A-Za-z0-9]+", query)]

    try:
        raw_items = crossref_search(query, max(args.limit * 3, 20))
    except Exception as exc:
        print(f"Crossref search failed: {exc}", file=sys.stderr)
        return 1

    papers = [item_to_paper(item, query_terms) for item in raw_items]
    papers = [paper for paper in dedupe(papers) if paper.title]
    if args.from_year:
        papers = [
            paper for paper in papers
            if paper.year.isdigit() and int(paper.year) >= args.from_year
        ]
    if args.to_year:
        papers = [
            paper for paper in papers
            if paper.year.isdigit() and int(paper.year) <= args.to_year
        ]
    if args.min_score:
        papers = [paper for paper in papers if paper.score >= args.min_score]
    papers.sort(key=lambda paper: (paper.score, paper.quality, paper.year), reverse=True)
    papers = papers[: args.limit]

    print(f"Query: {query}\n")
    print(to_markdown(papers))

    if args.cache:
        args.cache.parent.mkdir(parents=True, exist_ok=True)
        args.cache.write_text(
            json.dumps([paper.__dict__ for paper in papers], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\nSaved JSON: {args.cache}")

    if args.bibtex:
        args.bibtex.parent.mkdir(parents=True, exist_ok=True)
        args.bibtex.write_text(to_bibtex(papers), encoding="utf-8")
        print(f"Saved BibTeX: {args.bibtex}")

    time.sleep(0.1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
