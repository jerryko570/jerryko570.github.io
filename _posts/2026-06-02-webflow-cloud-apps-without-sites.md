---
title: "Webflow Cloud 공부 정리 | 사이트 없어도 앱이 된다고?"
description: "Webflow Cloud 앱이 사이트 없이도 독립 도메인에서 돌아간다. 발표 읽고 DevLink 포함해서 정리해봤다."
date: 2026-06-02 09:00:00 +0900
categories: [Design]
tags: [webflow, cloud, devlink, deployment]
image:
  path: /assets/img/thumbnail/webflow-cloud-apps-without-sites.png
  alt: "Webflow Cloud 공부 정리 | 사이트 없어도 앱이 된다고?"
---

Webflow 블로그에서 Cloud 관련 발표가 하나 있었다. 제목이 "One workspace for your site and your app. Or just the app."이었는데, 마지막 구절이 눈에 걸렸다. "Or just the app." — 앱만 올릴 수도 있다는 게 무슨 말일까 싶어서 문서를 찾아봤다.

Webflow Cloud는 원래 Webflow로 만든 사이트에 서버 사이드 로직을 얹는 방식이었다. 마케팅 페이지는 Webflow로, 거기서 필요한 백엔드 로직은 Cloud App으로 처리하는 구조. 근데 이번 발표 핵심은 그 전제가 달라졌다는 거다. 이제는 Webflow 사이트 없이, 앱만 독립 도메인에 올릴 수 있다.

처음엔 "그냥 배포 플랫폼 하나 더 추가된 거 아닌가" 싶었다. 근데 DevLink라는 기능을 보고 생각이 조금 달라졌다.

## 1️⃣ 이게 뭐냐?

Webflow Cloud는 Next.js나 Astro로 만든 앱을 배포하는 플랫폼이다. GitHub 연결 후 `git push`하면 자동 배포되고, CLI에서는 `webflow cloud init`과 `webflow cloud deploy`로 시작한다. 환경 변수 설정이나 런타임 로그도 같은 워크스페이스에서 관리된다.

스토리지도 세 종류가 기본으로 붙는다. 세션이나 설정용 키-값 저장소, 파일 업로드용 객체 저장소, 관계형 데이터용 SQLite. 보통 이런 걸 따로 붙이면 설정이 꽤 번거로운데, 한 워크스페이스 안에서 된다는 점은 확실히 편해 보였다.

DevLink는 Webflow에서 디자인한 컴포넌트를 React 컴포넌트로 뽑아내는 기능이다. 헤더, 푸터 같은 걸 Webflow에서 만들고, 그걸 Next.js나 Astro 앱에서 가져다 쓸 수 있다. 디자인 시스템을 양쪽에 따로 유지하지 않아도 된다는 콘셉트인 것 같다.

## 2️⃣ 내가 든 생각

DevLink가 흥미로웠던 이유는, 디자이너-개발자 갭을 도구 수준에서 메우려는 시도처럼 보여서다. Webflow에서 디자인이 바뀌면 코드에도 반영된다는 구조라면, 그냥 컴포넌트 공유가 아니라 디자인 소스를 실제 코드로 연결한다는 뜻인데 — 내가 이해한 게 맞다면 꽤 이상적인 방향이다.

👉🏻 근데 이 부분에서 궁금한 게 생겼다. Webflow에서 만든 컴포넌트가 React 컴포넌트로 나오면, 그 컴포넌트의 "책임"이 어디에 있는 걸까. 디자이너가 Webflow에서 수정하면 개발자 코드에 영향이 가고, 반대로 개발자 쪽에서 뭔가 바꾸면 디자인과 어긋날 수도 있는 구조 아닌가. 공식 문서를 더 읽어봐야 알겠지만, 지금 단계에서는 이 경계 관리가 어떻게 되는지가 제일 궁금했다.

> 💡 **여기서 드는 질문?**
> DevLink로 내보낸 컴포넌트가 Webflow 디자인과 동기화되는 방식이 구체적으로 어떻게 되는 걸까. 버전 관리는 어떻게 하나?

사이트 없이 앱만 올릴 수 있게 됐다는 건, Webflow가 "비주얼 웹빌더"에서 좀 더 넓은 배포 플랫폼 쪽으로 이동하고 있다는 인상이다. Vercel이나 Netlify가 하던 영역이랑 겹치는 부분이 생기는 건데, 거기서 Webflow가 내세우는 게 결국 DevLink, 즉 디자인 도구와의 연결이라는 게 흥미로웠다.

## ⭐️ 마지막으로, 이번에 정리하면서

공부 끝에 남은 건 이 한 줄이다 — Webflow Cloud는 배포 기능을 추가한 게 아니라, "디자인과 코드가 같은 워크스페이스에 있다"는 걸 차별점으로 잡은 것 같다. 그게 실제로 얼마나 강점이 될지는 문서만 본 입장에서는 판단이 안 되지만, 방향 자체는 흥미로웠다.

---

> 참고 원문: [Webflow Cloud. One workspace for your site and your app. Or just the app.](https://webflowmarketingmain.com/blog/cloud-apps-without-sites)
