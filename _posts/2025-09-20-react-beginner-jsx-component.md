---
layout: post
title: "[React] 입문을 위한 기초 개념 정리 (1) JSX·Component"
date: 2025-09-20 22:32:00 +0900
categories: [frontend, react]
tags: [react, jsx, component]
series: "react"
image: /assets/img/thumbnail/react.png
---

## **1. React? 리액트!** 
- 페이스북 메타에서 만든 **UI 라이브러리**이다.  
  - 화면을 **컴포넌트 단위로 재사용하며 효율적으로 관리할 수 있다.**  
  - 데이터가 바뀌면 **필요한 부분만 다시 그려주는 Virtual DOM**을 사용한다.

#### **사담. 협업할 때 항상 들었던 말 — "컴포넌트"**
- 디자인 시스템을 만들 때 개발자들이 자주 했던 말이 있다.  
  > "컴포넌트를 고려해주세요."  
  - 직접 컴포넌트를 만들고 다른 화면에서도 재사용해보니,
    컴포넌트는 단순한 UI 단위가 아니라  
    **팀이 협업하고 서비스 경험을 일관되게 확장하는 공통 언어**라는 걸 알게되었다.

---

## **2. JSX (JavaScript XML)**
- 자바스크립트 안에서 **HTML을 작성할 수 있는 문법 확장**이다.  
- `<div>` 또는 `<>...</>` 형태로 작성한다.  
- **모든 태그는 반드시 닫아야 한다.**  
- **표현식(Expressions)** 만 중괄호 `{}`로 감쌀 수 있다.

---

## **3. 컴포넌트 (Component)란?**
### 3-1. 특징
- 컴포넌트는 화면을 구성하는 **작은 블록 단위**이다.  
- JSX를 반환하는 **함수형 또는 클래스형 구조**로 정의한다.  
- 하나의 컴포넌트는 독립적으로 동작하며, 다른 컴포넌트와 조합해 **화면을 구성한다.**


```jsx
function Button() {
  return <button className="btn">클릭!</button>;
}

export default Button;
```

- 다른 컴포넌트 안에서 여러번 재사용성 증가함
- 컴포넌트 조립으로 UI 구조를 체계적으로 구성 가능

```jsx
function Header() {
  return <h1>나의 블로그</h1>;
}

function Footer() {
  return <footer>© 2025 jerry</footer>;
}

function App() {
  return (
    <div>
      <Header />
      <p>본문 내용입니다.</p>
      <Button>
      <Footer />
    </div>
  );
}
```

### 3-2. 파일 구조 예시

```
src/
 ├─ components/
 │   ├─ Header.jsx
 │   ├─ Button.jsx
 │   └─ Counter.jsx
 └─ App.jsx
 ```

### 3-3. 컴포넌트 이름 규칙

| 구분  | 규칙             | 예시                           |
| --- | -------------- | ---------------------------- |
| 파일명 | PascalCase     | `Button.jsx`, `UserCard.jsx` |
| 함수명 | PascalCase     | `function UserCard()`        |
| 태그명 | `<UserCard />` |                              |

### 3-3. 함수형 컴포넌트
- JSX를 반환하는 **자바스크립트 함수형 구조로 구성된다.**  
- 상태 관리가 가능하며, `useState`, `useEffect` 등 **다양한 Hook을 활용할 수 있다.**  
- **재사용성과 구조적 분리**가 용이하여 코드의 **가독성과 유지보수성**이 높아진다.  

---

<br />

💡 **학습정리**
> 리액트는 **“컴포넌트로 생각하고 JSX로 표현하는 UI 라이브러리”**이다.  
> 작은 단위를 조합해 **재사용성과 유지보수성을 높이는 것**이 핵심이다.