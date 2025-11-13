---
layout: post
title: "[Project] Rolling Paper — React 기반 UI·UX 구현기"
date: 2025-09-28 00:00:00 +0900
categories: [frontend, react]
tags: [react, teamwork, library, uiux, component, accessibility]
image: /assets/img/rollingpaper/main.png

---

## **1. 프로젝트 개요**
사용자가 메시지를 작성하고 공유할 수 있는 웹·앱 서비스로 UI·UX 플로우를 개선하고 <br />
공통 컴포넌트를 구현했으며, 접근성과 QA까지 진행했습니다.

![서비스 이미지](/assets/img/rollingpaper/project.png)


| 항목 | 내용 |
|------|------|
| **프로젝트명** | Rolling Paper |
| **유형** | 팀 프로젝트 |
| **기간** | 2025.09.25 ~ 2025.10.14 |
| **참여 인원** | 3명 |
| **역할** | 유저 플로우 개선, `/main` `/list` UI/UX 구현, 공통 컴포넌트 제작, 접근성 및 QA |
| **기술 스택** | React, Vite, SCSS, Swiper.js, React-Toastify |


## **2. 담당 역할 상세**
- Figma를 통해 프로토타입을 정리하고 사용자 흐름을 설계했습니다.
- 공통 컴포넌트(Button, Card, Toast, Header) 구축했습니다.
- 팀원이 작업한 컴포넌트를 Card의 props로 전달받아 데이터와 연결했습니다.
- Swiper.js와 React-Toastify를 프로젝트에 맞게 커스터마이징 했습니다.
- 리스트 GET API 함수로 데이터 불러오고 화면에 동적으로 렌더링했습니다.
- 라우터 세팅은 팀원이 했지만 페이지 연결을 직접 구현하며 구조를 이해했습니다.
- 시멘틱 마크업을 적용하여 접근성을 개선했습니다.
- `/main`, `/list` 페이지의 반응형 UI를 구현했습니다.
- 브라우저·디바이스별 QA 테스트를 수행했습니다.

## **3. 주요 구현 포인트**
- ### 3-1. Button 컴포넌트 - 재사용 가능한 UI 설계
  - 공통 Button 컴포넌트를 제작하여 라벨(label), 크기(size), 색상(variant), 아이콘(icon) 등을 <br />
  props로 제어할 수 있도록 설계했습니다. 이를 통해 다양한 화면에서도 동일한 버튼 스타일을 유지하고, <br />
  일관된 UI 시스템을 구축했습니다.

  - Button 스타일은 디자인 토큰 기반으로 구성했으며, 라운드 값·높이·타이포그래피 등은 SCSS 변수로 관리했습니다. <br />
  이를 통해 컴포넌트 간 일관성을 유지하고, 유지보수를 용이하게 했습니다.

전체 코드는 GitHub Repository
에서 확인 가능합니다.
```jsx
<Button label="보내기" variant="primary" size="lg" icon="send" />
<Button icon="add" size="sm" className="btn--icon-only" />
```

```scss
// 라운드 값 (공통 처리)
$radius-lg: 12px;
$radius-md: 6px;

// 버튼 높이 값 (공통 처리)
$btn-height-lg: 56px;
$btn-height-md: 40px;
$btn-height-sm: 36px;
$btn-height-xs: 28px;

// 버튼 기초 (공통 처리)
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  cursor: pointer;
  border-radius: $radius-lg;

  .btn__icon,
  .btn__label {
    display: inline-flex;
    align-items: center;
    white-space: nowrap;
  }
}

// 버튼 사이즈
.btn--lg {
  height: $btn-height-lg;
  padding: 0 24px;
  @include typo(18, 700);
}

.btn--md {
  height: $btn-height-md;
  padding: 0 16px;
  border-radius: $radius-md;
  @include typo(16, 400);
}
```

