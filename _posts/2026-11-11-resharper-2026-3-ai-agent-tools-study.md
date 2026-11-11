---
title: "ReSharper 2026.3 공부 정리 | 에이전트가 IDE 리팩터링을 직접 실행한다"
description: "Claude Agent, Codex가 VS에 추가됐다. AI가 IDE 리팩터링 도구를 직접 쓴다는 접근이 흥미로웠다."
date: 2026-11-11 09:00:00 +0900
categories: [DevTools]
tags: [jetbrains, resharper, ai-agent, visual-studio, refactoring]
image:
  path: /assets/img/thumbnail/jetbrains.png
  alt: "ReSharper 2026.3 공부 정리 | 에이전트가 IDE 리팩터링을 직접 실행한다"
---

JetBrains 블로그에서 ReSharper 2026.3 릴리스 발표를 봤다. 거창한 변화라기보다는, AI 에이전트 관련 업데이트가 있어서 훑어보게 됐다.

ReSharper는 Visual Studio에서 쓰는 .NET 개발용 플러그인이다. 코드 분석, 리팩터링, 코드 완성 같은 기능을 IDE에 추가해주는 도구다. 이번 릴리스에서 흥미로웠던 건 AI 에이전트 선택지가 늘었다는 점이었다.

## 1️⃣ 이게 뭐냐?

ReSharper 2026.2에서 Junie라는 JetBrains 코딩 에이전트가 Visual Studio에 처음 들어왔다. ReSharper에 AI 에이전트가 생긴 첫 번째 사례였다. 2026.3에서는 같은 도구 창 안에서 Claude Agent나 Codex도 선택할 수 있게 됐다. Junie, Claude Agent, Codex — 셋 중 하나를 골라서 쓰는 구조다.

여기서 세 에이전트 모두 공통으로 ReSharper의 리팩터링 스킬을 쓸 수 있다는 점이 발표에서 강조됐다. 예시로 나온 건 Rename 리팩터링이다. 에이전트가 코드를 수정하는 과정에서 Rename 같은 IDE 기능을 직접 호출할 수 있다는 뜻이다.

이번 릴리스에는 .NET 11과 C# 15 지원도 함께 들어갔다. 릴리스 당일부터 지원한다고 하는데, 자세한 변경 사항은 원문에서 더 살펴보는 편이 나을 것 같다.

## 2️⃣ 내가 든 생각

"리팩터링 스킬을 쓸 수 있다"는 문구가 처음엔 그냥 넘어가게 되는 표현이었다. 그런데 Rename이 어떻게 동작하는지 생각해봤을 때 좀 다르게 느껴졌다.

Rename 리팩터링은 단순 텍스트 교체가 아니다. IDE가 코드의 참조 관계를 분석하고, 같은 심볼이 쓰인 모든 위치를 찾아서 한꺼번에 수정해주는 작업이다. 타입 범위를 이해하고 충돌 여부도 확인하면서 진행한다. 그 작업을 에이전트가 직접 실행한다는 건, AI가 텍스트를 편집하는 게 아니라 IDE의 분석 도구를 호출하는 것에 가깝다.

👉🏻 AI가 "코드를 직접 쓴다"에서 "IDE가 가진 도구를 쓴다"로 넘어가는 흐름인 것 같다.

> 💡 **여기서 드는 질문?**
> 에이전트가 IDE 기능을 직접 실행할 수 있다면, 에이전트가 어디까지 작업할 수 있는지를 어떻게 파악할 수 있을까?

Junie, Claude, Codex를 같은 창에서 고른다는 것도 흥미롭게 읽혔다. 에이전트마다 잘하는 게 다를 테니 작업에 따라 선택하는 경험이 될 것 같다. 디자이너 관점에서 보면 이 선택지가 오히려 복잡하게 느껴질 수도 있겠다 싶었다. 셋을 나열했을 때 어떤 걸 쓸지 판단 기준이 명확하지 않으면 선택 피로가 생기기 쉬우니까.

## 3️⃣ 앞으로 어떻게 쓸까?

ReSharper는 Visual Studio 환경에서 쓰는 도구라 아직 직접 닿아본 적은 없다. 다만 "에이전트에게 IDE 고유의 도구를 스킬로 주는 방식"이라는 접근은 다른 개발 환경에서도 비슷한 패턴으로 나올 것 같다.

JetBrains Air나 Cursor, Claude Code 같은 도구들도 에이전트가 사용할 수 있는 도구 범위를 계속 넓혀가고 있다. 그 차이가 외부 MCP 연결인지, IDE 내부 기능을 직접 스킬로 쓰는 건지를 비교해서 보는 것도 재밌을 것 같다는 생각이 들었다.

## ⭐️ 마지막으로, 이번 공부에서 남은 것

공부 끝에 남은 건 "에이전트에게 어떤 방식으로 도구를 줄 수 있는가"라는 한 줄짜리 질문이다. IDE 고유의 분석 엔진을 스킬 형태로 주는 접근이 외부 연결 방식과 어떻게 다른 결과를 낼지, 아직 판단하기엔 공부가 더 필요할 것 같다.

---

> 참고 원문: [ReSharper 2026.3: Claude Agent and Codex in Visual Studio, .NET 11 and C# 15 Support, and More](https://blog.jetbrains.com/dotnet/2026/11/10/resharper-2026-3-release/)
