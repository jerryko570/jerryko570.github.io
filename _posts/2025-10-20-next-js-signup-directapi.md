---
layout: post
title: "[Next.js] 회원가입(Signup)과 Direct API Flow 정리"
date: 2025-10-20 00:00:00 +0900
categories: [frontend, nextjs]
tags: [nextjs, signup, api, authentication, fetch, typescript]
series: nextjs-auth
image: /assets/img/thumbnail/next-js.png
---

## **1. Next.js로 회원가입 기능을 만들며 느낀 점**
- 코드잇 두 번째 팀 프로젝트에서는 풀스택 웹 프레임워크인 Next.js를 사용해 공고 사이트를 제작했다.
여러 역할 중 나는 회원가입(Signup) 영역을 맡았고, 코드잇에서 제공한 API 명세서를 해석해
payload 구조를 만들고, 서버와 직접 통신하는 Direct API 흐름까지 담당하게 되었다.

- 단순히 React로 화면을 만드는 것과는 달리,
Next.js에서는 페이지 라우트, 서버 통신 방식, 인증 흐름, API Route 구조까지 함께 이해해야 했다.
이 과정이 나에게는 꽤 도전적이었고, 그래서 이번 글에서 전체 흐름을 정리하고 회고해본다.



## **2. Public API vs Authenticated API (쿠키 기반 인증)**
- 회원가입 작업을 진행하면서, 팀원과 로그인 구조를 논의하던 중
“회원가입(Signup)은 인증이 필요 없고, 로그인(Login)은 인증 API를 사용한다”는 말을 듣고 처음엔 많이 헷갈렸다. 하지만 공부해보니 개념이 매우 명확했다.

- 회원가입(Signup) API는 누구나 호출할 수 있는 Public API에 해당하며, 별도의 인증 과정이 필요하지 않다. 반면 로그인 이후에만 접근할 수 있는 /api/me, /api/orders, /api/profile 같은 API들은 쿠키 또는 토큰을 이용한 인증이 반드시 필요한 Private API로 분류된다.

- 이번 글에서는 인증이 필요 없는 회원가입 Public API의 전체 흐름과 작업 과정만 다루며,
로그인 과정에서 사용되는 쿠키 기반 인증, 로컬스토리지와의 차이, Authenticated API 구조 등은 다음 글에서 자세히 정리할 예정이다.

## **3. 회원가입 API 전체 Flow 정리**
- 회원가입을 제대로 이해하기 위해, 프론트에서 입력된 데이터가 어떤 식으로 백엔드를 거쳐 DB까지 저장되고 다시 프론트로 응답이 오는지 전체 흐름을 직접 플로우 차트로 정리해보았다. 언뜻 보면 복잡하지만 단계를 나누면 이렇게 흘러간다.

---

- API 명세서 확인 (payload 구조 이해)
- 컴포넌트 ➡  커스텀 훅 ➡  서비스 훅 분리
- payload 생성 (email, password, type)
- fetch/axios로 POST 요청 보내기
- 브라우저 내부에서 HTTP Request로 변환되어 서버로 전송
- 백엔드 라우팅 ➡  컨트롤러 ➡  서비스 로직 수행
- DB에 사용자 정보 저장
- 서버가 JSON 응답 반환 ➡  프론트에서 결과 처리

---


> 직접 정리한 흐름은 아래 이미지에 담았다.

![API 전체 흐름](/assets/img/next-js/next-js-flow.jpg){: width="1400px" }

## **4. 정리하며 느낀 점**
- 회원가입 기능은 단순한 기능처럼 보여도,
실제로는 프론트엔드 ➡ 서버 ➡ DB ➡ 다시 프론트로 돌아오는
전체 사이클을 이해해야만 제대로 구현할 수 있다는 걸 이번에 배웠다.

```bash
- payload 구조 설계
- fetch/axios 요청 방식
- HTTP Request로 변환되는 과정
- 백엔드 라우팅/컨트롤러/서비스 구조
- DB 저장 흐름
```

- 특히, 이 모든 단계가 연결되어 있다는 사실이 크게 와닿았다. Next.js로 작업하면서 프론트만 보는 것이 아니라
웹 애플리케이션 전체 구조를 이해하게 되었고, 이 경험이 나를 한 단계 성장시킨 프로젝트였다. 다음 글에서는 **로그인(Login) 흐름, 쿠키 기반 인증, 로컬스토리지 vs 쿠키 차이, 그리고 Authenticated API 사용 방법**을 더 깊게 다뤄보려고 한다.