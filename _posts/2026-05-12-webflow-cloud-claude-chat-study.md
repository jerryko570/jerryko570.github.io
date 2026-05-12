---
title: "Webflow Cloud + Claude 채팅 공부 정리 | API 키는 어떻게 숨기는 걸까"
description: "Webflow Cloud의 edge 함수로 Claude API 키를 노출 없이 프록시하는 구조를 공부했다."
date: 2026-05-12 10:00:00 +0900
categories: [Design]
tags: [webflow, claude, edge-runtime, api-security, webflow-cloud]
image:
  path: /assets/img/thumbnail/webflow-cloud-claude-chat-study.png
  alt: "Webflow Cloud + Claude 채팅 공부 정리 | API 키는 어떻게 숨기는 걸까"
---

Webflow 블로그에서 흥미로운 글을 봤다. Webflow 사이트에 Claude AI 채팅을 붙이되, API 키를 브라우저에 노출하지 않는 방법에 관한 내용이었다. Webflow Cloud라는 게 그 핵심이었는데, 이게 어떤 원리로 돌아가는지 잘 몰라서 공부해봤다.

Webflow를 디자인 툴로만 알고 있었기 때문에, Cloud라는 이름이 붙으면서 서버 사이드 로직까지 돌릴 수 있게 됐다는 게 처음 접한 개념이었다.

## 1️⃣ 이게 뭐냐?

보통 Webflow 사이트는 정적 파일(HTML/CSS/JS)로 구성된다. 여기서 AI API를 직접 붙이려면 클라이언트 코드에서 호출해야 하고, 그러면 브라우저 개발자 도구에서 API 키가 그대로 노출된다. 이걸 피하려면 지금까지는 별도 백엔드 서버를 따로 세우거나 서드파티 서비스를 끼워야 했다.

Webflow Cloud는 이 갭을 다르게 해결하는 방식인 것 같다. Next.js나 Astro 앱을 Webflow 인프라 위에서 직접 실행할 수 있고, 그 앱이 같은 도메인의 하위 경로(예: `/chat`)로 서빙된다. API 라우트가 서버 사이드에서 작동하니까, API 키는 환경변수로 서버에만 있고 클라이언트 코드에는 아예 노출되지 않는다.

핵심은 이 한 줄이다:

```typescript
export const runtime = 'edge';
```

이걸 API 라우트 파일에 넣으면 Cloudflare Workers 환경에서 실행된다. 대신 Node.js 내장 모듈(`fs`, `path` 등)은 쓸 수 없고, 웹 표준 API만 사용 가능하다는 제약이 따라온다.

## 2️⃣ 내가 든 생각

공부하면서 흥미로웠던 건 멀티턴 대화 구현 방식이었다. Claude API는 대화 상태를 서버에서 직접 관리해주지 않는다. 매 요청마다 이전 대화 전체를 배열로 전달해야 한다.

```
[
  { role: 'user', content: '질문' },
  { role: 'assistant', content: '답변' },
  { role: 'user', content: '다음 질문' }
]
```

이 구조 자체는 이해가 됐는데, 이게 React `useState`와 맞물릴 때 타이밍 이슈가 생긴다는 게 좀 신기했다. `setMessages(updated)`를 호출한 직후에 바로 `messages`를 읽으면 이전 값이 남아 있다. 상태 업데이트가 비동기이기 때문인데, 그래서 `updatedMessages`라는 로컬 변수를 따로 관리해서 API 호출에 넘겨야 한다는 패턴이 나왔다.

👉🏻 이 타이밍 이슈가 꽤 실질적인 함정인 것 같았다. 눈으로 보기엔 대화가 잘 되는 것 같다가, 특정 시점에 대화 흐름이 끊기는 버그로 조용히 이어질 수 있는 종류인 것 같아서.

또 한 가지, 대화가 길어질수록 매 요청에 보내는 히스토리가 쌓인다는 점도 눈에 들어왔다. 토큰 기반으로 비용이 나가는 구조라, 긴 대화에선 최근 N개만 슬라이싱해서 보내는 방식(슬라이딩 윈도우)이 필요하다는 내용도 있었다. 비용 제어 로직이 클라이언트 쪽에 있다는 게 디자인 차원에서도 신경 써야 하는 지점인 것 같다.

> 💡 **여기서 드는 질문?**
> edge runtime에서 Node.js 모듈을 못 쓴다는 제약이, 실제 개발에서 어떤 우회 패턴을 만들어내는지 궁금해졌다. 지금 본 Claude 프록시처럼 단순한 경우엔 큰 문제가 없어 보이는데, 로직이 복잡해지면 어느 지점에서 막히는지가 이 방식의 실제 한계일 것 같다.

## 3️⃣ 앞으로 어떻게 쓸까?

문서만 본 입장에서는, 이 방식이 자연스럽게 연결될 상황이 떠오르긴 한다. Webflow로 디자인된 사이트에 간단한 AI 기능이 필요할 때, 별도 서버를 따로 만들지 않아도 된다는 옵션. 아직 직접 닿아본 적은 없지만, 이런 구조가 있다는 걸 알고 있으면 나중에 협업할 때 "어떻게 연결하는지" 대화를 조금 다르게 할 수 있을 것 같다.

## ⭐️ 마지막으로, 디자이너 입장에서 공부하며 든 생각

공부 끝에 남은 건 "Webflow가 디자인 도구에서 인프라 쪽으로 영역을 넓히고 있다"는 인상이다. API 키 보안을 해결하는 방법을 공부하러 들어갔다가, 정작 흥미로웠던 건 Webflow가 어디까지 영역을 가져가는지에 대한 부분이었다.

---

> 참고 원문: [How do you add a Claude-powered chat to a Webflow site without exposing your API key?](https://webflowmarketingmain.com/blog/claude-chat-webflow)
