---
title: "Decisions API 공부 정리 | AI에게 판단만 맡기는 방식"
description: "Vercel AI Gateway에 추가된 Decisions API를 공부하면서, 텍스트 생성 모델과 결정 모델의 차이가 어떤 의미인지 정리해봤다."
date: 2026-10-08 12:00:00 +0900
categories: [Frontend]
tags: [vercel, ai-gateway, openai, decisions-api]
image:
  path: /assets/img/thumbnail/vercel.png
  alt: "Decisions API 공부 정리 | AI에게 판단만 맡기는 방식"
---

Vercel changelog를 보다가 Decisions API가 AI Gateway에 추가됐다는 글이 있었다. "결정 모델"이라는 표현이 처음이라 뭔지 궁금해서 문서를 찾아봤다.

이전까지 내가 알던 AI API는 단순한 구조였다. 텍스트를 넣으면 텍스트가 나온다. 그런데 Decisions API는 방향이 달랐다. 텍스트를 생성하는 게 아니라, 입력에 대해 타입이 정해진 답을 돌려준다. 응답이 확률이거나, 선택지 중 하나거나, 점수다.

## 1️⃣ 이게 뭐냐?

Decisions API는 공유된 입력에 대해 여러 질문을 한 번에 던지고, 각 질문마다 정해진 형태의 답을 받는 방식으로 이해했다. 지원하는 질문 유형은 세 가지다:

- **predicate**: 예/아니오 판단 (AI SDK에서는 `boolean`으로 부름)
- **choice**: 주어진 선택지 중 하나 고르기
- **score**: 숫자 점수 매기기

예를 들어 고객 문의 "환불해달라"가 들어왔을 때, `choice` 질문으로 이게 billing 팀 문의인지 technical 팀 문의인지 판단하게 할 수 있다. 기존 언어 모델처럼 "이 고객은 환불을 원하는 것 같습니다"를 생성하는 게 아니라, `billing`이라는 선택지 하나만 돌려준다.

같은 입력에 대해 여러 질문을 동시에 보낼 수 있는 것도 흥미로웠다. "긴급한 문의인가?"(boolean), "어느 팀 담당인가?"(choice), "심각도는?"(score)를 한 번의 요청으로 받을 수 있다. 각 답변은 `answers` 배열에 질문 순서대로 들어온다.

모델 ID도 분리되어 있다. `openai/gpt-6-luna`는 언어 모델, `openai/gpt-6-luna-decisions`는 결정 모델이다. 엔드포인트도 `/v1/decisions`로 따로 있고, 과금도 각각 다르다. OpenAI SDK에서는 `decisions.create()`로 호출하고, AI SDK에서는 실험적 기능인 `experimental_decide`를 쓴다.

## 2️⃣ 내가 든 생각

처음엔 "그냥 프롬프트를 잘 짜서 JSON으로 받으면 안 되나?"라는 생각이 먼저 들었다. 근데 문서를 읽다 보니 생각이 조금 달라졌다.

기존 텍스트 생성 모델로 판단을 받으면, 응답 형태 자체가 열려있다. 프롬프트가 조금만 바뀌어도 결과 형태가 달라질 수 있고, 예상치 못한 텍스트가 섞여 나오기도 한다. 반면 결정 모델은 질문 유형 자체를 타입으로 고정한다. `choice`면 반드시 선택지 중 하나만 나온다.

👉🏻 라우팅, 트리아지, 가드레일처럼 "판단은 필요하지만 자유로운 생성은 필요 없는" 자리에 AI를 끼워 넣는 방식이 훨씬 예측 가능해진다는 점이 인상적이었다.

> 💡 **여기서 드는 질문?**
>
> 질문의 타입을 미리 정한다는 건 "AI에게 무엇을 물을 것인가"를 사전에 설계해야 한다는 뜻이다. 이게 API 계약을 정의하거나 컴포넌트 props를 설계하는 것과 비슷한 작업 아닐까?

디자이너 입장에서 보면, 어떤 입력을 받고 어떤 출력을 낼지를 명시적으로 정하는 건 꽤 익숙한 작업이다. 컴포넌트의 책임 범위를 정하는 것처럼, AI에게도 "이 부분만 담당해"라고 경계를 긋는 개념이 가능하다는 게 내가 이해한 방향이었다.

## ⭐️ 마지막으로, 공부하면서 남은 인상

정리해보니 Decisions API는 AI를 어떻게 쓸 것인가라기보다, 어떤 자리에 끼워 넣을 것인가에 가까운 얘기였다. 자유로운 텍스트 생성과 구조화된 판단이 별도의 도구로 나뉘는 방향이, 지금 단계에서 내가 이해한 그림이다.

---

> 참고 원문: [OpenAI Decisions API now available on AI Gateway](https://vercel.com/changelog/openai-decisions-api-now-available-on-ai-gateway)
