---
layout: post
title: "[TypeScript] 데이터 타입 (3) 객체 타입 확장과 응용 Interface·Utility·Enum"
date: 2025-10-19 00:00:00 +0900
categories: [frontend, typeScript]
tags: [typescript, interface, utility-types, enum, record, partial, pick, omit]
image: https://images.velog.io/images/doodream/post/30a1865e-bfbf-4feb-8dfd-3122bda13845/ts%20%E1%84%8A%E1%85%A5%E1%86%B7%E1%84%82%E1%85%A6%E1%84%8B%E1%85%B5%E1%86%AF.png
---

## **1. 인터페이스 (Interface)**
- **인터페이스**는 객체의 형태(구조)를 정의한다.  
- `extends`, `readonly`, `?`, `[key: string]` 등을 통해 **유연하고 확장 가능**하다.  
- `type`과 달리 **병합 (Declaration Merging)** 이 가능하다.

---

### **1-1. 기본 구조**
- 객체의 속성과 타입 구조를 미리 정의해 **일관된 형태의 데이터**를 유지하게 한다.

```ts
interface User {
  name: string;
  age: number;
}

const user: User = {
  name: "jerry",
  age: 30,
};
```

### 1-2 선택적 속성과 읽기 전용 속성
- interface에서도 객체 리터럴 타입과 동일하게 `?(옵션), readonly(읽기 전용)` 을 사용할 수 있다. <br />
- **재사용성과 확장성 면에서 `type`보다 유리**하다.

```ts
interface User {
  name: string;
  age?: number; // 선택적 속성
  readonly id: number; // 읽기 전용 속성
}

const person: User = { id: 1, name: "poby" };
person.name = "jerry";
person.id = 2; // ❌ 에러 - 읽기 전용은 값 변경 안됨
```

### 1-3. 인터페이스 확장 (extends)
- `extends`를 사용하면 기존 인터페이스를 **상속**받하여 속성 추가할 수 있다.
- **중복 선언 없이 구조 재사용**이 가능하다.

```ts
interface Person {
  name: string;
  age: number;
}

interface Developer extends Person {
  skills: string[];
}

const dev: Developer = {
  name: "jerry",
  age: 30,
  skills: ["React", "Figma"],
};
```

### 1-4. 병합 (Declaration Merging)
- 같은 이름의 인터페이스를 여러 번 선언하면 **자동으로 병합된다.**
- `type`에서는 불가능한 **인터페이스 고유기능**이다.

```ts
interface Product {
  name: string;
}
interface Product {
  price: number;
}

const item: Product = {
  name: "Keyboard",
  price: 49000,
};
```

### 1-5. 인덱스 시그니처 (Index Signature)
- 키 이름이 **미리 정해지지 않은 객체 구조**를 정의할 때 사용한다.
- **모양만 같으면 같은 타입**으로 인식한다.

```ts
// type 별칭으로 정의(interface와 같은 의미)
type StringDictionary = {
  [key: string]: string;
};

// interface로 정의(확장성과 병합)
interface StringDictionary {
  [key: string]: string; 
}

const colors: StringDictionary = {
  red: "#FF0000",
  blue: "#0000FF",
};
```

### 1-6. 정리

|       키워드       | 기능    | 예시                        |
| :-------------: | :---- | :------------------------ |
|       `?`       | 선택 속성 | `age?: number`            |
|    `readonly`   | 수정 불가 | `readonly id: number`     |
|    `extends`    | 확장    | `interface B extends A`   |
|        병합       | 자동 합침 | `interface A {}` + `A {}` |
| `[key: string]` | 동적 키  | `{ [k: string]: string    |



## 2. 유틸리티 타입 (Utility Types)
- **타입을 만드는 함수형 도구**이다.
- 제네릭(Generic)과 조건부 타입을 활용해 **타입을 재가공**한다
- 실무에서 데이터 **구조를 변형하거나 일부 속성만 제어할 때 자주 사용된다.**

### 2-1. Partial<T>
- 특정 타입의 모든 속성을 **선택적 (옵션)** 으로 바꾼다.
- 일부 속성만 작성해도 오류가 나지 않는다.

```ts
interface Post {
  title: string;
  tags: string[];
  content: string;
  thumnailURL? : string
}

