# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
from .site import BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_FAQ = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "분당 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내에서 정자동, 서현동, 야탑동, 판교동, 수내동 등 대표동 기준으로 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "정자역이나 판교역 근처도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "정자역, 서현역, 야탑역, 판교역, 미금역 등 주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "정자1동, 수내2동처럼 숫자 동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "정자1~3동은 정자동, 수내1~3동은 수내동처럼 대표동 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "운중동, 구미동처럼 외곽 지역도 방문되나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "운중동·서판교, 구미동·오리역 인접 생활권도 방문 범위입니다. 차량 이동 기준과 추가 이동비는 예약 시 위치를 기준으로 안내합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "당일 예약도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 분당구 전지역</p>
    <h1>분당 출장마사지·분당 홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 프리미엄 방문 관리.<br>정자·서현·야탑·판교·미금 생활권 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/reservation/">예약 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>12개</strong><span>대표 지역</span></li>
      <li><strong>11개</strong><span>역세권 안내</span></li>
      <li><strong>12개</strong><span>생활권 안내</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="standard">
<h2>분당에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>
<p>분당 출장마사지를 찾는 분들은 보통 현재 위치가 정자동, 서현동, 야탑동, 판교동, 수내동, 미금역 주변 중 어디에 가까운지 먼저 확인합니다. 분당은 성남시 안에서도 생활권이 뚜렷하게 나뉘는 지역입니다. 정자동은 정자역과 카페거리, 수내동은 수내역과 중앙공원, 서현동은 서현역과 중심상권, 야탑동은 야탑역과 분당차병원, 판교는 판교역과 테크노밸리 생활권으로 구분됩니다. 그래서 이 사이트는 "분당 전지역 가능"만 적는 방식 대신, 대표동과 역세권을 나누어 안내하는 구조로 만들었습니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차에 따라 진행하며, 처음 이용하시는 분도 위치와 시간만 정하면 어렵지 않게 예약할 수 있도록 각 단계를 안내해 드립니다.</p>
</section>

<section id="vibe">
<h2>정자·서현·야탑·판교·미금 생활권 차이</h2>
<p>같은 분당이라도 동마다 분위기와 생활 리듬이 다릅니다. <a href="/areas/jeongja-dong/">정자동 출장마사지</a>는 정자역과 카페거리, 오피스텔 생활권이 함께 연결되는 분당의 대표 생활권입니다. <a href="/areas/sunae-dong/">수내동 출장마사지</a>는 중앙공원과 분당구청 인접의 핵심 주거권, <a href="/areas/seohyeon-dong/">서현동 출장마사지</a>는 AK플라자와 로데오거리 중심상권입니다. <a href="/areas/yatap-dong/">야탑동 출장마사지</a>는 분당차병원과 성남종합버스터미널 인접권, 판교권은 <a href="/areas/pangyo-dong/">판교동</a>·<a href="/areas/sampyeong-dong/">삼평동</a>·<a href="/areas/baekhyeon-dong/">백현동</a>이 판교역과 테크노밸리 검색 의도를 역할별로 나눠 담당합니다. 본인 생활권과 가까운 페이지를 먼저 확인하시면 방문 조건이 더 또렷하게 보입니다.</p>
</section>

<section id="areas">
<h2>대표동별 방문 가능 지역 안내</h2>
<p>지역별 안내는 분당구 대표동 기준으로 구성됩니다. 정자1~3동, 수내1~3동, 서현1·2동, 이매1·2동, 야탑1~3동, 구미동·구미1동처럼 숫자로 나뉜 행정동은 개별 페이지를 만들지 않고 각 대표동 페이지에서 통합해 안내합니다. 같은 생활권을 잘게 쪼개 비슷한 내용을 반복하기보다, 동 단위로 묶어 생활권 특징과 방문 조건을 한 번에 설명하는 편이 더 정확하기 때문입니다.</p>
<ul class="card-grid">
<li><a href="/areas/jeongja-dong/">정자동</a></li>
<li><a href="/areas/sunae-dong/">수내동</a></li>
<li><a href="/areas/seohyeon-dong/">서현동</a></li>
<li><a href="/areas/yatap-dong/">야탑동</a></li>
<li><a href="/areas/pangyo-dong/">판교동</a></li>
<li><a href="/areas/sampyeong-dong/">삼평동</a></li>
<li><a href="/areas/baekhyeon-dong/">백현동</a></li>
<li><a href="/areas/geumgok-dong/">금곡동</a></li>
<li><a href="/areas/gumi-dong/">구미동</a></li>
<li><a href="/areas/unjung-dong/">운중동</a></li>
<li><a href="/areas/imae-dong/">이매동</a></li>
<li><a href="/areas/bundang-dong/">분당동</a></li>
</ul>
<p>분당 전체 구조가 궁금하시면 <a href="/areas/">지역별 안내</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>정자역·서현역·야탑역·판교역 역세권 안내</h2>
<p>역세권 페이지는 분당 지역 안내에서 중요한 역할을 합니다. <a href="/stations/jeongja-station/">정자역 출장마사지</a>, <a href="/stations/seohyeon-station/">서현역 출장마사지</a>, <a href="/stations/yatap-station/">야탑역 출장마사지</a>, <a href="/stations/pangyo-station/">판교역 출장마사지</a>, <a href="/stations/migeum-station/">미금역 출장마사지</a>처럼 실제 검색 의도와 가까운 기준으로 정리했습니다. 다만 환승역을 노선별로 나누거나 출구별 페이지를 만들면 중복 위험이 크므로, 정자역·판교역·미금역도 역명 기준 1개 페이지만 운영합니다.</p>
<ul class="card-grid">
<li><a href="/stations/jeongja-station/">정자역</a></li>
<li><a href="/stations/sunae-station/">수내역</a></li>
<li><a href="/stations/seohyeon-station/">서현역</a></li>
<li><a href="/stations/imae-station/">이매역</a></li>
<li><a href="/stations/yatap-station/">야탑역</a></li>
<li><a href="/stations/pangyo-station/">판교역</a></li>
<li><a href="/stations/migeum-station/">미금역</a></li>
<li><a href="/stations/ori-station/">오리역</a></li>
</ul>
<p>동천역·보정역·모란역 인접 생활권은 <a href="/stations/">역세권 안내</a>에서 분당 기준 이동 안내로 확인하실 수 있습니다.</p>
</section>

