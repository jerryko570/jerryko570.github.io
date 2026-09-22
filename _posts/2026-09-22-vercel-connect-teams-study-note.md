---
title: "Vercel Connect Teams 커넥터 공부 정리 | Managed가 뭘 가져가는 걸까"
description: "Vercel이 Teams 봇 연동에서 Entra 앱 등록부터 토큰 갱신까지 담당한다는 게 어떤 의미인지 공부해봤다."
date: 2026-09-22 10:00:00 +0900
categories: [Frontend]
tags: [vercel, teams, bot, connect, azure]
image:
  path: /assets/img/thumbnail/vercel.png
  alt: "Vercel Connect Teams 커넥터 공부 정리 | Managed가 뭘 가져가는 걸까"
---

Vercel 블로그에서 Microsoft Teams 커넥터 발표를 봤다. 공식 changelog 형식이라 처음엔 금방 읽고 넘어갈 생각이었는데, "Managed Connector"라는 표현이 눈에 걸렸다. 관리형이라는 게 구체적으로 뭘 뜻하는 건지 더 읽어봤다.

Teams 봇을 Azure에 직접 만들어본 적은 없지만, 자격 증명 관리가 복잡하다는 건 문서들을 보면서 알고 있었다. 그 부분에서 이번 발표가 어떤 변화를 가져오는 건지가 궁금해졌다.

## 1️⃣ 이게 뭐냐?

Vercel Connect는 외부 서비스를 앱과 연결해주는 커넥터 시스템이다. 이번에 Microsoft Teams 지원이 추가됐는데, 커넥터 하나를 만들면 조직 Teams 채널에 봇이 생기고, 채널에서 @멘션하거나 직접 메시지를 보내면 코드가 그 메시지를 받아서 응답하는 구조다. 앱이나 AI 에이전트를 Teams 채널 안에서 직접 호출하는 걸 목표로 한 것 같다.

"Managed Connector"의 핵심은 Vercel이 Entra 앱과 Azure Bot 리소스를 테넌트에 직접 등록해준다는 점이다. Azure 봇을 직접 만들 때는 보통 Entra 앱 등록 → 클라이언트 시크릿 생성 → 환경 변수 보관 → 만료 전 갱신까지 개발자가 직접 챙겨야 한다. 이 발표는 그 자격 증명 관리 흐름을 Vercel이 가져가겠다는 거다.

토큰은 필요할 때만 요청하고 자동으로 갱신된다. CLI로는 `vc connect create microsoft-teams`로 만들 수 있고, `@vercel/connect` SDK나 AI SDK 어댑터와 연결해서 쓸 수 있다. 환경별로 커넥터를 선택적으로 붙이거나 뗄 수 있고, `vc connect revoke-tokens`로 즉시 접근을 회수할 수도 있다.

## 2️⃣ 내가 든 생각

처음엔 단순한 통합 기능 추가처럼 읽었는데, 조금 더 보니 Vercel이 계속 비슷한 방향으로 움직이고 있다는 생각이 들었다. 인프라나 인증처럼 반복적으로 처리해야 하는 부분을 플랫폼이 점점 흡수하는 방향이다.

👉🏻 흥미로운 건 "편리함"이라는 말 아래에 있는 구조다. 클라이언트 시크릿을 저장하지 않아도 된다는 건 편의의 문제이기도 하지만, 동시에 그 책임이 내 손에서 Vercel 손으로 넘어갔다는 의미이기도 하다. 코드 몇 줄 줄이는 게 아니라 인증이라는 책임 경계를 다시 그리는 거라는 생각이 들었다.

> 💡 **여기서 드는 질문?** 플랫폼이 인증을 가져갔을 때, 문제가 생기면 어디서 생긴 건지 파악하기 더 어려워지는 건 아닐까?

디자인 시스템에서 컴포넌트가 어디까지 책임지고 어디서부터 사용하는 쪽이 신경 써야 하는가를 고민하는 것과 비슷한 질문이 여기서도 나왔다. 책임의 경계를 나누는 문제는 코드에서도 디자인에서도 결국 같은 종류인 것 같다.

## ⭐️ 마지막으로, 이번 내용을 공부하면서

정리해보니 핵심은 Teams 봇이 생긴다는 기능보다, Vercel이 점점 더 많은 책임을 들고 가는 방식의 변화에 있는 것 같다. `revoke-tokens`로 즉시 접근을 끊을 수 있다는 건 그 구조가 최소한 제어권은 남겨두고 있다는 거긴 하다. 문서만 본 입장에서는 그게 충분한지까지는 아직 잘 모르겠다.

---

> 참고 원문: [Vercel Connect now supports Microsoft Teams](https://vercel.com/changelog/vercel-connect-microsoft-teams)
