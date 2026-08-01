---
title: "Figma Make에 Properties Panel 추가 — 공부하면서 든 생각"
description: "Figma Make에 시각적 속성 편집과 캔버스 주석 기능이 생겼다. 무엇이 달라지는 건지 정리해봤다."
date: 2026-08-01 10:00:00 +0900
categories: [Design]
tags: [figma, figma-make, properties-panel, annotations, design-tools]
image:
  path: /assets/img/thumbnail/figma-make-properties-panel-study.png
  alt: "Figma Make에 Properties Panel 추가 — 공부하면서 든 생각"
---

Figma 공식 블로그에 Figma Make 관련 발표가 올라왔다. Properties Panel과 Annotations라는 두 기능이 새로 추가됐다는 내용이었다.

Make는 AI 프롬프트로 UI를 생성하거나 수정하는 도구인데, 지금까지는 텍스트로만 변경을 요청할 수 있었다. 이번 업데이트로 시각적인 조작 방법이 생겼다는 게 핵심이었고, 그 부분이 흥미로워서 원문을 좀 더 읽어봤다.

## 1️⃣ 이게 뭐냐?

Properties Panel은 Make 에디터 안에 생긴 속성 편집 패널이다. spacing, typography, layout, opacity, z-index, border 같은 값들을 직접 클릭해서 조정할 수 있고, DOM 트리도 시각화돼 있어서 여러 요소를 한 번에 선택하는 것도 가능하다고 한다. 기존 코드베이스의 색상이나 타이포그래피 토큰도 인식한다는 내용도 있었다.

이전까지는 "헤더 폰트를 16px로 바꿔줘" 같은 식으로 전부 텍스트로 요청해야 했는데, 이제는 요소를 직접 선택해서 바꿀 수 있다. AI가 "어떤 요소를 말하는 건지" 추측하는 과정이 줄어드는 구조다.

Annotations는 캔버스 위에 번호가 붙은 주석을 달아두는 기능이다. 특정 영역을 지정하고 "이 버튼 hover 시 줌 인", "클릭하면 300ms fade-in" 같은 설명을 적으면, AI 에이전트가 그 내용을 읽고 코드에 반영한다고 한다. 원문의 예시는 hover 효과, press 애니메이션, 전체 화면 오버레이 같은 인터랙션 케이스들이었다.

변경사항은 즉시 적용되는 게 아니라 프롬프트 박스에 먼저 표시된 뒤 검토 후 적용하는 방식이라고 한다.

## 2️⃣ 내가 든 생각

처음에는 기존 Figma Design 패널과 뭐가 다른 건지 잘 안 와닿았다. 조금 생각해보니 레이어가 다른 것 같았다. Figma Design에서 속성 편집은 디자인 파일을 수정하는 거고, Make의 Properties Panel은 생성된 코드를 시각적 조작으로 수정하는 거다. 같은 "속성 편집"처럼 보이는데 대상이 다르다.

👉🏻 특히 흥미로웠던 건 Properties Panel이 토큰 사용량을 줄인다는 부분이었다. AI에게 텍스트로 설명하는 대신 직접 선택하고 바꾸면, AI가 "어떤 요소인지 찾고 해석하는" 과정 자체가 빠진다. 단순한 편의 기능이라기보다 프롬프트 흐름 자체를 줄이는 구조라는 인상이었다.

Annotations는 익숙한 방식이라 오히려 더 와닿았다. 디자인 협업에서 레드라인이나 코멘트를 특정 요소에 붙이는 것과 비슷한 발상이었다. 그걸 AI 도구 맥락으로 가져왔다는 게 흥미로웠다. 사람 간 협업에서 쓰던 방식이 AI와의 작업에서도 통할 수 있다는 거니까.

> 💡 **여기서 드는 질문?**
> 두 기능이 합쳐지면, AI에게 텍스트로 설명하는 시간보다 직접 선택하고 주석 다는 시간이 더 많아지는 건 아닐까? 그게 효율적인 방향인지는 문서만 본 입장에서는 판단하기 어렵다.

## ⭐️ 마지막으로, 디자인 도구 공부하면서 느낀 점

공부 끝에 남은 건 이런 인상이었다 — Make가 점점 "AI에게 설명하는 도구"에서 "AI와 함께 조작하는 도구"로 가고 있다는 것. 디자이너로서 봤을 때 익숙한 인터페이스 패턴이 생긴 셈이라, 그 방향이 나쁘지 않게 느껴졌다.

---

> 참고 원문: [A properties panel and annotations, now in Figma Make](https://www.figma.com/blog/properties-panel-and-annotations-now-in-figma-make/)
