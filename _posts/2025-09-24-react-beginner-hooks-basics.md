---
layout: post
title: "[React] 입문을 위한 기초 개념 정리 (2) useState·useEffect"
date: 2025-09-24 22:32:00 +0900
categories: [frontend, react]
tags: [react, useState, useEffect, EventHook]
image: https://velog.velcdn.com/images/henny/post/d3925f21-b23d-49a5-bbb9-1dc9087fe491/image.png
---

## **1. useState**
### 1-1. 특징
- `useState`는 **컴포넌트 안에서 변하는 값을 저장**하고,  
  값이 바뀌면 **UI가 다시 렌더링되게 만드는 상태 저장용 Hook**이다.  
- 컴포넌트가 **기억해야 하는 데이터를 리액트가 관리하도록 한다.**


```jsx
import { useState } from "react";

function Counter() {

const [count, setCount] = useState(0); // setCount : 상태를 변경하는 함수
const handleClick = () => {
  setCount(count + 1); // 클릭 시 count가 1 증가 (컴포넌트 전체 랜더링)
};

return (
  <div>
    <p>현재 카운트: {count}</p>
    <button onClick={handleClick}>+1</button>
  </div>
);
}

export default Counter;
```

### 1-2. 비동기 업데이트
- `setCount()`는 **즉시 실행되지 않고**, 리액트가 **다음 렌더링 사이클에서 한 번에 처리(batch)** 한다.  
- 따라서 `console.log()`로 바로 출력하면 **이전 값이 표시될 수 있다.**


```jsx
const [count, setCount] = useState(0);

const handleClick = () => {
  setCount(count + 1);
  console.log(count); // ❌ 여전히 이전 값
};

// 해결 방법 : 함수형 업데이트 사용하면 이전 상태값을 안전하게 참조 가능
setCount((prev) => prev + 1);
```

### 1-3. 여러 상태를 객체로 묶기
- 상태가 객체일 때는 반드시 **불변성(immutability)** 을 유지해야 한다.  
- 값을 직접 변경하면 리액트가 **변화를 감지하지 못한다.**


```jsx
const [user, setUser] = useState({ name: "jerry", age: 3 });

user.age = 4; // ❌ 직접 변경하면 리렌더링되지 않음

setUser({ ...user, age: 4 }); // 기존 값 복사 후 변경
```

### 1-4. 컴포넌트 단위로 독립적
- 동일한 컴포넌트를 여러 번 렌더링해도 **각자 독립된 상태를 가진다.**

### 1-5. 상태 유지
- 상태는 컴포넌트가 **언마운트되면 사라진다.**  
- 새로 마운트되면 다시 **useState의 초기값으로 돌아간다.**  
- 상태를 영구적으로 유지하려면  
  **`localStorage`, `sessionStorage`, `Redux`, `Context`** 등을 사용한다.

---

## **2. useEffect**
### 2-1. 주요 특징
- `useEffect`는 **렌더링 이후 실행되는 Hook**이다.  
- 컴포넌트의 **부수 효과(Side Effect)** 를 처리하는 역할을 한다.  
> 예: 데이터 fetch, 이벤트 등록, 타이머 설정, 콘솔 출력, DOM 조작 등  
- 컴포넌트가 **마운트되거나 상태·props가 변경될 때 실행된다.**


```jsx
import { useState, useEffect } from "react";

function Timer() {
  const [count, setCount] = useState(0);

  // count가 변경될 때마다 실행됨
  useEffect(() => {
    console.log("렌더링 또는 count 변경됨!");
  }, [count]); //  의존성 배열 (특정 값이 바뀔때만 실행되게 []로 제어함)

  return (
    <div>
      <p>카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}

export default Timer;
```

### 2-2. 의존성 배열 (Dependency Array)
- useEffect의 두번째 인자로 전달되는 배열은 언제 다시 실행할지 결정힌디.

| 패턴        | 설명         | 실행 시점                      |
| --------- | ---------- | -------------------------- |
| `[]`      | 의존성이 없음    | 컴포넌트가 **처음 마운트될 때 1회만 실행** |
| `[count]` | count 값 의존 | **count 값이 변경될 때마다 실행**    |
| (없음)      | 배열 자체를 생략  | **모든 렌더링마다 실행됨**           |


### 2-3. 클린업 (Cleanup)
- `useEffect` 내부에서 `return`문을 사용하면,  
  컴포넌트가 **언마운트되거나 의존성 값이 변경되기 직전에 정리(cleanup)** 작업이 실행된다.  
- 주로 **타이머, 이벤트 리스너, 외부 구독(API, WebSocket 등)** 을 정리할 때 사용한다.

```jsx
useEffect(() => {
  console.log("타이머 시작");
  const timer = setInterval(() => {
    console.log("1초 지남");
  }, 1000);

  // 클린업 함수
  return () => {
    console.log("타이머 정리");
    clearInterval(timer);
  };
}, []);

// 동작 흐름 
// 1. 컴포넌트 첫 랜더링 ➡ setInterval로 타이머 시작
// 2. 컴포넌트 언마운트 ➡ cleanInterval로 타이머 제거 
```

