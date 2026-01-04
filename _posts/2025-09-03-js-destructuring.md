---
layout: post
title: 'JavaScript 구조분해 할당 완벽 정리 | 배열·객체 활용 패턴과 React props'
description: 'JavaScript 배열과 객체 구조분해 문법을 예제 코드와 함께 쉽게 설명합니다. rest 문법, 중첩 구조분해, React props 활용까지 실무 패턴 총정리.'
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
  - 자바스크립트-구조분해
  - 자바스크립트-배열
series: javascript
image: /assets/img/thumbnail/javascript.png
---

JavaScript 구조분해 할당(Destructuring Assignment)은 배열과 객체에서 값을 간결하게 추출하는 ES6 문법이다. 이 글에서는 **배열·객체 구조분해의 동작 원리**와 **React props에서 자주 사용되는 패턴**을 예제 중심으로 정리한다.

구조분해 할당을 제대로 이해하려면 먼저 [JavaScript 자료형](/posts/my-first-post/)에서 배열과 객체의 기본 개념을 알아야 한다.

---

## **1️⃣ 구조분해 할당이란?**

배열이나 객체 내부 값을 변수로 분해해서 한 번에 할당할 수 있게 해주는 문법이다.

```javascript
// 기존 방식
const name = user.name;
const age = user.age;

// 구조분해 할당
const { name, age } = user;
```

<div class="study-card-grid">
  <div class="study-card">코드 간결화</div>
  <div class="study-card">가독성 향상</div>
  <div class="study-card">React 필수 문법</div>
  <div class="study-card study-card--benefit">실무 활용도 높음</div>
</div>

### 🔍 배열 vs 객체 구조분해 차이

| 타입 | 기준 | 예시 | 기억 포인트 |
|------|------|------|-------------|
| 배열 | **순서(index)** | `[a, b] = [10, 20]` | 자리에 따라 값이 들어감 |
| 객체 | **이름(key)** | `{name} = user` | 이름만 같으면 어디 있어도 연결됨 |

![배열은 순서 기준, 객체는 키 이름 기준으로 구조분해되는 차이를 보여주는 비교 다이어그램](/assets/img/javascript/js-destructuring-compare.png)

---

## **2️⃣ 배열 구조분해**

배열은 **순서(index)** 기준으로 값이 매칭된다.

### 👉🏻 기본 문법

```javascript
const numbers = [10, 20, 30];
const [a, b] = numbers;

console.log(a); // 10
console.log(b); // 20
```

### 👉🏻 값 건너뛰기

콤마(`,`)로 해당 위치를 건너뛸 수 있다.

```javascript
const arr = [5, 10, 15];
const [x, , z] = arr;

console.log(x); // 5
console.log(z); // 15
```

### 👉🏻 기본값 설정

값이 `undefined`일 때 사용할 기본값을 지정할 수 있다.

```javascript
const arr = [1];
const [a, b = 100] = arr;

console.log(a); // 1
console.log(b); // 100 (기본값 적용)
```

### 👉🏻 나머지 값 받기 (rest)

`...rest` 문법으로 남은 요소들을 모두 배열로 담는다.

```javascript
const numbers = [1, 2, 3, 4, 5];
const [a, b, ...rest] = numbers;

console.log(a);    // 1
console.log(b);    // 2
console.log(rest); // [3, 4, 5]
```

### 👉🏻 변수 값 교환

구조분해를 활용하면 임시 변수 없이 두 변수의 값을 교환할 수 있다.

```javascript
let x = 10;
let y = 20;

[x, y] = [y, x];

console.log(x); // 20
console.log(y); // 10
```

---

## **3️⃣ 객체 구조분해**

객체는 **키 이름** 기준으로 분해된다.

### 👉🏻 기본 문법

```javascript
const user = {
  name: 'jerry',
  age: 30,
  city: 'seoul'
};

const { name, age } = user;

console.log(name); // 'jerry'
console.log(age);  // 30
```

### 👉🏻 다른 이름으로 받기 (Alias)

`기존키: 새이름` 형태로 변수명을 바꿀 수 있다.

```javascript
const user = { name: 'jerry', age: 30 };
const { name: userName } = user;

console.log(userName); // 'jerry'
```

### 👉🏻 기본값 설정

```javascript
const user = { name: 'jerry' };
const { name, age = 25 } = user;

console.log(name); // 'jerry'
console.log(age);  // 25 (기본값 적용)
```

### 👉🏻 Alias + 기본값 함께 사용

