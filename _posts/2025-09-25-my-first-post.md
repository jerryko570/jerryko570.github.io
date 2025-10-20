---
layout: post
title: "[JavaScript] 기초 문법 정리"
date: 2025-09-02 19:52:00 +0900
categories: [frontend, JavaScript]
tags: [javascript, basic, variable, datatype, use-strict]
---

## **1. script 태그**
- `<script>` 태그는 브라우저에게 **“여기 자바스크립트 코드 있음!”** 하고 알려줌  
- `src="main.js"` 를 사용하면 **외부 파일을 불러올 수 있음**

### 💡 외부 스크립트를 사용하는 이유
- 코드 정리 깔끔! (HTML과 JS를 분리해서 보기 쉬움)  
- 재사용 가능! (같은 스크립트를 여러 페이지에서 사용 가능)  
- 유지보수 편함! (HTML 수정 없이 JS만 수정 가능)  
- 로딩 속도 향상! (브라우저 캐시에 저장되어 빠르게 실행)

### 🧠 언제 써야 할까?
- 코드가 짧고 한 페이지만 사용할 때 → HTML 안에 `<script>` 직접 작성  
- 코드가 많거나 여러 페이지에서 재사용할 때 → 외부 파일로 분리  

```html
<!-- HTML 안에서 직접 자바스크립트 코드 작성 -->
<script>
  console.log("자바스크립트 실행 중!");
</script>

<!-- 외부 파일을 연결할 때 -->
<script src="main.js"></script>
```

##  **2. 코드 구조 (statement)**

- 코드문은 명령, 세미콜론은 구분, 주석은 설명!

```javascript

// 코드문 (statement)
let name = "jerry";   

// 세미콜론 (;)
console.log(name);   

// 주석 (Comment)
// 사람을 위한 설명, 컴퓨터는 무시함
```

## 3.  **엄격 모드 (use strict)**
- `use strict`는 자바스크립트를 더 안전하고 정확하게 실행하도록 만듦
- 한 줄로 스크립트 전체에 적용되며, 항상 코드 맨 위에 배치해야 함
- 함수 내부에 쓰면 해당 함수에만 적용됨
- 한 번 켜면 끌 수 없음

```javascript
'use strict';
x = 10; // ❌ 오류! 변수 선언 안 함
let y = 10; // ✔️ 올바른 선언
```

## 4.  **변수 (variable)**
- 데이터를 저장하는 이름 붙은 상자
- 값 변경 가능

- **규칙은?**
    - `문자, 숫자, _, $`만 사용가능
    - 숫자로 시작 불가
    - 대소문자 구분
    - 예약어 사용금지 (`let, return, class`)

```javascript
let name = "jerry";   // 변수 선언
name = "bango";       // 값 변경 가능

let age = 20;
let user_name = "poby"; // _ 사용 가능
let $price = 1000;       // $ 사용 가능
```

## 5.  **상수 (constant)**
- 한 번 정하면 바꿀 수 없는 값 (고정값)
- 대문자 상수는 변하지 않는 설정값 (API, 색상 등)에 사용
- 이름은 의미 있고 읽기 쉽게 camelCase 권장

```javascript
const PI = 3.14; // 대문자 상수 (변하지 않는 값)
const apiUrl = "https://api.example.com"; // 의미 있는 이름
const mainColor = "#FF6600"; // 색상 코드

// ❌ 오류!
const PI = 3.14159;  //const는 값 변경 불가
```

## 6.  **자료형 (data types)**
- 값의 종류 (형태)를 자료형이라 함
- 같은 변수에 어떤 값이든 저장할 수 있고, 언제든 자료형이 바뀔 수 있음
- 자바스크립트는 유연한 (동적)타입 언어


| 자료형           | 설명                                 | 예시                                 |
| ------------- | ---------------------------------- | ---------------------------------- |
| **number**    | 숫자형 — 정수, 소수, `Infinity`, `NaN` 포함 | `let a = 10;`                      |
| **bigint**    | 아주 큰 정수 (끝에 `n` 붙임)                | `let big = 12345678901234567890n;` |
| **string**    | 문자형 — `"`, `'`, `` ` `` 모두 가능      | ``let name = `Hi ${user}`;``       |
| **boolean**   | 참/거짓                               | `let isOpen = true;`               |
| **null**      | 의도적으로 “값 없음”                       | `let data = null;`                 |
| **undefined** | 값이 아직 없음 (자동 할당)                   | `let x;`                           |
| **object**    | 여러 데이터를 묶음 `{}`, `[]`              | `let user = {name:"jerry"};`       |
| **symbol**    | 고유 식별자 (잘 안 씀)                     | `let id = Symbol("id");`           |


- type of 연산자
    - 자료형을 확인할 때 사용함

```javascript
let name = "jerry";
console.log(typeof name); // "string"
```


##  **7. 학습정리**
- 과거 문법보다 지금은 간결하고 표준화된 방식이 더 중요하다는 걸 배움
- `use strict`는 오타나 선언 누락을 잡아주는 안전장치라는 걸 이해함
- 변수 선언 시 `let`과 `const`를 구분해 쓰는 습관이 필요함
- `null`과 `undefined`의 차이를 개념적으로 정리함

🤔 표준 문법을 지키며 `use strict, let, const`를 올바르게 사용하면 더 안전하고 명확한 코드를 작성할 수 있음