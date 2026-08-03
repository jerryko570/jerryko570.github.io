---
title: "SvelteKit 3 프리뷰 공부 정리 | API가 꽤 많이 바뀌는 것 같다"
description: "SvelteKit 3 첫 프리뷰가 나왔다. goto와 라우팅 쪽이 많이 달라지는 것 같아서 훑어봤다."
date: 2026-08-03 10:00:00 +0900
categories: [Frontend]
tags: [svelte, sveltekit, frontend]
image:
  path: /assets/img/thumbnail/sveltekit-3-preview-study-note.png
  alt: "SvelteKit 3 프리뷰 공부 정리 | API가 꽤 많이 바뀌는 것 같다"
---

Svelte 블로그에서 8월 업데이트가 올라왔다. 매달 나오는 정기 포스트인데, 이번엔 SvelteKit 3의 첫 프리뷰 릴리스가 포함돼 있었다. 안정 버전도 조금씩 업데이트됐지만, 메이저 버전이 어떤 방향으로 바뀌는지가 궁금해서 집중해서 읽어봤다.

7월 한 달에만 next.5부터 next.13까지 열세 개 프리뷰가 나왔다는 게 꽤 빠른 편이었다. 뭔가 갈아엎고 있다는 느낌이 들었다.

## 1️⃣ 이게 뭐냐?

가장 눈에 띈 변화는 `goto` 함수에 `state` 옵션이 생긴 거다. 기존엔 shallow routing을 하려면 `pushState`, `replaceState`를 따로 써야 했는데, SvelteKit 3에선 `goto(url, { state: {...} })`로 처리할 수 있게 통합됐다. `persistState: true` 옵션을 주면 새로고침 이후에도 상태가 유지된다고 한다.

`noScroll`, `keepFocus` 같은 개별 옵션들도 `reset`이라는 단일 옵션으로 합쳐졌다. 옵션이 여럿으로 흩어져 있던 것보다 의도를 더 명확하게 표현할 수 있는 쪽으로 정리된 느낌이었다.

`invalidateAll`은 `refreshAll`로 이름이 바뀌었고, 기존 이름은 deprecated 처리됐다. `error()` 함수 API도 바뀌었는데, 두 번째 인자로 메시지를 반드시 넘겨야 하는 형식 — `error(status, message, {...})` — 으로 강제됐다. 에러 메시지가 누락되는 상황을 막으려는 의도인 것 같다.

안정 버전 쪽에선 remote forms에 `submitted` 속성이 생겼고, `defineEnvVars`가 `@sveltejs/kit/env`라는 전용 서브패스로 이동했다.

## 2️⃣ 내가 든 생각

목록을 훑으면서 든 인상은, API가 흩어진 걸 한 곳으로 모으는 방향으로 가고 있다는 거였다. `pushState`/`replaceState`를 따로 임포트해야 했던 걸 `goto` 안으로 끌어들인 게 그런 패턴이다. 공부 중에 "이 함수는 언제 쓰고 저건 언제 써야 하지?" 하던 순간이 있었는데, 이게 통합되면 그 혼란이 좀 줄어들 것 같다.

👉🏻 shallow routing이 `goto`에 내장된다는 게 디자이너 입장에서 흥미로웠다. URL은 바꾸지 않고 상태만 바꾸는 패턴은 탭 전환이나 모달 열기처럼 UI에서 자주 나오는 시나리오다. 이걸 더 자연스러운 방식으로 표현할 수 있게 된다면, 디자이너-개발자 간에 "이 인터랙션을 어떻게 구현할지" 얘기할 때 접점이 늘어나지 않을까 싶었다.

`invalidateAll → refreshAll` 이름 변경도 그냥 지나치기가 어려웠다. "무효화"보다 "새로 가져오기"가 의도를 더 명확히 담는다는 판단인 것 같은데, 이름 하나가 코드 읽는 사람한테 주는 신호가 생각보다 크다는 걸 새삼 느꼈다.

> 💡 **메이저 버전에서 deprecated가 이렇게 많으면, 기존 코드 마이그레이션은 얼마나 복잡할까?**

아직 프리뷰 단계니까 정식 출시 전에 더 달라질 수도 있겠지만, 지금 문서 기준으로는 규모가 작지 않은 변화였다.

## ⭐️ 마지막으로, 프론트엔드 공부하면서 느낀 점

정리해보니 SvelteKit 3로 넘어가는 게 기능 확장보다 API 정리에 가까운 작업인 것 같다. 흩어진 걸 한데 모으고, 이름이 불명확하던 걸 다시 짓고, 필수 인자를 명시하는 방식으로 — 겉보기엔 작은 변화들인데, 학습자 입장에서 오히려 이쪽이 배우기 쉬운 API가 되는 방향일 수 있다는 생각도 들었다. 버전업이 항상 새 기능을 더하는 일만은 아닌 것 같다는 걸 이번에 조금 실감했다.

---

> 참고 원문: [What's new in Svelte: August 2026](https://svelte.dev/blog/whats-new-in-svelte-august-2026)
