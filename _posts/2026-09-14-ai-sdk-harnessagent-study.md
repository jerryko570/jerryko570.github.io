---
title: "AI SDK HarnessAgent 공부 정리 | 에이전트 바꿔도 코드 그대로라는 얘기"
description: "Vercel AI SDK harness layer 문서를 읽다가 HarnessAgent 인터페이스 개념이 흥미로워서 정리해봤다."
date: 2026-09-14 10:00:00 +0900
categories: [Frontend]
tags: [vercel, ai-sdk, github-copilot]
image:
  path: /assets/img/thumbnail/ai-sdk-harnessagent-study.png
  alt: "AI SDK HarnessAgent 공부 정리 | 에이전트 바꿔도 코드 그대로라는 얘기"
---

Vercel changelog를 훑다가 짧은 항목 하나가 눈에 걸렸다. AI SDK harness layer에 GitHub Copilot 어댑터가 추가됐다는 내용이었는데, 처음엔 그냥 지원 목록에 이름 하나 더 들어간 것 정도로 읽혔다. 그런데 `HarnessAgent`라는 인터페이스 얘기가 같이 나와 있어서 조금 더 들여다봤다. 짧은 changelog 하나인데 생각보다 흥미로운 구조 이야기가 있었다.

## 1️⃣ 이게 뭐냐?

AI SDK harness layer는 코딩 에이전트들을 하나의 공통 인터페이스 아래 묶어주는 레이어다. `HarnessAgent`라는 인터페이스에 어떤 어댑터를 연결하느냐에 따라 Claude Code, Cursor, Cline, 그리고 이번에 추가된 GitHub Copilot 중 하나가 동작하는 구조를 취한다.

문서에 나와 있는 사용 방식을 보면:

```typescript
import { HarnessAgent } from '@ai-sdk/harness/agent';
import { githubCopilot } from '@ai-sdk/harness-github-copilot';

const agent = new HarnessAgent({ harness: githubCopilot });
```

`githubCopilot` 자리를 다른 어댑터로 바꾸면 에이전트가 교체된다. 내부적으로는 Agent Client Protocol(ACP)이라는 걸 통해 연결되는데, 어댑터 패키지 이름이 `@ai-sdk/harness-github-copilot`처럼 규칙이 통일되어 있는 것 같았다. 이 레이어 덕분에 에이전트가 바뀌어도 호출하는 쪽 코드는 그대로 둘 수 있다.

현재 지원 목록에는 Claude Code, Cline, Codex, Cursor, Deep Agents, GitHub Copilot 등 열 개가 넘는다.

## 2️⃣ 내가 든 생각

처음엔 "그냥 어댑터 패턴이잖아" 싶었는데, 조금 더 생각해보니 이 구조가 말하는 바가 흥미로웠다. 에이전트를 교체 가능한 단위로 설계한다는 건, 애플리케이션 입장에서 "어떤 에이전트를 쓰느냐"를 구현 디테일로 다루겠다는 방향이니까.

디자인 시스템에서 비슷한 논리를 본 것 같은 기억이 있다. 버튼 컴포넌트 내부 구현이 바뀌어도 사용하는 쪽은 동일한 props를 넘기면 된다. `HarnessAgent`가 에이전트 레이어에서 그 역할을 하는 것 같았다. Claude Code든 GitHub Copilot이든 호출하는 코드 입장에서는 같은 인터페이스를 쓰면 된다.

👉🏻 이게 흥미로웠던 건 "어떤 에이전트가 더 좋냐"는 질문을 일단 뒤로 미루게 만드는 구조인 것 같다는 점이었다. 교체가 쉬우면 특정 에이전트에 묶일 이유가 줄어드니까. MUI에서 shadcn/ui로 갈아타는 게 고통스러운 이유 중 하나가 컴포넌트 인터페이스 차이 때문인데, 에이전트도 그런 식으로 다루겠다는 거라면 의미가 조금 달랐다.

> 💡 **여기서 드는 질문**: ACP가 공통 인터페이스라면, 에이전트마다 다른 기능들은 어떻게 다루는 걸까? 추상화를 올리면 공통분모만 노출되는 트레이드오프가 생기는데, 그 부분을 문서에서는 아직 찾지 못했다.

## ⭐️ 마지막으로, 프론트엔드 공부하는 입장에서

이 changelog는 GitHub Copilot 하나가 지원 목록에 추가됐다는 짧은 메모인데, 문서를 따라가다 보니 harness layer 구조 자체가 더 인상에 남았다. 어떤 에이전트가 추가됐냐보다, 에이전트를 끼우는 구조를 어떻게 설계했냐가 더 흥미로운 공부거리였다.

이런 류의 도구를 볼 때 자꾸 같은 생각을 하게 되는 것 같다 — 기능이 늘어나는 것보다, 그 기능을 교체할 수 있냐 없냐가 더 중요한 설계 선택일 수 있겠다는.

---

> 참고 원문: [GitHub Copilot is now available in the AI SDK harness layer](https://vercel.com/changelog/github-copilot-ai-sdk-harness-adapter)
