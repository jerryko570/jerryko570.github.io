---
layout: post
title: 'JavaScript 스코프와 클로저 완벽 정리 | 실행 컨텍스트 기준 핵심 이해'
description: 'JavaScript 스코프 체인과 클로저가 실행 컨텍스트 안에서 어떻게 동작하는지 예제 코드와 함께 쉽게 설명합니다. 렉시컬 스코프와 프라이빗 변수 패턴까지.'
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
  - 자바스크립트-스코프
  - 자바스크립트-클로저
series: javascript
image: /assets/img/thumbnail/javascript.png
---

JavaScript 스코프(Scope)와 클로저(Closure)는 변수가 어디서 유효한지, 함수가 어떻게 외부 변수를 기억하는지를 결정하는 핵심 개념이다. 이 글에서는 **스코프 체인의 탐색 원리**와 **클로저가 메모리에서 변수를 유지하는 방식**을 실행 컨텍스트 기준으로 정리한다.

문법을 외우기보다는 **왜 이렇게 동작하는지**를 이해하는 데 초점을 맞춘 기초 정리 노트다. 스코프와 클로저를 이해하려면 먼저 [변수 선언(let, const)](/posts/my-first-post/)의 기본 개념을 알아야 한다.

---

## **1️⃣ 스코프(Scope)란?**

스코프는 **변수가 살아 있는 공간**이다. 코드 안에서 어디까지 그 변수를 쓸 수 있는지를 정하는 규칙이다.

### 👉🏻 전역 스코프 vs 함수 스코프

```javascript
let name = 'jerry'; // 전역 스코프 (Global Scope)

function sayHello() {
  let name = 'bango';  // 함수 스코프 (Local Scope)
  console.log('안쪽:', name);
}

sayHello(); // 안쪽: bango
console.log('바깥쪽:', name); // 바깥쪽: jerry
```

| 구분 | 설명 | name 값 |
|------|------|---------|
| 전역 스코프 | 프로그램 전체에서 접근 가능 | `'jerry'` |
| 함수 스코프 | 함수 내부에서만 유효 | `'bango'` |

---

## **2️⃣ 스코프 체인(Scope Chain)**

변수를 찾을 때는 **가장 가까운 스코프부터 바깥으로** 탐색한다. 이 탐색 경로를 스코프 체인이라고 하고, 이런 방식을 **렉시컬 스코프(Lexical Scope)**라고 부른다.

```javascript
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

### 🔍 변수 탐색 과정

`second()` 안에서 `a`를 찾는 과정은 다음과 같다:

<div class="study-card-grid">
  <div class="study-card">second() 스코프 확인</div>
  <div class="study-card">first() 스코프 확인</div>
  <div class="study-card study-card--benefit">전역 스코프에서 발견</div>
</div>

![second 함수 안에서 변수 a를 찾기 위해 스코프 체인을 따라 전역 스코프까지 탐색하는 과정을 보여주는 다이어그램](/assets/img/javascript/js-scope-chain-search.png)

---

## **3️⃣ 클로저(Closure)란?**

클로저는 **함수가 자신이 선언된 환경(스코프)을 기억하는 현상**이다. 외부 함수가 끝나도 내부 함수가 외부 변수를 참조하고 있으면, 그 변수는 사라지지 않는다.

```javascript
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

### 🤔 왜 count가 안 사라질까?

`outer()`는 실행이 끝났지만, `inner()`가 `count`를 참조하고 있어서 JavaScript 엔진이 `count`를 메모리에 유지하기 때문이다.

![일반 함수는 실행 후 변수가 사라지지만, 클로저는 외부 함수 종료 후에도 변수를 유지하는 차이를 보여주는 비교 다이어그램](/assets/img/javascript/js-closure-compare.png)

---

## **4️⃣ 클로저 실전 예제**

### 👉🏻 프라이빗 변수 만들기

클로저를 활용하면 외부에서 직접 접근할 수 없는 **프라이빗 변수**를 만들 수 있다.

```javascript
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

> **실무 활용**: `count`는 외부에서 직접 접근할 수 없고, 오직 반환된 메서드를 통해서만 조작 가능하다. 이게 클로저를 활용한 **프라이빗 변수** 패턴이다.

### 👉🏻 반복문에서 클로저 활용

클로저를 모르면 자주 실수하는 패턴이 있다:

```javascript
// ❌ 잘못된 예시 (var 사용)
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// 결과: 3, 3, 3

// ✅ 올바른 예시 (let 사용)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// 결과: 0, 1, 2
```

`let`은 블록 스코프를 가지기 때문에 각 반복마다 새로운 `i`가 생성되어 클로저가 제대로 동작한다. 이 차이를 이해하려면 [let과 const의 차이](/posts/my-first-post/)를 먼저 알아야 한다.

---

## **5️⃣ 자주 묻는 질문**

### 스코프와 컨텍스트는 같은 건가요?

다르다. **스코프**는 변수의 유효 범위를 말하고, **실행 컨텍스트**는 코드가 실행될 때 생성되는 환경 전체를 말한다. 실행 컨텍스트 안에 스코프 정보가 포함된다.

### 클로저는 메모리 누수를 일으키나요?

의도적으로 사용하면 문제없다. 다만 불필요한 참조를 계속 유지하면 가비지 컬렉션이 안 되어 메모리 누수가 발생할 수 있다. 사용이 끝난 클로저는 `null`로 참조를 끊어주는 것이 좋다.

### 화살표 함수도 클로저를 만드나요?

그렇다. 화살표 함수도 일반 함수와 마찬가지로 렉시컬 스코프를 따르기 때문에 클로저를 형성한다.

---

## **6️⃣ 학습 정리**

이번 글에서 다룬 JavaScript 스코프와 클로저의 핵심 포인트:

- **스코프**는 변수가 유효한 범위를 정하는 규칙이다
- **스코프 체인**은 안쪽에서 바깥으로 변수를 탐색하는 경로다
- **렉시컬 스코프**는 함수가 선언된 위치 기준으로 스코프가 결정된다는 의미다
- **클로저**는 함수가 자신이 선언된 환경을 기억해서, 외부 함수가 끝나도 변수가 유지되는 현상이다

스코프와 클로저를 이해하면 변수 충돌을 피하고, 데이터를 안전하게 보호하는 코드를 작성할 수 있다.

---

## 다음 글

👉 [JavaScript 구조분해 할당 이해하기](/posts/js-destructuring/) - 배열과 객체에서 값을 꺼내는 깔끔한 문법을 알아보자.

---

## 참고 자료

- [MDN Web Docs - 클로저](https://developer.mozilla.org/ko/docs/Web/JavaScript/Closures)
- [MDN Web Docs - 스코프](https://developer.mozilla.org/ko/docs/Glossary/Scope)
- [MDN Web Docs - 렉시컬 스코프](https://developer.mozilla.org/ko/docs/Web/JavaScript/Closures#lexical_scoping)