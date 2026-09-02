---
title: "Svelte 9월 업데이트 공부 정리 | SvelteKit 3 RC 앞에서"
description: "Svelte 5.57과 SvelteKit 3 RC 릴리스 노트를 읽으면서 정리한 것들. 모르는 개념이 생각보다 많았다."
date: 2026-09-02 09:00:00 +0900
categories: [Frontend]
tags: [svelte, sveltekit, frontend]
image:
  path: /assets/img/thumbnail/svelte-september-2026-study-note.png
  alt: "Svelte 9월 업데이트 공부 정리 | SvelteKit 3 RC 앞에서"
---

Svelte 블로그에서 9월 업데이트 글이 올라왔다. 이번 달도 SvelteKit 3 RC를 향해 패치들이 계속 쌓이는 구조였다.

Svelte를 배운 지 얼마 안 됐는데, 릴리스 노트를 읽다 보면 모르는 개념들이 생각보다 많다. 그래서 이번엔 이해한 것들 위주로 간단히 정리해봤다.

## 1️⃣ 이게 뭐냐?

Svelte 5.57에서 눈에 띈 건 `SvelteMap`에 `getOrInsert`와 `getOrInsertComputed`가 추가된 것이다. "읽거나 없으면 초기화" 패턴을 메서드 하나로 처리하게 됐다. 기존 `Map`에서 이 패턴을 직접 쓰려면 매번 조건문이 필요했는데, 그게 내장 메서드로 정리된 셈이다.

`createContext`도 변경이 있었다. 세 번째 반환값으로 `has` 함수가 생겼는데, 컨텍스트가 설정됐는지 `get`을 먼저 부르지 않고도 확인할 수 있게 됐다. 원래는 설정 안 된 컨텍스트에 `get`을 부르면 에러가 났다고 하는데, 그 케이스를 안전하게 처리하는 방법이 생긴 것 같다.

`<select>` 요소에 `defaultValue` 속성이 생긴 것도 흥미로웠다. 폼 리셋 시 select를 특정 값으로 되돌리는 게 이제 네이티브 동작이 됐다. 지금까지 이걸 별도로 처리해야 했다는 게 오히려 생소하기도 했다.

SvelteKit 3 RC에서는 변경이 더 많았다. 폼 액션이 성공·실패 시 모두 액션 페이지로 이동하는 게 기본 동작이 됐고, `+server.js`에서 `QUERY` HTTP 메서드도 지원하게 됐다. `QUERY`는 GET과 비슷하되 요청 본문을 포함할 수 있는 메서드라고 이해했다. 기존 `$lib` 경로가 Node subpath imports 방식인 `#lib`로 바뀌는 것도 있었는데, 이 부분은 아직 정확히 이해가 안 된 채로 읽었다.

## 2️⃣ 내가 든 생각

`<select>` defaultValue 같은 변화는 작아 보이지만, 디자이너 관점에서는 폼 UX에 직접 닿는 부분이다. 사용자가 리셋을 눌렀을 때 select가 예상대로 돌아가는지 안 돌아가는지 — 이런 디테일이 쌓여서 완성도가 달라지는 종류의 것이라는 생각이 들었다.

👉🏻 sv CLI에서 `mcp` 애드온이 `ai-tools`로 교체된 것도 눈에 들어왔다. MCP를 하나의 기능으로 좁게 두지 않고, AI 도구 전반으로 범위를 확장하는 방향인 것 같았다. 거기에 SvelteKit 3 마이그레이션을 위한 task-based 도구도 sv CLI에 포함됐다고 하는데, 이 쪽 변화가 앞으로 어디로 가는지 궁금해졌다.

SvelteKit 3 RC가 breaking change를 포함하면서도 계속 rolling하고 있다는 게 인상적이었다. `#lib` 경로 변경, `defineParams` 이전, 폼 액션 동작 변경 같은 것들이 3.0 전에 한꺼번에 정리되는 흐름. 출시 전에 가능하면 깔끔하게 끝내려는 것 같다는 느낌이었다.

> 💡 **여기서 드는 질문?**
> `$lib`에서 `#lib`로 바뀌는 게 실제로 어떤 차이를 만드는 걸까? Node subpath imports 방식이라고는 하는데, 아직 정확히 이해가 안 됐다. 이건 따로 파봐야 할 것 같다.

## ⭐️ 마지막으로, 배우는 입장에서 정리해보니

이번 업데이트는 큰 기능 하나보다 작은 개선들이 촘촘하게 쌓이는 구조였다. SvelteKit 3 RC라는 방향이 있고, 그 주변에 실용적인 패치들이 붙어오는 흐름. 공부 끝에 남은 건, 이런 축적이 프레임워크 DX를 만들어간다는 한 줄짜리 인상에 가까웠다.

---

> 참고 원문: [What's new in Svelte: September 2026](https://svelte.dev/blog/whats-new-in-svelte-september-2026)
