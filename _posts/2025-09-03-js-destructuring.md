---
layout: post
title: "JavaScript 구조분해 할당 이해하기 | 배열·객체 활용 패턴"
description: "배열과 객체 구조분해 문법을 실제 코드에서 어떻게 활용하면 좋은지 예제 중심으로 살펴봅니다."
date: 2025-09-03 00:00:00 +0900
categories: [frontend, javascript]
tags:
  - javascript
  - javascript-basic
  - destructuring
  - array
  - object
  - spread
  - rest
series: javascript
image: /assets/img/thumbnail/javascript.png
---

> **JavaScript · Basic Syntax**

JavaScript 구조분해 할당(Destructuring Assignment)은 배열과 객체에서 값을 간결하게 추출하는 ES6 문법이다. 이 글에서는 **배열·객체 구조분해의 동작 원리**와 **React props에서 자주 사용되는 패턴**을 예제 중심으로 정리한다.

---

## 1️⃣ 구조분해 할당이란

배열이나 객체 내부 값을 변수로 분해해서 한 번에 할당할 수 있게 해주는 문법이다.
```js
// 기존 방식
const name = user.name;
const age = user.age;

// 구조분해 할당
const { name, age } = user;
```

| 타입 | 기준 | 예시 | 기억 포인트 |
|------|------|------|-------------|
| 배열 | **순서(index)** | `[a, b] = [10, 20]` | 자리에 따라 값이 들어감 |
| 객체 | **이름(key)** | `{name} = user` | 이름만 같으면 어디 있어도 연결됨 |

![배열과 객체 구조분해 할당 비교](/assets/img/javascript/js-destructuring-compare.png)

## 2️⃣ 배열 구조분해

배열은 **순서(index)** 기준으로 값이 매칭된다.

### 기본 문법
```js
const numbers = [10, 20, 30];
const [a, b] = numbers;

console.log(a); // 10
console.log(b); // 20
```

### 값 건너뛰기

콤마(`,`)로 해당 위치를 건너뛸 수 있다.
```js
const arr = [5, 10, 15];
const [x, , z] = arr;

console.log(x); // 5
console.log(z); // 15
```

### 나머지 값 받기

`...rest` 문법으로 남은 요소들을 모두 배열로 담는다.
```js
const numbers = [1, 2, 3, 4, 5];
const [a, b, ...rest] = numbers;

console.log(a);    // 1
console.log(b);    // 2
console.log(rest); // [3, 4, 5]
```

---

## 3️⃣ 객체 구조분해

객체는 **키 이름** 기준으로 분해된다.

### 기본 문법
```js
const user = {
  name: 'jerry',
  age: 30,
  city: 'seoul'
};

const { name, age } = user;

console.log(name); // jerry
console.log(age);  // 30
```

### 다른 이름으로 받기

`기존키: 새이름` 형태로 변수명을 바꿀 수 있다. 이를 Alias라고 한다.
```js
const user = { name: 'jerry', age: 30 };
const { name: userName } = user;

console.log(userName); // jerry
```

---

## 4️⃣ 중첩 구조분해

배열 안의 배열, 객체 안의 객체도 한 번에 풀어낼 수 있다.

### 중첩 배열
```js
const arr = [1, [2, 3], 4];
const [a, [b, c], d] = arr;

console.log(a, b, c, d); // 1 2 3 4
```

### 중첩 객체
```js
const user = {
  name: "narae",
  age: 26,
  address: {
    city: "Seoul",
    zip: 12345
  }
};

const {
  name,
  age,
  address: { city, zip }
} = user;

console.log(name, age, city, zip);
// narae 26 Seoul 12345
```

---

## 5️⃣ React props 활용

React에서 props는 항상 **객체**로 전달된다. 구조분해를 사용하면 코드가 훨씬 간결해진다.
```jsx
// 파라미터에서 바로 구조분해
function Button({ label, size }) {
  return <button>{label}</button>;
}
```

`{label, size}`가 구조분해 할당이다. `label`은 `props.label`을, `size`는 `props.size`를 꺼낸 변수다.

### 🔎 React에서 props 흐름

![React props 구조분해 흐름도](/assets/img/javascript/js-react-props-flow.png)

---

## 6️⃣ 정리

| 패턴 | 문법 | 용도 |
|------|------|------|
| 배열 기본 | `[a, b] = arr` | 순서대로 추출 |
| 배열 건너뛰기 | `[a, , c] = arr` | 특정 인덱스 스킵 |
| 배열 rest | `[a, ...rest] = arr` | 나머지 모아담기 |
| 객체 기본 | `{name} = obj` | 키 이름으로 추출 |
| 객체 alias | `{name: n} = obj` | 다른 변수명 사용 |
| 중첩 | `{a: {b}} = obj` | 깊은 값 추출 |