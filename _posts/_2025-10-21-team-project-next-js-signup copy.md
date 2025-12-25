---
layout: post
title: "[Team Project] 회원가입(Signup) 구축기"
date: 2025-10-21 00:00:00 +0900
categories: [frontend]
tags: [nextjs, signup, api]
image: /assets/img/thumbnail/next-js.png
---


## **1. 왜 회원가입 흐름부터 정리했을까?**
- 2차 팀 프로젝트에서 Next.js 기반 공고 사이트 개발을 진행했고, 그중 회원가입(Signup), Tailwind 기반 UI 시스템, 프로필 수정, 공고 모집 카드 컴포넌트를 담당했다.

- 그래서 구현에 들어가기 전에 먼저 회원가입이 실제로 어떤 경로로 동작하는지 흐름 (브라우저 ➡  API ➡  서버 ➡  DB ➡  응답) 부터 정리했고, 그 뒤에 UI와 코드를 얹는 방식으로 진행했다. 

- 그 결과 회원가입은 단순히 폼 UI를 만드는 작업이 아니라, 데이터 흐름을 설계하고 구현하는 문제라는 관점으로 접근하게 되었다.

## **2. 회원가입 기능을 흐름 기준으로 나누기**
- 한 번에 코드를 작성하기보다,
“이 단계에서는 무엇을 책임져야 하는지”를 먼저 정의하는 것이 목표였다.

```bash
📌 회원가입 전체 흐름
- 사용자가 회원가입 폼에 정보 입력
- 프론트엔드에서 입력값 상태 관리 및 유효성 검사
- API 명세에 맞는 payload 구성
- 회원가입 API 요청 전송
- 서버 응답에 따른 결과 처리
```

## **3. Step 1. UI에서 사용자 입력 받기**
- 
3. Step 1. UI에서 사용자 입력 받기

회원가입 화면에서는 아래 정보를 입력받는다.

이메일

비밀번호

비밀번호 확인

회원 유형 선택 (사장님 / 알바생)

UI 컴포넌트는
입력값을 받는 역할과 이벤트 전달만 담당하도록 구성했다.

이 단계에서는

유효성 검사

API 호출
같은 로직을 UI에서 처리하지 않도록 의도적으로 배제했다.

4. Step 2. 커스텀 훅에서 상태와 유효성 관리

입력된 값들은 useSignupForm 커스텀 훅에서 관리한다.
이 훅은 회원가입 흐름에서 중앙 제어 역할을 한다.

function useSignupForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [memberType, setMemberType] = useState<"employee" | "employer">("employee");

  const isFormValid =
    isValidEmail(email) &&
    isValidPassword(password) &&
    isSamePassword(password, confirmPassword);

  return {
    email,
    password,
    confirmPassword,
    memberType,
    setEmail,
    setPassword,
    setConfirmPassword,
    setMemberType,
    isFormValid,
  };
}


이 단계에서 이미
**“지금 상태로 서버에 요청을 보내도 되는지”**를 판단할 수 있다.

5. Step 3. 회원 유형 분기와 Payload 구성

회원가입 API는
사장님과 알바생을 type 값으로 분기 처리한다.

const payload = {
  email,
  password,
  type: memberType,
};


UI에서 선택한 회원 유형

커스텀 훅에서 관리하던 상태

API 명세의 payload 구조

이 세 가지를 하나의 흐름으로 연결하는 것이 핵심이었다.

6. Step 4. 회원가입 API 요청

폼이 유효한 상태일 경우,
회원가입 API로 POST 요청을 전송한다.

{
  "email": "string",
  "password": "string",
  "type": "employee"
}


브라우저에서 전송된 요청은
서버 → 컨트롤러 → 서비스 로직 → DB 저장 과정을 거친 후
JSON 형태의 응답으로 다시 프론트엔드로 돌아온다.

7. Step 5. 응답에 따른 UI 처리

서버 응답에 따라 화면을 분기 처리했다.

201 : 회원가입 성공 → 다음 화면 이동

400 : 입력값 오류 안내

409 : 중복 이메일 안내

이 단계에서
에러를 어디서, 어떤 메시지로 보여줄지를 함께 고민했다.

8. 이 흐름을 통해 느낀 점

회원가입 기능을 구현하며 느낀 점은 명확했다.

회원가입은 단순한 폼 UI가 아니라,
데이터가 어떻게 이동하고 처리되는지를 설계하는 작업이었다.

특히 흐름을 먼저 정리한 뒤 구현에 들어가니

코드의 역할이 명확해졌고

수정과 확장이 훨씬 쉬워졌다.

9. 회원가입 기능을 구현하며 배운 점

이번 회원가입 기능 구현을 통해 가장 크게 배운 점은,
프론트엔드 개발에서 UI보다 먼저 데이터 흐름을 이해하는 것이 중요하다는 것이었다.

처음에는 입력 폼부터 만들고 싶었지만,
브라우저 → API → 서버 → DB → 응답 흐름을 먼저 정리하고 나니
각 단계에서 프론트엔드가 맡아야 할 역할이 훨씬 명확해졌다.

특히 아래 세 가지를 체감했다.

회원 유형 분기 처리의 중요성
사장님 / 알바생을 UI에서만 구분하는 것이 아니라,
API payload의 type 값으로 일관되게 관리해야 이후 로직이 단순해진다는 점을 배웠다.

상태 관리와 UI의 역할 분리
커스텀 훅을 통해 상태와 유효성 검사를 분리하면서,
UI 컴포넌트는 입력과 렌더링에만 집중할 수 있었다.

API 명세를 기준으로 한 구현
API 구조를 먼저 이해하고 그에 맞춰 코드를 작성하니,
불필요한 변환 로직이 줄고 디버깅도 수월해졌다.

결과적으로 회원가입 기능은
단순한 화면 구현이 아니라,
데이터 흐름을 설계하고 이를 코드로 옮기는 과정이라는 것을 명확히 인식하게 된 작업이었다.

