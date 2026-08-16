---
title: "SvelteKit 3 RC 훑어보면서 든 생각"
description: "SvelteKit 3 RC가 나왔다. 설정 파일 통합, $lib에서 #lib 변경 등 breaking changes를 중심으로 공부한 내용을 정리했다."
date: 2026-08-16 09:00:00 +0900
categories: [Frontend]
tags: [svelte, sveltekit, vite, frontend]
image:
  path: /assets/img/thumbnail/sveltekit-3-rc-study-note.png
  alt: "SvelteKit 3 RC 훑어보면서 든 생각"
---

SvelteKit 3 RC 발표가 나왔다. 정식 릴리스 전 RC 단계인데, Breaking changes가 여럿 포함돼 있어서 공부 겸 정리해봤다.

공식 블로그를 읽어보니 "코드베이스의 잡초를 뽑고, 앞으로의 진화를 위한 기반을 마련한다"는 표현이 나왔다. 그 말이 이번 릴리스를 꽤 잘 요약하는 것 같았다. 큰 기능 추가보다 구조 정리에 가까운 업데이트라는 인상이었다.

마이그레이션 도구(`npx sv@next migrate sveltekit-3`)도 같이 발표됐는데, 자동 처리 범위 밖의 작업은 TODO 리스트로 나온다고 한다. 그 범위가 어디까지인지 궁금해서 내용을 더 파봤다.

## 1️⃣ 이게 뭐냐?

핵심 변화를 두 가지로 정리했다.

첫째, 설정 파일이 통합된다. 기존엔 `svelte.config.js`와 `vite.config.ts` 두 곳에 설정을 뒀는데, SvelteKit 3부터는 Vite 설정 파일 안으로 통합된다. 이유가 꽤 구체적이었는데 — Vite 플러그인은 설정에 즉시 접근해야 하는데, `svelte.config.js`를 비동기로 해석하는 방식은 그걸 막았다는 거다. "아, 그래서 두 파일이 따로 있었구나"를 처음 이해한 대목이었다.

둘째, 라이브러리 별칭이 `$lib`에서 `#lib`으로 바뀐다. Node.js의 서브경로 임포트(Subpath Imports) 표준을 활용하는 방식으로, 기존처럼 도구마다 따로 alias를 처리할 필요가 없어진다. 대신 확장자를 명시적으로 써야 하는데(`#lib/foo.ts` 식으로), 이게 익숙해지기까지 좀 걸릴 것 같다는 생각이 들었다.

이 외에도 환경 변수를 `src/env.ts`에서 선언해서 타입 안전하게 쓰는 방식이 정식 지원으로 들어오고, 얕은 라우팅(Shallow Routing)에서 `pushState`/`replaceState` 대신 `goto()`의 `shallow: true` 옵션으로 통일된다. Vite 8과 Svelte 5가 필수 요구사항이고, Vite 8의 Rolldown 빌드 덕에 빌드 속도도 빨라진다고 한다.

## 2️⃣ 내가 든 생각

처음엔 "또 설정이 바뀌는 거야?" 하는 마음이 먼저였다. 그런데 이유를 읽으면서 생각이 달라졌다. SvelteKit을 공부할 때 `svelte.config.js`와 `vite.config.ts` 두 파일을 번갈아 보는 게 맥락 없이 헷갈렸는데, 통합되면 그 부분이 줄어들 것 같다는 인상을 받았다.

`$lib`에서 `#lib`으로 바뀌는 건 기호 하나 차이지만, 이런 path alias가 내부에서 어떻게 동작하는지 잘 모른 채로 쓰는 경우가 많았다. 표준을 따른다는 방향이 장기적으로는 덜 헷갈리겠다는 생각이 들었다.

👉🏻 얕은 라우팅에서 `pushState` 대신 `goto({ shallow: true })`로 바뀌는 것도 흥미로웠다. 같은 역할을 하는 API가 여러 곳에 흩어져 있을 때의 혼란을 줄이는 방향이라는 게 느껴졌다.

> 💡 **여기서 드는 질문?**  
> 마이그레이션 도구가 어디까지 자동으로 잡아주는지 궁금했다. 코드베이스가 크면 남겨지는 TODO 리스트가 얼마나 길어질까.

## ⭐️ 마지막으로, 학습자 관점에서 공부하며 느낀 점

정리해보니 SvelteKit 3은 "새 기능 추가"보다 "불필요한 복잡함 제거" 쪽에 가까운 업데이트인 것 같다. 설정 파일 통합, 표준 alias, 환경 변수 개선 모두 기존의 마찰을 줄이는 방향이었다. 공부 끝에 남은 건 — 프레임워크가 성숙해간다는 게, 결국 처음 배우는 사람이 따로 설명받아야 할 부분이 줄어드는 일에 가깝지 않을까 하는 생각이었다.

---

> 참고 원문: [The SvelteKit 3 Release Candidate is here](https://svelte.dev/blog/sveltekit-3-release-candidate)
