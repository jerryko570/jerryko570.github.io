---
layout: post
title: 'JavaScript 기초 문법 완벽 정리 | use strict, let, const, 자료형 총정리'
description: 'JavaScript use strict 모드가 왜 필요한지, let과 const 차이, 8가지 자료형을 예제 코드와 함께 쉽게 설명합니다. 입문자를 위한 실행 흐름 기준 핵심 정리.'
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
  - 자바스크립트-기초
  - 자바스크립트-변수
series: javascript
image: /assets/img/thumbnail/javascript.png
---

JavaScript를 처음 배울 때 가장 먼저 마주치는 개념은 **script 태그**, **use strict**, **변수 선언**, 그리고 **자료형**이다. 이 글에서는 브라우저가 JavaScript를 어떻게 읽고 실행하는지를 시작으로, 변수 선언 방식과 자료형 개념을 실행 흐름 기준으로 하나씩 정리한다.

문법을 외우기보다는 **왜 이렇게 써야 하는지**를 이해하는 데 초점을 맞춘 기초 정리 노트다.

---

## **1️⃣ script 태그란? JavaScript 실행의 시작점**

JavaScript 코드는 브라우저가 자동으로 실행하지 않는다. `<script>` 태그는 브라우저에게 **'여기부터 JavaScript 코드야'**라고 알려주는 역할을 한다.

### 🤔 외부 스크립트를 사용하는 이유

코드가 많아질수록 JavaScript를 HTML 안에 계속 적는 것은 관리가 어렵다. 그래서 JavaScript 코드는 **외부 파일로 분리**하는 방식이 실무에서도 일반적이라고 한다.

<div class="study-card-grid">
  <div class="study-card">HTML/JavaScript 분리</div>
  <div class="study-card">재사용 가능</div>
  <div class="study-card">유지보수 쉬움</div>
  <div class="study-card study-card--benefit">성능 개선</div>
</div>

### 🧠 언제 어떤 방식을 쓰면 좋을까?
코드가 짧고 한 페이지만 사용하는 경우에는 **HTML 내부 작성**하고, 코드가 많거나 여러 페이지에서 사용하면 **외부 파일 분리로 사용**하면 좋을 것 같다.

```html
<!-- HTML 안에서 직접 자바스크립트 코드 작성 -->
<script>
  console.log('자바스크립트 실행 중!');
</script>

<!-- 외부 파일을 연결할 때 -->
<script src='main.js'></script>
```

---

## **2️⃣ JavaScript 코드 구조: Statement란?**

JavaScript는 **위에서 아래로 한 줄씩 실행**된다. 이때 실행되는 최소 단위를 **문(Statement)**이라고 한다.

```javascript
// 코드문 (statement)
let name = 'jerry';   

// 세미콜론(;)으로 문장 구분
console.log(name);  

// 주석(Comment): 사람을 위한 설명이며, 실행에는 영향을 주지 않는다.
```

하나의 statement는 하나의 동작을 수행하며, 세미콜론으로 문장의 끝을 명시하는 것이 권장된다.

---

## **3️⃣ use strict 모드: 왜 써야 할까?**

**use strict**는 JavaScript를 더 안전하고 정확하게 실행하도록 만드는 엄격 모드이다. 선언 누락이나 문법 실수를 미리 잡아주는 안전장치 역할을 한다.

### 📌 use strict의 특징

<div class="study-card-grid">
  <div class="study-card">최상단 선언</div>
  <div class="study-card">함수 단위 적용</div>
  <div class="study-card">해제 불가</div>
  <div class="study-card study-card--benefit">선언·문법 오류 방지</div>
</div>

```javascript
'use strict';

x = 10;      // ReferenceError: x is not defined
let y = 10;  // 정상 동작
```

use strict를 사용하면 실수로 전역 변수를 생성하거나, 예약어를 변수명으로 사용하는 등의 오류를 사전에 방지할 수 있다.

---

## **4️⃣ let과 const 차이점: 언제 뭘 쓸까?**

변수는 **값을 저장하기 위한 이름이 붙은 공간**이다. JavaScript에서는 `let`과 `const` 두 가지 방식으로 변수를 선언한다. 이 개념은 [스코프와 클로저](/posts/js-closure-scope/)를 이해하는 데 기초가 된다.

![let은 선언 후 할당과 재할당이 가능하고, const는 선언과 동시에 할당해야 하며 재할당이 불가능한 흐름을 보여주는 다이어그램](/assets/img/javascript/js-let-const-lifecycle.png)

### 👉🏻 let: 값이 바뀔 수 있는 변수

프로그램 실행 중에 **값을 변경할 수 있다**는 점이 가장 큰 특징이다.

```javascript
let name = 'jerry';  // 변수 선언
name = 'bango';      // 값 변경 가능

let age = 20;
let user_name = 'poby';  // 언더스코어(_) 사용 가능
let $price = 1000;       // 달러 기호($) 사용 가능
```

### 👉🏻 const: 값이 고정된 상수

상수는 **한번 값을 정하면 다시 바꿀 수 없다.** 변하지 않아야 하는 값이나 의미가 고정된 설정값을 표현할 때 사용한다.

```javascript
// 재할당 불가한 상수
const PI = 3.14;
PI = 3.14159;  // TypeError: Assignment to constant variable

// 프로젝트 전반에서 공유되는 설정값
const API_URL = 'https://api.example.com';
const MAIN_COLOR = '#FF6600';
```

> **실무 권장사항**: 변수 선언은 **const를 기본**으로 사용하고, 값 변경이 필요한 경우에만 **let**을 사용한다. 이렇게 하면 의도치 않은 값 변경을 방지할 수 있다고 한다.

