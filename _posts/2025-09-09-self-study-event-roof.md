---
layout: post
title: "[셀프스터디] 이벤트 루프 딥다이브"
date: 2025-09-09 00:00:00 +0900
categories: [frontend, javaScript]
tags: [javascript, event-loop, async, microtask, callback]
series: "셀프스터디"
image: /assets/img/thumbnail/self-study.png
---

## **1. 이벤트 루프란?**
- 자바스크립트는 단일 스레드 언어이지만, 이벤트 루프(Event Loop) 를 통해 비동기 작업을 효율적으로 처리한다. 이벤트 루프는 **콜 스택(Call Stack)** 과 **태스크 큐(Task Queue)** 를 감시하며, 실행 가능한 작업을 순서대로 처리하는 역할을 한다.

---

## **2. 이벤트 루프 실행순서**
1. 자바스크립트는 단일 스레드이다. 한 번에 하나의 작업만 **`Call Stack`**에서 실행 가능!
2. **`Stack`**이 비면 **`Event Loop`**가 동작한다.
3. **`Event Loop`**는 먼저 **`Microtask Queue`**를 확인해서 안의 작업을 모두 실행한다.
4. 그다음에 **`Macrotask Queue`**에서 하나의 작업을 꺼내 실행한다.
5. 챗바퀴 돌듯 또 다시 **`Microtask` ➡ `Macrotask`** 순으로 반복한다.

![이벤트 루프 동작 흐름](/assets/img/self-study/event-roof.gif)

## **3. 태스크큐? 마이크로큐? 매크로큐?**
### 3-1. 태스크 큐 (Task Queue)
- **비동기 작업들이 대기하는 줄**로, 스택이 비면 **이벤트 루프가 하나씩 꺼내 실행**한다.
내부에는 **급한 일(Microtask)** 과 **일반 일(Macrotask)** 이 구분되어 있다.
> 이벤트 루프가 콜 스택이 비면 이 큐에서 하나씩 꺼내 실행
- **예시:**  `태스크큐 = 마이크로태스크 + 매크로태스크`

---

### 3-2. 마이크로큐 (Micro Queue)
- `Promise`처럼 **즉시 처리 가능한 빠른 비동기 작업**을 예약하는 대기열이다.
- 매크로태스크가 끝날 때마다 그 사이 생긴 모든 마이크로태스크를 전부 처리 후 랜더링한다.
- **예시:**  `Promise.then(), queueMicrotask()`

---

### 3-3. 매크로태스크 큐 (Macrotask Queue)
- **조금 느긋한 비동기 작업**들이 대기하는 큐다.
- **마이크로태스크 실행 이후 처리**되며, 일반적인 비동기 함수들이 여기에 들어간다.
- **예시**: `setTimeout(), setInterval(), fetch(), DOM 이벤트 (click, scroll 등)`

---

### 3-4. 마이크로큐 vs 매크로태스크 큐

| 구분           | 실행 시점         | 예시                                     | 특징                |
| ------------ | ------------- | -------------------------------------- | ----------------- |
|  **Microtask** | 매크로 뒤 즉시 실행   | `Promise.then()`<br>`queueMicrotask()` | **급함**, 렌더링 전 처리  |
| **Macrotask** | 이벤트 루프 1회당 1개 | `setTimeout()`<br>`fetch()`            | **느긋함**, 렌더링 후 처리 |


---

<br />
![태스크 큐 흐름](/assets/img/self-study/event-roof-2.png)

### 3-5. 태스크 큐 작업 순서 중 필수로 알아야 할 개념
- 브라우저는 매크로태스크 하나 실행하고 쌓인 마이크로태스크를 모두 처리하고 그제야 화면을 다시 그린다.
- 마이크로태스크가 너무 많으면 **렌더링이 지연되거나 멈춘 것처럼 보이는 현상**이 발생한다.

```js
setTimeout(() => console.log("매크로태스크 끝!"), 0);

Promise.resolve()
  .then(() => console.log("마이크로태스크 1"))
  .then(() => console.log("마이크로태스크 2"))
  .then(() => console.log("마이크로태스크 3"));

// 실행순서 ➡ 마이크로태스크 1 ➡ 2 ➡ 3 ➡ 매크로태스크 끝! ➡ 랜더링!
```

<br />

💡 **학습정리**

| 순서 | 설명 |
|------|------|
| ① | 매크로태스크 하나 실행 (`setTimeout`, `click event` 등) |
| ② | 그 사이 쌓인 마이크로태스크 전부 처리 (`Promise.then`) |
| ③ | 렌더링 수행 (화면 업데이트) |
| ④ | 다음 매크로태스크 실행 |

> 즉, “매크로 ➡  마이크로 전부 처리 ➡  렌더링”  
> 그래서 콘솔에선 **마이크로 ➡  매크로 순서**로 찍힌다!


<br />
<br />
<br />

# 경이롭구만...

![경이로운 세계구나](/assets/img/funny/pepe.gif)