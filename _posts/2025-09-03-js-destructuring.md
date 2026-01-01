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

## **1.구조분해 할당 (Destructuring)**
- 값을 **쉽게 꺼내쓰기 위한 문법**이고, 배열이나 객체 내부 값을 변수로 분해해서 한 번에 할당할 수 있게 해주는 자바스크립트 기능이다.
> const {구조분해할 데이터들 } = 진짜 데이터
> const [ 내가 받을 값들 ] = 실제 배열



| 타입 | 기준            | 예시                  | 기억 포인트             |
| -- | ------------- | ------------------- | ------------------ |
| 배열 | **순서(index)** | `[a, b] = [10, 20]` | 자리에 따라 값이 들어감      |
| 객체 | **이름(key)**   | `{name} = user`     | 이름만 같으면 어디 있어도 연결됨 |


#### 1-1.배열 구조 분해 할당
- 배열의 **순서(index)** 기준으로 값이 들어간다.

```js
const numbers = [10, 20, 30];
const [a, b] = numbers;

console.log(a); // ✔️ 10
console.log(b); // ✔️ 20
```

#### 1-2.값 건너뛰기

```js
const arr = [5,10,15];
const [x, ,z] = arr;

console.log(x) // ✔️ 5
console.log(z) // ✔️ 15
```
- **콤마(,)**는 해당 위치를 건너뛴다.

#### 1-3.나머지 값 받기 (...rest)
- 남은 요소들을 모두 배열로 담는다.

```js
const numbers = [1, 2, 3, 4, 5];
const [a, b, ...rest] = numbers;

console.log(a) // ✔️ 1
console.log(b) // ✔️ 2
console.log(rest) // ✔️ [3, 4, 5]
```


## **2.객체 구조 분해 할당**
- 객체는 **키 이름 기준**으로 분해된다.

```js
const user = {
  name: 'jerry',
  age: 30;
  city: 'seoul'

  const {name, age} = user;

  console.log(name) // ✔️ jerry
  console.log(age) // ✔️ 30
}
```

### 2-1.다른 이름으로 변수 받기 (Alias)

```js
const user = {name: 'jerry', age: 30};
const {name: userName} = user;

console.log(userName) // ✔️ jerry
```

### 2-2.중첩 구조 분해 할당
- 배열 안에 배열이 있거나, 객체 안에 객체가 있을 때 **한 번에 구조를 풀어내는 문법**
- 배열의 구조 그대로 모양을 맞춰서 변수에 담는다.

#### 배열 안에 배열이 있는 경우 
```js
const arr = [1, [2,3], 4];

// 중첩 구조분해를 사용하면 
const [a, [b, c], d] = arr;
console.log(a, b, c, d); // 1 2 3 4
```

#### 객체 안에 객체가 있는 경우 
- 객체의 구조를 그대로 따라가면서 값들을 꺼낼 수 있다.

```js
const user = {
  name: "narae",
  age: 26,
  address: {
    city: "Seoul",
    zip: 12345
  }
};

// 중첩 구조분해를 사용하면
const {
  name,
  age,
  address: { city, zip }
} = user;

console.log(name, age, city, zip);
```

### 3.React에서 props 받을 때의 구조분해 
- 파라미터 { label, size} 이부분이 구조분해 할당이고, props.label과 props.size를 미리 꺼내놓은 변수이다.
> {} ➡ 구조 분해 할당 문법
> label ➡ props.label을 꺼낸 “새 변수”
> size ➡ props.size를 꺼낸 “새 변수”
- 리액트에서 props 항상 객체로 전달된다.

```jsx
// props.label 계속 써아햠 
function Button(props) {
  const label = props.label;
  const size = props.size;

  return <button>{label}</button>;
}

// 구조분해 할당 문법으로 함수 파라미터에서 바로 꺼내 쓸 수 있음!
function Button({ label, size }) {
  return <button>{label}</button>;
}
```