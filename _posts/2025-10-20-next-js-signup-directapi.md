---
layout: post
title: "Next.js 회원가입(Signup) 구현 정리: Direct API Flow와 Public API 이해"
description: "Next.js 회원가입 구현을 통해 API 분리 구조와 서버–DB까지의 흐름을 정리한 기록"
date: 2025-10-20 00:00:00 +0900
categories: [frontend, nextjs]
tags: [nextjs, signup, authentication, api-flow, fetch, typescript]
series: nextjs-auth
image: /assets/img/thumbnail/next-js.png
---


> **Next.js Auth Series · Signup Flow** 단순히 회원가입 입력 폼을 만드는 것을 넘어, 프론트엔드에서 입력된 데이터가 **서버 ➡️ DB ➡️ 다시 프론트로 돌아오기까지**  어떤 과정을 거치는지 전체 흐름을 이해하는 데 목적이 있다.

---

## **1️⃣ Next.js로 회원가입 기능을 만들며 느낀 점**
코드잇 두 번째 팀 프로젝트에서는 풀스택 웹 프레임워크인 **Next.js**를 사용해 공고 사이트를 제작했다.  
여러 역할 중 나는 **회원가입(Signup) 영역**을 맡았고, 코드잇에서 제공한 API 명세서를 해석해

- payload 구조 설계
- 서버와 직접 통신하는 Direct API 방식 구현
- 회원가입 요청/응답 흐름 정리

까지 담당하게 되었다.

React로 단순히 화면만 만들던 경험과 달리,  
Next.js에서는 다음 요소들을 함께 이해해야 했다.

- 페이지 라우트 구조
- 서버 통신 방식
- 인증 여부에 따른 API 분기
- API Route 개념

이 과정이 꽤 도전적이었고,  
그래서 이번 글에서는 **회원가입 기능 구현 전체 흐름을 정리하며 회고**해보려 한다.

---

## 2️⃣ Public API vs Authenticated API (쿠키 기반 인증)
**회원가입은 Public API, 로그인 이후부터 Auth API**라는 개념이 처음엔 다소 헷갈렸지만 정리해보니 기준은 명확했다.

회원가입(Signup) API는 누구나 호출할 수 있는 Public API에 해당하며, 별도의 인증 과정이 필요하지 않다. 주소 예시는 `/api/signup` 이고, 로그인 이후에만 접근할 수 있는 `/api/me, /api/orders, /api/profile` 같은 API들은 쿠키 또는 토큰을 이용한 인증이 반드시 필요한 Authenticated API로 분류된다.

이번 글에서는 **인증이 필요 없는 회원가입(Signup) Public API 흐름**만 다루고,
로그인 이후 인증 흐름은 다음 글에서 별도로 정리할 예정이다.

## **3️⃣ 회원가입 API 전체 Flow 정리**
- 회원가입 과정을 제대로 이해하기 위해, 프론트에서 입력된 데이터가 어떤 플로우로 백엔드를 거쳐 DB까지 저장되고 다시 프론트로 응답이 오는지 전체 흐름을 직접 플로우 차트로 정리해보았다. 언뜻 보면 복잡하지만 단계를 나누면 이렇게 흘러간다.

---

### 👉🏻 회원가입 Direct API Flow
1. API 명세서 확인 (payload 구조 이해)
2. 컴포넌트 ➡️ 커스텀 훅 ➡️ 서비스 훅 분리
3. payload 생성 `email, password, type`
4. `fetch/axios`로 POST 요청 보내기
5. 브라우저 내부에서 HTTP Request로 변환되어 서버로 전송
6. 백엔드 라우팅 ➡️ 컨트롤러 ➡️ 서비스 로직 수행
7. DB에 사용자 정보 저장
8. 서버가 JSON 응답 반환
9. 프론트엔드에서 응답 결과 처리

---

> 직접 정리한 흐름은 아래 이미지에 담았다.
![API 전체 흐름](/assets/img/next-js/next-js-flow.jpg){: width="1400px" }

## 4️⃣ 회원가입 기능 구현을 통해 배운 점
회원가입 기능은 단순한 기능처럼 보여도 실제로는 프론트엔드 ➡️ 서버 ➡️ DB ➡️ 다시 프론트엔드로 돌아오는
전체 사이클을 이해해야만 제대로 구현할 수 있다는 걸 이번에 배웠다.

```bash
- payload 구조 설계
- fetch/axios 요청 방식
- HTTP Request로 변환되는 과정
- 백엔드 라우팅/컨트롤러/서비스 구조
- DB 저장 흐름
```

특히 인상 깊었던 점은, 이 모든 단계가 하나라도 어긋나면 기능 전체가 동작하지 않는다는 점이었다.
Next.js로 작업하면서 프론트엔드만 보는 것이 아니라 웹 애플리케이션 전체 구조를 이해하게 되었고,
이 경험은 나를 한 단계 성장시킨 프로젝트였다.

---

## 5️⃣ 다음 글에서 다룰 내용
다음 글에서는 이번 회원가입 흐름을 기반으로, 로그인(Login) API 흐름, 쿠키 기반 인증 구조, 로컬스토리지 vs 쿠키 차이
, Authenticated API 사용 방법을 더 깊게 정리해볼 예정이다.

회원가입이 웹 인증 구조의 출발점이라면, 로그인은 그 구조가 실제로 어떻게 작동하는지를 보여주는 핵심 단계라고 생각한다.