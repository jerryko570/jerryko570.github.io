---
title: "GitHub Copilot 과금 방식 공부 정리 | 결국 뭘 사는 걸까"
description: "Copilot이 AI Credits 기반 과금으로 바뀌었다. raw API랑 어떻게 다른 건지 공부하면서 든 생각."
date: 2026-07-23 10:00:00 +0900
categories: [DevTools]
tags: [copilot, github, ai-coding, llm, api]
image:
  path: /assets/img/thumbnail/copilot-vs-raw-api-study-note.png
  alt: "GitHub Copilot 과금 방식 공부 정리 | 결국 뭘 사는 걸까"
---

GitHub 블로그에서 흥미로운 글을 읽었다. "Copilot vs. raw API access: What are you actually paying for?" — 제목부터 좀 찔렸다. 프론트엔드 공부하면서 AI 코딩 도구들을 막연하게 쓰고 있었는데, 돈 내고 쓰는 거라면 뭘 사는 건지 정도는 알아둬야 할 것 같아서 찬찬히 읽어봤다.

생각보다 단순한 가격 비교 글이 아니었다. "Copilot을 쓰면 raw API랑 뭐가 다른가"를 꽤 구체적으로 풀어놓은 글이었는데, 정리하면서 드는 생각이 있어서 남겨둔다.

## 1️⃣ 이게 뭐냐?

Copilot이 과금 방식을 바꿨다. 기존에는 구독료에 거의 다 포함됐는데, 이제는 AI Credits 시스템으로 나뉜다. 코드 완성이나 Next Edit Suggestions 같은 기본 기능은 유료 플랜에 계속 포함이고, Chat이나 에이전틱 작업은 크레딧 차감 방식이다. 입력·출력·캐시 토큰 기준으로, 선택한 모델의 공시 요금대로 계산된다.

BYOK(Bring Your Own Key)도 생겼다. Anthropic, OpenAI, Google AI Studio 같은 곳의 자체 키를 연결하면 청구처를 바꿀 수 있다. Copilot의 편집기 통합은 그대로 쓰면서. 이 옵션이 흥미로웠는데, 결국 "모델은 내 걸 쓸 테니까, 나머지 하네스만 Copilot에서 빌릴게" 같은 선택이 가능해진 거라는 인상이었다.

조직 단위에서는 관리자가 대시보드에서 크레딧 사용량을 추적하고 예산을 관리할 수 있다고 한다. 이 부분은 팀 단위 도입을 고려하는 곳에서 의미 있는 변화일 것 같다.

## 2️⃣ 내가 든 생각

글에서 가장 인상적이었던 건 "raw API vs. Copilot"을 비교하는 방식이었다.

raw API는 모델 엔드포인트만 준다. 프롬프트, 라우팅, 로깅, 보안 같은 건 다 직접 만들어야 한다. 반면 Copilot은 편집기, 저장소, 터미널, 조직 정책이 이미 연결된 상태로 온다고 설명한다.

👉🏻 그러니까 Copilot을 구독한다는 건 "모델 접근권"이 아니라 "그 모델이 내 GitHub 워크플로우 안에 이미 세팅된 환경"을 사는 거라는 얘기다.

> 💡 **그럼 raw API가 더 싸다는 비교 자체가 단순하지 않은 이유가 여기 있는 걸까?**

raw API가 토큰 단가는 낮을 수 있어도, 그 위에 에이전트 하네스를 직접 구성해야 하면 그게 또 다른 비용이 된다. 글에서는 Copilot의 에이전트 하네스가 평가에서 더 적은 토큰을 사용한다고도 했는데, 공부한 내용 기준으로는 그 구체적인 수치까지는 확인하기 어려웠다. 자세한 건 원문을 직접 봐야 할 것 같다.

디자이너 입장에서 보면, 이게 결국 "툴킷을 직접 조합할 거냐, 이미 세팅된 환경을 살 거냐"는 질문이랑 비슷하게 느껴졌다. 개발 도구에서도 같은 논쟁이 나온다는 게 흥미로웠다.

## ⭐️ 마지막으로, 이 글을 공부하며 남는 생각

결국 핵심은 모델 자체가 아니라, 그 모델이 어떤 환경에 연결돼 있는가에 있는 것 같다.

"비싼 모델이냐 싼 모델이냐"가 아니라 "그 모델이 내 작업 흐름과 얼마나 이미 이어져 있는가" — Copilot이 raw API보다 비쌀 수 있는 이유이고, 동시에 쓸 만한 이유도 거기 있는 것 같다.

---

> 참고 원문: [Copilot vs. raw API access: What are you actually paying for?](https://github.blog/ai-and-ml/github-copilot/copilot-vs-raw-api-access-what-are-you-actually-paying-for/)
