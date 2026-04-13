#!/usr/bin/env python3
"""
Generates all RSS feeds and writes them to the feeds/ directory.
Add new sites to the FEEDS list below.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from scrape_rss import fetch, SITE_EXTRACTORS, extract_generic, build_rss
from urllib.parse import urlparse

FEEDS = [
    {
        "url": "https://www.anthropic.com/research",
        "output": "feeds/anthropic-research.xml",
        "title": "Anthropic Research",
        "description": "Research posts from Anthropic",
    },
    {
        "url": "https://www.anthropic.com/engineering",
        "output": "feeds/anthropic-engineering.xml",
        "title": "Anthropic Engineering",
        "description": "Engineering posts from Anthropic",
    },
]

def generate(feed_cfg, root_dir):
    url = feed_cfg["url"]
    out = os.path.join(root_dir, feed_cfg["output"])
    print(f"Scraping {url} ...", end=" ", flush=True)
    html = fetch(url)
    parsed = urlparse(url)
    key = parsed.netloc + parsed.path
    extractor = SITE_EXTRACTORS.get(key, extract_generic)
    items = extractor(html, url)
    items.sort(key=lambda x: x.get("date") or "", reverse=True)
    rss = build_rss(url, items,
                    title=feed_cfg.get("title"),
                    description=feed_cfg.get("description"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(rss)
    print(f"{len(items)} items -> {feed_cfg['output']}")

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for cfg in FEEDS:
        try:
            generate(cfg, root)
        except Exception as e:
            print(f"ERROR {cfg['url']}: {e}", file=sys.stderr)
