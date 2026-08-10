---
title: "Webflow Gemini 콘텐츠 어시스턴트 공부 정리"
description: "Webflow Cloud에서 Gemini API로 CMS 필드 포맷에 맞는 JSON을 바로 받는 구조를 공부하며 든 생각 정리."
date: 2026-08-10 09:00:00 +0900
categories: [Design]
tags: [webflow, gemini, cms, ai]
image:
  path: /assets/img/thumbnail/webflow-gemini-content-assistant-study-note.png
  alt: "Webflow Gemini 콘텐츠 어시스턴트 공부 정리"
---

Webflow 블로그에서 Gemini를 CMS에 붙이는 글이 올라왔다. Webflow Cloud가 나온 뒤로 이런 류의 튜토리얼이 부쩍 늘었는데, 이번 글은 제목의 "belongs inside your CMS"라는 표현이 눈에 걸렸다. 그냥 AI 초안 툴이 아니라 CMS 안에 있어야 한다는 게 어떤 의미인지가 궁금해서 읽어봤다.

AI가 글 초안을 잡아주는 기능은 이미 여러 곳에서 볼 수 있다. 근데 그것들이 불편한 이유는 보통 별도 창에서 쓰고 복사해서 CMS에 붙여넣는 과정이 끼기 때문이다. 포맷이 안 맞으면 정리도 한 번 더 해야 한다. 이 글은 그 과정을 없애는 쪽에서 출발한다는 인상이었다.

## 1️⃣ 이게 뭐냐?

구조는 이렇다. Webflow Cloud에 Next.js Route Handler를 올리고, 거기서 Gemini API를 두 가지 방식으로 호출한다.

첫 번째는 스트리밍 드래프트 모드. `/api/assist/stream` 엔드포인트에서 `ReadableStream`으로 응답을 흘린다. 글자가 타이핑되듯 실시간으로 나오는 방식이다. AI 채팅 UI에서 흔히 보던 것과 비슷하다.

두 번째가 이 글에서 새로운 지점이었다. CMS 모드(`/api/assist/cms`)에서는 Gemini에 `responseMimeType: 'application/json'`을 설정한다. 그러면 일반 텍스트 응답 대신 JSON이 나온다. 그냥 JSON이 아니라 Webflow CMS 필드 구조에 맞춰진 JSON이다.

이게 가능한 건 시스템 프롬프트 덕분이다. Gemini한테 "제목, 본문, 슬러그 이런 필드 구조로 응답해"라고 미리 알려주면, 그에 맞는 포맷으로 응답이 나온다. `@google/genai` SDK를 쓰고, Webflow Data API까지 연동하면 그 JSON을 CMS에 바로 밀어넣는 것도 가능하다.

## 2️⃣ 내가 든 생각

이 구조에서 흥미로웠던 건 AI가 CMS를 '이해했다'는 게 아니라는 점이었다. Gemini가 Webflow를 아는 게 아니라, 개발자가 CMS 필드 구조를 프롬프트로 직접 알려주는 방식이다. AI 입장에서는 그냥 지정된 포맷으로 JSON을 만드는 일에 가깝다.

그러면 자연스럽게 드는 생각은 프롬프트 설계가 얼마나 중요한가였다. CMS 필드가 많고 복잡해지면 시스템 프롬프트도 그만큼 길어질 텐데, 그 유지보수가 어느 역할의 몫인지가 글을 읽어서는 명확하지 않았다. CMS 구조를 가장 잘 아는 건 에디터나 콘텐츠 디자이너 쪽인데, 그걸 프롬프트 언어로 옮기는 건 개발자 작업에 가깝다.

👉🏻 이 간격이 실제로 어떻게 해소되는지가 더 궁금해졌다.

> 💡 **여기서 드는 질문**: CMS 필드 구조가 자주 바뀌는 팀이라면 프롬프트도 계속 업데이트해야 할 텐데, 그 흐름을 누가 챙기는 역할이 될까?

## 3️⃣ 앞으로 어떻게 쓸까?

Webflow Cloud 없이는 이 구조 그대로 쓰기 어렵다. 하지만 핵심 아이디어는 다른 환경에도 가져갈 수 있을 것 같다. "AI 응답을 특정 스키마로 받는다"는 패턴 자체는 어떤 CMS나 관리 툴에서도 비슷하게 응용될 수 있다.

문서 기준으로 보면 `responseMimeType` 설정 하나로 JSON 출력 모드로 전환되는 게 의외로 간단했다. 복잡한 부분은 기술 설정보다 어떤 프롬프트를 쓰느냐인 것 같다는 인상이었다.

## ⭐️ 마지막으로, 디자인 도구 관점에서 공부하며 느낀 점

정리해보니 "AI가 CMS를 이해한다"라기보다 "CMS가 AI한테 자기 구조를 설명해주는 일"에 가까웠다. 그리고 그 설명을 얼마나 잘 쓰느냐가 결과 품질을 가른다는 생각이 들었다. CMS 구조를 명확하게 정의해두는 일이 AI 연동의 시작점에 가까운 것 같다.

---

> 참고 원문: [How to build a Gemini content assistant that belongs inside your Webflow CMS](https://webflowmarketingmain.com/blog/gemini-content-assistant-webflow)
