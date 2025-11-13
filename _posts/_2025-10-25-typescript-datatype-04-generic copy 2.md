---
layout: post
title: "[TypeScript] 데이터 타입 (4) 제네릭 심화와 응용"
date: 2025-10-25 00:00:00 +0900
categories: [frontend, typeScript]
tags: [typescript, generic, keyof, extends, utility-type, infer]
image: https://images.velog.io/images/doodream/post/30a1865e-bfbf-4feb-8dfd-3122bda13845/ts%20%E1%84%8A%E1%85%A5%E1%86%B7%E1%84%82%E1%85%A6%E1%84%8B%E1%85%B5%E1%86%AF.png
---

## **1. 제네릭 (Generic)이란?**
- **제네릭(Generic)**은 타입을 **함수처럼 재사용**할 수 있게 해주는 기능이다.  
- 데이터 타입을 **고정하지 않고**, **사용하는 시점에 타입을 결정**한다.  
- 즉, 타입에 **유연성과 재사용성**을 부여하는 문법이다.  
- 흔히 타입 매개변수(Type Parameter)로 `T`, `U`, `K` 등을 사용한다.

```ts
function identity<T>(value: T): T {
  return value;
}

let arr = func<[number, number, number]>([1,2,3]); // 튜플 활용
identity<string>("hello"); // "hello"
identity<number>(123);     // 123
identity(true);            // 타입 추론으로 boolean 인식
```

### **1-1. 타입 변수 응용**
- 제네릭은 여러 개의 타입 변수를 동시에 사용할 수도 있고,  
배열과 함께 쓰면 **타입 안정성**을 유지하면서 데이터를 다룰 수 있다.

```ts
// 예시 1 : 타입 변수 여러개 선언
function swap<T, U>(a:T, b:U) { 
  return [b,a]
}

const [a,b] = swap('1',2);

// 예시 2 : 제네릭 + 배열
function returnFirstValue<T>(data: T[]) { // T[] : T 타입의 배열
  return data[0]; // 그 배열의 첫번째 요소 반환
}

let num = returnFirstValue([0, 1, 2]); // 0

let str = returnFirstValue(["hello", "mynameis"]); // hello

// 예시 3 : 
function first<T>(data: [T, ...unknown[]]) { // 첫번째 값만 타입 고정
  return data[0];
}

let a = first(["jerry", 1, true]);  // jerry
let b = first([99, "hi", false]); // 99
```

### **1-2. 제네릭 + 배열 메서드 (map, forEach)**
- 제네릭은 `map()`이나 `forEach()` 같은 배열 메서드에서도
**타입을 안전하게 유지하면서 반복 작업**을 수행할 수 있다.

#### map()
- 제네릭으로 구현하면 타입이 자동 추론되어 `any` 없이도 안전하게 동작함

```ts
// 기본 map() 메서드 함수
const arr = [1, 2, 3];
const newArr = arr.map((it) => it * 2); // [2, 4, 6]

//  제네릭으로 map() 구현
function map<T>(arr: T[], callback: (item: T) => T) {
  let result = [];
  for (let i = 0; i < arr.length; i++) {
    result.push(callback(arr[i]));
  }
  return result;
}

const doubled = map(arr, (it) => it * 2); 

// 실행결과
map([1, 2, 3], (n) => n * 2); // [2, 4, 6]
map(["a", "b"], (ch) => ch.toUpperCase()); // ["A", "B"]
```

#### forEach()
- `forEach()`는 배열의 각 요소를 순회하면서 **특정 동작을 수행**하는 함수이다.
- `map()`과 달리 **새 배열을 반환하지 않고** 주어진 콜백 함수를 실행한다.
- 제네릭을 사용하면 어떤 타입의 배열이든 안전하게 처리할 수 있다.

```ts
// 기본 forEach() 메서드 함수
const animals = ["dog", "cat", "bird"];

animals.forEach((animal) => {
  console.log(`I love ${animal}!`); 
});

// 제네릭으로 forEach() 구현

function forEach<T>(arr: T[], callback: (item: T) => void) {
  for (let i = 0; i < arr.length; i++) {
    callback(arr[i]); // 배열의 각 요소를 콜백으로 전달
  }
}

// 실행 예시
forEach(["jerry", "bango", "poby"], (name) => {
  console.log(`This is ${name}`);
});

```

### **1-3. 제약 조건 (Extends)**
- `extends`는 **제네릭 타입에 조건을 걸 때** 사용한다.

```ts
// 예시 1 : map()
 
```