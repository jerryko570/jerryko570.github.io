---
title: "VoidZero 인수 공부 정리 | Vite와 오픈소스 지속가능성"
description: "Cloudflare가 VoidZero를 인수했다는 소식을 접하고 오픈소스 생태계를 공부한 내용 정리"
date: 2026-07-27 09:00:00 +0900
categories: [DevTools]
tags: [vite, javascript, open-source, cloudflare]
image:
  path: /assets/img/thumbnail/voidzero-cloudflare-acquisition-study.png
  alt: "VoidZero 인수 공부 정리 | Vite와 오픈소스 지속가능성"
---

Stack Overflow Blog 팟캐스트에서 Cloudflare가 VoidZero를 인수했다는 이야기가 나왔다. 제목을 처음 봤을 때는 별 감흥이 없었다.

VoidZero가 뭔지 몰랐기 때문이다. 찾아보니 Evan You가 세운 회사였다. Vue.js와 Vite를 만든 바로 그 사람. 프론트엔드 개발을 공부하다 보면 Vite는 피하기가 어렵다. 그걸 만든 사람의 회사가 Cloudflare에 인수됐다는 소식이었다.

## 1️⃣ 이게 뭐냐?

VoidZero는 Evan You가 2023년에 창업한 회사다. 목표는 차세대 JavaScript 툴링을 만드는 것. Vite뿐만 아니라 Oxc(JavaScript 파서·린터)와 Rolldown(번들러)처럼 기존 도구보다 훨씬 빠른 것들을 Rust로 재작성하고 있었다.

이 회사를 Cloudflare가 인수했다. Cloudflare는 CDN, DNS, Workers(서버리스 실행 환경)를 주력으로 하는 인프라 회사인데, 왜 JavaScript 툴링 회사를 샀는지가 처음엔 이해가 잘 안 됐다.

팟캐스트에서 Evan You와 Cloudflare의 Dane Knecht가 직접 이야기한 내용을 들어보니, 핵심은 **오픈소스 지속가능성** 문제였다. Vite가 수백만 프로젝트에서 쓰이는 도구가 됐지만, 풀타임으로 유지하고 개발할 인력의 생계를 어떻게 해결하느냐가 쉽지 않다는 거다. Cloudflare의 인수는 그 문제에 대한 한 가지 대답인 것 같았다.

Cloudflare 입장에서도 계산이 있다. 개발자들이 쓰는 빌드 도구와 Cloudflare Workers 같은 인프라가 잘 맞물리면 서로 시너지가 생긴다. Cloudflare의 분산 시스템이 Vite의 개발자 경험 개선에 직접 쓰일 수 있다는 이야기도 나왔다.

## 2️⃣ 내가 든 생각

Vite를 처음 배울 때는 "왜 빠르냐"만 생각했지, 이걸 만드는 사람들이 어떻게 운영하는지는 생각해본 적이 없었다. 이번 공부에서 그 부분이 새롭게 보였다.

👉🏻 내가 매일 쓰는 도구 뒤에 회사가 있고, 그 회사도 지속가능하게 운영돼야 한다는 당연한 사실을 막연하게만 알고 있었던 것 같다.

> 💡 **여기서 드는 질문?**  
> 기업이 인수하면 오픈소스 라이선스는 그대로여도, 프로젝트의 방향이 기업의 이해관계에 맞게 조금씩 바뀌지 않을까? 팟캐스트에서는 계속 열린 방향이라고 했는데, 그게 얼마나 유지될지는 지금 단계에서 알기 어렵다.

디자이너로서 봤을 때 흥미로웠던 건 다른 부분이었다. "파트너십으로 오픈소스를 지속가능하게"라는 프레임 자체가, 오픈소스를 유지하는 방식이 지금 진지하게 고민되고 있다는 신호처럼 보였다. 단순 후원이나 기부 모델이 아닌 인수라는 형태를 택했다는 것도 그렇고. 어떤 의미에서 이건 빌드 도구의 이야기가 아니라 오픈소스 비즈니스 모델 이야기에 가까운 것 같다.

## ⭐️ 마지막으로

정리해보니 이번 공부에서 Vite보다 오픈소스 생태계 쪽을 더 많이 생각하게 됐다. 도구를 배우는 입장에서 그 도구가 어떻게 살아남는지까지 신경 쓸 일은 별로 없는데, 이번 인수 소식은 그 부분을 한 번 짚게 만들었다. 이런 류의 소식을 볼 때 자꾸 같은 질문을 하게 되는 것 같다 — 오픈소스가 무료로 계속 있을 수 있는 이유는 뭘까.

---

> 참고 원문: [Partnerships can keep open source sustainable](https://stackoverflow.blog/2026/07/24/partnerships-can-keep-open-source-sustainable/)