- ### 3-2. Swiper 라이브러리 적용 
 - Swiper.js를 활용해 **RollingCard** 컴포넌트를 슬라이드 형태로 렌더링했습니다.  
  - **커스텀 네비게이션 버튼(좌·우 화살표)** 과 애니메이션이 어색한 부분이 있지만  
  **반응형 breakpoints**를 셋팅했으며, 모바일·태블릿·PC 화면 크기별로 반응하는 카드 배치를 구현했습니다.  
  - 또한 `useRef`를 통해 Swiper 인스턴스와 DOM을 직접 연결하고,  
    `resize` 이벤트 리스너를 추가하여 리사이징 시에도 **현재 슬라이드 상태를 유지**하도록 처리했습니다.

{% raw %}
```jsx
import { useRef, useEffect } from "react";

// Swiper 컴포넌트 및 네비게이션/페이지네이션 모듈
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";

// Swiper 제공 CSS
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

// 프로젝트 내부 컴포넌트 및 스타일
import Icon from "./Icon";
import RollingCard from "./RollingCard";
import "./RollingSlider.scss";

function RollingSlider({ cards = [] }) {
  // Swiper 인스턴스 및 버튼 DOM 참조
  const swiperRef = useRef(null); // Swiper 인스턴스 저장
  const prevBtnRef = useRef(null); // 커스텀 왼쪽 버튼
  const nextBtnRef = useRef(null); // 커스텀 오른쪽 버튼

  // PC 기준 한 화면에 4개까지 보이므로, 카드가 4개 초과일 때만 버튼 표시
  const showNav = cards.length > 4;

  // 화면 좌우 값 리사이즈 시 Swiper 현재 페이지 유지 (리사이징 대응)
  useEffect(() => {
    const handleResize = () => {
      const swiper = swiperRef.current;
      if (!swiper) return;

      const currentIndex = swiper.activeIndex; // 현재 활성 페이지 저장
      swiper.update(); // 슬라이드 크기 및 위치 재갱신
      swiper.slideTo(currentIndex, 0); // 같은 페이지로 복귀 (즉시 이동)

      // 네비/페이지네이션 상태도 최신으로 동기화
      if (swiper.navigation && swiper.navigation.update) {
        swiper.navigation.update();
      }
      if (swiper.pagination && swiper.pagination.update) {
        swiper.pagination.update();
      }
    };

    // 컴포넌트가 처음 실행할 때 resize 이벤트를 등록하고 사라질 때 자동으로 해제함
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="rolling-slider">
      {/* Swiper : 카드들을 슬라이드 형태로 보여주는 영역 */}
      <Swiper
        // onSwiper 콜백 : swiper 초기화 직 후 한번 실행됨
        // swiper 인스턴스를 ref에 저장해 다른 곳에서 제어할 수 있음
        onSwiper={(swiper) => {
          swiperRef.current = swiper;

          //DOM이 랜더링 된 후 연결된 버튼 ref가 유효할 수 있도록 setTimeout 사용
          //랜더 직후에는 ref.current가 아직 null일 가능성 있음
          setTimeout(() => {
            //swiper 네비게이션 버튼 DOM 연결
            swiper.params.navigation.prevEl = prevBtnRef.current;
            swiper.params.navigation.nextEl = nextBtnRef.current;

            //네비게이션 기능 초기화 및 상태 업데이트
            swiper.navigation.init();
            swiper.navigation.update();
          }, 100);
        }}
        //사용 모듈 설정
        modules={[Navigation, Pagination]}
        // 기본 동작 및 옵션 설정
        centerInsufficientSlides={false}
        observer={true}
        observeParents={true}
        slidesPerGroupSkip={0}
        pagination={{ clickable: true }}
        spaceBetween={16}
        speed={700}
        loop={false}
        loopFillGroupWithBlank={true}
        slidesPerGroup={1}
        watchOverflow={true}
        resistanceRatio={0}
        edgeSwipeDetection={true}
        allowTouchMove={true}
        // 반응형 구간별 한 화면 카드 수 설정
        breakpoints={{
          360: { slidesPerView: 1.1, spaceBetween: 10 },
          640: { slidesPerView: 2.0, spaceBetween: 18 },
          1024: { slidesPerView: 3.1, spaceBetween: 20 },
          1280: { slidesPerView: 4.0, spaceBetween: 20 },
        }}
      >
        {/* 카드 리스트 렌더링 */}
        {cards.map((card) => (
          <SwiperSlide key={card.id}>
            <RollingCard {...card} />
          </SwiperSlide>
        ))}
      </Swiper>

      {/* 카드가 한 화면에 다 들어가지 않을 때만 버튼 표시 */}
      {showNav && (
        <>
          <div ref={prevBtnRef} className="custom-prev">
            <Icon name="arrowLeft" size={50} />
          </div>
          <div ref={nextBtnRef} className="custom-next">
            <Icon name="arrowRight" size={50} />
          </div>
        </>
      )}
    </div>
  );
}

export default RollingSlider;
```
{% endraw %}