#### 클린업이 필요한 상황
- setInterval / setTimeout 제거
- 이벤트 리스너 제거 (window.addEventListener ➡ removeEventListener)
- API 구독이나 WebSocket 연결 해제 
- 외부 리소스 정리

---

### 2-4. 비동기 작업 (fetch)
- `useEffect`는 **렌더링 이후 실행되므로**, API 호출이나 비동기 데이터 요청을 **이 안에서 수행한다.**  
- `async` 함수는 **직접 useEffect에 붙이지 않고 내부에서 선언 후 호출한다.**  
- 렌더링 직후 실행되는 특성상, **DOM이 완성된 뒤 데이터를 다루기에 적합하다.**

```jsx
import { useState, useEffect } from "react";

function PostList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // 비동기 함수는 내부에서 따로 정의해야 함
    async function fetchData() {
      const res = await fetch("url");
      const data = await res.json();
      setPosts(data.slice(0, 5)); // 5개만 표시
    }

    fetchData();
  }, []); // 처음 마운트될 때만 실행

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### 2-5. 주의할 점
- `useEffect` 내부에서 상태를 바꾸면 **무한 렌더링이 발생할 수 있으므로** 의존성 배열을 반드시 확인한다.  
- 비동기 함수(`async`)는 **useEffect에 직접 사용하지 말고 내부에서 정의한다.**  
- **클린업 함수**를 통해 타이머나 이벤트 리스너를 해제해 **메모리 누수를 방지한다.**


<img src="https://i.pinimg.com/1200x/81/f0/ae/81f0aeac69ffe2f7f493d8c48eb6c073.jpg" alt="semojjal image" width="500" />


## **3. EventHook**
### 3-1. 특징
- 리액트에서 이벤트를 다루기 위한 Hook 함수
- 사용자의 클릭, 입력, 포커스, 스크롤 등 **행동**에 반응하도록 도와줌

### 3-2. 종류

| Hook              | 설명                              |
| ----------------- | ------------------------------- |
| `useEvent`        | React 19 신규 훅, 이벤트 핸들러 안정적 등록   |
| `useCallback`     | 핸들러 함수 메모이제이션으로 재렌더 최소화         |
| `useRef`          | DOM 접근·포커스 제어 등 참조용             |
| `useEffect` + 이벤트 | 외부(window·document) 이벤트 등록 시 사용 |

```jsx
import { useState, useEvent, useCallback, useRef, useEffect} from "react";

function EventExample() {
  const [count, setCount] = useState(0); // 상태 관리
  const inputRef = useRef(null); // DOM 직접 접근
  const [key, setKey] = useState("");

  // useCallback : 재렌더링 시에도 동일한 핸들러 유지
  const handleClick = useCallback(() => {
    setCount((prev) => prev + 1);
    console.log("버튼 클릭!");
  }, []);

  // useEvent 
  const handleKeyDown = useEvent((e) => {
    setKey(e.key);
    console.log("눌린 키:", e.key);
  });

  // useEffect : 마운트 시 이벤트 등록, 언마운트 시 클린업
  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    console.log("키보드 이벤트 등록");

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      console.log("키보드 이벤트 제거");
    };
  }, [handleKeyDown]);

  // 버튼 클릭 시 input 포커스 이동
  const focusInput = useCallback(() => {
    inputRef.current.focus();
    console.log("입력창 포커스!");
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>이벤트 Hook 예시</h2>

      <input
        ref={inputRef}
        placeholder="여기에 포커스 됨"
        style={{ padding: "8px", marginBottom: "10px" }}
      />
      <br />

      <button onClick={handleClick}>클릭 횟수: {count}</button>
      <button onClick={focusInput} style={{ marginLeft: "10px" }}>
        입력창 포커스
      </button>

      <p>눌린 키: {key || "아직 없음"}</p>
    </div>
  );
}

export default EventExample;

```

## **4. 핵심요약**

| Hook            | 역할     | 위치              | 설명                   |
| --------------- | ------ | --------------- | -------------------- |
| **useState**    | 상태 관리  | `count`, `key`  | 값 저장·변경 시 UI 자동 업데이트 |
| **useRef**      | DOM 참조 | `inputRef`      | 요소 직접 접근·포커스 제어      |
| **useCallback** | 함수 최적화 | `handleClick`   | 함수 재생성 방지·성능 개선      |
| **useEvent**    | 이벤트 관리 | `handleKeyDown` | 최신 상태로 이벤트 안정 처리     |
| **useEffect**   | 부수효과   | `window` 등록     | 타이머·이벤트 등록·정리 수행     |


<br />

💡 **학습정리**
> `useHook`은 **상태 관리(state)**, **부수 효과(effect)**, **참조(ref)**, **최적화(callback/memo)** 등  
> 리액트 컴포넌트의 생명주기 전반을 제어하는 핵심 도구이다.  
> 리액트의 본질은 **상태 변화에 따라 UI를 자동으로 갱신하는 것**이다.