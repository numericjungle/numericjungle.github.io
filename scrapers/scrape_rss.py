#!/usr/bin/env python3
"""
Generate an RSS feed for websites that don't have one.
Usage:
    python3 scrape_rss.py https://www.anthropic.com/research > anthropic-research.xml
    python3 scrape_rss.py https://www.anthropic.com/research --output feeds/anthropic-research.xml
"""

import argparse
import datetime
import html
import json
import re
import sys
import time
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape


HEADERS = {"User-Agent": "Mozilla/5.0 (RSS scraper)"}
DEFAULT_LANGUAGE = "en-US"
GENERATOR_NAME = "numericjungle scrape_rss.py"
MAX_DESCRIPTION_CHARS = 500
ANTHROPIC_CHROME_PREFIXES = (
    "Research",
    "Economic Futures",
    "Commitments",
    "Learn",
    "News",
    "Try Claude",
    "Research at Anthropic",
    "Engineering at Anthropic",
)


def fetch(url):
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def normalize_text(text):
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_html(fragment):
    fragment = re.sub(r"<script\b[^>]*>.*?</script>", " ", fragment, flags=re.IGNORECASE | re.DOTALL)
    fragment = re.sub(r"<style\b[^>]*>.*?</style>", " ", fragment, flags=re.IGNORECASE | re.DOTALL)
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.IGNORECASE)
    fragment = re.sub(r"</p\s*>", "\n\n", fragment, flags=re.IGNORECASE)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return normalize_text(fragment)


def decode_json_string(raw):
    try:
        return json.loads(f'"{raw}"')
    except Exception:
        return raw.replace('\\"', '"').replace("\\n", "\n")


def split_paragraphs(text):
    paragraphs = []
    for chunk in re.split(r"\n\s*\n", text):
        chunk = normalize_text(chunk)
        if chunk:
            paragraphs.append(chunk)
    return paragraphs


def truncate_text(text, limit):
    if len(text) <= limit:
        return text
    clipped = text[: max(0, limit - 1)].rsplit(" ", 1)[0].rstrip(" ,.;:")
    return (clipped or text[: max(0, limit - 1)]).rstrip() + "..."


def format_rfc2822(dt):
    return dt.astimezone(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")


def parse_iso_datetime(value):
    if not value:
        return None
    value = value.strip()
    try:
        dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)


def parse_human_published_date(value):
    try:
        dt = datetime.datetime.strptime(value, "%b %d, %Y")
    except ValueError:
        return ""
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat()


