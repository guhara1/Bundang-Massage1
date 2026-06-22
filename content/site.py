# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
# URL은 메인도메인 루트 기준의 짧고 깔끔한 구조를 사용합니다(깊은 경로 중첩 없음).
BASE_URL = "https://barogo-massage.com"

BRAND = "바로 GO"
BRAND_MARK = "Go"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 푸터 오렌지 버튼 — 텔레그램 링크
TELEGRAM_BUILD = "https://t.me/googleseolab"   # 웹사이트 제작문의
TELEGRAM_PARTNER = "https://t.me/googleseolab"  # 제휴문의

# 상단 메뉴 — 메뉴명·URL에는 "출장마사지"를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("분당 홈", "/", []),
    ("지역별 안내", "/areas/", [
        ("분당 전체", "/areas/"),
        ("분당동", "/areas/bundang-dong/"),
        ("수내동", "/areas/sunae-dong/"),
        ("정자동", "/areas/jeongja-dong/"),
        ("서현동", "/areas/seohyeon-dong/"),
        ("이매동", "/areas/imae-dong/"),
        ("야탑동", "/areas/yatap-dong/"),
        ("판교동", "/areas/pangyo-dong/"),
        ("삼평동", "/areas/sampyeong-dong/"),
        ("백현동", "/areas/baekhyeon-dong/"),
        ("금곡동", "/areas/geumgok-dong/"),
        ("구미동", "/areas/gumi-dong/"),
        ("운중동", "/areas/unjung-dong/"),
    ]),
    ("역세권 안내", "/stations/", [
        ("역 전체", "/stations/"),
        ("정자역", "/stations/jeongja-station/"),
        ("수내역", "/stations/sunae-station/"),
        ("서현역", "/stations/seohyeon-station/"),
        ("이매역", "/stations/imae-station/"),
        ("야탑역", "/stations/yatap-station/"),
        ("판교역", "/stations/pangyo-station/"),
        ("미금역", "/stations/migeum-station/"),
        ("오리역", "/stations/ori-station/"),
        ("동천역 인접", "/stations/dongcheon-nearby-area/"),
        ("보정역 인접", "/stations/bojeong-nearby-area/"),
        ("모란역 인접", "/stations/moran-nearby-area/"),
    ]),
    ("생활권 안내", "/zones/", [
        ("생활권 전체", "/zones/"),
        ("정자카페거리", "/zones/jeongja-cafe-street/"),
        ("서현역·AK플라자", "/zones/seohyeon-ak-plaza/"),
        ("야탑역·분당차병원", "/zones/yatap-cha-hospital/"),
        ("수내역·중앙공원", "/zones/sunae-central-park/"),
        ("판교역·테크노밸리", "/zones/pangyo-techno-valley/"),
        ("삼평동·테크노밸리", "/zones/sampyeong-techno-valley/"),
        ("백현동·판교역", "/zones/baekhyeon-pangyo/"),
        ("미금역·금곡동", "/zones/migeum-geumgok/"),
        ("오리역·구미동", "/zones/ori-gumi/"),
        ("운중동·서판교", "/zones/unjung-west-pangyo/"),
        ("이매역·탄천", "/zones/imae-tancheon/"),
        ("분당동·율동공원", "/zones/bundang-yuldong-park/"),
    ]),
    ("예약 안내", "/reservation/", [
        ("예약 가능 지역", "/reservation/#place"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("추가 이동비 안내", "/reservation/#travel"),
        ("결제 방식 안내", "/reservation/#payment"),
        ("예약 변경 안내", "/reservation/#change"),
        ("취소 기준 안내", "/reservation/#cancel"),
    ]),
    ("이용 전 확인사항", "/check/", [
        ("방문 가능 주소 확인", "/check/#address"),
        ("자택 이용 전 확인", "/check/#home"),
        ("숙소 이용 전 확인", "/check/#hotel"),
        ("오피스텔 이용 전 확인", "/check/#officetel"),
        ("사무실 인근 이용 전 확인", "/check/#office"),
        ("개인정보 처리 기준", "/check/#privacy"),
        ("고객 안전 안내", "/check/#safety"),
    ]),
    ("홈타이 이용 가이드", "/hometai-guide/", [
        ("홈타이란?", "/hometai-guide/#about"),
        ("출장마사지와 홈타이 차이", "/hometai-guide/#diff"),
        ("분당 홈타이 이용 기준", "/hometai-guide/#standard"),
        ("지역별 이동 기준", "/hometai-guide/#move"),
        ("추가 비용 확인 기준", "/hometai-guide/#cost"),
        ("처음 이용하는 고객 안내", "/hometai-guide/#first"),
    ]),
    ("고객센터", "/support/", [
        ("문의하기", "/support/#contact"),
        ("자주 묻는 질문", "/support/#faq"),
        ("운영 기준", "/support/#policy"),
        ("사이트 소개", "/about/"),
        ("개인정보 처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
