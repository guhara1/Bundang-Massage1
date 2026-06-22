# 공통 이용 기준 블록 — 메인·지역·역·생활권 페이지 공용 컴포넌트.
# class="pricing" 래퍼는 빌드의 본문 글자수 측정에서 제외되므로(페이지 고유성 보호),
# 페이지마다 반복되는 신뢰 안내(예약 기준·추가 이동비·결제·취소)는 이 블록에 모은다.
from .site import PHONE, PHONE_DISPLAY

PRICING = f"""
<section class="pricing">
<h2>예약 전 공통 확인사항</h2>
<p class="pricing-lead">모든 지역에 공통으로 적용되는 예약 기준입니다. 숨은 비용 없이 예약 시 총액으로 먼저 안내합니다.</p>
<div class="price-grid">
  <div class="price-card">
    <p class="price-name">방문 가능 지역</p>
    <p class="price-time">예약 시 위치 기준 확인</p>
    <p class="price-desc">자택·숙소·오피스텔·사무실 인근 방문 가능 여부를 위치로 확인합니다.</p>
  </div>
  <div class="price-card featured">
    <p class="price-badge">기준</p>
    <p class="price-name">예약 가능 시간</p>
    <p class="price-time">상담 24시간 · 배정 시간대별 확인</p>
    <p class="price-desc">피크 시간대와 주말은 여유를 두고 연락 주시면 대기 없이 안내됩니다.</p>
  </div>
  <div class="price-card">
    <p class="price-name">추가 이동비·결제</p>
    <p class="price-time">예약 시 총액 안내</p>
    <p class="price-desc">지역·시간대·이동 거리에 따른 기준을 예약 확정 시 함께 안내합니다.</p>
  </div>
</div>
<p class="price-note">방문 가능 여부와 추가 이동비 기준은 <a href="/reservation/#travel">예약 안내</a>에서 확인하세요. 전화 예약 <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></p>
</section>
"""
