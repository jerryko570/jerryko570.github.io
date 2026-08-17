---
title: "Compose HTML SSR 공부 정리 | JVM에서 HTML을 Kotlin 함수로 렌더링한다는 게 어떤 건지"
description: "JetBrains가 탐색 중인 Compose HTML SSR 아이디어를 읽고, 타입 안전한 서버 렌더링이 뭔지 정리해봤다."
date: 2026-08-17 12:00:00 +0900
categories: [DevTools]
tags: [kotlin, compose-html, ssr, jetbrains]
image:
  path: /assets/img/thumbnail/compose-html-ssr-study-note.png
  alt: "Compose HTML SSR 공부 정리 | JVM에서 HTML을 Kotlin 함수로 렌더링한다는 게 어떤 건지"
---

JetBrains 블로그에서 Compose HTML을 서버사이드 렌더링에 활용하는 탐색 글이 올라왔다. "Kotlin으로 서버에서 HTML을 렌더링한다"는 요약만 봤을 땐 정확히 어떤 이야기인지 감이 안 왔는데, 읽어보니 기존 JVM 템플릿 엔진을 대체하려는 방향에 가까운 얘기였다.

글의 출발점은 최근 SSR을 다시 들여다보는 흐름이었다. React Server Components, HTMX, Phoenix LiveView처럼 여러 생태계가 서버에서 UI를 렌더링하는 방향을 탐색하고 있는데, JVM 쪽엔 그에 해당하는 현대적인 접근이 없다는 게 배경이었다. Thymeleaf나 FreeMarker 같은 템플릿 엔진이 있긴 하지만, 그걸 "컴포넌트 방식"이라고 부르긴 어렵다는 문제의식이었다.

## 1️⃣ 이게 뭐냐?

Compose HTML은 원래 Kotlin/JS 기반으로 브라우저 UI를 만드는 라이브러리다. 이번 탐색의 핵심은 여기에 JVM 타겟을 추가해서, 브라우저 없이 서버 환경에서 HTML 문자열을 생성할 수 있게 하자는 방향이었다.

제안된 API 형태는 이랬다:

```kotlin
fun renderToString(content: @Composable DOMScope<DomElement>.() -> Unit): String
```

한 번의 렌더 패스로 컴포지션을 실행하고 HTML 문자열로 직렬화하는 구조다. 재구성(recomposition)이나 이펙트, 상태 변화는 지원하지 않는다. 서버에서 한 번 렌더링해서 클라이언트에 보내는 SSR 특성상 그 제약은 자연스럽다는 생각이 들었다.

기존 Thymeleaf와 뭐가 다르냐면, 핵심은 타입 안전성 쪽이었다. Thymeleaf는 HTML 템플릿에 `th:text="${value}"` 같은 표현을 쓰는데, 값이 잘못 넘어와도 컴파일 타임엔 잡히지 않는다. Kotlin 함수로 정의하면 속성이 잘못 넘겨질 경우 컴파일이 안 되고, IDE 리팩토링도 자동으로 지원된다. 런타임에야 오류를 발견하던 걸 더 앞 단계로 끌어오는 방향인 것 같았다.

## 2️⃣ 내가 든 생각

읽다 보니 카드나 폼처럼 서버에서 반복 렌더링하는 UI 패턴이 먼저 떠올랐다. 타입이 지정된 Kotlin 함수로 컴포넌트를 정의해두면, 속성을 잘못 넘길 때 컴파일 단계에서 잡힌다. 디자이너 입장에서는 컴포넌트 속성이 명시적으로 정의돼 있으면, 개발자와 "이 값은 어떤 형태야?" 얘기할 때 공통 언어가 생기는 것 같다는 생각이 들었다.

👉🏻 흥미로웠던 건 서버와 클라이언트를 같은 코드로 커버한다는 방향이었다. SSR에서 쓰는 컴포넌트를 Kotlin/JS 브라우저 렌더링에서도 공유할 수 있다면, 같은 UI를 두 벌 작성하거나 두 언어를 오가지 않아도 된다는 그림이 나온다.

> 💡 **React의 Server Components랑 뭐가 다를까?** RSC도 같은 언어로 서버/클라이언트를 나누는 구조인데, JVM 쪽에서 비슷한 방향이 탐색되고 있다. 언어가 달라도 접근 방식이 수렴한다면, 결국 그게 SSR이라는 문제 자체가 끌어당기는 건지 공부하면서 자꾸 같은 질문으로 돌아왔다.

한 가지 짚어두고 싶었던 건, 이 글이 아직 탐색 단계라는 점이었다. 공식 로드맵도 아니고 API도 확정되지 않은, 아이디어를 공개하고 피드백을 구하는 형태였다. 발표처럼 읽힐 수 있는데, 읽어보면 "같이 방향을 고민해보자"에 가까웠다.

## ⭐️ 마지막으로, 공부하면서 느낀 점

공부 끝에 남은 한 줄은 이거다. 서버에서 HTML을 렌더링하는 문제는 생태계마다 각자의 언어로 답을 찾고 있는데, 그 답들이 슬금슬금 비슷한 형태로 수렴하고 있다. React든 Kotlin이든 결국 같은 물음 앞에 서 있는 것 같다는 인상이었다. JVM이 이 방향으로 가면 실제로 어떤 모양이 될지, 탐색 단계가 지금은 오히려 흥미롭게 느껴졌다.

---

> 참고 원문: [Exploring Compose HTML for Server Side Rendering](https://blog.jetbrains.com/kotlin/2026/08/exploring-compose-html-for-server-side-rendering/)
