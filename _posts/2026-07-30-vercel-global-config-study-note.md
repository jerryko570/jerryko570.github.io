---
title: "Vercel Global Config 공부 정리 | Edge Config가 왜 이름을 바꿨을까"
description: "Vercel이 Edge Config를 Global Config로 바꿨다. 이름 변경과 함께 용량 제한도 크게 달라졌다."
date: 2026-07-30 10:00:00 +0900
categories: [Frontend]
tags: [vercel, feature-flags, global-config]
image:
  path: /assets/img/thumbnail/vercel-global-config-study-note.png
  alt: "Vercel Global Config 공부 정리 | Edge Config가 왜 이름을 바꿨을까"
---

Vercel 체인지로그를 보다가 `@vercel/edge-config`가 `@vercel/global-config`로 바뀌었다는 공지가 눈에 띄었다. 처음엔 단순한 이름 바꾸기겠거니 싶었는데, 저장 용량 제한이 꽤 크게 달라진 걸 보고 좀 더 읽어보게 됐다.

공부하면서 파악한 건, 이름 변경에 이유가 있다는 거였다. Edge Config라는 이름이 Vercel 엣지 런타임이나 엣지 함수 같은 다른 개념과 섞여서 헷갈렸던 것 같다. 실제로는 모든 리전에서 ~1ms 읽기가 가능한 전역 복제 데이터 스토어인데, "엣지"라는 이름이 그걸 잘 못 표현했던 거다. Global Config가 더 직관적인 이름에 가깝다는 생각이 들었다.

## 1️⃣ 이게 뭐냐?

Global Config는 앱이 런타임에 읽는 설정값을 저장하는 곳이다. 피처 플래그, 리다이렉트 규칙, A/B 테스트 설정 같은 것들. 코드 배포 없이 값을 바꿀 수 있다는 게 핵심이다.

이번 발표에서 달라진 건 세 가지다. 이름(Edge Config → Global Config), 패키지(`@vercel/edge-config` → `@vercel/global-config`), 환경변수(`EDGE_CONFIG` → `GLOBAL_CONFIG`). 그리고 저장 용량이 크게 늘었다. Hobby 기준으로 8KB에서 1MB로 뛰었고, Pro 기준으로는 64KB에서 1MB다. Pro와 Enterprise는 저장소 개수 제한도 없어졌다.

```js
// 패키지 교체 후
import { get } from '@vercel/global-config';
```

마이그레이션은 급하지 않다. 기존 SDK와 `EDGE_CONFIG` 환경변수는 계속 작동하고, 새 SDK는 `GLOBAL_CONFIG`를 기본으로 읽다가 `EDGE_CONFIG`로 폴백한다. 다만 새 저장소를 프로젝트에 연결할 때는 SDK를 먼저 업그레이드해야 한다. 그 전에 연결하면 레거시 SDK가 새 저장소를 못 읽는다.

## 2️⃣ 내가 든 생각

이름 변경이 생각보다 자연스럽게 느껴졌다. 엣지 런타임, 엣지 함수, 엣지 미들웨어처럼 "엣지"라는 단어를 이미 여러 곳에서 써온 탓에 Edge Config가 어디에 속하는 개념인지 처음엔 모호했던 것 같다. Global Config로 바뀌니까 위치보다 역할이 먼저 보이는 느낌이었다.

👉🏻 흥미로웠던 건 용량 제한이 올라간 방식이었다. Hobby가 8KB에서 1MB로 뛰었는데, 이게 단순히 "더 많이 저장해라"가 아니라 "설정값으로 더 많은 걸 담을 수 있도록" 허용한다는 의미처럼 읽혔다. 피처 플래그가 많아질수록, 실험이 늘어날수록 용량 걱정을 덜 해도 되는 구조가 된 거다.

> 💡 **여기서 드는 질문?**
> 설정값을 코드 밖에 두는 게 언제 유리할까? 배포 없이 값을 바꿀 수 있다는 건, 그 값이 자주 바뀌거나 실험적인 경우에 특히 의미 있다는 뜻일 것 같다.

디자이너 관점에서 보면, 이런 설정 스토어는 UI 변경을 배포 없이 제어할 수 있는 여지를 만든다. 특정 사용자 그룹에게 다른 UI를 보여주거나, 신기능을 점진적으로 켜는 흐름. 공부하면서 이 부분이 특히 와닿았다.

## 3️⃣ 공부한 내용 기준으로는

문서를 읽어보니, Global Config는 데이터베이스가 아니라 "자주 읽히지만 자주 쓰지 않는 설정 전용"이라는 걸 강조하고 있었다. 이 경계를 어떻게 긋느냐가 앞으로 공부할 과제가 될 것 같다는 생각이 들었다.

저장소 개수 제한이 Pro 기준 무제한으로 바뀐 건, 환경별로 설정을 분리하기가 쉬워진다는 의미이기도 한 것 같다. 개발, 스테이징, 프로덕션 각각 다른 설정을 유지하는 게 더 자연스러워지는 구조다.

## ⭐️ 마지막으로, 이름 하나가 설명하는 것

공부 끝에 남은 건 "이름 하나가 생각보다 많은 걸 설명한다"는 한 줄이었다. Edge Config라고 불렸을 때보다 Global Config라고 불릴 때 이게 어디에 쓰이는 도구인지가 훨씬 빨리 이해되는 것 같았다. 기능이 성숙할수록 이름도 따라간다는 게, 이번에 조금 실감됐다.

---

> 참고 원문: [Edge Config is now Global Config](https://vercel.com/changelog/edge-config-is-now-global-config)
