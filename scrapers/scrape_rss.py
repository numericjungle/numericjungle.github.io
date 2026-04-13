#!/usr/bin/env python3
"""
Generate an RSS feed for websites that don't have one.
Usage:
    python3 scrape_rss.py https://www.anthropic.com/research > anthropic-research.xml
    python3 scrape_rss.py https://www.anthropic.com/research --output feeds/anthropic-research.xml
"""

import sys, re, argparse, datetime, time
from urllib.request import urlopen, Request
from urllib.parse import urljoin, urlparse
from xml.sax.saxutils import escape


HEADERS = {"User-Agent": "Mozilla/5.0 (RSS scraper)"}


def fetch(url):
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_anthropic_content(url):
    """Fetch a single Anthropic post and return its body as plain text paragraphs."""
    try:
        html = fetch(url)
        raw = html.replace('\\"', '"')
        # Extract text blocks from Next.js portable text JSON
        texts = re.findall(r'"_type":"block"[^}]*?"text":"([^"]+)"', raw)
        if not texts:
            # fallback: grab paragraph text from HTML
            texts = re.findall(r'<p[^>]*>([^<]{20,})</p>', html)
        paragraphs = [t for t in texts if len(t.strip()) > 30]
        return "\n\n".join(paragraphs[:30])  # cap at 30 paragraphs
    except Exception:
        return ""


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
        item["summary"] = fetch_anthropic_content(item["url"])
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


# ── RSS builder ───────────────────────────────────────────────────────────────

def build_rss(feed_url, items, title=None, description=None):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    feed_title = title or f"RSS: {feed_url}"
    feed_desc  = description or f"Auto-generated RSS feed for {feed_url}"

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        f'    <title>{escape(feed_title)}</title>',
        f'    <link>{escape(feed_url)}</link>',
        f'    <description>{escape(feed_desc)}</description>',
        f'    <lastBuildDate>{now}</lastBuildDate>',
        f'    <atom:link href="{escape(feed_url)}" rel="self" type="application/rss+xml"/>',
    ]

    for item in items:
        pub_date = ""
        if item.get("date"):
            try:
                dt = datetime.datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
                pub_date = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
            except Exception:
                pass

        lines += [
            "    <item>",
            f'      <title>{escape(item["title"])}</title>',
            f'      <link>{escape(item["url"])}</link>',
            f'      <guid>{escape(item["url"])}</guid>',
        ]
        if pub_date:
            lines.append(f"      <pubDate>{pub_date}</pubDate>")
        summary = item.get("summary") or ""
        if summary:
            # wrap paragraphs in <p> tags for RSS readers
            html_body = "".join(f"<p>{escape(p)}</p>" for p in summary.split("\n\n") if p.strip())
            lines.append(f"      <description><![CDATA[{html_body}]]></description>")
        lines.append("    </item>")

    lines += ["  </channel>", "</rss>"]
    return "\n".join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate RSS for a website")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--output", "-o", help="Write to file instead of stdout")
    parser.add_argument("--title", help="Feed title override")
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

    rss = build_rss(url, items, title=args.title)

    if args.output:
        with open(args.output, "w") as f:
            f.write(rss)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(rss)


if __name__ == "__main__":
    main()
