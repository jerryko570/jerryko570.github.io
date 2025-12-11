---
layout: post
title: "[JavaScript] 클로저와 스코프"
date: 2025-09-02 00:00:00 +0900
categories: [frontend, javascript]
tags: [javascript, basic, scope, closure, variable]
series: "javascript"
image: /assets/img/thumbnail/javascript.png
---

## **1. 스코프(Scope)**
- 변수가 살아 있는 공간이다. 코드 안에서 어디까지 그 변수를 쓸 수 있는가를 정하는 규칙이다.

```js
// 기본 스코프
let name = "Jerry"; // 전역 스코프

function sayHello() {
  console.log("Hello", name); // 함수 내부에서도 접근 가능 (스코프 체인)
}

sayHello();
console.log(name);

// 블록 스코프
let name = "jerry";  // 전역 스코프 (Global Scope)

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

## 2. 스코프 체인(Scope Chain)
- 변수는 가장 가까운 곳부터 찾는다. 이걸 렉시컬 스코프라고 한다.

```js
let a = 10;

function first() {
  let b = 20;

  function second() {
    let c = 30;
    console.log(a, b, c);
  }

  second();
}

first();
```
```text
// 스코프 체인 시각화
전역 스코프
 └─ a = 10
 └─ first()
      └─ b = 20
      └─ second()
           └─ c = 30
           └─ console.log(a, b, c)
```
