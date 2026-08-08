---
title: "Vercel Hermes Agent 공부 정리 | AI Gateway랑 Sandbox 통합이 뭔 말인가"
description: "Hermes Agent에 AI Gateway와 Vercel Sandbox가 붙었다는 게 구체적으로 어떤 변화인지 정리해봤다."
date: 2026-08-08 10:00:00 +0900
categories: [Frontend]
tags: [vercel, hermes, ai-gateway, sandbox, agent]
image:
  path: /assets/img/thumbnail/vercel-hermes-agent-gateway-sandbox-study.png
  alt: "Vercel Hermes Agent 공부 정리 | AI Gateway랑 Sandbox 통합이 뭔 말인가"
---

Vercel 블로그에서 Hermes Agent 업데이트 발표가 있었다. AI Gateway를 추론 레이어로 쓸 수 있게 됐고, 에이전트 명령을 Vercel Sandbox라는 클라우드 마이크로VM 안에서 실행하는 것도 지원된다는 내용이었다.

두 가지가 한꺼번에 발표돼서 처음엔 각각 무슨 역할인지 바로 와닿지 않았다. "AI Gateway가 추론 레이어라는 게 정확히 뭐지?" 싶어서 문서를 좀 더 읽어봤다.

## 1️⃣ 이게 뭐냐?

Hermes Agent는 Vercel이 만든 AI 코딩 에이전트인데, 이번에 두 가지 연결이 추가됐다.

첫째는 AI Gateway다. Vercel이 운영하는 모델 라우팅 레이어인데, 200개 이상 모델에 접근할 수 있고 토큰 비용에 별도 마크업을 붙이지 않는다. Hermes 설정 마법사에서 AI Gateway를 선택하면 실시간 모델 가용성과 가격을 바로 확인할 수 있다. 사용량은 AI Gateway 대시보드에 통합돼서 나머지 프로젝트 사용량과 함께 보인다.

둘째는 Vercel Sandbox다. 기본 설정에서는 에이전트 명령이 로컬에서 실행되는데, `terminal.backend`를 `vercel_sandbox`로 설정하면 클라우드 마이크로VM에서 실행된다. node24(기본값), node22, python3.13 런타임을 지원한다. 로컬 개발 시에는 `vercel link`와 `vercel env pull`로 OIDC 토큰을 받아 쓴다.

## 2️⃣ 내가 든 생각

"에이전트가 어떤 모델을 쓸지 직접 고를 수 있다"는 게 생각보다 흥미로웠다. 코딩 에이전트를 생각하면 Claude나 GPT가 고정돼 있는 구조를 떠올리게 되는데, 200개 이상 모델 중 선택한다는 건 관점이 좀 다른 것 같았다.

👉🏻 그보다 더 인상적이었던 건 Sandbox 옵션이었다. "내 머신에서 실행되느냐, 클라우드에서 실행되느냐"가 설정 하나로 바뀐다는 건 생각보다 큰 차이인 것 같았다. 에이전트가 실수로 예상 밖의 파일을 건드려도 로컬에는 영향이 없으니까.

> 💡 **여기서 드는 질문?**
> 처음엔 Sandbox가 안전해 보이는데, 매번 클라우드에서 실행하면 속도나 비용 차이가 날 것 같다. 어느 시점에 로컬로 돌아오는 게 맞는 건지, 그 판단 기준이 궁금해졌다.

디자이너 관점에서 보면, Sandbox는 도구의 "부작용 범위"를 격리하는 방식에 가까운 것 같았다. UX를 설계할 때 위험한 액션을 되돌릴 수 있게 만들거나 미리보기 단계를 두는 것처럼, 에이전트 명령을 격리된 환경에서 실행하면 실수의 여파를 제한할 수 있다. 에이전트 도구가 더 많이 쓰이게 되면 이런 격리 설계가 중요한 고민이 될 것 같다.

## ⭐️ 마지막으로, 디자이너 입장에서 공부하며 느낀 점

정리해보니, AI Gateway 통합보다 Sandbox 옵션 쪽이 더 크게 와닿았다. 모델이 많아지는 건 선택지의 문제고, 실행 환경이 격리되는 건 에이전트를 얼마나 신뢰할 것이냐의 문제에 가까운 것 같았다. 공부 끝에 남은 건, "어디서 실행되느냐"가 에이전트 도구에서 꽤 핵심적인 변수일 수 있다는 한 줄이었다.

---

> 참고 원문: [Vercel AI Gateway and Vercel Sandbox now available on Hermes Agent](https://vercel.com/changelog/vercel-ai-gateway-and-vercel-sandbox-now-available-on-hermes-agent)
