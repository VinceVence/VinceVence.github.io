#!/usr/bin/env python3
"""Validate Guwa's static website without external dependencies."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "index.html": "https://guwa.app/",
    "privacy/index.html": "https://guwa.app/privacy/",
    "support/index.html": "https://guwa.app/support/",
    "account-deletion/index.html": "https://guwa.app/account-deletion/",
    "play-assets/index.html": "https://guwa.app/play-assets/",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.assets: list[str] = []
        self.images_without_alt: list[str] = []
        self.canonical: str | None = None
        self.description: str | None = None
        self.title_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag in {"img", "script"} and values.get("src"):
            self.assets.append(values["src"] or "")
        if tag == "link" and values.get("href"):
            href = values["href"] or ""
            self.assets.append(href)
            if values.get("rel") == "canonical":
                self.canonical = href
        if tag == "meta" and values.get("name") == "description":
            self.description = values.get("content")
        if tag == "img" and "alt" not in values:
            self.images_without_alt.append(values.get("src") or "<unknown>")
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)


def local_target(raw_url: str) -> Path | None:
    parsed = urlparse(raw_url)
    if parsed.scheme or parsed.netloc or raw_url.startswith(("#", "mailto:")):
        return None
    path = unquote(parsed.path)
    if not path.startswith("/"):
        return None
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target /= "index.html"
    return target


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    require((ROOT / "CNAME").read_text().strip() == "guwa.app", "CNAME must be exactly guwa.app", errors)

    for relative, canonical in PAGES.items():
        path = ROOT / relative
        require(path.is_file(), f"Missing page: {relative}", errors)
        if not path.is_file():
            continue

        source = path.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(source)

        require("".join(parser.title_parts).strip() != "", f"Missing title: {relative}", errors)
        require(parser.description is not None, f"Missing meta description: {relative}", errors)
        require(parser.canonical == canonical, f"Wrong canonical in {relative}: {parser.canonical}", errors)
        require(not parser.images_without_alt, f"Images without alt in {relative}: {parser.images_without_alt}", errors)
        require("support@questle.org" not in source, f"Old support email in {relative}", errors)
        require("https://questle.org" not in source, f"Old canonical/public URL in {relative}", errors)

        for raw_url in parser.links + parser.assets:
            target = local_target(raw_url)
            if target is not None:
                require(target.exists(), f"Broken local target in {relative}: {raw_url}", errors)

    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    require("GUWAFOUNDERPASS2026" in homepage, "Founder Pass code missing", errors)
    require('data-copy-code="GUWAFOUNDERPASS2026"' in homepage, "Copy Code control missing", errors)
    require("com.vincevence.questle" in homepage, "Existing Play package URL changed", errors)

    css = (ROOT / "assets/css/guwa.css").read_text(encoding="utf-8").lower()
    for color in ("#6467d9", "#343779", "#e9eafb", "#f48b74", "#d9a64e", "#171b2d"):
        require(color in css, f"Approved palette color missing: {color}", errors)
    require('font-family: "sora"' in css, "Sora typography missing", errors)

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for canonical in list(PAGES.values())[:4]:
        require(canonical in sitemap, f"Sitemap missing {canonical}", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Guwa website verification passed for {len(PAGES)} pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
