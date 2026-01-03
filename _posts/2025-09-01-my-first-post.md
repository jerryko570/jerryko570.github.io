---
layout: post
title: "JavaScript 기초 문법 이해하기 | use strict와 변수·자료형 흐름"
description: "JavaScript 실행을 시작하기 전 반드시 짚고 넘어가야 할 use strict 선언과 변수, 자료형의 기본 개념을 실행 흐름 기준으로 설명합니다."
date: 2025-09-01 19:52:00 +0900
categories: [frontend, javascript]
tags:
  - javascript
  - javascript-basic
  - use-strict
  - variable
  - let
  - const
  - data-type
series: javascript
image: /assets/img/thumbnail/javascript.png
---

> **JavaScript · Basic Syntax**

JavaScript를 처음 배울 때 가장 먼저 마주치는 개념은 `script 태그`, `use strict`, `변수`, 그리고 `자료형`이다. 이 글에서는 **브라우저가 JavaScript를 어떻게 읽고 실행하는지**를 시작으로, 변수 선언 방식과 자료형 개념을 **실행 흐름 기준**으로 하나씩 정리한다.

문법을 외우기보다는 👉🏻 **왜 이렇게 써야 하는지**를 이해하는 데 초점을 맞춘 기초 정리 노트다.

---

## **1️⃣ script 태그란? JavaScript 실행의 시작점**
JavaScript 코드는 브라우저가 자동으로 실행하지 않는다. `<script>` 태그는 브라우저에게 **여기부터 JavaScript 코드야** 라고 알려주는 역할을 한다.

#### **🤔 외부 스크립트를 사용하는 이유**
코드가 많아질수록 JavaScript를 HTML 안에 계속 적는 것은 관리가 어렵기 때문에 JavaScript 코드는 **외부 파일로 분리**한다.

<div class="study-card-grid">
  <div class="study-card">HTML/JavaScript 분리</div>
  <div class="study-card">재사용 가능</div>
  <div class="study-card">유지보수 쉬움</div>
  <div class="study-card study-card--benefit">성능 개선</div>
</div>

> 이런 이유로 실무에서는 JavaScript 코드를 HTML 내부에 직접 작성하기보다는 외부 파일로 분리하는 방식이 일반적으로 사용된다.

---

#### **🧠 언제 어떤 방식을 쓰면 좋을까?**
- 코드가 짧고 한 페이지만 사용하는 경우 ➡ HTML 안에 `<script>` 직접 작성  
- 코드가 많거나 여러 페이지에서 사용하는 경우 ➡ JavaScript 파일을 외부로 분리

```html
<!-- HTML 안에서 직접 자바스크립트 코드 작성 -->
<script>
  console.log("자바스크립트 실행 중!");
</script>

<!-- 외부 파일을 연결할 때 -->
<script src='main.js'></script>
```
---

## **2️⃣ 코드 구조(statement)는 무엇인가?**
JavaScript는 **위에서 아래로 한 줄씩 실행**된다. 이 때 실행되는 최소 단위를 **문(Statement)**이라고 한다.

```javascript
// 코드문 (statement)
let name = 'jerry';   

// 세미콜론 (;)으로 문장 구분
console.log(name);  

// 주석 (Comment): 사람을 위한 설명이며, 실행에는 영향을 주지 않는다.
```

---

## **3️⃣ 엄격 모드(use strict) 왜 써야 할까?**
**use strict**는 JavaScript를 더 안전하고 정확하게 실행하도록 만드는 모드이다. 선언누락이나 문법 실수를 미리 잡아주는 안전장치 역할을 한다.

<div class="study-card-grid">
  <div class="study-card">최상단 선언</div>
  <div class="study-card">함수 단위 적용</div>
  <div class="study-card">해제 불가</div>
  <div class="study-card study-card--benefit">선언·문법 오류 방지</div>
</div>

```javascript
'use strict';
x = 10; // ❎ 오류! 변수 선언 안 함
let y = 10; // ✅ 올바른 선언
```
---

## **4️⃣ let과 const는 언제 뭘 쓸까?**
변수는 **값을 저장하기 위한 이름이 붙은 공간**이고, JavaScript에서는 `let`과 `const` 두 가지 방식으로 변수를 선언한다.

![let과 const의 생애](/assets/img/javascript/js-let-const-lifecycle.png)

---

#### **👉🏻 let: 값이 바뀔 수 있는 변수**
프로그램 실행 중에 **값을 바꿀 수 있다는 점**이 가장 큰 특징이다.

