---
title: "GitHub Copilot에게 코드베이스 가르치기 | 설정 방법 공부 정리"
description: "custom instructions, skills, agents, MCP — Copilot이 매번 설명을 요구하지 않도록 저장소에 맥락을 담는 네 가지 방법"
date: 2026-10-13 10:00:00 +0900
categories: [DevTools]
tags: [github-copilot, mcp, ai-tools, custom-agents]
image:
  path: /assets/img/thumbnail/github.png
  alt: "GitHub Copilot에게 코드베이스 가르치기 | 설정 방법 공부 정리"
---

GitHub Blog에서 Copilot에게 코드베이스를 이해시키는 방법을 소개하는 글을 읽었다. 제목은 초급자 대상이지만, 내용은 꽤 실용적인 설정 방법들이었다.

매 작업마다 "우리 프로젝트는 Next.js 써, 이 네이밍 규칙 따라"를 반복 설명하는 대신, 그 정보를 저장소 파일에 한 번 써두면 Copilot이 알아서 참조한다는 게 이 글의 핵심이다.

## 1️⃣ 이게 뭔가?

소개된 방법은 네 가지다.

**Custom instructions** — `.github/copilot-instructions.md`에 전체 규칙을 적어두는 방식이다. 아키텍처나 네이밍 규칙처럼 저장소 전반에 적용되는 내용을 담는다. 파일별로 다른 지침이 필요하면 `.github/instructions/` 폴더를 쓰고 `applyTo` 필드로 대상을 지정하면 된다.

**Agent skills** — `.github/skills/` 아래 폴더를 만들고 `SKILL.md`를 둔다. 테스트와 린트를 어떻게 실행하는지, 무엇을 점검하는지를 써두면 Copilot이 필요할 때 꺼내 쓴다. `SKILL.md`의 description으로 스킬 적용 여부를 판단한다는 구조가 흥미로웠다.

**Custom agents** — `.github/agents/`에 에이전트 프로필을 정의한다. 목적, 사용할 도구, 프로젝트 맥락을 담는 구조다. 접근성 점검처럼 여러 파일에 걸친 반복 작업에 적합한 방식이라고 했다.

**MCP servers** — 외부 도구나 서비스를 연결하는 방식이다. Playwright MCP 서버를 연결하면 Copilot이 브라우저에서 앱을 직접 열고 조작해서 기능을 검증할 수 있다고 한다.

## 2️⃣ 내가 든 생각

AI 코딩 도구를 쓸 때 매번 같은 배경을 설명하는 게 번거롭다고 느낀 적이 있었다. "이 프로젝트는 TypeScript strict 모드야, App Router 써" 같은 걸 매번 프롬프트 앞에 붙이는 식이었는데, 이 접근은 그 반복을 파일로 빼내는 것에 가까운 것 같았다.

👉🏻 skills와 agents를 구분하는 방식이 흥미로웠다. skills는 "이 작업은 이렇게 실행해"라는 절차 정의, agents는 "이런 목적으로 움직이는 역할"에 가까운 것 같았다. 처음엔 비슷해 보였는데 읽어보니 결이 달랐다.

디자이너 입장에서 보면 Custom instructions는 디자인 시스템 문서와 비슷한 역할 같았다. "버튼은 이 스타일 써, 이 패턴 따라"를 문서화해두는 것처럼, 코딩 맥락도 파일로 보관하는 개념이니까.

> 💡 **여기서 드는 질문?**
> 이 파일들을 직접 유지보수해야 한다는 게 걸렸다. 처음 설정할 때랑 몇 달 뒤 상태가 달라지면, Copilot은 오래된 파일을 그대로 참조할 텐데 — 그 간극은 누가 관리하는 걸까?

## 3️⃣ 어디서 먼저 닿아올 것 같냐면

글에서 "작게 시작하라"고 권한다. 가장 자주 반복해서 설명하는 규칙 하나를 골라 `.github/copilot-instructions.md`에 써보는 것부터.

공부 중인 입장에서 skills 설정이 특히 눈에 들어왔다. 테스트 명령어나 lint 실행 방법을 미리 정의해두면, 다시 돌아올 때 "이걸 어떻게 돌리더라" 하고 찾는 수고가 줄어들 것 같다. 프로젝트 세팅 메모 용도로도 쓸 수 있겠다는 생각이 들었다.

## ⭐️ 마지막으로, 디자이너가 공부하면서 느낀 점

결국 이 네 가지 모두 "프로젝트 지식을 어디에 보관하는가"에 가까운 이야기였다. AI 프롬프트로 해결하던 걸 저장소 파일로 옮긴 것. 팀이라면 같은 맥락을 공유하기도 쉬워진다는 게 합리적으로 느껴졌다.

공부 끝에 남은 건, "Copilot을 더 잘 쓰는 법"이 아니라 "프로젝트 지식을 어떻게 관리할 것인가"라는 한 줄짜리 질문이었다.

---

> 참고 원문: [GitHub Copilot app for Beginners: How to teach Copilot about your codebase](https://github.blog/ai-and-ml/github-copilot/github-copilot-app-for-beginners-how-to-teach-copilot-about-your-codebase/)
