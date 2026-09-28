---
title: "Webflow Cloud 사용자 인증 공부 정리 | 같은 사이트 안에서 멤버십까지"
description: "Webflow Cloud에서 Next.js 미들웨어로 인증을 구현하는 방식을 공부하면서 든 생각들."
date: 2026-09-28 09:00:00 +0900
categories: [Design]
tags: [webflow, authentication, nextjs, webflow-cloud]
image:
  path: /assets/img/thumbnail/webflow.png
  alt: "Webflow Cloud 사용자 인증 공부 정리 | 같은 사이트 안에서 멤버십까지"
---

Webflow 블로그에서 Webflow Cloud를 이용한 사용자 인증 구현 방법 글이 올라왔다. 제목만 보면 그냥 튜토리얼 같았는데, 읽다 보니 내용이 좀 달랐다.

Webflow에서 로그인이 필요한 멤버 전용 페이지를 어떻게 만드는지, 기술적으로 어떤 구조인지 궁금해서 공부해봤다.

## 1️⃣ 이게 뭐냐?

Webflow Cloud는 Webflow 사이트 안에 Next.js 앱을 마운트할 수 있는 기능이다. `/members` 같은 경로에 앱을 붙이면, 그 경로 안에서는 Next.js가 처리하고 나머지 공개 콘텐츠는 기존처럼 Webflow Designer로 관리하는 구조가 된다.

인증 흐름을 보면, 비밀번호는 PBKDF2 해시로 저장되고 로그인 성공 시 서명된 쿠키가 발급된다. 이 쿠키는 HMAC-SHA-256으로 서명된 상태 비저장(stateless) 방식이라 요청마다 DB를 조회하지 않아도 된다. Edge Middleware가 모든 요청에서 이 쿠키를 검증하는 구조다.

환경 변수는 세 개 — `AUTH_SECRET`(쿠키 서명용), `AUTH_USERS`(계정 목록 JSON), `NEXT_PUBLIC_BASE_PATH`(마운트 경로) — 로 설정을 관리한다.

👉🏻 공개 콘텐츠는 Designer에서, 인증이 필요한 영역은 Next.js Route Handler와 미들웨어가 담당하는 식으로 역할이 나뉘는 구조다.

## 2️⃣ 내가 든 생각

디자이너 입장에서 "Webflow에서 이걸 직접 처리할 수 있구나"가 제일 먼저 든 생각이었다. 멤버십 사이트를 만들려면 별도 인증 서비스나 외부 솔루션이 필요하다고 막연히 알고 있었는데, 같은 사이트 플랜 안에서 경로 하나를 마운트하는 방식으로 해결된다는 부분이 흥미로웠다.

기술 문서를 읽다가 좀 멈칫했던 부분이 있었다. "Workers 런타임 제약 때문에 상수시간 비교를 커스텀 XOR 루프로 구현했다"는 내용이다. 타이밍 공격이 뭔지는 대충 알겠는데, 왜 런타임 제약이 생기는지, 그게 어떻게 XOR 루프로 해결되는지는 아직 이해가 부족한 것 같다.

> 💡 **여기서 드는 질문:** Webflow Cloud가 이런 걸 지원할수록, 디자이너가 "어디까지 알아야 하나"라는 범위가 어떻게 바뀌는 걸까?

디자이너-개발자 갭 관점에서 보면, 이런 도구가 생길수록 두 역할의 경계가 더 복잡해지는 것 같기도 하다. 도구가 쉬워질수록 더 많은 걸 스스로 해결해야 하는 상황이 오는 것 같은 느낌이 있었다.

## ⭐️ 마지막으로, 디자인 도구 관점에서 공부하며 느낀 점

정리해보니 이게 "Webflow에서 인증 구현"이라기보다, 디자인 도구가 런타임 위에서 동작하는 로직까지 감싸기 시작하는 흐름의 한 단계처럼 느껴졌다. Webflow Cloud, Framer의 코드 컴포넌트, 비슷한 방향들이 하나의 흐름처럼 읽혔다.

지금 단계에서 정리해보면, 이게 "디자이너도 백엔드를 다루는 시대"라기보다 "프레임워크와 디자인 도구 사이의 경계가 계속 움직이는 중"이라는 쪽에 가까운 것 같다.

---

> 참고 원문: [How to add user authentication for Webflow site visitors (Webflow Cloud)](https://webflowmarketingmain.com/blog/user-authentication-webflow-site-visitors)
