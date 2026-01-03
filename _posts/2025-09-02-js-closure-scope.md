---
layout: post
title: "JavaScript 스코프와 클로저 이해하기 | 실행 컨텍스트 기준"
description: "스코프 체인과 클로저가 실행 컨텍스트 안에서 어떻게 생성되고 유지되는지를 코드 흐름 관점에서 풀어봅니다."
date: 2025-09-02 00:00:00 +0900
categories: [frontend, javascript]
tags:
  - javascript
  - javascript-basic
  - scope
  - closure
  - execution-context
  - lexical-environment
  - hoisting
series: javascript
image: /assets/img/thumbnail/javascript.png
---


## **1️⃣ 스코프(Scope)란?**
스코프는 **변수가 살아 있는 공간**이다. 코드 안에서 어디까지 그 변수를 쓸 수 있는지를 정하는 규칙이다.

#### **👉🏻 전역 스코프 vs 함수 스코프**

```js
// 기본 스코프
let name = "Jerry"; // 전역 스코프 (Global Scope)

function sayHello() {
  let name = "bango";  // 함수 스코프 (Local Scope)
  console.log("안쪽:", name);
}

sayHello(); // 안쪽: bango
console.log("바깥쪽:", name); // 바깥쪽: jerry
```

| 구분     | 설명              | name 값    |
| ------ | --------------- | --------- |
| 전역 스코프 | 프로그램 전체에서 접근 가능 | `"jerry"` |
| 함수 스코프 | 함수 내부에서만 유효     | `"bango"` |

## **2️⃣ 스코프 체인(Scope Chain)**
변수를 찾을 때는 **가장 가까운 스코프부터 바깥으로** 탐색한다. 이 탐색 경로를 스코프 체인이라고 하고, 이런 방식을 **렉시컬 스코프(Lexical Scope)**라고 부른다.

```js
let a = 10;

function first() {
  let b = 20;

  function second() {
    let c = 30;
    console.log(a); // 10
  }

  second();
}

first();
```
---

#### **🔍 변수 탐색 과정**
`👉 스코프 체인(Scope Chain): second() 안에서 a를 찾는 과정`

![스코프 체인](/assets/img/javascript/js-scope-chain-search.png)

---

## **3️⃣ 클로저(Closure)란?**
클로저는 **함수가 자신이 선언된 환경(스코프)을 기억하는 현상**이다. 외부 함수가 끝나도 내부 함수가 외부 변수를 참조하고 있으면, 그 변수는 사라지지 않는다.

```js
function outer() {
  let count = 0;

  function inner() {
    count++;
    console.log(count);
  }

  return inner;
}

const counter = outer(); // outer 실행 종료
counter(); // 1 👉🏻 count가 살아있음!
counter(); // 2
counter(); // 3
```

#### **🤔 왜 count가 안 사라질까?**
`outer()`는 실행이 끝났지만, `inner()`가 `count`를 참조하고 있어서 자바스크립트 엔진이 `count`를 메모리에 유지하기 때문이다.

![클로저](/assets/img/javascript/js-closure-compare.png)

---

## **4️⃣ 클로저 실전 예제**

#### **👉🏻 프라이빗 변수 만들기**
```js
function createCounter() {
  let count = 0; // 외부에서 직접 접근 불가

  return {
    increase: () => ++count,
    decrease: () => --count,
    getCount: () => count
  };
}

const counter = createCounter();
console.log(counter.getCount()); // 0
counter.increase();
counter.increase();
console.log(counter.getCount()); // 2
```

> 💡 `count`는 외부에서 직접 접근할 수 없고, 오직 반환된 메서드를 통해서만 조작 가능하다. 이게 클로저를 활용한 **프라이빗 변수** 패턴이다.

---

## **5️⃣ 학습 정리**

이번 글에서 정리한 핵심 개념:

- **스코프**는 변수가 유효한 범위를 정하는 규칙이다
- **스코프 체인**은 안쪽에서 바깥으로 변수를 탐색하는 경로다
- **렉시컬 스코프**는 함수가 선언된 위치 기준으로 스코프가 결정된다는 의미다
- **클로저**는 함수가 자신이 선언된 환경을 기억해서, 외부 함수가 끝나도 변수가 유지되는 현상이다

👉 스코프와 클로저를 이해하면 변수 충돌을 피하고, 데이터를 안전하게 보호하는 코드를 작성할 수 있다.
