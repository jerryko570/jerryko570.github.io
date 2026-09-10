---
title: "React 19.3 릴리스 훑어보면서 든 생각"
description: "View Transitions 안정화, Fragment Refs, browser() API — 이번 릴리스 노트를 공부하며 정리한 것들"
date: 2026-09-10 10:00:00 +0900
categories: [Frontend]
tags: [react, view-transitions, fragment-refs, ssr]
image:
  path: /assets/img/thumbnail/react-19-3-study-note.png
  alt: "React 19.3 릴리스 훑어보면서 든 생각"
---

React 공식 블로그에서 19.3 릴리스 노트가 올라왔다. React 18에서 19로 넘어올 때도 꽤 많은 게 바뀌었는데, 19.3에서도 눈에 걸리는 게 있어서 정리해봤다.

이번에 주목한 건 View Transitions가 실험 단계를 벗어났다는 것이었다. Fragment Refs와 browser()라는 API도 새로 추가됐고, Trusted Types 지원도 이번에 들어왔다.

## 1️⃣ 이게 뭐냐?

View Transitions는 UI 요소가 화면에 들어오거나 나갈 때, 또는 위치나 크기가 바뀔 때 애니메이션을 적용해주는 기능이다. 브라우저의 View Transition API를 React 컴포넌트 형태로 감싼 것에 가깝다.

`<ViewTransition>` 컴포넌트로 요소를 감싸면 되고, `addTransitionType()`을 쓰면 같은 상태 업데이트에도 방향에 따라 다른 애니메이션을 지정할 수 있다. 다음 페이지로 넘어갈 땐 왼쪽에서, 이전 페이지로 돌아올 땐 오른쪽에서 슬라이드하는 식이다. 이전에는 여러 Transition이 동시에 실행되면 가장 느린 것이 나머지를 기다리게 만들었는데, 이제는 독립적으로 처리된다.

Fragment Refs는 형제 요소 그룹을 하나의 ref로 제어할 수 있게 해주는 기능이다. 기존엔 래퍼 `<div>`를 추가해야 했는데, 그게 flexbox나 grid 레이아웃에 간섭을 일으키기도 했다. 이제 `<Fragment ref={fragmentRef}>`로 직접 연결할 수 있고, 이벤트 리스닝·포커스 제어·IntersectionObserver 연결 같은 메서드도 쓸 수 있다.

browser()는 SSR 환경에서 브라우저 전용 코드를 처리하는 API다. `typeof window !== 'undefined'`로 분기하던 패턴이 공식 API로 정리됐다. 서버에서는 Suspense 폴백을, 클라이언트에서는 정상 렌더링을 하는 구조다.

## 2️⃣ 내가 든 생각

View Transitions 중에서 흥미로웠던 건 `addTransitionType()`이었다. 앱을 디자인할 때 "뒤로 가면 오른쪽에서, 앞으로 가면 왼쪽에서"는 별 고민 없이 쓰이는 관습인데, 그게 이제 코드 레벨의 API로 정리됐다는 게 낯설면서도 자연스러웠다. CSS나 별도 애니메이션 라이브러리로 처리하던 것을 React 쪽에서 흡수한 느낌이다.

디자이너 입장에서 보면, 이 기능은 단순히 애니메이션 추가가 아니라 화면 전환의 맥락을 표현하는 수단에 더 가까운 것 같다. 어떤 Transition에 어떤 타입을 붙이느냐에 따라 UX가 달라지는데, 그 판단이 CSS 클래스가 아니라 컴포넌트 로직 안으로 들어온다. 그게 편한 건지 어색한 건지는 공부한 내용만으론 잘 모르겠다.

👉🏻 Fragment Refs가 해결하는 문제는 생각보다 구체적이었다. 감싸는 `<div>` 하나가 레이아웃을 망치는 상황은 구현하다 보면 자주 상상하게 되는 일인데, 특히 외부 라이브러리 컴포넌트를 쓸 때 DOM 구조를 건드리지 않고도 ref를 붙일 수 있다는 게 실용적으로 느껴졌다.

> 💡 **여기서 드는 질문:** `observeUsing()`이 IntersectionObserver나 ResizeObserver와 연결된다고 하는데, 무한 스크롤이나 lazy loading 같은 것들을 라이브러리 레벨에서 추상화할 때 Fragment Refs가 어떻게 쓰일 수 있을지 궁금해졌다.

## 3️⃣ 앞으로 어떻게 쓸까?

문서 기준으로는, View Transitions는 페이지 전환 애니메이션이 있는 앱에서 자연스럽게 쓰일 것 같다는 생각이 들었다. 발표 글 안에 Suspense와의 통합 예제가 꽤 구체적으로 나와 있어서, 그 부분을 따라가 보면서 공부하면 좋을 것 같다.

Next.js 같은 프레임워크에서 어떻게 통합이 되는지는 별도로 문서를 찾아봐야 할 것 같다. 릴리스 노트엔 프레임워크 연동 부분이 구체적으로 다뤄지지 않아서, 그게 지금 단계에서 남은 궁금증이다.

## ⭐️ 마지막으로, 프론트엔드 입문자 관점에서 공부하며 느낀 점

정리해보니 이번 릴리스는 새 개념의 추가라기보다, 이전에 불편하게 우회해서 쓰던 패턴들을 공식 API로 정리한 것에 더 가까운 것 같다. View Transitions, Fragment Refs, browser() 모두 그 범주에 들어간다. 공부 끝에 남은 건 "React가 점점 브라우저 API와 잘 맞닿아가고 있다"는 한 줄이다.

---

> 참고 원문: [React 19.3](https://react.dev/blog/2026/09/09/react-19-3)