```javascript
const user = { name: 'jerry' };
const { name: userName, age: userAge = 25 } = user;

console.log(userName); // 'jerry'
console.log(userAge);  // 25
```

---

## **4️⃣ 중첩 구조분해**

배열 안의 배열, 객체 안의 객체도 한 번에 풀어낼 수 있다.

### 👉🏻 중첩 배열

```javascript
const arr = [1, [2, 3], 4];
const [a, [b, c], d] = arr;

console.log(a, b, c, d); // 1 2 3 4
```

### 👉🏻 중첩 객체

```javascript
const user = {
  name: 'narae',
  age: 26,
  address: {
    city: 'Seoul',
    zip: 12345
  }
};

const {
  name,
  age,
  address: { city, zip }
} = user;

console.log(name, age, city, zip);
// 'narae' 26 'Seoul' 12345
```

> **주의**: 중첩 구조분해에서 `address`는 변수로 선언되지 않는다. `city`와 `zip`만 변수로 사용할 수 있다.

---

## **5️⃣ 함수 파라미터에서 구조분해**

함수의 파라미터에서 바로 구조분해하면 코드가 더 깔끔해진다.

```javascript
// 기존 방식
function greet(user) {
  console.log(`안녕, ${user.name}!`);
}

// 구조분해 활용
function greet({ name, age }) {
  console.log(`안녕, ${name}! 나이는 ${age}살이구나.`);
}

greet({ name: 'jerry', age: 30 });
// '안녕, jerry! 나이는 30살이구나.'
```

---

## **6️⃣ React props 활용**

React에서 props는 항상 **객체**로 전달된다. 구조분해를 사용하면 코드가 훨씬 간결해진다.

```jsx
// 구조분해 없이
function Button(props) {
  return <button>{props.label}</button>;
}

// 파라미터에서 바로 구조분해
function Button({ label, size }) {
  return <button className={size}>{label}</button>;
}
```

`{label, size}`가 구조분해 할당이다. `label`은 `props.label`을, `size`는 `props.size`를 꺼낸 변수다.

### 🔍 React에서 props 흐름

![부모 컴포넌트에서 자식 컴포넌트로 props가 전달되고 구조분해로 추출되는 흐름을 보여주는 다이어그램](/assets/img/javascript/js-react-props-flow.png)

React를 더 배우고 싶다면 [React 입문 가이드](/posts/react-beginner-jsx-component/)를 참고하자.

---

## **7️⃣ 자주 묻는 질문**

### 구조분해 할당은 언제 쓰나요?

API 응답 데이터를 처리하거나, 함수에서 여러 값을 반환받을 때, React에서 props나 state를 다룰 때 자주 사용한다.

### spread 연산자와 rest는 같은 건가요?

문법은 같지만(`...`) 용도가 다르다. **spread**는 배열/객체를 펼칠 때, **rest**는 나머지를 모을 때 사용한다.

```javascript
// spread: 펼치기
const arr1 = [1, 2];
const arr2 = [...arr1, 3, 4]; // [1, 2, 3, 4]

// rest: 모으기
const [a, ...rest] = [1, 2, 3, 4]; // rest = [2, 3, 4]
```

### 구조분해가 성능에 영향을 주나요?

일반적인 사용에서는 성능 차이가 거의 없다. 가독성과 유지보수성을 높여주기 때문에 적극적으로 사용하는 것이 좋다.

---

## **8️⃣ 학습 정리**

이번 글에서 다룬 JavaScript 구조분해 할당의 핵심 포인트:

| 패턴 | 문법 | 용도 |
|------|------|------|
| 배열 기본 | `[a, b] = arr` | 순서대로 추출 |
| 배열 건너뛰기 | `[a, , c] = arr` | 특정 인덱스 스킵 |
| 배열 rest | `[a, ...rest] = arr` | 나머지 모아담기 |
| 객체 기본 | `{name} = obj` | 키 이름으로 추출 |
| 객체 alias | `{name: n} = obj` | 다른 변수명 사용 |
| 중첩 | `{a: {b}} = obj` | 깊은 값 추출 |

구조분해 할당을 익히면 코드가 간결해지고, 특히 React 개발에서 필수적으로 사용하게 된다.

---

## 다음 글

👉 [JavaScript 얕은 복사 vs 깊은 복사](/posts/js-shallow-and-deep/) - 객체 참조와 불변성의 개념을 알아보자.

---

## 참고 자료

- [MDN Web Docs - 구조분해 할당](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)
- [MDN Web Docs - 전개 구문](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/Spread_syntax)
- [MDN Web Docs - 나머지 매개변수](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Functions/rest_parameters)