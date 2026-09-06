---
title: "Cursor Cloud Agents 공부 정리 | Vercel Sandbox에서 에이전트 돌리기"
description: "Cursor Cloud Agents가 Vercel Sandbox에서 실행되는 구조를 공부하면서 에이전트 격리와 실행 환경에 대해 처음으로 구체적으로 생각해봤다."
date: 2026-09-06 10:00:00 +0900
categories: [Frontend]
tags: [cursor, vercel, ai-agents, sandbox]
image:
  path: /assets/img/thumbnail/cursor-cloud-agents-vercel-sandbox-study.png
  alt: "Cursor Cloud Agents 공부 정리 | Vercel Sandbox에서 에이전트 돌리기"
---

Vercel changelog를 훑다가 눈에 띄는 공지가 있었다. Cursor Cloud Agents를 Vercel Sandbox에서 실행할 수 있게 됐다는 내용이었다. 처음엔 인프라 관련 발표겠거니 싶어 넘기려 했는데, 조금 읽어보니 AI 에이전트가 코드를 실제로 실행하는 방식 자체에 대한 이야기라는 걸 알게 됐다.

어떤 구조인지 공부하면서 정리해봤다.

## 1️⃣ 이게 뭐냐?

Cursor Cloud Agents는 AI가 저장소를 직접 클론하고, 파일을 수정하고, 테스트를 실행하는 방식으로 코딩 작업을 처리한다. 지금까지는 이 작업이 Cursor의 자체 서버에서 돌아갔는데, 이번 발표로 Vercel Sandbox를 대신 실행 환경으로 쓸 수 있게 됐다.

핵심은 에이전트 요청마다 **Firecracker microVM**이라는 격리된 가상 환경이 생긴다는 점이다. 작업이 끝나면 그 환경은 사라진다. 이 방식을 scale-to-zero라고 부르는데, 장기 운영하는 VM 없이 요청이 있을 때만 워커가 생기는 구조다.

전체 흐름은 Vercel Functions와 Vercel Workflow가 제어한다. 큐에 쌓인 에이전트 요청을 가져오고, 워커를 프로비저닝하고, 세션을 감시하고, 정리까지 자동으로 처리한다. Cursor는 에이전트 로직과 추론 루프만 담당하고, 실행 환경 자체는 Vercel이 제공하는 구조다.

이 연결은 Self-Hosted Machines API라는 인터페이스를 통해 이뤄진다. 실행 환경을 외부에서 제공할 수 있도록 Cursor가 열어둔 API인데, 이번 Vercel Sandbox 연동은 그 위에서 구현된 것에 가까운 것 같았다. Cursor Enterprise 플랜이 필요하다는 제약도 있다.

## 2️⃣ 내가 든 생각

공부하면서 가장 흥미로웠던 건 "격리"라는 개념이었다. 에이전트가 코드를 실행한다는 건, 그 환경이 다른 세션이나 외부와 섞이지 않아야 한다는 걸 전제로 한다는 생각이 들었다. 요청마다 새 VM이 뜨고 끝나면 사라지는 방식은 그 요구에 대한 한 가지 대답처럼 보였다.

👉🏻 각 세션에 **단기 자격증명**이 부여된다는 부분도 눈에 들어왔다. AI 에이전트가 저장소에 접근할 때 어떤 권한을 가져야 하는지, 생각보다 복잡한 문제라는 걸 처음으로 실감했다. "단기"라는 단어 하나에 꽤 많은 설계 고민이 담겨 있을 것 같았다.

내가 이해한 바로는, 이 구조의 가장 큰 의미는 "에이전트가 코드를 건드리는 환경을 누가 책임지는가"라는 질문에 대한 답이 생겼다는 점인 것 같다. 도구 안에 통합되어 있던 실행 환경이 명시적인 계층으로 분리된 것에 가까운 느낌이었다.

> 💡 **여기서 드는 질문?**
> 이런 실행 환경 계층이 앞으로 다른 AI 코딩 도구들에서도 표준처럼 자리 잡을까, 아니면 각자 다른 방식으로 가져갈까?

## 3️⃣ 앞으로 어떻게 쓸까?

일단 이 기능은 Cursor Enterprise 플랜 사용자 대상이라, 지금 내가 직접 닿아볼 수 있는 단계는 아니다. 문서에 Vercel Sandbox 레퍼런스 구현을 자기 계정에 직접 배포해볼 수 있다는 내용도 있어서, 언젠가 구조를 따라가 보고 싶다는 생각도 들었다.

공부한 내용 기준으로는, 에이전트 실행 환경이라는 개념 자체를 의식하게 됐다는 게 지금 단계에서 가져갈 수 있는 것 같다.

## ⭐️ 마지막으로, 프론트엔드 공부하는 입장에서 느낀 점

공부 끝에 남은 건 "에이전트도 결국 실행 환경이 필요하다"는 당연해 보이는 한 줄이었다. 다만 그 안에 격리, 자격증명, 내구성 재시도 같은 개념들이 쌓여 있다는 걸, 이번에 구조를 따라가면서 처음으로 구체적으로 보게 됐다. 디자이너 입장에서도, 도구가 어떤 환경 위에서 동작하는지는 그냥 넘어가기 어려운 질문인 것 같다.

---

> 참고 원문: [Cursor Cloud Agents can now run in Vercel Sandbox](https://vercel.com/changelog/run-cursor-cloud-agents-vercel-sandbox)
