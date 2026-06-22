# 색인·SEO 운영 가이드

도메인: **https://bundang-massage1.pages.dev**

빌드 한 번이면 색인에 필요한 파일이 모두 생성됩니다.

```bash
python3 build.py
```

생성물:
- `sitemap.xml` — 색인 대상 44개 URL (lastmod·changefreq·priority 포함)
- `rss.xml` — RSS 2.0 피드 (색인 발견 가속, 네이버 서치어드바이저 RSS 제출용)
- `robots.txt` — 구글·빙·네이버(Yeti)·다음(Daumoa) 명시 허용 + sitemap/rss 안내
- `<INDEXNOW_KEY>.txt` — IndexNow 키 파일 (루트에서 접근 가능)
- 메인페이지 `<head>` — 네이버 사이트 소유확인 메타 자동 출력

---

## 1. 최초 1회 등록 (배포 후)

1. **네이버 서치어드바이저** (https://searchadvisor.naver.com)
   - 사이트 등록 → 메인페이지 메타 태그로 소유확인 (이미 삽입됨)
   - 요청 → 사이트맵 제출: `https://bundang-massage1.pages.dev/sitemap.xml`
   - 요청 → RSS 제출: `https://bundang-massage1.pages.dev/rss.xml`

2. **구글 서치 콘솔** (https://search.google.com/search-console)
   - 사이트 등록 (HTML 태그 방식이면 `content/site.py`의 `GOOGLE_SITE_VERIFICATION`에 입력 후 재빌드)
   - Sitemaps → `sitemap.xml` 제출
   - ※ 구글은 IndexNow 미참여. 개별 페이지는 "URL 검사 → 색인 생성 요청"으로 즉시 크롤 요청.

3. **빙 웹마스터** (https://www.bing.com/webmasters)
   - 구글 서치 콘솔에서 가져오기(import) 가능. IndexNow 키도 여기서 확인됩니다.

---

## 2. IndexNow — 빙·네이버 등에 즉시 통보

배포가 끝나(키 파일이 라이브 상태) 본 뒤 실행합니다.

```bash
# 전체 URL 일괄 통보 (최초 1회 / 대량 갱신 시)
python tools/indexnow.py

# 글/페이지 하나만 통보 (수정·신규 발행 때마다)
python tools/indexnow.py https://bundang-massage1.pages.dev/areas/jeongja-dong/

# 전송 없이 대상만 확인
python tools/indexnow.py --dry
```

IndexNow 파트너(빙·네이버·얀덱스·Seznam)에 한 번에 분배됩니다. HTTP 200/202면 정상 접수입니다.

---

## 3. 구글 즉시 색인 (선택 — Indexing API)

구글은 sitemap ping이 2023년 폐지되어 자동 ping이 동작하지 않습니다. 가장 빠른 방법은 서치 콘솔의
"색인 생성 요청"이며, 자동화가 필요하면 서비스 계정으로 Indexing API를 쓸 수 있습니다.

```bash
pip install google-auth requests
GOOGLE_APPLICATION_CREDENTIALS=service_account.json \
python tools/google_indexing.py https://bundang-massage1.pages.dev/areas/jeongja-dong/
```

준비: GCP에서 Indexing API 사용 설정 → 서비스 계정 키(JSON) 발급 → 서치 콘솔 속성에 서비스 계정
이메일을 '소유자'로 추가. 자세한 안내는 `tools/google_indexing.py` 상단 주석 참고.

---

## 글 올릴 때마다 (운영 루틴)

```bash
python3 build.py                                   # 1) 재빌드
git add -A && git commit -m "..." && git push      # 2) 배포(Cloudflare 자동)
python tools/indexnow.py <새 URL>                   # 3) 빙·네이버 즉시 통보
# 4) (선택) 구글 서치 콘솔에서 해당 URL "색인 생성 요청"
```
