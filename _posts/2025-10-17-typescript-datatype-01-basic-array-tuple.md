---
layout: post
title: "[TypeScript] 데이터 타입 (1) 기본과 배열·튜플"
date: 2025-10-17 00:00:00 +0900
categories: [frontend, typescript]
tags: [typescript, basic, any, unknown, void, never, array, tuple]
series: "typescript"
image: /assets/img/thumbnail/typescript.png
---

## **1. 기본 타입 (Basic Types)**
- 가장 기본적인 데이터 타입  
- `number`, `string`, `boolean`, `null`, `undefined` 등 기본 자료형  

```ts
let age: number = 25; // 숫자형     
let username: string = "jerry"; // 문자열
let isAdmin: boolean = true; // 불리언
let empty: null = null; // null
let notDefined: undefined = undefined; // undefined
```

## **2. 원시 타입 (Primitive Types)**

- 값 자체를 저장하는 타입 (`string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`)  
- 복사할 때 **참조가 아닌 값 그대로 복사됨**  
- 모두 **값 타입(Value Type)** 으로, 메모리 상에서 독립적으로 존재함  

```ts
let id: symbol = Symbol("id"); // 고유한 식별자
let big: bigint = 12345678901234567890n; // 아주 큰 정수
```

## **3. 특수 타입 (Special Types)**
- 타입스크립트에서만 제공되는 타입으로, **자바스크립트의 한계를 보완하기 위해 만들어짐**

| 구분 | 타입 | 설명 |
|:--:|:--:|:--|
| 3-1 | **Any** | 모든 타입 허용(비추천) |
| 3-2 | **Unknown** | 안전한 any — 타입 검사 필요 |
| 3-3 | **Void** | 반환값 없음 |
| 3-4 | **Never** | 절대 종료되지 않음 / 예외 발생 |


### **3-1. Any**
- 모든 타입을 허용하는 **무제한 타입**  
- 편리하지만 **타입 안정성이 전혀 없음**  
- 주로 **임시 변수**나 **점진적 마이그레이션** 과정에서만 사용  

```ts
let data: any = 5;
data = "Hello"; // OK
data = true;    // OK
data = [1, 2, 3]; // OK
data(); // ❌ 에러! (컴파일러가 체크 불가)

```

### **3-2. Unknown**
- `any`처럼 모든 값을 받을 수 있지만, **사용 전 반드시 타입을 확인해야 함**  
- 주로 **외부 데이터 (API 응답)** 처리 시 안전하게 사용됨  
- **타입을 좁히기 (narrowing)** 해야만 내부 속성이나 메서드 사용 가능  

```ts
let input: unknown = "hello";

if (typeof input === "string") {
  console.log(input.toUpperCase()); // ✔️ 타입 좁히기 후 사용 가능
}

input.toUpperCase(); // ❌ 에러! 타입 확인 전엔 사용 불가

```

### **3-3. Void**
- **아무것도 반환하지 않는 함수의 반환 타입**  
- 오직 `undefined`만 허용되며, `return`문이 없는 함수에 사용  
- `console.log`, `alert` 등 **출력 전용 함수**에서 자주 사용  
- `void`는 **타입**, `undefined`는 **값**을 의미함  

```ts
function logMessage(message: string): void {
  console.log(message);
}

```

### **3-4. Never**
- **절대 끝나지 않는 함수의 반환 타입**  
- `throw`(예외 발생) 또는 `while(true)`(무한 루프)처럼  
  **프로그램이 멈추거나 종료되지 않는 흐름**을 표현할 때 사용  
- **어떠한 값도 반환하지 않으며**, 실행이 정상적으로 끝나지 않음  
- `switch` 문에서 **모든 경우의 수를 처리했는지 검사**할 때도 활용됨  

```ts
function throwError(msg: string): never {
  throw new Error(msg); // ❌ 예외 발생 후 프로그램 중단
}

function infiniteLoop(): never {
  while (true) {} // 🔁 무한 반복 — 함수가 끝나지 않음
}
```

## **4. 배열 (Array)**
- 같은 타입의 데이터를 묶어서 저장할 때 사용함

| 구분     | 표기              | 예시                | 설명           |
| ------ | --------------- | ----------------- | ------------ |
| 기본 배열  | `type[]`        | `number[]`        | 단순하고 직관적     |
| 제네릭 배열 | `Array<T>`      | `Array<string>`   | 제네릭 문법 형태    |
| 2차원 배열 | `type[][]`      | `number[][]`      | 배열 안의 배열     |
| 다차원 배열 | `Array<type[]>` | `Array<number[]>` | 제네릭으로 다차원 표현 |

```ts
// 기본 배열 : type[]
let scores: number[] = [90, 80, 85]; 

// 2차원 배열 : type[][]
let doubleArr1: Array<number[]> = [
  [1, 2],
  [3, 4],
];

// 제네릭 문법 : Array<T>
let fruitsArr: Array<string> = ["apple", "banana", "cherry"]; 
let booArr: Array<boolean> = [true, false, true]

// 다차원 배열 (제네릭 문법 사용)
let doubleArr2: Array<number[]> = [
  [1, 2],
  [3, 4],
];

// 유니언 타입 (문자열과 숫자가 함께 들어갈 수 있음, 제네릭 문법 덕분에 복잡한 배열 가능)
let multiArr: Array<string | number> = ["a", 1, "b", 2];
```

## **5. 튜플 (Tuple)**
### **5-1. 특징**
- **배열의 길이와 타입이 고정된 배열**  
- 순서를 바꾸거나 길이가 달라지면 오류가 발생한다.
- 선언 시 각 위치(`index`)의 타입이 **미리 정의**되어 있다.
- `push`, `pop` 메서드는 가능하지만, **타입 체크가 완벽하지 않음**에 주의헤애 힌디.

```ts
let tup1: [number, number] = [1, 2];
let tup2: [number, string, boolean] = [1, "2", true];

// ❌ 오류 예시
tup1 = [1, 2, 3];  // Error: 길이 불일치
tup2 = ["2", 1, true]; // Error: 타입 순서 불일치

```

<br />

💡 **학습정리**

> **`기본 → 배열 → 튜플`** 순서로 갈수록 **구조 제약이 강해짐** <br />
> **`기본 타입`:** 값 하나에 대한 정확성 <br />
> **`any:`** 타입 검사 포기 <br />
> **`unknown:`** 타입 검사 필수 <br />
> **`void:`** 반환 없음 <br />
> **`never:`** 실행이 끝나지 않음 <br /> 
> **`배열:`** 같은 타입 값들의 집합 <br />
> **`튜플:`** 길이 + 순서 + 각 위치 타입까지 포맷 보장 <br />
> 타입은 **컴파일 단계에서만 검사**되고, **런타임에는 제거되어 JS로 실행됨**

