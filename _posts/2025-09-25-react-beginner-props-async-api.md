---
layout: post
title: "[React] 입문을 위한 기초 개념 정리 (3) props비동기 데이터 통신"
date: 2025-09-25 14:11:00 +0900
categories: [frontend, react]
tags: [react, useState, props, async, fetch, api, axios]
image: https://velog.velcdn.com/images/henny/post/d3925f21-b23d-49a5-bbb9-1dc9087fe491/image.png
---

## **1. props (Property)**
- 부모 컴포넌트가 자식 컴포넌트로 데이터를 **전달한다.**  
- props는 함수 매개변수처럼 **읽기 전용으로 사용된다.**

```jsx
function Greeting({ name }) {
  return <p>안녕하세요, {name}님!</p>;
}

function App() {
  return <Greeting name="jerry" />; // Greeting 컴포넌트의 props.name 으로 전달
}
```

| 구분 | 설명 |
| ---- | ---- |
| 전달 방식 | `<Component propName={value} />` 형태로 전달한다. |
| 읽기 전용 | 자식 컴포넌트에서 `props` 값을 수정할 수 없다. |
| 구조 분해 | 함수 매개변수에서 `{ propName }` 형태로 구조 분해하여 받는다. |
| 디폴트값 | `Component.defaultProps = { propName: "기본값" }` 으로 기본값을 설정한다. |


## **2. 비동기 데이터 통신 (Async / Fetch)**
- 즉시 끝나지 않는 작업(API 호출, 파일 읽기 등)을 **비동기적으로 처리한다.**  
- 기다리는 동안 다른 코드가 먼저 실행되며, 결과가 준비되면 **Promise**를 통해 나중에 전달된다.  
- `async / await` 문법을 사용하면 비동기 코드를 **동기 코드처럼 읽기 쉽게 작성할 수 있다.**

```jsx
async function getUser() {
  const res = await fetch("https://jsonplaceholder.typicode.com/users/1");
  const data = await res.json();
  console.log(data);
}

getUser();

```

## 3. fetch 구조
### 3-1. 기본 구조
- `fetch()`는 자바스크립트의 **내장 함수**이다.  
- 서버에 **요청(request)** 을 보내고, **응답(response)** 을 받아오는 **비동기 함수**이다.  
- 결과는 **Promise 객체로 반환**되며, `await`를 통해 결과를 받을 수 있다.  

```jsx
fetch("https://api.example.com/data")
  .then((response) => response.json()) // 응답을 JSON으로 변환한다.
  .then((data) => console.log(data))   // 변환된 데이터를 사용한다.
  .catch((error) => console.error("에러 발생:", error)); // 에러를 처리한다.

```

### **3-2. async / await 형태**
- `then()` 체인보다 코드가 **깔끔하고 순서가 명확하다.**  
- 에러를 처리할 때 **try / catch 구문을 함께 사용한다.**  
- 비동기 코드를 **동기 코드처럼 읽기 쉽게 작성할 수 있다.**

```jsx
async function getData() {
  try {
    const response = await fetch("url");
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("데이터 불러오기 실패:", error);
  }
}

getData();
```

### 3-3. fetch 동작 순서 

| 단계 | 설명                           |
| -- | ---------------------------- |
| ①  | `fetch()`가 서버에 요청을 보냄        |
| ②  | 서버가 요청을 받고, 응답 데이터를 생성       |
| ③  | `response` 객체로 응답이 도착함       |
| ④  | `.json()`으로 응답 본문을 JS 객체로 변환 |
| ⑤  | 변환된 데이터(`data`)를 UI나 콘솔에서 사용 |


### 3-4. 리액트 컴포넌트에서 데이터 불러오기

```jsx
import { useEffect, useState } from "react";

 // 컴포넌트 랜더링
function PostList() { 
  const [posts, setPosts] = useState([]);

  // 마운트 직후 useEffect 실행하여 fetch() 요청함 
  useEffect(() => {
    async function fetchData() { 
      const res = await fetch("url"); // fetch : 서버에 데이터 요청
      const data = await res.json(); // await : 응답 데이터 요청 (JS 객체로 변환)
      setPosts(data.slice(0, 5));  // setPost : 상태 변경으로 리랜더링
    }

    fetchData();
  }, []); 

  return (
    <ul>
      {posts.map((post) => ( // 데이터 목록 <li> 랜더링
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}

export default PostList;
```

### **3-5. UI와 API 파일은 따로 분리하기**
- 예시 코드와 달리, 실제 프로젝트에서는 **UI와 API를 분리하는 것이 좋다.**  
- 이렇게 하면 **비즈니스 로직을 컴포넌트와 분리**하여 유지보수를 쉽게 할 수 있다.  

#### **분리하는 이유**
- 컴포넌트가 너무 많은 일을 하게 되면 코드가 복잡해진다.  
- 여러 컴포넌트에서 같은 API를 사용할 때 **중복이 발생한다.**  
- 나중에 `axios`로 교체하거나 **API 주소가 변경될 경우 수정 범위가 커진다.**

  #### 구조 예시

        src/
      ├─ apis/
      │   └─ postApi.js (fetch 함수 정의)
      ├─ components/
      │   └─ PostList.jsx (화면 렌더링)
      └─ App.jsx

### **3-6. axios 구조**
- **axios**는 `Promise` 기반의 **HTTP 클라이언트 라이브러리**이다.  
- 주로 **API 호출, 에러 처리, 헤더 설정** 등에 사용한다.  
- 리액트에서는 `import { getPosts } from "../apis/postApi";` 형태로 불러와 사용한다.  
- `fetch`와 마찬가지로 **UI와 API 파일을 분리하여 관리한다.**  
  > 이유: 유지보수 용이, 코드 중복 방지, 네트워크 로직 재사용성 향상


#### 기본 사용법과 코드

```terminal
# 설치
npm install axios
```
```jsx
import axios from "axios";

async function getData() {
  try {
    const response = await axios.get("https://jsonplaceholder.typicode.com/posts");
    console.log(response.data); // 응답 본문은 .data 로 접근
  } catch (error) {
    console.error("데이터 요청 실패:", error);
  }
}

getData();
```

#### fetch vs axios

| 항목        | fetch()             | axios                    |
| --------- | ------------------- | ------------------------ |
| 기본 내장 여부  | 브라우저 내장됨           | ❌ 설치 필요 (npm)            |
| 응답 데이터 접근 | `res.json()`        | `res.data`               |
| 에러 처리     | 수동 (`res.ok` 확인 필요) | 자동 throw 처리              |
| 추가 기능     | 제한적                 | 인터셉터, 기본 URL, 헤더 설정 등 풍부 |


## 4. React 데이터 통신 핵심 요약

| 구분            | 사용법             | 특징                     |
| ------------- | --------------- | ---------------------- |
| **props**     | 부모 → 자식 데이터 전달  | 읽기 전용, 구조분해로 사용        |
| **fetch**     | 기본 내장 API       | `.json()` 필요, 단순하고 가벼움 |
| **axios**     | 외부 라이브러리        | `.data`로 접근, 에러 처리 간편  |
| **useEffect** | 마운트 시 실행        | 데이터 요청·렌더링 제어          |
| **API 분리**    | `apis/` 디렉토리 관리 | 재사용·유지보수 용이            |


<br />

💡 **학습정리**

> props는 부모가 자식에게 데이터를 전달하는 읽기 전용 값이고, <br />
> 비동기는 기다리지 않는 흐름으로 Promise, async/await, fetch, axios로 처리하며, <br />
> 리액트에서는 useEffect 안에서 API를 호출하고 상태로 관리하는 것이 핵심