```javascript
let name = 'jerry'; // 변수 선언
name = 'bango'; // 값 변경 가능

let age = 20;
let user_name = 'poby'; // _ 사용 가능
let $price = 1000; // $ 사용 가능
```
---

#### **👉🏻 const: 값이 고정된 상수**
상수는 **한번 값을 정하면 다시 바꿀 수 없다.** 변하지 않아야 하는 값이나 의미가 고정된 설정값을 표현할 때 사용한다.

<div class="study-card-grid">
  <div class="study-card">값 재할당 불가</div>
  <div class="study-card">설정·기준값에 적합</div>
  <div class="study-card">의미가 변하지 않는 값</div>
</div>

```javascript
// ❎ 재할당 불가한 상수
const PI = 3.14;
PI = 3.14159; // 오류! const는 값 변경 불가

// ✅ 프로젝트 전반에서 공유되는 설정값
const apiUrl = 'https://api.example.com';
const mainColor = '#FF6600';
```
---

## **5️⃣ 변수 이름 규칙**
`문자/숫자/_/$만 사용가능` `숫자로 시작 불가` `대소문자 구분` `예약어 사용금지(let/return/class)`

> 💡 **실무 팁**: 변수 선언은 **const를 기본**으로, 변경이 필요한 경우만 **let**을 사용한다.

---

## **6️⃣ JavaScript 자료형 8가지 한눈에 정리**
자료형은 값이 어떤 성격을 가지고 있는지를 나타내는 분류다. JavaScript에서는 변수에 값을 담는 순간 자료형이 자동으로 결정되며, 같은 변수라도 다른 자료형의 값을 다시 담을 수 있다.


<div class="study-card-grid">
  <div class="study-card">값에 따라 자동 결정</div>
  <div class="study-card">타입 선언 불필요</div>
  <div class="study-card study-card--benefit">실행 중 타입 변경</div>
</div>

> 이런 특성 때문에 JavaScript는 **동적 타입 언어(Dynamic Typing Language)**라고 불린다.

---

| 자료형           | 설명                                 | 예시                                 |
| ------------- | ---------------------------------- | ---------------------------------- |
| **number**    | 숫자형 — 정수, 소수, `Infinity` `NaN` 포함 | `let a = 10;`                      |
| **bigint**    | 아주 큰 정수 (끝에 `n` 붙임)                | `let big = 12345678901234567890n;` |
| **string**    | 문자형 — `"` `'` `` ` `` 모두 가능      | ``let name = `Hi ${user}`;``       |
| **boolean**   | 참/거짓                               | `let isOpen = true;`               |
| **null**      | 의도적으로 “값 없음”                       | `let data = null;`                 |
| **undefined** | 값이 아직 없음 (자동 할당)                   | `let x;`                           |
| **object**    | 여러 데이터를 묶음 `{}` `[]`              | `let user = {name:"jerry"};`       |
| **symbol**    | 고유 식별자 (잘 안 씀)                     | `let id = Symbol("id");`           |

####  **🔍 null vs undefined**
<div class="study-card-grid study-card-grid--vertical">
  <div class="study-card study-card--null">
    <strong>null</strong> 👉🏻 의도적 비움 | 개발자가 직접 설정 | API는 '값 없음' 응답
  </div>
  <div class="study-card study-card--undefined">
    <strong>undefined</strong> 👉🏻 아직 값 없음 | 자동 할당 | 선언만 한 변수
  </div>
</div>

---

#### **🔍 typeof 연산자**
**typeof**는 **변수에 담긴 값의 자료형을 확인할 때** 사용하는 연산자다. 디버깅이나 값의 상태를 확인할 때 자주 쓰인다.

```javascript
let name = "jerry";
console.log(typeof name); // "string"
```
---

##  **7️⃣ 학습정리**
이번 글을 통해 JavaScript 기초 문법에서 다음 포인트를 정리했다.

- JavaScript는 과거 문법보다 간결하고 표준화된 작성 방식이 중요하다
- **use strict**는 선언 누락이나 실수를 미리 잡아주는 안전장치다
- 변수 선언은 **const를 기본**으로, 변경이 필요한 경우만 **let**을 사용한다
- **null**과 **undefined**는 모두 "없음"이지만 의미와 사용 의도가 다르다
- 자료형은 값에 따라 자동으로 결정되며, 실행 중에도 바뀔 수 있다

👉 기본 문법을 정확히 이해하고 `use strict`, `let`, `const`를 올바르게 사용하면 더 안전하고 예측 가능한 JavaScript 코드를 작성할 수 있다.