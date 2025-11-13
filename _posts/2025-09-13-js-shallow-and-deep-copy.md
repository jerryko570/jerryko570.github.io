---
layout: post
title: "[JavaScript] 얕은 복사와 깊은 복사의 차이"
date: 2025-09-13 15:11:00 +0900
categories: [frontend, javaScript]
tags: [javascript, vshallow copy, deep copy, object, reference]
image: https://joshua1988.github.io/images/posts/web/javascript/js.png
---

## **1. 얕은 복사 (Shallow Copy)**
### 1-1. 특징
- 객체의 **최상위 레벨(1단계) 속성만 복사하는 방식**이다.  
  - 원본 객체의 속성이 **기본 타입(숫자, 문자열, 불린)** 이면 **값 자체가 복사된다.**  
  - 원본 객체의 속성이 **참조 타입(객체, 배열 등)** 이면 **주소(레퍼런스)** 만 복사된다.

### **1-2. Object.assign()**
- `Object.assign()`은 **하나 이상의 객체를 합치거나 복사할 때 사용하는 메서드**이다.  
- 1단계(최상위) 속성만 복사하며, **얕은 복사만 수행한다.**

```javascript
Object.assign(복사될_객체, 원본_객체);
```

```javascript
const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = Object.assign({}, original);

console.log(copy);  // { name: 'jerry', address: { city: 'seoul' } }

copy.name = 'poby';  // 복사본의 최상위 속성 변경
console.log(original.name);  // 'poby' (원본은 영향 없음)

copy.address.city = 'busan';  // 중첩 객체의 속성 변경
console.log(original.address.city);  // 'busan' (원본도 변경됨, 참조 공유)
```

### 1-3. 스프레드 연산자
- `...`(스프레드 연산자)는 객체나 배열의 내용을 **펼쳐서 복사할 수 있다.**  
- 겉보기에는 완전히 복사된 것처럼 보이지만, 내부에 **참조 타입(객체, 배열)** 이 포함되어 있으면 **얕은 복사**가 된다.

```javascript
const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = { ...original };

console.log(copy);  // { name: 'jerry', address: { city: 'seoul' } }

copy.address.city = 'busan';  // 중첩 객체 수정
console.log(original.address.city);  // 'busan' (원본도 변경됨, 참조 공유)
```

### 1-4. 얕은 복사 방식 정리

| 복사 방법             | 복사 수준 | 특징                    |
| ----------------- | ----- | --------------------- |
| `...` 스프레드        | 얕은 복사 | 1단계만 복사, 중첩 객체는 참조 유지 |
| `Object.assign()` | 얕은 복사 | 동일하게 참조 복사, 원본 영향 있음  |


## **2. 깊은 복사 (Deep Copy)**
### 2-1. 깊은 복사는 무엇일까?
- 깊은 복사는 **객체의 내부 구조(중첩된 객체나 배열)까지 완전히 새로운 메모리에 복사하는 방식**이다.  
- 원본과 사본은 **서로 완전히 독립적이며**, 중첩 객체를 수정해도 **원본은 영향을 받지 않는다.**

### 2-2. JSON.stringify() + JSON.parse() 사용
- 가장 간단하고 널리 쓰이는 **깊은 복사 방식**이다.  
- 객체를 `JSON` 문자열로 바꿨다가 다시 객체로 변환해 복사한다.

```javascript
const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = JSON.parse(JSON.stringify(original));

copy.address.city = 'busan';

console.log(original.address.city); // 'seoul' (원본 영향 없음)
```

### 2-3. Lodash의 _.cloneDeep() 사용
- 가장 안정적이고 강력한 깊은 복사 방식
- 외부 라이브러리 lodash가 제공하는 기능

```javascript
const _ = require('lodash');

const original = { name: 'jerry', address: { city: 'seoul' } };
const copy = _.cloneDeep(original);

copy.address.city = 'busan';

console.log(original.address.city); // 'seoul'
```

### 2-4. 재귀 함수로 직접 구현한 깊은 복사
- 가장 안정적이고 강력한 깊은 복사 방식

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

### 2-5. 깊은 복사 방식 정리

| 방식                             | 장점          | 단점                    |
| ------------------------------ | ----------- | --------------------- |
| `JSON.parse(JSON.stringify())` | 간단, 빠름      | 함수·Symbol 손실, 순환참조 불가 |
| `_.cloneDeep()`                | 완전한 복사, 안전함 | 외부 라이브러리 필요           |
| `deepClone()` (직접 구현)          | 원리 이해에 도움   | 코드 길고, 예외처리 필요        |


## **3. 얕은 복사 vs 깊은 복사**

| 항목        | 얕은 복사 (Shallow Copy)     | 깊은 복사 (Deep Copy)               |
| --------- | ------------------------ | ------------------------------- |
| **복사 범위** | 1단계 속성만 복사, 중첩 객체는 참조 공유 | 모든 레벨 완전 복사                     |
| **참조 관계** | 원본과 복사본이 같은 참조 사용        | 서로 독립적인 참조                      |
| **영향 여부** | 원본 변경 시 복사본도 영향          | 서로 영향 없음                        |
| **방법**    | `Object.assign()`, `...` | `JSON.parse()`, `_.cloneDeep()` |


<br />

💡 **학습정리**
> 얕은 복사는 **복사처럼 보이지만 내부가 연결되어 있다.** <br />
> 깊은 복사는 **완전히 새로운 객체를 생성한다.** <br />
> 복사 수준을 이해하면 **데이터 불변성을 유지하고 버그를 예방하기 쉬워진다.**