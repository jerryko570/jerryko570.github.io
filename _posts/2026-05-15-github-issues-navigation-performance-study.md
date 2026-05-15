---
title: "GitHub Issues 내비게이션 성능 최적화 공부 정리 | 캐시 먼저, 검증은 나중에"
description: "GitHub가 Issues 화면을 즉각 반응으로 만들기 위해 IndexedDB, 서비스 워커, 프리히팅을 어떻게 조합했는지 공부한 노트."
date: 2026-05-15 09:00:00 +0900
categories: [DevTools]
tags: [github, performance, service-worker, indexeddb, caching]
image:
  path: /assets/img/thumbnail/github-issues-navigation-performance-study.png
  alt: "GitHub Issues 내비게이션 성능 최적화 공부 정리 | 캐시 먼저, 검증은 나중에"
---

GitHub 블로그에 Issues 내비게이션을 빠르게 만들었다는 글이 올라왔다. "latency to instant"라는 제목이 눈에 띄어서 읽어봤는데, 단순한 최적화 팁이 아니라 꽤 구조적인 이야기였다.

프론트엔드를 공부하다 보면 "빠른 화면 전환" 같은 게 추상적으로만 느껴지는데, GitHub가 어떻게 구체적으로 접근했는지 정리해봤다.

## 1️⃣ 이게 뭐냐?

GitHub Issues 화면 이동할 때 매번 서버에서 데이터를 받아왔다. 당연한 방식인데, 네트워크 상태에 따라 응답이 길어진다는 게 문제였다.

새 방식의 핵심은 "렌더링 먼저, 검증 나중"이다. 캐시에 데이터가 있으면 그걸로 먼저 화면을 그리고, 서버 응답이 오면 조용히 업데이트한다. 브라우저 내부 저장소인 IndexedDB를 썼는데, 새로고침해도 캐시가 살아있다는 게 포인트다.

여기에 메모리 레이어를 하나 더 얹었다. IndexedDB는 비동기라 읽는 데 약간 시간이 걸리는데, 자주 쓰이는 데이터는 메모리에 따로 두는 식이다. 메모리 → IndexedDB → 서버 순서로 확인하는 계층 구조다.

👉🏻 서비스 워커도 붙어있다. 탭을 새로 열거나 새로고침할 때도 캐시를 활용하게 해준다. 요청을 가로채서 로컬 캐시를 먼저 확인하고, 있으면 서버에 신호를 보내 SSR 처리를 줄이는 구조다.

## 2️⃣ 내가 든 생각

"프리히팅(preheating)"이라는 개념이 특히 흥미로웠다. 사용자가 이슈 목록에 마우스를 올릴 때, 클릭 전에 미리 데이터를 준비해두는 거다.

처음엔 단순한 prefetch인 줄 알았는데, 읽다 보니 다르다. 이미 캐시에 있으면 네트워크 요청을 아예 안 하고, 없을 때만 낮은 우선순위로 가져온다. 서버 부하를 줄이면서 캐시를 채우는 방식인 것 같다.

> 💡 **여기서 드는 질문?**
> 캐시 데이터가 서버랑 달라지면 어떻게 처리할까. 글을 보면 일부 불일치를 허용하고, 완벽한 신선도보다 체감 속도를 우선한다는 선택이 나온다.

디자이너 관점에서 보면 이 선택이 더 흥미롭다. "사용자가 느끼는 빠름"과 "데이터의 정확함" 사이 결정은 기술 문제가 아니라 UX 판단에 가까운 것 같다.

## 3️⃣ 이번에 더 공부해보고 싶어진 것

서비스 워커는 이름만 알고 있었는데, 요청을 가로채서 캐시를 확인하는 패턴이 구체적으로 어떤 건지 이 글 보면서 좀 더 이해됐다.

IndexedDB도 그렇다. localStorage랑 뭐가 다른지, 이 글 덕분에 더 구체적으로 궁금해졌다. 비동기라는 점에서 다루기 까다로울 것 같은데, 어떻게 쓰는 건지 따로 파봐야 할 것 같다.

## ⭐️ 마지막으로, 프론트엔드 공부하면서 느낀 점

공부 끝에 남은 건 "기술 선택보다 어느 수준의 타협을 허용할 것인가"라는 한 줄짜리 인상이다.

---

> 참고 원문: [From latency to instant: Modernizing GitHub Issues navigation performance](https://github.blog/engineering/architecture-optimization/from-latency-to-instant-modernizing-github-issues-navigation-performance/)