## 4. 구현 결과 시각 자료 
### 4-1. Figma 시안과 실제 구현 비교

| 항목 | Figma 시안 | 실제 구현 |
|------|-------------|-----------|
| **메인 페이지** | <img src="/assets/img/rollingpaper/figma-list.png" width="400"/> | <img src="/assets/img/rollingpaper/list.png" width="300"/> |
| **리스트 페이지** | <img src="/assets/img/rollingpaper/figma-list.png" width="400"/> | <img src="/assets/img/rollingpaper/list.png" width="400"/> |


###  4-2. 공통 컴포넌트 재사용성 예시

```jsx
<Button label="보내기" variant="primary" size="lg" icon="send" />
<Button label="취소" variant="secondary" size="md" />
<Button icon="add" size="sm" className="btn--icon-only" />
일한 Button 컴포넌트를 props만 변경하여 다양한 UI에서 재사용했습니다.
공통 토큰(색상, 라운드, 타이포)을 기반으로 일관성 있는 디자인 시스템을 유지했습니다.

  ### 4-3. Swiper & Toastify 적용 결과
기능	설명	미리보기
Swiper 슬라이드	반응형 Breakpoints + 커스텀 네비게이션 버튼 연결	

Toast 알림	React-Toastify를 프로젝트에 맞게 커스터마이징	

useRef를 활용해 DOM을 직접 제어하고,
반응형 설정으로 화면 크기별 UI 변화를 자연스럽게 처리했습니다.
사용자 행동에 즉시 피드백을 제공하기 위해 Toastify를 커스터마이징했습니다.

🔗 4-4. API 연동 전/후 비교
상태	화면
로딩 전 (Empty State)	

데이터 로드 후 (List State)	

GET API로 서버 데이터를 불러와 props로 전달하고,
상태에 따라 로딩/빈 화면/데이터 렌더링을 구분했습니다.
데이터 흐름을 명확히 하기 위해 컴포넌트 props 구조를 통일했습니다.

📱 4-5. 반응형 & 접근성 구현
항목	PC	Mobile
메인 화면	
	

리스트 화면	
	

시멘틱 마크업(<header>, <main>, <button>)을 적용하여 접근성을 확보했습니다.
미디어 쿼리와 SCSS 믹스인을 활용해 디바이스별 UI 크기와 간격을 최적화했습니다.

5. 프로젝트 회고

Figma로 설계한 사용자 여정을 React 구조로 옮기는 과정에서
UI 설계와 코드 구조의 연결을 명확히 이해할 수 있었습니다.

Button, Card 등 공통 컴포넌트를 직접 설계·구현하면서
디자인 시스템의 일관성과 재사용성의 중요성을 체감했습니다.

Swiper와 Toastify 등 외부 라이브러리를 단순히 적용하는 데서 그치지 않고,
프로젝트 요구에 맞게 커스터마이징하며 유지보수성을 높였습니다.

접근성과 QA 과정을 통해 사용자 중심의 인터페이스 품질 관리 경험을 쌓았습니다.

💬 한줄 요약:
“UI/UX 설계부터 실제 코드 구현, 테스트까지 전 과정을 직접 주도한 팀 프로젝트였습니다.”