<section id="zones">
<h2>생활권으로 위치 찾기</h2>
<p>생활권 페이지는 사용자가 본인 위치를 더 쉽게 찾도록 돕습니다. <a href="/zones/jeongja-cafe-street/">정자카페거리</a>, <a href="/zones/seohyeon-ak-plaza/">서현역·AK플라자</a>, <a href="/zones/pangyo-techno-valley/">판교역·판교테크노밸리</a>, <a href="/zones/sunae-central-park/">수내역·중앙공원</a>, <a href="/zones/yatap-cha-hospital/">야탑역·분당차병원</a>처럼 익숙한 거점을 기준으로 안내합니다. 전체 목록은 <a href="/zones/">생활권 안내</a>에서 확인하세요.</p>
</section>

<section id="check">
<h2>분당 홈타이 예약 전 확인사항</h2>
<p>분당 출장마사지·분당 홈타이 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 개인정보 처리 기준을 먼저 확인하는 것이 좋습니다. 정자역, 서현역, 야탑역처럼 접근성이 좋은 지역도 있지만 운중동, 분당동, 구미동 일부는 시간대에 따라 차량 이동 기준이 달라질 수 있습니다. 분당 홈타이는 자택, 숙소, 오피스텔, 사무실 인근에서 예약 가능 여부를 확인한 뒤 이용하는 방문형 관리 서비스입니다. 자세한 기준은 <a href="/reservation/">예약 안내</a>와 <a href="/check/">이용 전 확인사항</a>, <a href="/hometai-guide/">홈타이 이용 가이드</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="dedup">
<h2>분당 페이지 중복 방지 운영 기준</h2>
<p>분당 홈타이 사이트를 만들 때 중요한 부분은 번호 동을 무리하게 쪼개지 않는 것입니다. 수내1동, 수내2동, 수내3동을 각각 개별 페이지로 만들면 본문이 비슷해질 위험이 큽니다. 정자1동, 정자2동, 정자3동도 마찬가지입니다. 그래서 수내동, 정자동, 서현동, 이매동, 야탑동처럼 대표동으로 통합하고, 각 페이지 안에서 세부 생활권을 설명합니다. 또한 정자동 페이지와 정자역 페이지는 같은 본문을 쓰지 않고, 판교동·삼평동·백현동은 판교 키워드를 반복하지 않고 역할을 나눕니다. 이렇게 구성하면 출장마사지와 홈타이 키워드를 포함하면서도 중복 콘텐츠 위험을 줄일 수 있습니다. 사이트의 작성·검수 원칙은 <a href="/about/">사이트 소개</a>에서 공개합니다.</p>
</section>

<section id="how">
<h2>분당 출장마사지 사이트 이용 방법</h2>
<p>메인페이지는 분당 전체 안내를 담당하고, 대표동 페이지는 정자동, 수내동, 서현동, 야탑동, 판교동, 금곡동, 구미동 같은 세부 검색을 담당합니다. 역세권 페이지는 정자역, 서현역, 야탑역, 판교역, 미금역처럼 실제 검색 수요가 생길 수 있는 위치를 담당하고, 생활권 페이지는 정자카페거리, 서현역, 판교테크노밸리, 미금역, 오리역, 서판교처럼 위치를 더 쉽게 찾도록 보조합니다. 거주하시거나 머무시는 위치와 가까운 페이지를 골라 방문 조건을 확인하신 뒤, 위치와 희망 시간을 정해 전화 주시면 가능 여부를 바로 안내해 드립니다.</p>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>분당 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "분당 출장마사지｜정자·서현·야탑·판교 홈타이 지역 안내",
    "desc": "분당 출장마사지·홈타이 예약 전 정자동, 서현동, 야탑동, 판교동, 수내동 생활권을 확인하세요.",
    "h1": "분당 출장마사지 · 분당 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _FAQ,
    "breadcrumb": [],
    "hero": _HERO,
}
