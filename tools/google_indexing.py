#!/usr/bin/env python3
"""구글 색인 통보 도우미.

구글은 IndexNow에 참여하지 않습니다. 구글 색인을 가장 빠르게 받는 방법은 두 가지입니다.

1) (권장) Google Search Console
   - 사이트 등록 후 sitemap.xml 제출:  https://search.google.com/search-console
   - 개별 URL은 "URL 검사 → 색인 생성 요청" 으로 즉시 크롤 요청.
   - 별도 키/서버 코드가 필요 없고 가장 안정적입니다.

2) Indexing API (서비스 계정 필요)
   - 공식적으로는 JobPosting / BroadcastEvent 대상이지만 일반 URL도 크롤 큐에 들어갑니다.
   - 준비물: GCP 프로젝트 → Indexing API 사용 설정 → 서비스 계정 키(JSON)
            → Search Console 속성에 서비스 계정 이메일을 '소유자'로 추가.
   - 아래 함수는 google-auth, requests 설치 시 동작합니다.
       pip install google-auth requests
       GOOGLE_APPLICATION_CREDENTIALS=service_account.json \
       python tools/google_indexing.py https://<도메인>/<URL>/

참고: 구글 sitemap ping 엔드포인트(/ping?sitemap=)는 2023년 폐지되어 더 이상 동작하지 않습니다.
따라서 자동 ping 대신 Search Console 제출 또는 Indexing API를 사용하세요.
"""
import sys


def notify(urls):
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("google-auth 가 필요합니다:  pip install google-auth requests")

    import os
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path:
        sys.exit("환경변수 GOOGLE_APPLICATION_CREDENTIALS 에 서비스 계정 JSON 경로를 지정하세요.")

    scopes = ["https://www.googleapis.com/auth/indexing"]
    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=scopes)
    session = AuthorizedSession(creds)
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    for u in urls:
        body = {"url": u, "type": "URL_UPDATED"}
        r = session.post(endpoint, json=body, timeout=30)
        print(f"{u} -> HTTP {r.status_code}")
        if r.status_code != 200:
            print("   ", r.text)


if __name__ == "__main__":
    targets = sys.argv[1:]
    if not targets:
        sys.exit("사용법: python tools/google_indexing.py <URL> [<URL> ...]")
    notify(targets)
