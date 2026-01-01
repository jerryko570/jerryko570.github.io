---
layout: post
title: "React 기초 개념 정리 (2) | useState·useEffect 흐름"
description: "상태 변화와 사이드 이펙트가 렌더링에 어떤 영향을 주는지 흐름으로 이해해봅니다."
date: 2025-09-24 22:32:00 +0900
categories: [frontend, react]
tags:
  - react
  - hooks
  - useState
  - useEffect
  - state
  - side-effect
  - rendering
series: react
image: /assets/img/thumbnail/react.png
---

## **1. useState**
### 1-1. 특징
- `useState`는 **컴포넌트 안에서 변하는 값을 저장**하고,  
  값이 바뀌면 **UI가 다시 렌더링되게 만드는 상태 저장용 Hook**이다.  
- 컴포넌트가 **기억해야 하는 데이터를 리액트가 관리하도록 한다.**

{% raw %}
```jsx
import { useState } from "react";

function Counter() {

  const [count, setCount] = useState(0); 
  const handleClick = () => {
    setCount(count + 1); 
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
{% endraw %}

---

### 1-2. 비동기 업데이트
- `setCount()`는 **즉시 실행되지 않고**, 리액트가 **다음 렌더링 사이클에서 한 번에 처리(batch)** 한다.  
- 따라서 `console.log()`로 바로 출력하면 **이전 값이 표시될 수 있다.**

{% raw %}
```jsx
const [count, setCount] = useState(0);

const handleClick = () => {
  setCount(count + 1);
  console.log(count); // ❌ 여전히 이전 값
};

// 해결 방법
setCount((prev) => prev + 1);
```
{% endraw %}

---

### 1-3. 여러 상태를 객체로 묶기

{% raw %}
```jsx
const [user, setUser] = useState({ name: "jerry", age: 3 });

user.age = 4; // ❌ 직접 변경하면 리렌더링되지 않음

setUser({ ...user, age: 4 }); // 불변성 유지
```
{% endraw %}

---

## **2. useEffect**

{% raw %}
```jsx
import { useState, useEffect } from "react";

function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log("렌더링 또는 count 변경됨!");
  }, [count]);

  return (
    <div>
      <p>카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}

export default Timer;
```
{% endraw %}

---

### 2-3. 클린업

{% raw %}
```jsx
useEffect(() => {
  const timer = setInterval(() => {
    console.log("1초 지남");
  }, 1000);

  return () => {
    clearInterval(timer);
  };
}, []);
```
{% endraw %}

---

### 2-4. 비동기 작업

{% raw %}
```jsx
import { useState, useEffect } from "react";

function PostList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const res = await fetch("url");
      const data = await res.json();
      setPosts(data.slice(0, 5));
    }

    fetchData();
  }, []);

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```
{% endraw %}

## **3. EventHook**

{% raw %}
```jsx
import { useState, useEvent, useCallback, useRef, useEffect} from "react";

function EventExample() {
  const [count, setCount] = useState(0);
  const inputRef = useRef(null);
  const [key, setKey] = useState("");

  const handleClick = useCallback(() => {
    setCount((prev) => prev + 1);
  }, []);

  const handleKeyDown = useEvent((e) => {
    setKey(e.key);
  });

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  const focusInput = useCallback(() => {
    inputRef.current.focus();
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
{% endraw %}

---

## **4. 핵심요약**

| Hook            | 역할     | 설명 |
| --------------- | ------ | ----- |
| **useState**    | 상태 관리 | 값 변경 시 UI 업데이트 |
| **useRef**      | DOM 참조 | 포커스·직접 접근 |
| **useCallback** | 함수 최적화 | 불필요한 재생성 방지 |
| **useEvent**    | 이벤트 관리 | 최신 상태 이벤트 처리 |
| **useEffect**   | 부수효과 | 이벤트 등록·정리, fetch 등 |

<br />

💡 **학습정리**  
리액트 Hook은 **상태 → UI 자동 갱신**을 기반으로 동작한다.
