"""Check generated pages and their local links without external dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links, self.errors = path, set(), [], []
        self.headings = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate id: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.headings += 1
        if tag == "img" and not attrs.get("alt"):
            self.errors.append("Image missing alternative text")
        if tag == "a" and attrs.get("target") == "_blank":
            if "noopener" not in attrs.get("rel", "").split():
                self.errors.append("External window link missing noopener")
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


pages = [Page(ROOT / "index.html")]
pages += [Page(path) for path in sorted((ROOT / "projects").glob("*.html"))]
assert len(pages) == 7, "Expected a home page and six project pages"
by_path = {page.path.resolve(): page for page in pages}
errors = []
checked = 0
for page in pages:
    if page.headings != 1:
        page.errors.append("Expected exactly one h1")
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (page.path.parent / unquote(url.path)).resolve() if url.path else page.path.resolve()
        if not target.is_file():
            page.errors.append(f"Missing local file: {link}")
        elif url.fragment and target in by_path and unquote(url.fragment) not in by_path[target].ids:
            page.errors.append(f"Missing section: {link}")
        checked += 1
    errors += [f"{page.path.relative_to(ROOT)}: {error}" for error in page.errors]
if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS: {len(pages)} pages, {checked} local links/assets, headings and image labels.")
