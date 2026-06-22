#!/usr/bin/env python3
"""바로 GO — 분당 출장마사지·홈타이 안내 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 메타 디스크립션 80자 초과 시 경고
  - 모든 페이지에 WebPage·BreadcrumbList·Organization·ImageObject 스키마 자동 주입
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, BRAND_MARK, NAV, PHONE, PHONE_DISPLAY,
                          TELEGRAM_BUILD, TELEGRAM_PARTNER,
                          NAVER_SITE_VERIFICATION, GOOGLE_SITE_VERIFICATION,
                          INDEXNOW_KEY, SITE_TITLE, SITE_DESC)
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000
MAX_DESC_CHARS = 80
SITE = BASE_URL.rstrip("/")
OG_IMAGE = f"{SITE}/assets/og-image.png"


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 안내 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def render_schema(page: dict, canonical: str) -> str:
    """모든 페이지에 공통 적용되는 구조화 데이터(@graph).
    WebSite·Organization·WebPage·BreadcrumbList·ImageObject 포함.
    실제 오프라인 사업장 주소가 없는 방문형 서비스이므로 LocalBusiness는 사용하지 않는다."""
    title = page["title"]
    desc = page["desc"]
    crumbs = page.get("breadcrumb") or []

    image_node = {
        "@type": "ImageObject",
        "@id": f"{SITE}/#primaryimage",
        "url": OG_IMAGE,
        "contentUrl": OG_IMAGE,
        "width": 1200,
        "height": 630,
        "caption": f"{BRAND} — 분당 출장마사지·홈타이 안내",
    }
    org_node = {
        "@type": "Organization",
        "@id": f"{SITE}/#org",
        "name": BRAND,
        "url": f"{SITE}/",
        "telephone": PHONE,
        "image": {"@id": f"{SITE}/#primaryimage"},
        "logo": {"@id": f"{SITE}/#primaryimage"},
        "areaServed": {"@type": "AdministrativeArea", "name": "경기도 성남시 분당구"},
        "sameAs": [TELEGRAM_BUILD],
    }
    website_node = {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": BRAND,
        "inLanguage": "ko",
        "publisher": {"@id": f"{SITE}/#org"},
    }
    webpage_node = {
        "@type": "WebPage",
        "@id": f"{canonical}#webpage",
        "url": canonical,
        "name": title,
        "description": desc,
        "inLanguage": "ko",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "primaryImageOfPage": {"@id": f"{SITE}/#primaryimage"},
        "about": {"@id": f"{SITE}/#org"},
    }
    graph = [website_node, org_node, image_node, webpage_node]

    # BreadcrumbList
    items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": f"{SITE}/"}]
    pos = 2
    for label, href in crumbs:
        entry = {"@type": "ListItem", "position": pos, "name": label}
        if href:
            entry["item"] = SITE + href
        else:
            entry["item"] = canonical
        items.append(entry)
        pos += 1
    if crumbs:
        graph.append({
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumb",
            "itemListElement": items,
        })
        webpage_node["breadcrumb"] = {"@id": f"{canonical}#breadcrumb"}

    data = {"@context": "https://schema.org", "@graph": graph}
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = SITE + "/" + path
    schema = render_schema(page, canonical)

    # 사이트 소유확인 메타 — 메인페이지(루트)에만 출력
    verify = ""
    if path == "":
        if NAVER_SITE_VERIFICATION:
            verify += f'<meta name="naver-site-verification" content="{NAVER_SITE_VERIFICATION}">\n'
        if GOOGLE_SITE_VERIFICATION:
            verify += f'<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">\n'

    page_head = hero if hero else ""
    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
{verify}<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 업데이트" href="{SITE}/rss.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0b0e15">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{schema}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">{BRAND_MARK}</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 분당구 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">전화예약</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">분당구 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">상호</span> {BRAND}</span>
        <span class="footer-contact-row"><span class="footer-label">전화예약</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 경기도 성남시 분당구 전지역</span>
      </address>
      <div class="footer-inquiry">
        <a class="footer-btn-orange" href="{TELEGRAM_BUILD}" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
        <a class="footer-btn-orange" href="{TELEGRAM_PARTNER}" target="_blank" rel="noopener nofollow">제휴문의 ↗</a>
      </div>
    </div>
    <nav class="footer-col" aria-label="지역 안내">
      <p class="footer-title">지역 안내</p>
      <ul>
        <li><a href="/areas/">지역별 안내</a></li>
        <li><a href="/stations/">역세권 안내</a></li>
        <li><a href="/zones/">생활권 안내</a></li>
        <li><a href="/areas/jeongja-dong/">정자동</a></li>
        <li><a href="/areas/pangyo-dong/">판교동</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/check/">이용 전 확인사항</a></li>
        <li><a href="/hometai-guide/">홈타이 이용 가이드</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">사이트 소개</a></li>
        <li><a href="/support/privacy/">개인정보 처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/check/#safety">고객 안전 안내</a></li>
        <li><a href="/check/#privacy">개인정보 처리 기준</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">전화 예약</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    sitemap_urls = []
    rss_entries = []
    warnings = []
    seen = set()

    for page in PAGES:
        path = page["path"]  # "" 또는 "areas/jeongja-dong/" 형태
        if path in seen:
            warnings.append(f"중복 경로: /{path}")
        seen.add(path)

        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        desc_len = len(page["desc"])
        if desc_len > MAX_DESC_CHARS:
            warnings.append(f"디스크립션 {desc_len}자(80자 초과): /{path}")

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            sitemap_urls.append(SITE + "/" + path)
            rss_entries.append((path, page["title"], page["desc"]))
        report.append((path or "/", chars, desc_len, "noindex" if noindex else "index"))

    now = datetime.now(timezone.utc)
    lastmod = now.strftime("%Y-%m-%d")
    rfc822 = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    # sitemap.xml (lastmod 포함 — 색인 갱신 신호)
    urls = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{lastmod}</lastmod>"
        f"<changefreq>weekly</changefreq>"
        f"<priority>{'1.0' if u.rstrip('/') == SITE else '0.8'}</priority></url>"
        for u in sitemap_urls
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml (RSS 2.0 — 색인 발견 가속 + 네이버 서치어드바이저 피드)
    items = []
    for path, title, desc in rss_entries:
        loc = SITE + "/" + path
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(title)}</title>\n"
            f"      <link>{loc}</link>\n"
            f"      <guid isPermaLink=\"true\">{loc}</guid>\n"
            f"      <description>{html.escape(desc)}</description>\n"
            f"      <pubDate>{rfc822}</pubDate>\n"
            "    </item>"
        )
    rss_items = "\n".join(items)
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{html.escape(SITE_TITLE)}</title>\n"
            f"    <link>{SITE}/</link>\n"
            f'    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>\n'
            f"    <description>{html.escape(SITE_DESC)}</description>\n"
            "    <language>ko</language>\n"
            f"    <lastBuildDate>{rfc822}</lastBuildDate>\n"
            f"{rss_items}\n"
            "  </channel>\n</rss>\n"
        )

    # robots.txt — 주요 봇 명시 허용 + sitemap/rss 안내
    robots = [
        "User-agent: *",
        "Allow: /",
        "",
        "# 검색 로봇 명시 허용 (구글·빙·네이버·다음)",
        "User-agent: Googlebot", "Allow: /",
        "User-agent: Bingbot", "Allow: /",
        "User-agent: Yeti", "Allow: /",          # 네이버
        "User-agent: Daumoa", "Allow: /",        # 다음(카카오)
        "",
        f"Sitemap: {SITE}/sitemap.xml",
        f"Sitemap: {SITE}/rss.xml",
    ]
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(robots) + "\n")

    # IndexNow 키 파일 — https://<도메인>/<KEY>.txt 에서 접근 가능해야 함
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  DESC  ROBOTS")
    for p, c, d, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2700) else "  ⚠CHARS"
        dflag = "" if d <= MAX_DESC_CHARS else "  ⚠DESC"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {str(d).rjust(4)}  {r}{flag}{dflag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")
    if warnings:
        print("\n경고:")
        for w in warnings:
            print(" -", w)


if __name__ == "__main__":
    build()
