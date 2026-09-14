---
title: "Webflow Cloud AI 앱 공부 정리 | 배포가 하나로 묶이면 뭐가 달라질까"
description: "Webflow Cloud에서 OpenAI와 Supabase로 스트리밍 AI 채팅 앱을 만드는 튜토리얼을 정리했다"
date: 2026-09-08 09:00:00 +0900
categories: [Design]
tags: [webflow, openai, supabase, streaming, webflow-cloud]
image:
  path: /assets/img/thumbnail/openai.png
  alt: "Webflow Cloud AI 앱 공부 정리 | 배포가 하나로 묶이면 뭐가 달라질까"
---

Webflow 블로그에서 흥미로운 글을 발견했다. Webflow Cloud에서 OpenAI와 Supabase를 연결해 스트리밍 AI 채팅 앱을 만드는 튜토리얼이었다. 솔직히 처음에는 "또 AI 앱 만드는 법 글이겠지"라고 생각했는데, 읽다 보니 Webflow의 포지셔닝이 꽤 달라진 게 눈에 들어왔다.

Webflow Cloud라는 이름을 처음 접했을 때는 그냥 호스팅 서비스인 줄 알았다. 근데 정확히는 Cloudflare Workers 위에서 Next.js 앱을 직접 실행하는 구조에 가까웠다. 지금까지 Webflow로 만든 사이트를 Vercel에 따로 올리거나 백엔드를 외부 서비스로 뺐다면, 이제 그 파편화를 하나로 묶는다는 개념이다.

## 1️⃣ 이게 어떻게 돌아가나

이 튜토리얼의 핵심은 세 가지로 정리할 수 있을 것 같다.

첫 번째는 **스트리밍**이다. OpenAI 응답을 통째로 기다렸다가 보여주는 게 아니라, 토큰이 생성되는 즉시 브라우저에 흘려보내는 방식이다. `TransformStream`을 써서 서버 라우트에서 Response를 즉시 반환하고, 클라이언트에서는 `ReadableStream`으로 받아서 글자씩 화면에 붙이는 구조다. 코드 자체는 복잡하지 않은데, UX 결과는 꽤 다르다는 게 흥미로웠다.

두 번째는 **대화 히스토리 유지**다. 새로고침해도 대화가 날아가지 않도록 Supabase에 메시지를 저장하고, 매 요청마다 누적 히스토리를 OpenAI에 보내서 모델이 맥락을 잃지 않게 한다. 단, 컨텍스트가 무한정 늘어나지 않도록 최근 20개 메시지만 전달하는 식으로 잘라낸다는 부분도 정리됐다.

세 번째는 **환경변수 통합 관리**다. `OPENAI_API_KEY`, `SUPABASE_URL` 같은 값을 Webflow Settings 한 곳에서 관리할 수 있다. Cloudflare Workers가 Web 표준 Fetch API를 지원하기 때문에 OpenAI SDK도 추가 설정 없이 작동한다고 한다.

## 2️⃣ 읽으면서 든 생각

👉🏻 디자이너 관점에서 가장 눈에 들어온 건 배포 구조였다.

기존에는 Webflow 디자인 → Vercel 배포 → 별도 백엔드 서비스 식으로 맥락이 여러 곳에 흩어져 있었다. Webflow Cloud가 이걸 하나로 묶는다는 건, "에디터에서 뭔가를 바꾸면 어디까지 영향이 미치는가"를 훨씬 추적하기 쉬워진다는 의미로 읽혔다. 디자이너가 작업한 부분과 AI 백엔드가 같은 환경에서 돌아간다는 게 협업 맥락에서도 의미 있어 보였다.

스트리밍 방식의 UX 차이도 따라가다 보니 생각해볼 게 있었다. "5초 동안 아무것도 안 보이다가 갑자기 전체 텍스트가 나오는 것"과 "글자가 하나씩 나타나는 것"은 같은 속도라도 체감이 다르다. 디자이너 입장에서 로딩 상태를 어떻게 표현하느냐의 문제인데, 스트리밍 자체가 UX 패턴이 된다는 게 흥미로운 지점이었다.

> 💡 **근데 이런 질문이 생겼다.** Webflow Cloud가 Cloudflare Workers 위에서 돈다면, 기존 서버리스 함수와 어떻게 구분되는 걸까? Webflow가 그 위에 무엇을 더하는 건지가 아직 잘 안 잡힌다.

## ⭐️ 마지막으로, 이번 공부에서 남은 것

결론까지는 못 내렸지만, Webflow가 "노코드 웹 빌더"에서 "풀스택 배포 환경"으로 확장하는 방향을 읽고 있다는 정도가 지금 든 생각이다. 디자이너가 이 파이프라인을 얼마나 직접 다룰 수 있는지는 공부한 내용만으론 아직 판단하기 어렵다. 다만 배포와 디자인 사이 거리가 줄어드는 방향 자체는, 앞으로 어떻게 달라지는지 좀 더 지켜보고 싶다.

---

> 참고 원문: [How to build an AI-powered app on Webflow Cloud with OpenAI and Supabase](https://webflowmarketingmain.com/blog/ai-app-webflow-cloud-openai-supabase)
