#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 스크립트.

sitemap.xml 의 모든 URL(또는 인자로 받은 URL)을 IndexNow 엔드포인트에 한 번에 통보한다.
IndexNow 파트너인 Microsoft Bing, Naver, Yandex, Seznam 등에 동시에 전달된다.
(구글은 IndexNow 미참여 — 구글은 tools/google_indexing.py 또는 Search Console 사용)

사용법:
    python tools/indexnow.py                 # sitemap.xml 의 전체 URL 일괄 통보
    python tools/indexnow.py https://.../a/  # 특정 URL만 통보(글 올릴 때마다)
    python tools/indexnow.py --dry           # 전송 없이 대상만 출력

키 파일은 빌드 시 루트에 <KEY>.txt 로 생성되어 https://<도메인>/<KEY>.txt 에서 접근 가능해야 한다.
"""
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

SITE = BASE_URL.rstrip("/")
HOST = SITE.split("://", 1)[-1]
KEY_LOCATION = f"{SITE}/{INDEXNOW_KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"  # 파트너 엔진에 자동 분배
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 python3 build.py 를 실행하세요.")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(path)
    return [loc.text.strip() for loc in tree.findall(".//s:loc", ns)]


def submit(urls):
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode("utf-8", "ignore")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    urls = args if args else sitemap_urls()
    if not urls:
        sys.exit("통보할 URL이 없습니다.")
    print(f"대상 {len(urls)}개 URL → IndexNow ({HOST})")
    for u in urls:
        print("  ", u)
    if dry:
        print("\n--dry: 전송하지 않았습니다.")
        return
    # IndexNow 는 1회 요청당 최대 10,000 URL
    for i in range(0, len(urls), 10000):
        status, body = submit(urls[i:i + 10000])
        print(f"\n응답: HTTP {status}")
        if body.strip():
            print(body)
    print("\n완료. 200/202 이면 정상 접수입니다.")


if __name__ == "__main__":
    main()