---

## **5️⃣ JavaScript 변수 이름 규칙**

변수명을 작성할 때 지켜야 할 규칙이 있다:

- 문자, 숫자, 언더스코어(_), 달러 기호($)만 사용 가능
- 숫자로 시작할 수 없음
- 대소문자 구분: `name`과 `Name`은 다른 변수
- 예약어 사용 금지: `let` `return` `class` `function` 등

```javascript
// 올바른 변수명
let userName = 'jerry';
let _privateVar = 100;
let $element = document.body;

// 잘못된 변수명
let 1stPlace = 'gold';  // 숫자로 시작 불가
let let = 'value';      // 예약어 사용 불가
```

---

## **6️⃣ JavaScript 자료형 8가지 총정리**

자료형(Data Type)은 값이 어떤 성격을 가지고 있는지를 나타내는 분류다. JavaScript에서는 변수에 값을 담는 순간 자료형이 자동으로 결정되며, 같은 변수라도 다른 자료형의 값을 다시 담을 수 있다.

이런 특성 때문에 JavaScript는 **동적 타입 언어(Dynamically Typed Language)**라고 불린다.

| 자료형 | 설명 | 예시 |
|--------|------|------|
| **number** | 정수, 소수, Infinity, NaN 포함 | `let a = 10;` |
| **bigint** | 아주 큰 정수 (끝에 n 붙임) | `let big = 12345678901234567890n;` |
| **string** | 문자열 (큰따옴표, 작은따옴표, 백틱 사용) | `` let name = `Hi ${user}`; `` |
| **boolean** | 참(true) 또는 거짓(false) | `let isOpen = true;` |
| **null** | 의도적으로 '값 없음'을 표현 | `let data = null;` |
| **undefined** | 값이 아직 할당되지 않음 | `let x;` |
| **object** | 여러 데이터를 묶은 복합 자료형 | `let user = {name: 'jerry'};` |
| **symbol** | 고유한 식별자 생성 | `let id = Symbol('id');` |

object 자료형에 대해 더 알고 싶다면 [구조분해 할당](/posts/js-destructuring/) 글에서 객체 활용 패턴을 확인할 수 있다.

### 🔍 null vs undefined 차이점

이 두 가지는 모두 '값이 없음'을 나타내지만 의미가 다르다:

**null**: 개발자가 의도적으로 '비어있음'을 설정한 값. API 응답에서 데이터가 없을 때 자주 사용된다.

**undefined**: JavaScript 엔진이 자동으로 할당하는 값. 변수를 선언만 하고 값을 넣지 않았을 때의 상태다.

```javascript
let intentionalEmpty = null;      // 개발자가 의도적으로 비움
let notYetAssigned;               // undefined (자동 할당)
console.log(notYetAssigned);      // undefined
```

### 🔍 typeof 연산자로 자료형 확인하기

**typeof**는 변수에 담긴 값의 자료형을 문자열로 반환하는 연산자다. 디버깅이나 조건 분기에 자주 사용된다.

```javascript
let name = 'jerry';
console.log(typeof name);    // 'string'

let count = 42;
console.log(typeof count);   // 'number'

let isActive = true;
console.log(typeof isActive); // 'boolean'
```

---

## **7️⃣ 자주 묻는 질문**

### use strict를 꼭 써야 하나요?

필수는 아니지만 사용을 권장한다. 특히 ES6 모듈(`import`/`export`)을 사용하면 자동으로 strict 모드가 적용된다. 레거시 코드가 아니라면 항상 사용하는 것이 좋다.

### let과 const 중 뭘 먼저 써야 하나요?

**const를 기본**으로 사용하고, 값을 변경해야 할 때만 let으로 바꾸는 것이 좋다. 이렇게 하면 의도치 않은 재할당을 방지하고 코드의 의도를 명확하게 전달할 수 있다.

### var는 왜 사용하지 않나요?

`var`는 함수 스코프를 가지고 호이스팅 동작이 혼란스러워 예기치 않은 버그를 유발할 수 있다. ES6 이후로는 블록 스코프를 가진 `let`과 `const` 사용이 표준이다. 스코프에 대해 더 알고 싶다면 [스코프와 클로저](/posts/js-closure-scope/) 글을 참고하자.

---

## **8️⃣ 학습 정리**

이번 글에서 다룬 JavaScript 기초 문법의 핵심 포인트:

- `<script>` 태그는 브라우저에게 JavaScript 코드의 시작을 알린다
- **use strict**는 선언 누락이나 실수를 미리 잡아주는 안전장치다
- 변수 선언은 **const를 기본**으로, 변경이 필요한 경우만 **let**을 사용한다
- **null**과 **undefined**는 모두 '없음'이지만 의미와 사용 의도가 다르다
- 자료형은 값에 따라 자동으로 결정되며, 실행 중에도 바뀔 수 있다

기본 문법을 정확히 이해하고 use strict, let, const를 올바르게 사용하면 더 안전하고 예측 가능한 JavaScript 코드를 작성할 수 있다.

---

## 다음 글

👉 [JavaScript 스코프와 클로저 이해하기](/posts/js-closure-scope/) - 실행 컨텍스트 기준으로 스코프 체인과 클로저를 정리해보고자 한다.

---

## 참고 자료

- [MDN Web Docs - JavaScript 기초](https://developer.mozilla.org/ko/docs/Learn/Getting_started_with_the_web/JavaScript_basics)
- [MDN Web Docs - Strict mode](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Strict_mode)
- [MDN Web Docs - let](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/let)
- [MDN Web Docs - const](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/const)