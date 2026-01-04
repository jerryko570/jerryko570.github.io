---
layout: post
title: 'JavaScript 얕은 복사 vs 깊은 복사 완벽 정리 | 객체 참조와 불변성 이해'
description: 'JavaScript 얕은 복사와 깊은 복사의 차이를 예제 코드와 함께 쉽게 설명합니다. Object.assign, 스프레드 연산자, JSON, lodash까지 복사 방법 총정리.'
date: 2025-09-04 15:11:00 +0900
categories: [frontend, javascript]
tags:
  - javascript
  - shallow-copy
  - deep-copy
  - object
  - reference
  - immutability
  - 자바스크립트-복사
  - 자바스크립트-객체
series: javascript
image: /assets/img/thumbnail/javascript.png
---

JavaScript에서 객체를 복사할 때 **얕은 복사**와 **깊은 복사**의 차이를 이해하는 것은 매우 중요하다. 이 글에서는 **객체 참조 구조**를 기준으로 얕은 복사와 깊은 복사가 언제 문제를 만들고 어떻게 피할 수 있는지 살펴본다.

객체 복사를 이해하려면 먼저 [JavaScript 자료형](/posts/my-first-post/)에서 참조 타입의 개념을 알아야 한다.

---

## **1️⃣ 왜 복사 방식이 중요할까?**

JavaScript에서 객체는 **참조 타입**이다. 변수에 객체를 할당하면 값이 아닌 **메모리 주소(참조)**가 저장된다.

<div class="study-card-grid">
  <div class="study-card">기본 타입: 값 복사</div>
  <div class="study-card">참조 타입: 주소 복사</div>
  <div class="study-card study-card--benefit">복사 방식 이해 필수</div>
</div>

```javascript
const original = { name: 'jerry' };
const copy = original; // 참조만 복사됨

copy.name = 'poby';
console.log(original.name); // 'poby' (원본도 변경됨!)
```

![기본 타입은 값이 복사되고, 참조 타입은 메모리 주소가 복사되어 같은 객체를 가리키는 것을 보여주는 다이어그램](/assets/img/javascript/js-reference-copy.png)

---

## **2️⃣ 얕은 복사 (Shallow Copy)**

얕은 복사는 객체의 **최상위 레벨(1단계) 속성만 복사**하는 방식이다.

### 🔍 얕은 복사의 특징

<div class="study-card-grid">
  <div class="study-card">1단계만 복사</div>
  <div class="study-card">중첩 객체는 참조 공유</div>
  <div class="study-card study-card--benefit">빠르고 간단</div>
</div>

- 원본 객체의 속성이 **기본 타입**(숫자, 문자열, 불린)이면 **값 자체가 복사**된다
- 원본 객체의 속성이 **참조 타입**(객체, 배열 등)이면 **주소(레퍼런스)**만 복사된다

### 👉🏻 Object.assign()

`Object.assign()`은 하나 이상의 객체를 합치거나 복사할 때 사용하는 메서드이다.

```javascript
const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = Object.assign({}, original);

copy.name = 'poby';
console.log(original.name); // 'jerry' (원본 영향 없음)

copy.address.city = 'busan';
console.log(original.address.city); // 'busan' (원본도 변경됨!)
```

### 👉🏻 스프레드 연산자 (...)

`...`(스프레드 연산자)는 객체나 배열의 내용을 펼쳐서 복사할 수 있다.

```javascript
const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = { ...original };

copy.address.city = 'busan';
console.log(original.address.city); // 'busan' (원본도 변경됨!)
```

> **주의**: 겉보기에는 완전히 복사된 것처럼 보이지만, 내부에 참조 타입이 포함되어 있으면 얕은 복사가 된다.

### 👉🏻 배열의 얕은 복사

배열도 마찬가지로 얕은 복사가 적용된다.

```javascript
const original = [1, 2, { value: 3 }];
const copy = [...original];

copy[2].value = 100;
console.log(original[2].value); // 100 (원본도 변경됨!)
```

### 📌 얕은 복사 방식 정리

| 복사 방법 | 복사 수준 | 특징 |
|-----------|-----------|------|
| `{ ...obj }` 스프레드 | 얕은 복사 | 1단계만 복사, 중첩 객체는 참조 유지 |
| `Object.assign()` | 얕은 복사 | 동일하게 참조 복사, 원본 영향 있음 |
| `[...arr]` 배열 스프레드 | 얕은 복사 | 배열도 동일한 규칙 적용 |
| `Array.slice()` | 얕은 복사 | 배열 복사 시 자주 사용 |

---

## **3️⃣ 깊은 복사 (Deep Copy)**

깊은 복사는 **객체의 내부 구조(중첩된 객체나 배열)까지 완전히 새로운 메모리에 복사**하는 방식이다.

### 🔍 깊은 복사의 특징

<div class="study-card-grid">
  <div class="study-card">모든 레벨 복사</div>
  <div class="study-card">완전히 독립적</div>
  <div class="study-card study-card--benefit">원본 안전 보장</div>
</div>

- 원본과 사본은 **서로 완전히 독립적**이며, 중첩 객체를 수정해도 **원본은 영향을 받지 않는다**

### 👉🏻 JSON.stringify() + JSON.parse()

가장 간단하고 널리 쓰이는 깊은 복사 방식이다. 객체를 JSON 문자열로 바꿨다가 다시 객체로 변환해 복사한다.

