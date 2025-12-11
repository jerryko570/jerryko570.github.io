---
layout: post
title: "[셀프스터디] 테일윈드 CSS 딥다이브"
date: 2025-10-30
categories: [frontend, tailwind]
tags: [tailwind, css, study, routine]
image: /assets/img/thumbnail/self-study.png
---

## 🧭 왜 Tailwind를 공부하게 되었나
프로젝트에서 빠르게 UI를 구성하고 싶어서 시작했다.

## 📚 공부 순서
1. 공식 문서 훑어보기  
2. 색상 / spacing / flexbox 실험  
3. 스프린트 과제에 적용해보기  

## 💡 느낀 점
Tailwind는 외우기보다 “디자인 감각 + 실습”으로 익히는 게 빠르다.  
처음엔 복잡했지만, 오히려 CSS나 SCSS보다 직관적이어서  
**결국 CSS 이해가 더 깊어지는 효과**가 있었다.  
디자인 가이드를 구조적으로 정리하고 접근하니 개발 속도도 훨씬 빨라졌다.

---

### 🧩 처음에 어려웠던 점
CSS처럼 파일이 분기되지 않고,  
JS 문법 안에서 `className`에 Tailwind를 사용하는 게 처음엔 어색했다.  
깔끔해야 하는데 코드가 ‘더러워지는 느낌’이랄까...

3일 정도 꾸준히 실습해보면서 적응했고,  
왜 업계에서 이걸 강력히 추천하는지 이해하게 되었다.  
**디자이너 없어도 이거 하나면 개발 가능하다는 말, 이제 알겠다.**

---

### 🌟 장점
디자이너로서 **세밀한 디자인 가이드라인을 Tailwind 토큰화**해서  
일관된 디자인 시스템을 구축할 수 있다.

---

### 🌀 헷갈렸던 부분
문법이 SCSS나 CSS와 달라서 처음엔 패턴이 헷갈렸다.  
특히 **요소의 위치 이동(position)** 부분이 어렵게 느껴졌다.

예를 들어 `input` 안에  
왼쪽엔 돋보기, 오른쪽엔 삭제 아이콘을 넣고 싶었는데,  
아이콘과 인풋의 위치를 정확히 맞추는 게 쉽지 않았다.

처음엔 `flex items-center` 조합으로 해결될 줄 알았는데 잘 안 됐다.  
결국 **부모를 `relative`, 아이콘을 `absolute`로 배치**하고,  
`translate`까지 써서 해결했다 😂  
덕분에 `position` 개념을 아주 정확히 이해하게 됐다.

---

### 🚀 성장 포인트
자주 쓰는 패턴들을 반복해서 적용하다 보니  
이제 Tailwind 문법이 자연스럽게 손에 익고 있다.  
앞으로는 반응형 레이아웃과 컴포넌트 단위에서  
**Tailwind Utility Pattern**을 더 정리할 예정이다.

---

### 🧭 위치 관련 Tailwind 패턴 요약

| 패턴     | Tailwind                                                      | 설명        |
| -------- | ------------------------------------------------------------- | --------- |
| 왼쪽 정렬  | `absolute left-0`                                             | 왼쪽에 딱 붙임  |
| 오른쪽 정렬 | `absolute right-0`                                            | 오른쪽에 딱 붙임 |
| 세로 중앙  | `absolute top-1/2 -translate-y-1/2`                           | 수직 중앙     |
| 가로 중앙  | `absolute left-1/2 -translate-x-1/2`                          | 수평 중앙     |
| 정중앙    | `absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2` | 완전 중앙     |


```bash
src/
 └ app/globals.css ← 여기서 tailwind+token 묶어서 관리
 └ styles/theme.css ← 컬러/폰트/토큰
 └ styles/base.css  ← reset/base, body 속성 + 폰트 프리셋
 └ styles/components.css ← 버튼 등 UI 컴포넌트
 └ styles/utilities.css ← 간단한 헬퍼 클래스들


| 요소                             | v4 방식                    |
| ------------------------------ | ------------------------ |
| Tailwind import                | `@import "tailwindcss";` |
| Token 정의                       | CSS 변수(`:root`)로 사용      |
| Theme Override                 | `@theme` 블록 사용           |
| Base, Components, Utilities 확장 | `@layer` 사용              |
| config.js 없음(선택사항)             | → CSS에서 즉시 설정 가능         |

```
## 컴포넌트 제작

## @layer base 와 root의 차이
- :root는 css변수를 정의할 때 사용 (전역에서 사용할 값들을 저장)
- @layer base는 html 요소에 스타일을 적용할 때 사용 (한파일에서 관리하면 :root를 해야함)

## 처음에는 component.css에서 각각의 컴포넌트화를 했는데..
- tailwind스럽게 리팩토링해서 자율적인 구조로 옯기고자 함 @apply 기반으로 압축하고 TS컴포넌트로 역할 분리
- 현재는 스타일 대부분을 CSS에서 직접 정의해서 토큰 유틸리티 확장성이 떨어지고 클래스 수가 늘어날 수록 유지보수가 어려워짐을 느낌
- CSS는 Base Style과 Token만 유지
- 사이즈, variant, state는 props로 리엑트 컴포넌트에서 관리하도록 함