const draft: Partial<Post> = { // 일부만 있어도 OK
  title: `jerry's blog`
}
```

### 2-2. Required<T>
- 특정 객체 타입의 모든 속성을 **필수 (required)** 로 만든다.
- 하나라도 빠지면 오류 발생한다.

```ts
interface User { 
  name: string; 
  age?: number; }

const u2: Required<User> = { 
  name: "jerry" }; // ❌ 오류! age가 빠져있음

```


### 2-3. Pick<T>
- 필요한 속성만 **골라서 새로운 타입**을 만든다.

```ts
interface User { 
  name: string;
  age: number; 
  email: string; }

type BasicInfo = Pick<User, "name" | "age">;
const u3: BasicInfo = { name: "jerry", age: 3 };
```

### 2-4. Omit<T,K>
- 특정 속성만 **제외 (Omit)** 해서 새 타입을 만든다.
- `Pick` 의 반대 개념이다.

```ts
type ProductBasic = Omit<Product, "description">;

const p2: ProductBasic = {
  id: 2,
  name: "딸기우유",
  price: 1800,
  // description: "맛있어요" 은 제외됨
};
```

### 2-5. Readonly<T>
- 모든 속성을 읽기 전용(Readonly) 으로 만들어
수정이 불가능하도록 한다.

```ts
const user: Readonly<User> = {
  name: "Poby",
  age: 5,
  email: "poby@gmail.com",
};

user.age = 6; // ❌ 에러!
```
### 2-6. Record<K,T>
- **`key`와 `value`의 타입을 동시에 정의**할 수 있는 구조
- 객체를 사전처럼 다룰 때 유용하다.

```ts
// Key는 string, Value는 boolean
const permission: Record<string, boolean> = {
  admin: true,
  editor: false,
};

// Key를 특정 값으로 제한할 수도 있음
type Role = "admin" | "user" | "guest";
const roleAccess: Record<Role, number> = {
  admin: 1,
  user: 2,
  guest: 3,
};
```

### 2-7. 한눈에 비교하기

| 유틸리티     | 설명   | 예시                    |
| -------- | --------- | --------------------- |
| Partial  | 속성 선택적    | `Partial<User>`       |
| Required | 속성 필수     | `Required<User>`      |
| Pick     | 선택 사용     | `Pick<User, "name">`  |
| Omit     | 제외 사용     | `Omit<User, "pw">`    |
| Readonly | 읽기 전용     | `Readonly<User>`      |
| Record   | key-value | `Record<string, num>` |

## 3. enum  (열거형)
- 의미 있는 **상수 집합**을 정의하는 타입.
- 고정된 선택지를 만들어 코드의 가독성과 안정성을 높인다.

```ts
// 기본형
enum Direction {
  Up,
  Down,
  Left,
  Right,
}

let move: Direction = Direction.Up;
console.log(move); // 0

// 문자열 (직접 값 지정)
enum Role {
  Admin = "ADMIN",
  User = "USER",
  Guest = "GUEST",
}

const userRole: Role = Role.Admin;
console.log(userRole); // "ADMIN"
```

### 3-1. as const + type (요즘 방식)
- `enum` 대신 **가벼운 상수 객체**를 만드는 최신 패턴이다.

```ts
const Day = {
  Mon: "Mon",
  Tue: "Tue",
  Wed: "Wed",
  Thu: "Thu",
  Fri: "Fri",
} as const;

let today = Day.Mon; // ✔️ 가능
today = Day.Fri;     // ✔️ 가능
today = "Sunday";    // ❌ 에러! 

```

![js vs ts 이미지](https://edgio.clien.net/F01/13061098/2643ecab6c3e05.jpg?scale=width:480)

<br />

💡 **학습정리**

> **인덱스 시그니처** ➡ 키 이름이 정해지지 않은 객체 구조를 표현할 때 사용 <br/>
> **interface** ➡ 확장(`extends`), **type** ➡ 교차(`&`) 로 확장 방식이 다름 <br/>
> 일반적으로 **type**은 데이터 구조 정의용, **interface**는 컴포넌트 `props`나 `API` 응답 구조에 적합 <br/>
> **Partial:** 선택적 / **Required:** 필수 / **Pick:** 선택 / **Omit:** 제외 / **Readonly:** 수정 불가 / **Record:** 키-값 정의 <br/>
> **enum:** 정해진 값만 사용할 수 있는 상수 집합 <br/>
> **as const:** `enum`처럼 가볍게 쓸 수 있는 **읽기 전용 상수 객체**

