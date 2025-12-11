---
layout: post
title: "[셀프스터디] Tailwind v4"
date: 2025-09-12 00:00:00 +0900
categories: [frontend, javascript]
tags: [tailwind, design-system, css, design-tokens, typography, ui]
series: "셀프스터디"
image: /assets/img/thumbnail/self-study.png
render_with_liquid: false
---

## **Tailwind v4가 혁신적인 이유**

### **1) v3 ➡ v4 : 토큰 구조의 변화**
- v4는 **디자인 토큰을 JS 객체가 아닌 CSS 변수 기반**으로 완전히 재설계했다.  
- 색상·폰트·간격 등 모든 값이 CSS 변수로 관리되며 UI가 자동으로 연결되고 디자인 시스템 구축 속도와 유지보수성이 압도적으로 향상된다.
- config에서는 CSS 변수로 정의한 색을 이름에 매핑해 tailwind 유틸로 사용할 수 있다.

---

#### **config와 utility**  

| 항목             | config (선택)                           | 유틸(utility – UI 적용)                      |
|------------------|-----------------------------------------|----------------------------------------------|
| CSS 변수 연결     | CSS 변수를 Tailwind 이름에 매핑           | 매핑된 값을 UI에서 실제 스타일로 사용          |
| 디자인 토큰 반영  | 원본 토큰을 유틸 이름으로 연결            | 토큰 기반으로 실제 UI 스타일을 표현            |
| Tailwind 기본 동작 | 없어도 v4는 바로 동작                     | 항상 사용. 조합해 UI 구성                      |
| 커스텀 기능       | 컬러·spacing·플러그인 확장 가능            | 유틸 조합으로 화면 구성                        |


#### **tailwind v4 타입스케일 흐름** 

![tailwind-thumbnail](/assets/img/self-study/tailwind-v4-2.png)
- **token**: 디자인 시스템의 원본 값 (size, weight, spacing)
- **mapping**: 토큰을 UI에서 쓰는 클래스(text-h1 등)로 연결하는 단계
- **preset**: Tailwind가 기본 제공하는 완성형 타입스케일 스타일
> v4는 폰트 스타일을 token ➡ mapping ➡ preset 구조로 처리해  
> 디자인 시스템과 UI를 자연스럽게 이어준다.

---

### **2)  오토 컬러 팔레트**
- RGB 컬러 한 줄만 선언하면 50~900 단계 팔레트를 tailwind가 바로 자동 유틸 생성한다. (HEX는 자동 생성 불가)


```css
/* .theme.css (디자인 토큰 선언) */
:root { --color-brand: 255 102 0; }

/* 자동으로 유틸 클래스 생성 */
.bg-brand-50    {}
.bg-brand-100   {}
.bg-brand-200   {}
...
.bg-brand-900   {}

/* 자동 유틸 이름을 만들려면 config에 작성해야 함 */
colors: {
  brand: "rgb(var(--color-brand) / <alpha-value>)",
}
```

### **3) 폰트 타입스케일 자동 프리셋**
- Tailwind가 폰트 사이즈 + line-height + letter-spacing 값을
**미리 조합된 프리셋(text-h1, text-body1 등)**으로 제공한다. 
- 디자인 시스템의 타입스케일을 그대로 유틸리티로 사용할 수 있어 일관성이 높아진다.
- theme.css에 정의한 토큰 값을 font.css에서 이렇게 매핑하면, 단어만 붙여도 완성된 타입 스타일이 적용된다.

```css
.text-h1 {
  font-size: var(--text-h1);
  font-weight: var(--weight-h1);
  letter-spacing: var(--tracking-h1);
}
```

### **5) 브랜딩 컬러 교체가 쉬워지고 디자인 개발 토큰 일관성 향상**
- 리브랜딩 할 때도 컬러 변수만 바꾸면 끝! (와........)
- 디자인 토큰을 색 1개로 통합해서 관리 할 수 있다.
- 버튼, 텍스트, 보더, 뱃지, hover, active, 그림자, 카드강조, 신규 컴포넌트 등
모든 UI가 자동으로 새로운 브랜드 컬러로 렌더링된다.. 
- 디자인 & 개발의 표준 언어가 통일되는 효과
디자인 토큰 하나로 전체 UI를 컨트롤할 수 있어
디자인과 개발의 일관성이 극대화된다.

```css
/* 1) 디자인 토큰(원본) */
--primary-500: #FF4040;

/* 2) semantic UI 토큰으로 연결 */
--color-primary-500: var(--primary-500);

/* 3) Tailwind는 utility로 알아서 매핑 */
bg-primary-500
text-primary-500
border-primary-500
shadow-primary-500/30
```



## 2. 파일 적용
- tailwind.config.js, postcss.config.js 파일 필요 없어졌다.
- base / components / utilities를 분리 호출할 필요 없음.
- globals.css 1개만 일반적으로 사용

```css
/* 글로벌 css 필수였다 */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Next.js에서는 */
@import "tailwindcss";

/* tailwind v4 에서는 */
@import "tailwindcss";
@import "../styles/theme.css";
@import "../styles/fonts.css";

:root {
  --primary: #FF4040;
}

@theme inline {
  --color-primary: var(--primary);
}
```

- 폰트 프리셋 
- theme.css에 적용했떤 폰트 정리 기준으로 font.css에 아래처럼 적용하면
단어 적용시 시스템 적용 완료

```css
.text-h1 {
  font-size: var(--text-h1);
  font-weight: var(--weight-h1);
  letter-spacing: var(--tracking-h1);
}
```

![tailwind-thumbnail](/assets/img/self-study/tailwind-v4.png)
