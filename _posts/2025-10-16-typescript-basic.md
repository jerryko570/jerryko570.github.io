---
layout: post
title: "TypeScript 기본 동작 원리 | 컴파일과 타입 체크 흐름"
description: "TypeScript 코드가 컴파일되고 타입이 검사되는 과정을 전체 흐름 관점에서 이해해봅니다."
date: 2025-10-16 22:02:00 +0900
categories: [frontend, typescript]
tags:
  - typescript
  - transpile
  - compile
  - javascript
  - tsc
  - type-checking
series: typescript
image: /assets/img/thumbnail/typescript.png
---

## **1. TypeScript? 타입스크립트!**
- **TypeScript**는 **타입을 통해 오류를 미리 잡고**, **자바스크립트로 변환되는 언어**이다.  
- 새로운 언어가 아니라, **자바스크립트의 상위(Superset) 언어**이다.  
> 즉, 자바스크립트 문법 위에 **타입 시스템이 추가된 확장 언어**이다.  
- 코드 실행 전에 오류를 감지하고, **컴파일 후에는 순수한 자바스크립트(.js)** 로 변환되어  
  **브라우저나 Node.js 환경에서 실행된다.**


---

## **2. 동작 원리**
![타입스크립트 동작원리](/assets/img/typescript/typescript.png)

> 타입스크립트는 **실행 전에 코드의 안전성을 검사하고,실행은 자바스크립트가 맡는 구조**이다.

#### **작성 (Authoring)**
- `.ts` 파일에 타입이 포함된 코드를 작성한다.

#### **컴파일 준비 (tsc)**
- **`tsc`**(TypeScript Compiler) 가 코드를 읽고 AST(추상 문법 트리) 라는 구조를 만든다.
- 즉, 이 코드에 어떤 변수,함수,타입이 있는지 구조적으로 분석함.

#### **타입 검사 (Type Checking)**
  - AST를 기반으로 **타입이 맞는지 확인**한다. 
  - 모든 설정은 **tsconfig.json**에 따라 달라진다.
  - **`target`** : 변환될 JS 버전 
  - **`strict`** : 검사 강도
  - **`outDir`** : 결과 저장 위치

#### **트랜스파일 (Transpile)**
- 검사 통과 후, **타입 정보는 싹 지우고 순수 JS 코드로 변환한**다.
- 브라우저나 Node.js가 이해할 수 있는 형태로 바뀐다.

#### **실행 (Runtime)**
- 변환된 `.js` 파일이 `브라우저`나 `Node.js` 환경에서 실행된다.  
- 이 시점부터는 타입스크립트의 역할이 끝난다.  
- 타입 검사는 컴파일 시점에만 이루어지며, **실행 시점에는 자바스크립트 코드만 동작한다.**

---

## **3. 컴파일 과정 예시**

```ts
let message: string = "Hello TypeScript!";

// ❌ 타입 오류 발생
// message 변수에 string(문자열) 타입을 선언한다.
// 숫자 123을 대입하여 타입 불일치 오류가 발생한다.
message = 123;
```

#### 타입 컴파일러 (tsc) 오류 출력
  > `Type 'number' is not assignable to type 'string'.`
  - 실행 전(Compile-time) 단계에서 오류를 감지하여 **버그를 사전에 방지**한다.

  
#### 변환 후 자바스크립트 코드**
  - 모든 타입 정보 (:string)가 제거되고 순수 자바스크립트 코드로 변환된다.

```javascript
// JavaScript (Transpiled)
let message = "Hello TypeScript!";
message = 123;
```

## **4. TypeScript vs JavaScript**

| 구분        | TypeScript (.ts)          | JavaScript (.js)  |
| --------- | ------------------------- | ----------------- |
| **코드 예시** | `let count: number = 10;` | `let count = 10;` |
| **타입 검사** | 있음 (컴파일 시점)               | 없음 (런타임 시점)       |
| **실행 환경** | 컴파일러(tsc)                 | 브라우저 / Node.js    |
| **타입 정보** | 유지됨 (개발 중만)               | 제거됨               |


<br />

💡 **학습정리**

> 타입스크립트는 **개발 중에 오류를 미리 잡고**, 실행 시에는 **자바스크립트 코드로만 동작한다.**  
> 브라우저와 Node.js는 **타입 정보를 인식하지 못하며**, 변환된 코드만 실행한다.  
> 따라서 타입스크립트는 **개발자의 실수를 예방하고 코드 품질과 유지보수 효율을 높이는 언어이다.**