```javascript
const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = JSON.parse(JSON.stringify(original));

copy.address.city = 'busan';
console.log(original.address.city); // 'seoul' (원본 영향 없음!)
```

> **한계**: 함수, Symbol, undefined, Date 객체 등은 제대로 복사되지 않는다. 순환 참조도 처리 불가.

### 👉🏻 structuredClone() (최신 방법)

ES2022에서 추가된 네이티브 깊은 복사 메서드이다.

```javascript
const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = structuredClone(original);

copy.address.city = 'busan';
console.log(original.address.city); // 'seoul'
```

> **장점**: JSON 방식의 한계를 극복하고, Date, Map, Set 등도 제대로 복사된다.

### 👉🏻 Lodash의 _.cloneDeep()

가장 안정적이고 강력한 깊은 복사 방식이다. 외부 라이브러리 lodash가 제공하는 기능이다.

```javascript
const _ = require('lodash');

const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = _.cloneDeep(original);

copy.address.city = 'busan';
console.log(original.address.city); // 'seoul'
```

### 👉🏻 재귀 함수로 직접 구현

깊은 복사의 원리를 이해하기 위해 직접 구현해볼 수 있다.

```javascript
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;

  const clone = Array.isArray(obj) ? [] : {};

  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      clone[key] = deepClone(obj[key]);
    }
  }

  return clone;
}

const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = deepClone(original);

copy.address.city = 'busan';
console.log(original.address.city); // 'seoul'
```

### 📌 깊은 복사 방식 정리

| 방식 | 장점 | 단점 |
|------|------|------|
| `JSON.parse(JSON.stringify())` | 간단, 빠름 | 함수·Symbol 손실, 순환참조 불가 |
| `structuredClone()` | 네이티브, Date/Map 지원 | 구형 브라우저 미지원 |
| `_.cloneDeep()` | 완전한 복사, 안전함 | 외부 라이브러리 필요 |
| 재귀 함수 직접 구현 | 원리 이해에 도움 | 코드 길고, 예외처리 필요 |

---

## **4️⃣ 얕은 복사 vs 깊은 복사 비교**

![얕은 복사는 1단계만 복사하고 중첩 객체는 참조를 공유하지만, 깊은 복사는 모든 레벨을 완전히 새로운 메모리에 복사하는 차이를 보여주는 비교 다이어그램](/assets/img/javascript/js-shallow-deep-compare.png)

| 구분 | 얕은 복사 | 깊은 복사 |
|------|----------|----------|
| 기준 | 1단계만 복사 | 전체 복사 |
| 중첩 객체 | 참조 공유 | 완전 분리 |
| 영향 | 원본 영향 있음 | 영향 없음 |
| 성능 | 빠름 | 느림 |
| 방법 | `...` `assign` | `JSON` `structuredClone` |


---

## **5️⃣ 실무에서 언제 뭘 쓸까?**

### 👉🏻 얕은 복사가 적합한 경우

```javascript
// 단순한 1단계 객체
const config = { theme: 'dark', language: 'ko' };
const newConfig = { ...config, theme: 'light' };
```

### 👉🏻 깊은 복사가 필요한 경우

```javascript
// 중첩된 객체, 불변성이 중요한 상태 관리
const state = {
  user: { name: 'jerry', settings: { notifications: true } }
};
const newState = structuredClone(state);
newState.user.settings.notifications = false;
// 원본 state는 그대로 유지됨
```

React나 Redux에서 상태 관리를 할 때 불변성을 유지하려면 깊은 복사가 필요하다. [구조분해 할당](/posts/js-destructuring/)과 함께 사용하면 더 깔끔한 코드를 작성할 수 있다.

---

## **6️⃣ 자주 묻는 질문**

### spread 연산자는 깊은 복사인가요?

아니다. spread 연산자(`...`)는 **얕은 복사**만 수행한다. 1단계 속성만 복사하고, 중첩된 객체나 배열은 참조를 공유한다.

### structuredClone은 어디서 사용할 수 있나요?

Chrome 98+, Firefox 94+, Safari 15.4+, Node.js 17+ 등 최신 환경에서 사용 가능하다. 구형 브라우저를 지원해야 한다면 lodash를 사용하는 것이 안전하다.

### 불변성(Immutability)이 왜 중요한가요?

불변성을 유지하면 데이터 변경을 추적하기 쉽고, 예상치 못한 사이드 이펙트를 방지할 수 있다. 특히 React에서 상태 비교 시 불변성이 필수적이다.

---

## **7️⃣ 학습 정리**

이번 글에서 다룬 JavaScript 복사의 핵심 포인트:

- **얕은 복사**는 복사처럼 보이지만 내부가 연결되어 있다
- **깊은 복사**는 완전히 새로운 객체를 생성한다
- 복사 수준을 이해하면 **데이터 불변성을 유지하고 버그를 예방**하기 쉬워진다
- 실무에서는 상황에 따라 `structuredClone()` 또는 `_.cloneDeep()`을 선택한다

---

## 다음 글

👉 [React 입문 가이드](/posts/react-beginner-jsx-component/) - JSX와 컴포넌트 기본 개념을 알아보자.

---

## 참고 자료

- [MDN Web Docs - Object.assign()](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)
- [MDN Web Docs - 전개 구문](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/Spread_syntax)
- [MDN Web Docs - structuredClone()](https://developer.mozilla.org/en-US/docs/Web/API/structuredClone)
- [Lodash - cloneDeep](https://lodash.com/docs/4.17.15#cloneDeep)