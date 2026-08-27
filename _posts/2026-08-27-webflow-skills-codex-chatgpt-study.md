---
title: "Webflow Skills 공부 정리 | Codex랑 ChatGPT에서 뭐가 달라지는 걸까"
description: "Webflow가 Codex와 ChatGPT에 통합됐다는 발표를 읽고, Skills 추상화가 뭔지 정리해봤다."
date: 2026-08-27 10:00:00 +0900
categories: [Design]
tags: [webflow, codex, chatgpt, mcp, ai-tools]
image:
  path: /assets/img/thumbnail/webflow-skills-codex-chatgpt-study.png
  alt: "Webflow Skills 공부 정리 | Codex랑 ChatGPT에서 뭐가 달라지는 걸까"
---

Webflow 블로그에서 Codex·ChatGPT 통합 발표가 있었다. 처음엔 "또 AI 통합 소식이구나" 싶었는데, 읽다 보니 Skills라는 개념이 눈에 들어왔다.

단순히 "MCP 연동됐어요" 수준이 아니라, 내장 Skills라는 추상화 레이어를 따로 만들었다는 점이 좀 달랐다. 이전 Claude Connector 발표 때와 구조가 비슷한 것 같기도 했지만, 이번엔 좀 더 구체적인 형태가 보였다. 이게 기존 MCP 연동과 실제로 뭐가 다른 건지 궁금해서 공부해봤다.

## 1️⃣ 이게 뭐냐?

Webflow가 OpenAI의 Codex에 공식 통합됐다. ChatGPT에서도 쓸 수 있고, 두 플랫폼 모두에 내장 Skills가 포함됐다. 기술 기반은 올여름 출시된 Webflow MCP 2.0이라고 한다.

Skills는 네 가지 영역으로 정리된다. 사이트 SEO·AEO 기회, 접근성 이슈, 깨진 링크를 점검하는 감사 기능. CMS 컬렉션 생성과 콘텐츠 항목 수정·재구성. 프로덕션 배포 전 커스텀 코드를 검토하는 검증 기능. 그리고 프로젝트 스캐폴딩, 컴포넌트 생성, 확장 프로그램 배포 같은 개발자용 워크플로우.

이 Skills들이 특이한 건 사용자가 API를 직접 알 필요가 없다는 점이다. "내 사이트에서 SEO 기회를 찾아줘"라고 자연어로 말하면, AI가 알아서 맞는 Skill을 골라 실행한다. Skills은 또 "내 실제 Webflow 사이트의 맥락"에 접근할 수 있다고 한다. 그냥 일반적인 AI 지식이 아니라, 연결된 워크스페이스를 기준으로 동작하는 방식이다.

MCP를 직접 다루는 것보다 입문 장벽이 낮아지는 건 맞는데, 동시에 AI가 내 사이트에 직접 접근한다는 뜻이기도 하다. 이 부분에서 자연스럽게 질문이 생겼다.

## 2️⃣ 내가 든 생각

디자이너 입장에서 보면 CMS 콘텐츠 관리 쪽이 가장 눈에 들어왔다. 지금까지 Webflow CMS는 에디터 UI를 직접 써야 했는데, "이 컬렉션 항목을 전부 수정해줘" 같은 명령이 자연어로 된다면 반복 작업 흐름이 꽤 달라질 수도 있겠다 싶었다. 특히 디자이너가 개발자 없이 CMS를 다루는 상황이라면 더 그렇다.

👉🏻 Skills 추상화의 핵심은 결국 "책임 범위"인 것 같다. 사용자에게는 API를 모르게 해준다는 편의를 주는데, 그 대신 Skill이 어디까지 실행할 수 있는지를 사용자가 파악하고 있어야 한다. 그걸 모르면 의도보다 많은 것이 바뀔 수 있다.

> 💡 **여기서 드는 질문?**
> CMS 항목을 잘못 수정했을 때 undo가 얼마나 쉬울까. 자동화 도구일수록 실수의 영향 범위가 넓어지는 경향이 있어서, 이 부분이 계속 마음에 걸렸다.

MCP 2.0 위에 Skills 추상화를 얹은 구조 자체는 합리적인 레이어 분리처럼 느껴졌다. 사용자 인터페이스와 실제 API 호출을 분리한 건 디자인 관점에서 봐도 익숙한 패턴이다. 다만 공부한 내용 기준으론, 각 Skill이 얼마나 좁은 책임을 갖도록 설계됐는지는 아직 파악하지 못했다.

## ⭐️ 마지막으로, 디자이너 관점에서 공부하며 느낀 점

정리해보니 이번 발표의 포인트는 Codex 통합 그 자체보다 Skills 레이어에 있는 것 같다. "AI에게 말로 시키면 알아서 적절한 API를 고른다"는 구조를 공식 파트너십 형태로 내놨다는 게, Webflow가 AI 도구 생태계 안에서 어떤 자리를 잡으려는지를 보여주는 것 같았다.

공부 끝에 남은 건 이 한 줄이다 — 자동화를 편하게 만들수록, 내부에서 무슨 일이 일어나는지를 파악하는 게 더 중요해지는 것 같다.

---

> 참고 원문: [Webflow is now available in Codex and ChatGPT](https://webflowmarketingmain.com/blog/webflow-is-now-available-in-codex-and-chatgpt)
