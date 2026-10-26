---
title: "Webflow Cloud RSS 피드 공부 정리 | CMS 필드 설계가 출력을 정한다"
description: "Webflow Cloud Route Handler로 커스텀 RSS 피드를 구축하는 방법을 공부하며 든 생각들. CMS 구조 설계가 자동화 범위를 결정한다."
date: 2026-10-26 10:00:00 +0900
categories: [Design]
tags: [webflow, rss, cms, route-handler, newsletter]
image:
  path: /assets/img/thumbnail/webflow.png
  alt: "Webflow Cloud RSS 피드 공부 정리 | CMS 필드 설계가 출력을 정한다"
---

Webflow 블로그에서 Webflow Cloud를 이용한 커스텀 RSS 피드 구축 글이 올라왔다. 처음엔 그냥 RSS 튜토리얼이겠거니 했는데, 읽다 보니 CMS 필드 설계 쪽에서 생각해볼 게 있어서 정리해봤다.

Webflow는 비주얼 빌더로 알고 있는데, Webflow Cloud는 그 안에서 서버 사이드 로직을 직접 돌릴 수 있는 환경인 것 같다. 이 글은 Next.js Route Handler를 이용해서 CMS 데이터를 읽고 XML 응답을 반환하는 엔드포인트를 만드는 방식이었다.

## 1️⃣ 이게 뭐냐?

Webflow CMS에는 기본 RSS 피드 기능이 있다. 근데 기본 피드는 발행된 모든 글이 포함되고, 수정 후 재발행하면 뉴스레터 도구가 그 글을 새 글로 인식하기도 한다. 뉴스레터를 자동 발송하는 입장에서는 꽤 거슬리는 문제다.

이 글에서 만드는 건 `app/feed.xml/route.ts` 파일이다. Webflow Data API의 `items/live` 엔드포인트에 `filter`와 `sort` 파라미터를 붙여서 최신 글 20개를 가져오고, XML 문자열을 직접 조립해서 반환한다. RSS 전용 라이브러리는 쓰지 않는다.

👉🏻 핵심은 CMS 필드 설계에 있었다. `send-to-newsletter`라는 불리언 필드로 에디터가 선택한 글만 피드에 넣고, 고정 발행일 필드를 따로 두어서 글을 수정해도 뉴스레터 도구가 같은 글을 다시 발송하지 않도록 한다. 어떤 필드를 처음에 만들어두느냐가 이후 자동화 전체를 결정하는 구조였다.

> 💡 **여기서 드는 질문?**
> 이런 CMS 필드 설계를 "콘텐츠 구조 설계"라고 부를 수 있는 건지, 아니면 그냥 "기능 설계"인지 공부하면서 계속 헷갈렸다. 경계가 어디쯤인지는 아직 잘 모르겠다.

## 2️⃣ 내가 든 생각

제일 낯선 대목은 RSS 라이브러리를 안 쓴다는 부분이었다. XML 문자열을 직접 조립하고, 특수문자 이스케이프도 수동으로 처리한다. 처음엔 투박해 보였는데, Workers 환경에서 `node:fs` 같은 모듈이 제대로 안 된다는 제약을 생각하면 오히려 그쪽이 안전한 선택이라는 게 이해가 됐다.

GUID 처리 방식도 인상적이었다. 여기서는 글의 URL을 GUID로 쓴다. 덕분에 수정된 글이라도 URL이 안 바뀌면 뉴스레터 도구가 새 글로 인식하지 않는다. 반대로 슬러그를 바꾸면 URL이 달라지니까 다시 발송될 수 있다. 이런 제약이 "슬러그는 처음에 잘 정해야 한다"는 CMS 관리 규칙으로 이어진다는 점이 흥미로웠다.

배포 과정의 트러블슈팅도 공부가 됐다. 공식 문서에 있는 `runtime = 'edge'` 지시문을 그대로 쓰면 OpenNext 어댑터와 충돌해서 배포 자체가 실패한다고 한다. 또 마운트 경로를 `/feeds`로 설정하지 않으면 `/feed.xml` 요청이 404로 떨어진다. 문서를 따랐는데 안 되는 경우가 실제로 있다는 걸, 이런 사례를 통해 조금씩 이해하게 되는 것 같다.

## ⭐️ 마지막으로, 공부하면서 정리해보니

정리해보니 이 글은 Route Handler 구현보다 CMS 구조 설계에 가까운 이야기였다. 어떤 필드를 미리 만들어두느냐가 이후에 가능한 자동화 범위를 결정하고, 잘못 설계한 슬러그 하나가 중복 발송으로 이어질 수 있다. 디자이너가 CMS 구조를 잡을 때 이런 제약까지 같이 생각해야 한다는 건, 공부하기 전에는 연결이 잘 안 됐던 부분이다.

---

> 참고 원문: [How to send Webflow blog posts to your newsletter with an RSS feed on Webflow Cloud](https://webflowmarketingmain.com/blog/webflow-blog-rss-newsletter-feed)
