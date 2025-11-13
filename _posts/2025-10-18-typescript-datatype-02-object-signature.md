---
layout: post
title: "[TypeScript] 데이터 타입 (2) 객체 타입 리터럴·별칭·시그니처"
date: 2025-10-18 00:00:00 +0900
categories: [frontend, typeScript]
tags: [typescript, object, index-signature, literal, type, type-alias]
image: https://images.velog.io/images/doodream/post/30a1865e-bfbf-4feb-8dfd-3122bda13845/ts%20%E1%84%8A%E1%85%A5%E1%86%B7%E1%84%82%E1%85%A6%E1%84%8B%E1%85%B5%E1%86%AF.png
---

## **1. 객체 리터럴 타입 (Object Literal Type)**
- `{ key: value }` 구조를 가지며, 각 속성의 **타입을 명시**할 수 있다.  
- 타입스크립트는 **구조적 타입 시스템(Structural Type System)** 을 사용해  <br />
  모양(형태)이 같으면 허용, 다르면 오류를 낸다.  
- 선언 시 **모든 속성의 타입이 일치**해야 하며, 누락되거나 다른 타입이 들어가면 오류 발생.

```ts
// ✔️ 올바른 예시 
let user: { name: string; age: number } = {
  name: "jerry",
  age: 3,
};

// ❌ 오류 (타입 불일치)
user = {
  name: "jerry",
  age: "30",
};
```

### 1-1. 선택적 속성 (Optional Property)
- 있어도 되고 없어도 되는 속성은 `?` 로 표시

```ts
let user: { name: string; age?: number } = { name: "jerry" };
```

### 1-2. 읽기 전용 속성 (Readonly Property)
- 한 번 지정하면 **수정이 불가능**하다.

```ts
let config: { readonly version: string } = { version: "1.0.0" };
// config.version = "2.0"; ❌ 오류
```

## **2. 타입 별칭 (Type Alias)**
- 자주 쓰는 타입 구조에 **이름을 붙여 재사용**할 수 있다.
- `type` 키워드를 사용하며, **객체 타입이 복잡하거나 반복**될 때 유용하다.
- 객체 타입이 복잡하거나 반복될 때 유용함
- 함수 내부에서 같은 이름을 쓰면 **안쪽이 우선 적용**된다.

```ts
// ✔️ 타입 별칭 선언
type User = {
  name: string;
  age: number;
};

// ✔️ 타입 별칭 사용
let user1: User = { name: "jerry", age: 3 };
let user2: User = { name: "tom", age: 5 };
```

## **3. 인덱스 시그니처 (Index Signature)**
- 객체의 `key`가 **정해져 있지 않고 동적일 때** 타입을 지정하는 문법  
- `[key: string]: valueType` 형태로 정의하여 **유연한 객체 구조**를 표현할 수 있다.
- 모든 `key`의 **`value` 타입이 동일해야 함**에 주의.

```ts
// ✔️ 모든 key와 value는 문자열이어야 함
type CountryCodes = {
  [key: string]: string;
};

let countryCodes: CountryCodes = {
  Korea: "ko",
  Japan: "jp",
  UnitedStates: "us",
};

// ✔️ 값 타입 제한 예시
type UserAge = {
  [key: string]: number;
};

let userAge: UserAge = {
  jerry: 3,
  tom: "5", // ❌ 오류 (모든 속성의 값 타입이 동일해야 함)
};
```

## 4. 객체 타입 요약 정리

| 구분   | 문법                   | 핵심        | 시점    | 주의          |
| ---- | -------------------- | --------- | ----- | ----------- |
| 리터럴  | `{ name: string }`   | 객체 구조 명시  | 기본 정의 | 타입 불일치 ❌    |
| 선택속성 | `{ age?: number }`   | 생략 가능     | 값 선택적 | 존재 안 할 수도   |
| 별칭   | `type User = {...}`  | 타입 이름화    | 재사용   | 중복명 주의      |
| 시그니처 | `{ [k: string]: n }` | 동적 key 정의 | 유동 구조 | value 타입 통일 |

<br />

💡 **학습정리**

> **객체 리터럴** ➡ 객체의 틀을 정함 <br />
> **선택적 속성** ➡ 있어도 되고 없어도 됨 <br />
> **타입 별칭** ➡ 이름 붙여 재사용 가능 <br />
> **인덱스 시그니처** ➡ `key`가 바뀌어도 OK (동적 구조)
