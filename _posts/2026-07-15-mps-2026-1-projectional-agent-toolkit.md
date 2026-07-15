---
title: "MPS 2026.1 공부 정리 | AI 에이전트가 DSL 모델을 직접 읽는다는 것"
description: "JetBrains MPS 2026.1의 Projectional Agent Toolkit을 공부하면서 든 생각 — AI 에이전트가 언어 구조를 의미론적으로 다룬다는 게 어떤 의미인지 정리해봤다."
date: 2026-07-15 12:00:00 +0900
categories: [DevTools]
tags: [mps, jetbrains, ai-agent, mcp, dsl]
image:
  path: /assets/img/thumbnail/mps-2026-1-projectional-agent-toolkit.png
  alt: "MPS 2026.1 공부 정리 | AI 에이전트가 DSL 모델을 직접 읽는다는 것"
---

JetBrains 블로그에서 MPS 2026.1 릴리스 발표가 올라왔다. MPS라는 이름은 이번에 처음 제대로 들어봤다. DSL(Domain-Specific Language)을 직접 설계하고 사용할 수 있게 해주는 도구라고 하는데, 일반 코드 에디터와는 결이 꽤 달랐다. 릴리스 노트를 읽다가 한 줄이 눈에 걸렸다.

"Projectional Agent Toolkit — AI 코딩 에이전트가 MPS 모델을 읽고 쓸 수 있게 됐다."

이게 무슨 말인지 궁금해져서 좀 더 파봤다.

## 1️⃣ 이게 뭐냐?

MPS는 텍스트가 아니라 AST(추상 구문 트리)를 직접 편집하는 방식으로 동작한다. Projectional Editing이라고 부르는 방식인데, 에디터에서 보이는 표현과 내부 구조가 분리되어 있다. 구조적으로 올바른 편집만 허용되어 문법 오류 자체가 생기지 않는 구조다.

MPS가 주로 쓰이는 분야는 항공, 자동차, 금융처럼 엄격한 도메인이라고 한다. 팀 고유의 언어가 필요한 경우, 그 언어를 MPS로 직접 설계해서 쓰는 방식이다. Java나 TypeScript가 아니라, 내가 정의한 문법으로 코드를 작성할 수 있다는 개념이다. 도메인 전문가와 개발자 사이의 다리 역할을 언어가 한다는 접근이 흥미로웠다.

문제는 내부 파일(.mps)이 XML이라는 점이었다. AI 에이전트 입장에서는 이 XML이 불투명한 덩어리로 보일 뿐이었다. 언어 구조를 이해하지 못하니 자동화도 어려웠다.

이번 2026.1에서 Projectional Agent Toolkit이 번들로 포함됐다. Claude Code, Codex 같은 에이전트들이 MCP를 통해 MPS 모델에 접근하면, XML 파싱 없이 DSL 구조를 의미론적으로 다룰 수 있다. 도구셋은 12가지로, 프로젝트·모델 열거, 개념 계층 검사, 노드 CRUD, 참조 쿼리 같은 것들이다.

## 2️⃣ 내가 든 생각

"AI가 코드를 생성한다"가 아니라 "AI가 언어 구조를 이해하고 편집한다"는 방향이 흥미로웠다.

👉🏻 Projectional Editing 특성상, 도구셋 자체가 잘못된 노드 관계를 만드는 걸 막는 구조라고 한다. AI 에이전트도 그 제약 안에서 작동하니, 텍스트 생성과 달리 구조적 오류는 원천적으로 줄어드는 방식이라는 생각이 들었다. 언어를 먼저 정의하고, 에이전트가 그 언어 안에서 작동한다는 순서가 인상적이었다.

> 💡 **여기서 드는 질문?** 텍스트 기반 코드 생성과 AST 레벨 편집은 결과물 품질에서 실제로 얼마나 차이가 날까?

MCP가 다양한 에디터, 도구와 연동되는 걸 봐왔는데, MPS처럼 Projectional Editing 기반 도구에도 붙기 시작했다는 게 흥미로웠다. 텍스트가 아닌 구조를 기반으로 동작하는 도구들이 앞으로 AI 에이전트와 어떻게 연동될지 궁금해졌다.

릴리스에서 함께 업데이트된 것들도 있었다. IntelliJ Platform 2026.1, JDK 25, Kotlin 2.3으로 기반이 올라갔다. Build Language의 전이 의존성 처리가 자동화되어 선언이 단순해졌고, 마이그레이션도 모듈 descriptor 기록을 기준으로 결정되어 재현성이 높아졌다고 한다.

## ⭐️ 마지막으로, 개발 도구 공부하면서

MPS는 지금 공부하는 영역과 거리가 꽤 있는 도구다. 그래도 Projectional Agent Toolkit 이야기를 읽으면서 한 질문이 계속 맴돌았다.

이런 류의 도구를 볼 때 자꾸 같은 질문을 하게 되는 것 같다 — AI가 "텍스트 예측"에서 "구조 조작"으로 넘어가면, 실제로 뭐가 달라질까?

---

> 참고 원문: [MPS 2026.1 Has Been Released!](https://blog.jetbrains.com/mps/2026/07/mps-2026-1-released/)
