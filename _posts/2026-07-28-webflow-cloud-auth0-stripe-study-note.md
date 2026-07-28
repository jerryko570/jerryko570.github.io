---
title: "Webflow Cloud에 Auth0 + Stripe 붙이는 흐름 공부 정리"
description: "Webflow Cloud에서 Auth0 v4로 인증하고 Stripe로 결제 받는 흐름을 공부하면서 정리했다."
date: 2026-07-28 09:00:00 +0900
categories: [Design]
tags: [webflow, auth0, stripe, webflow-cloud]
image:
  path: /assets/img/thumbnail/webflow-cloud-auth0-stripe-study-note.png
  alt: "Webflow Cloud에 Auth0 + Stripe 붙이는 흐름 공부 정리"
---

Webflow 블로그를 보다가, Webflow Cloud에 Auth0 인증과 Stripe 결제를 같이 붙이는 글이 올라왔다. 인증이랑 결제를 하나의 앱에서 연결하는 흐름이 어떻게 생겼는지 궁금해서 공부해봤다.

이 글에서 다루는 건 Webflow Cloud 위에서 돌아가는 Next.js 앱이다. Auth0로 로그인을 붙이고, 로그인한 유저가 Stripe Checkout으로 결제하는 경로를 만드는 과정이다. Auth0가 v4로 올라가면서 설정 방식이 달라진 게 있어서, 그 부분이 특히 눈에 들어왔다.

## 1️⃣ Auth0 v4에서 달라진 점

예전 v3에서는 `/api/auth/[auth0]/route.ts` 파일을 따로 만들어야 인증 라우트가 생겼다. 로그인, 로그아웃, 콜백 경로 같은 게 여기에 묶였다. v4에서는 이 파일이 없어지고, `middleware.ts` 하나에서 처리된다.

이유는 Webflow Cloud 환경 때문인 것 같다. Webflow Cloud는 Cloudflare Workers 위에서 돌아가는 엣지 런타임 환경인데, Auth0 v4는 여기에 맞게 설계된 것 같다. 기존 v3는 별도 설정이 필요했는데, v4에서는 `middleware.ts`가 자동으로 마운트된다는 설명이었다.

세션 확인 코드는 이렇게 생겼다.

```typescript
const session = await auth0.getSession();
if (!session) redirect("/auth/login?returnTo=/dashboard");
```

로그인하지 않은 유저를 `/auth/login`으로 보내면서, `returnTo` 파라미터로 원래 가려던 경로를 넘긴다. 디자이너 관점에서 이 흐름이 꽤 흥미로웠다. 결제 페이지로 들어오려다 로그인 창으로 튕긴 유저가, 로그인 후 다시 결제 페이지로 돌아오는 처리니까. `returnTo` 하나가 없으면 유저는 로그인 후 홈화면으로 떨어지게 된다.

## 2️⃣ Stripe와 연결되는 구조

인증이 확인되면 Stripe Checkout 세션을 만드는 단계로 넘어간다. 핵심은 Auth0에서 받은 사용자 ID(`session.user.sub`)를 `client_reference_id`로 Stripe에 넘기는 것이다.

```typescript
const checkoutSession = await stripe.checkout.sessions.create({
  client_reference_id: session.user.sub,
});
```

결제가 완료되면 Stripe가 서버로 웹훅을 보내는데, 이때 이 ID가 그대로 돌아온다. "어느 유저가 결제를 마쳤는지"를 파악하는 키가 되는 셈이다. Auth0와 Stripe는 서로 다른 시스템인데, 이 ID 하나로 연결되는 방식이 인상에 남았다.

👉🏻 웹훅 처리 부분에서 특이한 게 하나 있었다. 보통은 `stripe.webhooks.constructEvent()`를 쓰는데, 여기서는 `constructEventAsync()`를 쓴다. Cloudflare Workers의 WebCrypto API가 비동기식이라서, 동기 버전이 동작하지 않기 때문이라는 설명이었다.

> 💡 **처음엔 왜 다른 메서드를 쓰나 싶었는데**, 같은 라이브러리도 실행 환경마다 써야 하는 방식이 달라질 수 있다는 게 이번 공부에서 새로 알게 된 부분이었다. Node.js에서는 동기 API가 되는데, 엣지 런타임에서는 그게 안 된다. 이런 차이를 미리 알지 못하면 왜 안 되는지 한참 찾아야 할 것 같다는 생각이 들었다.

## ⭐️ 마지막으로

정리해보니 "Auth0랑 Stripe를 어떻게 붙이나"라기보다, 결국 **두 시스템이 공유할 ID를 어디서 만들고 어떻게 넘기냐**에 가까운 문제였다. 인증 시스템에서 만들어진 `user.sub`가 결제 흐름을 거쳐 웹훅으로 돌아오는 구조. 개별 기능보다 그 연결 방식이 더 기억에 남는다.

---

> 참고 원문: [How to add authentication and payments to a Webflow Cloud app with Auth0 and Stripe](https://webflowmarketingmain.com/blog/auth-payments-webflow-cloud-auth0-stripe)