def extract_published_date(page_html):
    patterns = [
        r'"datePublished":"([^"]+)"',
        r'"publishedOn":"([^"]+)"',
        r'<meta[^>]+property="article:published_time"[^>]+content="([^"]+)"',
        r'<meta[^>]+name="article:published_time"[^>]+content="([^"]+)"',
        r'<time[^>]+datetime="([^"]+)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, page_html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    visible_match = re.search(r"\bPublished\s+([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})\b", page_html)
    if visible_match:
        return parse_human_published_date(visible_match.group(1))
    return ""


def build_plain_summary(summary):
    summary = normalize_text(summary)
    if not summary:
        return ""
    summary = " ".join(split_paragraphs(summary))
    return truncate_text(summary, MAX_DESCRIPTION_CHARS)


def clean_anthropic_paragraph(paragraph, title):
    paragraph = normalize_text(paragraph)
    if not paragraph:
        return ""

    # Anthropic pages often expose header/nav text in the same extracted block.
    changed = True
    while changed:
        changed = False
        for prefix in ANTHROPIC_CHROME_PREFIXES:
            token = f"{prefix} "
            if paragraph.startswith(token):
                paragraph = paragraph[len(token):].lstrip()
                changed = True

    if title and title in paragraph:
        paragraph = paragraph[paragraph.index(title):].lstrip()

    boilerplate_prefixes = (
        "Published ",
        "Written by ",
    )
    for prefix in boilerplate_prefixes:
        if paragraph == prefix.strip():
            return ""

    return paragraph


def fetch_anthropic_article(url):
    """Fetch a single Anthropic post and return summary text plus published date."""
    try:
        page_html = fetch(url)
    except Exception:
        return {"summary": "", "date": ""}

    texts = re.findall(r'"_type":"block".*?"text":"((?:\\.|[^"\\])*)"', page_html, re.DOTALL)
    paragraphs = [
        normalize_text(decode_json_string(text))
        for text in texts
        if normalize_text(decode_json_string(text))
    ]
    if not paragraphs:
        paragraphs = [
            strip_html(fragment)
            for fragment in re.findall(r"<p[^>]*>(.*?)</p>", page_html, re.IGNORECASE | re.DOTALL)
            if strip_html(fragment)
        ]

    cleaned = []
    seen = set()
    title_match = re.search(r"<title>(.*?)</title>", page_html, re.IGNORECASE | re.DOTALL)
    title = strip_html(title_match.group(1)) if title_match else ""
    for paragraph in paragraphs:
        paragraph = clean_anthropic_paragraph(paragraph, title)
        if not paragraph or paragraph in seen:
            continue
        seen.add(paragraph)
        cleaned.append(paragraph)

    return {
        "summary": "\n\n".join(cleaned[:30]),
        "date": extract_published_date(page_html),
    }


# ── site-specific extractors ──────────────────────────────────────────────────

def extract_anthropic_section(html, base_url, section):
    """Generic extractor for anthropic.com/<section> pages (research, engineering, etc.)"""
    raw = html.replace('\\"', '"')

    slugs = re.findall(r'"current":"([\w-]+)"', raw)
    dates = re.findall(r'"publishedOn":"([^"]+)"', raw)

    title_map = {}
    for slug, title in re.findall(
        r'href="/' + section + r'/([\w-]+)"[^>]*>.*?<h[2-4][^>]*>([^<]+)<', raw, re.DOTALL
    ):
        title_map.setdefault(slug, title.strip())

    skip = {section, "team", "not-found"}
    skip_titles = {"products", "research", "engineering", "not found", "company"}

    seen = set()
    items = []
    for i, slug in enumerate(slugs):
        if slug in seen or slug in skip:
            continue
        seen.add(slug)
        date = dates[i] if i < len(dates) else ""
        title = title_map.get(slug) or slug.replace("-", " ").title()
        if title.lower() in skip_titles:
            continue
        url = urljoin(base_url, f"/{section}/{slug}")
        items.append({"title": title, "url": url, "date": date, "summary": None})

    # fetch content only for the 30 most recent posts (sorted by date desc)
    recent = sorted(items, key=lambda x: x.get("date") or "", reverse=True)[:30]
    print(f"  fetching content for {len(recent)} recent posts...", end=" ", flush=True)
    for item in recent:
        details = fetch_anthropic_article(item["url"])
        item["summary"] = details["summary"]
        if not item.get("date") and details["date"]:
            item["date"] = details["date"]
        time.sleep(0.2)
    print("done")

    return items


def extract_anthropic(html, base_url):
    return extract_anthropic_section(html, base_url, "research")


def extract_anthropic_engineering(html, base_url):
    return extract_anthropic_section(html, base_url, "engineering")


def extract_generic(html, base_url):
    """Generic extractor for blog/news index pages."""
    path_prefix = urlparse(base_url).path.rstrip("/")
    items = []
    seen = set()

    pattern = re.compile(
        r'href="(' + re.escape(path_prefix) + r'/[^"#?]+)"[^>]*>'
        r'(?:(?!</a>).){0,500}?'
        r'(?:<[^>]*(?:title|heading|h[1-4])[^>]*>|<h[1-4][^>]*>)'
        r'([^<]{10,200})<',
        re.DOTALL | re.IGNORECASE
    )
    for m in re.finditer(pattern, html):
        url, title = m.group(1), m.group(2).strip()
        if url not in seen and title:
            seen.add(url)
            items.append({"title": title, "url": urljoin(base_url, url), "date": "", "summary": ""})

    if not items:
        for href in re.findall(r'href="(' + re.escape(path_prefix) + r'/[\w/-]+)"', html):
            if href not in seen:
                seen.add(href)
                items.append({
                    "title": href.split("/")[-1].replace("-", " ").title(),
                    "url": urljoin(base_url, href),
                    "date": "",
                    "summary": "",
                })

    return items


SITE_EXTRACTORS = {
    "www.anthropic.com/research":    extract_anthropic,
    "www.anthropic.com/engineering": extract_anthropic_engineering,
}


def build_rss(feed_url, items, title=None, description=None, self_url=None, language=DEFAULT_LANGUAGE):
    build_time = datetime.datetime.now(datetime.timezone.utc)
    now = format_rfc2822(build_time)
    feed_title = title or f"RSS: {feed_url}"
    feed_desc  = description or f"Auto-generated RSS feed for {feed_url}"
    feed_self_url = self_url or feed_url

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        f'    <title>{escape(feed_title)}</title>',
        f'    <link>{escape(feed_url)}</link>',
        f'    <description>{escape(feed_desc)}</description>',
        f'    <language>{escape(language)}</language>',
        f'    <generator>{escape(GENERATOR_NAME)}</generator>',
        f'    <lastBuildDate>{now}</lastBuildDate>',
        f'    <atom:link href="{escape(feed_self_url)}" rel="self" type="application/rss+xml"/>',
    ]

    for item in items:
        dt = parse_iso_datetime(item.get("date", ""))
        pub_date = format_rfc2822(dt) if dt else ""
        plain_summary = build_plain_summary(item.get("summary") or "")

        lines += [
            "    <item>",
            f'      <title>{escape(item["title"])}</title>',
            f'      <link>{escape(item["url"])}</link>',
            f'      <guid isPermaLink="true">{escape(item["url"])}</guid>',
        ]
        if pub_date:
            lines.append(f"      <pubDate>{pub_date}</pubDate>")
        if plain_summary:
            lines.append(f"      <description>{escape(plain_summary)}</description>")
        lines.append("    </item>")

    lines += ["  </channel>", "</rss>"]
    return "\n".join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate RSS for a website")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--output", "-o", help="Write to file instead of stdout")
    parser.add_argument("--title", help="Feed title override")
    parser.add_argument("--self-url", help="Public URL of the generated feed")
    args = parser.parse_args()

    url = args.url.rstrip("/")
    parsed = urlparse(url)
    key = parsed.netloc + parsed.path

    print(f"Fetching {url} ...", file=sys.stderr)
    html = fetch(url)

    extractor = SITE_EXTRACTORS.get(key, extract_generic)
    items = extractor(html, url)
    items.sort(key=lambda x: x.get("date") or "", reverse=True)

    print(f"Found {len(items)} items", file=sys.stderr)

    rss = build_rss(url, items, title=args.title, self_url=args.self_url)

    if args.output:
        with open(args.output, "w") as f:
            f.write(rss)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(rss)


if __name__ == "__main__":
    main()
