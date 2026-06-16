---
title: "Workflow SDK inflight cancellation 공부 정리 | AbortSignal이 step 경계를 넘는다"
description: "Vercel Workflow SDK 5 베타에 추가된 AbortController/AbortSignal 지원 발표를 읽고 정리한 학습 노트."
date: 2026-06-16 10:00:00 +0900
categories: [Frontend]
tags: [vercel, workflow-sdk, abortsignal, web-api]
image:
  path: /assets/img/thumbnail/workflow-sdk-inflight-cancellation-study-note.png
  alt: "Workflow SDK inflight cancellation 공부 정리 | AbortSignal이 step 경계를 넘는다"
---

Vercel 블로그에 Workflow SDK 5 베타 업데이트가 올라왔다. 이번에 추가된 건 AbortController와 AbortSignal 지원이다. 브라우저에서 fetch 요청을 취소할 때 쓰던 그 표준 Web API가, 이번엔 워크플로우와 step 경계를 넘어 동작한다는 발표였다.

처음엔 가볍게 넘기려 했다. 근데 "서스펜션을 거쳐도 취소 상태가 유지된다"는 표현이 걸렸다. 단순히 API를 래핑한 게 아니라는 생각이 들어서 발표를 좀 더 읽어봤다.

## 1️⃣ 이게 뭐냐?

AbortController와 AbortSignal은 원래 브라우저에서 비동기 작업을 취소할 때 쓰는 표준 Web API다. 컨트롤러를 만들고, 거기서 signal을 꺼내 fetch에 넘긴 뒤, `controller.abort()`를 호출하면 진행 중인 요청이 중단된다. fetch 튜토리얼에서 한 번쯤은 마주치는 패턴이다.

Workflow SDK에서도 이제 같은 방식이 통한다. 워크플로우 안에서 컨트롤러를 생성하고, signal을 하나 이상의 step에 넘기면 된다. `abort()`를 호출하면 그 signal을 받은 step들이 취소 처리를 받는다.

발표에서 눈에 걸렸던 표현은 "signal stays durable across suspensions and deterministic replay"였다. Workflow는 특성상 중간에 일시 정지됐다가 나중에 별도 함수 호출로 재개될 수 있는데, 이 서스펜션 구간을 거쳐도 취소 상태가 그대로 유지된다. 단순히 메모리에 들고 있는 게 아니라, 지속성 있게 저장된다는 뜻에 가깝다.

또 하나, "협력적(cooperative) 취소"라는 개념이 나왔다. step이 signal을 직접 확인하거나, AbortSignal을 지원하는 API에 그 signal을 넘겨야 실제로 멈춘다. 발표에서 제시한 활용 예시는 이런 것들이었다. 타임아웃이 먼저 끝났을 때 느린 step을 중단하거나, 병렬 요청 중 첫 번째가 성공하면 나머지를 취소하거나, 외부 조건이 바뀌었을 때 파이프라인 전체를 멈추는 것들이다.

## 2️⃣ 내가 든 생각

AbortController를 처음 배울 때는 fetch 하나를 멈추는 도구 정도로 이해했다. 근데 워크플로우 레벨에서 쓰면 signal 하나가 step 여러 개에 걸쳐 전파되고, 서스펜션을 거쳐도 유효하다. 같은 Web API인데 동작 범위가 상당히 달라진다.

👉🏻 "cooperative"라는 단어가 특히 인상적이었다. 강제로 종료하는 게 아니라, 각 step이 스스로 signal을 확인하고 멈추는 구조다. signal을 넘기는 것만으로는 부족하고, step 내부에서 그 signal을 실제로 읽는 코드가 있어야 취소가 일어난다. 개발 중에 signal을 넘겼는데 step 안에서 무시하면 취소가 안 일어나는 셈이라서, 주의가 필요한 부분이기도 하다.

> 💡 **여기서 드는 질문?** step이 signal을 확인하지 않는 경우, 호출자는 이 상태를 어떻게 인지할 수 있을까? 취소를 요청했는데 step이 계속 실행되는 경우를 어떻게 추적하는 건지 궁금해졌다.

디자이너 관점에서 보면, 취소 처리는 보통 UI 레벨의 문제였다. 로딩 중 취소 버튼을 달거나, 오래 걸리는 요청을 사용자가 멈출 수 있게 하는 것들. 근데 서버 워크플로우 레벨에서도 비슷한 구조가 생겼다는 게 흥미로웠다. "어디서 취소를 책임지냐"는 질문이 클라이언트 UI뿐 아니라 서버의 작업 흐름에도 해당된다는 게 와 닿았다.

## ⭐️ 마지막으로, 프론트엔드 공부하면서 느낀 것

결국 이번 업데이트에서 인상적인 건 기능의 새로움이 아니라, 이미 알던 API가 다른 레이어에서 그대로 쓰인다는 점이었던 것 같다. fetch에서 배운 AbortSignal 패턴이 서버 워크플로우에도 동일하게 적용된다는 건, 새 API를 배우는 것보다 기존 API의 적용 범위가 넓어지는 방향에 가까운 이야기였다. 배우는 입장에서는 그게 더 반가운 방식이었다.

---

> 참고 원문: [Workflow SDK now supports inflight cancellation](https://vercel.com/changelog/workflow-sdk-now-supports-inflight-cancellation)
