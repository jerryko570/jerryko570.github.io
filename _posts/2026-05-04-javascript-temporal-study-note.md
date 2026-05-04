---
title: "JavaScript Temporal 공부 정리 | Date 문제가 9년짜리였던 이유"
description: "JS Date가 왜 항상 불편했는지, TC39 Temporal 제안이 뭘 바꾸는지 공부한 메모."
date: 2026-05-04 12:00:00 +0900
categories: [DevTools]
tags: [javascript, temporal, tc39, date, frontend]
image:
  path: /assets/img/thumbnail/javascript-temporal-study-note.png
  alt: "JavaScript Temporal 공부 정리 | Date 문제가 9년짜리였던 이유"
---

Stack Overflow 블로그에서 JavaScript Date 관련 팟캐스트 글이 올라왔다. Bloomberg 엔지니어이자 Rust 기반 JS 엔진 Boa를 만든 Jason Williams가 나와서 JS의 날짜/시간 처리가 왜 이렇게 복잡한지, TC39 Temporal 제안이 뭘 바꾸려는지를 얘기하는 내용이었다. "9년이 걸렸다"는 부분에서 한번 멈칫했다.

프론트 공부를 시작하면서 `new Date()`를 처음 만졌을 때 뭔가 이상하다는 느낌이 들었다. 월이 0부터 시작한다. `new Date(2026, 0, 1)`이 1월 1일이다. 타임존 처리도 직관적이지 않았고, 날짜 계산을 하다 보면 뭔가 자꾸 어긋나는 기분이었다. 그래서 찾아보면 어김없이 나오는 게 Moment.js였는데, 이게 왜 필요한지를 이해하는 데 꽤 시간이 걸렸다.

## 1️⃣ Date가 이렇게 된 이유

`Date` 객체는 원래 Java의 `java.util.Date`에서 거의 그대로 가져온 것이라고 한다. JavaScript가 초창기에 빠르게 만들어지던 시절의 흔적인데, 지금 와서 이걸 바꾸면 기존 코드가 전부 깨지니 사실상 손을 못 대는 상황인 것 같다.

그 결과로 Moment.js 같은 라이브러리가 오랫동안 표준처럼 쓰였다. 근데 Moment.js도 결국 유지보수를 중단하는 방향으로 흘러가고 있다. 번들 크기도 크고, 가변(mutable) 객체라 예상치 못한 버그가 생기는 경우도 있었다고 한다.

👉🏻 표준에 구멍이 생기니까 라이브러리로 메웠고, 그 라이브러리도 결국 한계에 부딪혔다는 거다. 이게 9년짜리 작업의 배경인 것 같다.

## 2️⃣ Temporal이 달라지는 점

`Temporal`은 `Date`를 대체하기 위해 TC39에서 설계한 새 API다. 가장 눈에 들어온 건 날짜·시간·타임존을 분리해서 다룰 수 있다는 구조였다.

- `Temporal.PlainDate` — 타임존 없는 순수한 날짜
- `Temporal.ZonedDateTime` — 타임존을 포함한 날짜
- `Temporal.Instant` — 절대적인 특정 시점

기존 `Date`는 이 구분이 없었다. 타임존을 신경 쓰지 않아도 되는 날짜와, 신경 써야 하는 날짜가 같은 타입이라 거기서 오해가 생기곤 했다.

> 💡 **그러면 지금 당장 쓸 수 있나?**
> 브라우저 지원이 어느 정도 올라와야 프로덕션에서 쓸 수 있을 텐데, 폴리필 없이 바로 쓸 수 있는 시점이 언제인지는 아직 잘 모르겠다.

디자이너 입장에서 보면 날짜 표시는 UI에서 꽤 자주 나오는 요소다. "3일 전", "오늘", "D-7" 같은 텍스트를 다루다 보면 Date 계산이 어떻게 돌아가는지 매번 조금 불투명한 부분이 있었는데, 타입으로 구분이 되면 좀 달라질 것 같긴 하다.

## 3️⃣ 앞으로 어떻게 쓸까?

당장 Temporal을 프로젝트에 넣을 생각은 없다. 브라우저 지원 확인이 먼저고, 기존에 쓰던 `date-fns`를 대체할 만큼 익숙해지는 것도 시간이 필요할 것 같다.

다만 이번에 "왜 Date가 이렇게 됐는지"를 이해한 건 지금 당장 써먹을 수 있는 부분이다. 라이브러리 선택할 때나 기존 코드 읽을 때 조금 다르게 볼 수 있을 것 같다.

## ⭐️ 마지막으로

이런 류의 도구를 볼 때 자꾸 같은 질문을 하게 되는 것 같다 — 왜 처음부터 이렇게 설계됐고, 고치는 데 왜 이렇게 오래 걸리는가. Temporal 자체의 기능보다 그 맥락 — 설계의 유산과 그 대가를 치르는 9년 — 이 더 인상에 남았다.

---

> 참고 원문: [Time is a construct but it can still break your software](https://stackoverflow.blog/2026/05/01/time-is-a-construct-but-it-can-break-your-software/)
