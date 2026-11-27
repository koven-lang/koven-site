"""Check crawlability and canonical URLs in the artifact uploaded to Pages."""

import json
from collections import defaultdict, deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.meta = defaultdict(list)
        self.links = []
        self.assets = []
        self.modules = []
        self.title = ""
        self.main_text = ""
        self.schema = []
        self.section = ""
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "meta" and ("name" in attrs or "property" in attrs):
            self.meta[attrs.get("name") or attrs["property"]].append(attrs.get("content"))
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.meta["canonical"].append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") in {"stylesheet", "modulepreload"}:
            self.assets.append(attrs["href"])
        if tag == "script" and attrs.get("src"):
            self.assets.append(attrs["src"])
            if attrs.get("type") == "module":
                self.modules.append(attrs["src"])
        if tag in {"title", "main"}:
            self.section = tag
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.section = tag

    def handle_endtag(self, tag):
        if tag == self.section:
            self.section = ""

    def handle_data(self, data):
        if self.section == "title":
            self.title += data
        if self.section == "main":
            self.main_text += data
        if self.section == "script":
            self.schema.append(json.loads(data))


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def check(dist):
    xml = ElementTree.parse(dist / "sitemap.xml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locations = [node.text for node in xml.findall(f"{namespace}url/{namespace}loc")]
    require(xml.getroot().tag == namespace + "urlset" and locations, "Invalid or empty sitemap.xml")
    require(all(locations) and len(locations) == len(set(locations)), "Empty or duplicate sitemap URLs")
    canonicals = Page((dist / "index.html").read_text(encoding="utf-8")).meta["canonical"]
    require(len(canonicals) == 1 and canonicals[0], "Missing or duplicate homepage canonical")
    home = canonicals[0]
    origin = urlsplit(home)
    sitemap = urljoin(home, "sitemap.xml")
    robots = (dist / "robots.txt").read_text(encoding="utf-8").splitlines()
    require(f"Sitemap: {sitemap}" in robots, "Sitemap URL disagrees with robots.txt")
    require(origin.scheme == "https" and origin.netloc and origin.path.endswith("/"), "Invalid homepage canonical")

    def local_path(url):
        parts = urlsplit(url)
        if (parts.scheme, parts.netloc) == (origin.scheme, origin.netloc) and parts.path.startswith(origin.path):
            return dist / unquote(parts.path.removeprefix(origin.path))

    pages = set(locations)
    expected = {file.parent for file in dist.rglob("index.html")}
    actual_files = {local_path(url) for url in pages}
    require(len(actual_files) == len(pages) and actual_files == expected and home in pages,
            "Sitemap and static HTML differ")

    titles = set()
    graph = {}
    for url in pages:
        parts = urlsplit(url)
        require(parts.path.endswith("/") and not (parts.query or parts.fragment), f"Noncanonical sitemap URL: {url}")
        page = Page((local_path(url) / "index.html").read_text(encoding="utf-8"))
        require(page.title.strip() and page.title not in titles and page.main_text.strip(), f"Missing main content or unique title: {url}")
        titles.add(page.title)
        require(page.meta["canonical"] == [url] and page.meta["og:url"] == [url], f"Canonical mismatch: {url}")
        require(page.meta["robots"] == ["index, follow"], f"Non-indexable sitemap page: {url}")
        require(len(page.meta["description"]) == 1 and (page.meta["description"][0] or "").strip(), f"Missing description: {url}")
        images = page.meta["og:image"]
        require(len(images) == 1 and images[0] and page.meta["twitter:image"] == images, f"Share image mismatch: {url}")
        require(len(page.modules) == 1, f"Missing or duplicate app entry: {url}")
        require(len(page.schema) == (1 if url == home else 0), f"Unexpected homepage JSON-LD: {url}")
        if url == home:
            schema, = page.schema
            require(isinstance(schema, dict) and schema.get("@context") == "https://schema.org" and
                    isinstance(schema.get("@graph"), list), "Invalid homepage JSON-LD")
            require({node.get("@type") for node in schema["@graph"]
                     if isinstance(node, dict) and node.get("url") == home} == {"WebSite", "SoftwareSourceCode"},
                    "Homepage JSON-LD needs the canonical website and source-code entries")

        for asset in [*images, *page.assets]:
            file = local_path(urljoin(url, asset))
            require(file is not None and file.is_file(), f"Missing asset: {url} → {asset}")
        graph[url] = set()
        for href in page.links:
            link = urlsplit(urljoin(url, href))._replace(query="", fragment="").geturl()
            if (file := local_path(link)) is not None:
                require(link in pages if link.endswith("/") else file.is_file(), f"Broken internal link: {url} → {href}")
                if link in pages:
                    graph[url].add(link)

    visited, pending = {home}, deque([home])
    while pending:
        targets = graph[pending.popleft()] - visited
        visited.update(targets)
        pending.extend(targets)
    require(visited == pages, f"Pages unreachable from home: {sorted(pages - visited)}")
    for source in Path("public").glob("google*.html"):
        published = dist / source.name
        require(published.is_file() and published.read_bytes() == source.read_bytes(),
                f"Google verification file missing or changed: {source.name}")

    print(f"SEO artifact checks passed ({len(pages)} reachable pages)")


if __name__ == "__main__":
    check(Path("dist"))
