---
title: "IntelliJ LSP Client API 오픈소스화 정리 | 플러그인 개발의 구조가 달라지는 지점"
description: "JetBrains가 IntelliJ IDEA 2026.2에서 LSP Client API를 오픈소스로 공개했다. 플러그인 개발 구조에 어떤 변화가 생기는지 공부하면서 정리해봤다."
date: 2026-06-29 09:00:00 +0900
categories: [DevTools]
tags: [lsp, jetbrains, intellij, plugin, ide]
image:
  path: /assets/img/thumbnail/intellij-lsp-client-api-open-source.png
  alt: "IntelliJ LSP Client API 오픈소스화 정리 | 플러그인 개발의 구조가 달라지는 지점"
---

JetBrains 블로그에서 IntelliJ IDEA 2026.2 관련 발표를 읽었다. LSP Client API를 오픈소스화한다는 내용이었다. LSP 자체는 이름 정도는 들어봤는데, 이번에 왜 오픈소스가 되는 건지, 플러그인 작성하는 사람들한테 어떤 의미인지가 궁금해서 문서를 좀 읽어봤다.

처음엔 IDE 플러그인 개발 얘기라 나랑 좀 먼 영역인가 싶었다. 근데 읽다 보니 이게 "언어 지원을 어떻게 구조화하는가"의 문제였고, 그 관점에서는 흥미로웠다.

## 1️⃣ 이게 뭐냐?

LSP는 Language Server Protocol의 약자다. 예전에는 IDE마다 각 언어를 별도로 구현해야 했다. Python 자동완성을 IntelliJ에 넣으려면 IntelliJ용으로 만들고, VS Code에 넣으려면 VS Code용으로 따로 구현해야 했던 구조였다.

LSP는 이 반복 작업을 줄이려고 만들어진 공통 프로토콜이다. 자동완성, 포매팅, 문서 검색 같은 기능을 하나의 언어 서버에 구현해두면, 다양한 에디터가 그 서버를 가져다 쓸 수 있는 구조가 된다.

그런데 IntelliJ의 LSP 클라이언트 구현은 지금까지 상업용 확장에만 포함되어 있었다. Azure DevOps Pipeline 플러그인이 Android Studio에서 작동하지 않았던 이유도 이것 때문이었다. Android Studio는 IntelliJ의 상업 버전이 아니기 때문이다.

이번 변화의 핵심은 이 API를 IntelliJ 플랫폼 오픈소스 레포로 옮겨서, 모든 IntelliJ 기반 IDE에서 공통으로 쓸 수 있게 하는 거다.

## 2️⃣ 내가 든 생각

이번 발표와 함께 API 이름도 바뀐다. `LspServer`가 `LspClient`로, Provider 관련 클래스가 `LspIntegrationProvider`로 이동한다. 이름만 보면 사소해 보이는데, 왜 바꾸는지가 흥미로웠다. 서버 프로토콜을 다루는 쪽은 결국 클라이언트이므로, `LspServer`보다 `LspClient`가 이름 자체로 더 정확한 표현에 가까웠다. 기존 이름이 좀 헷갈릴 만했겠다 싶었다.

👉🏻 오픈소스화와 API 이름 정리가 동시에 이뤄진다는 점이 인상적이었다. 보통 이런 변화는 한 번에 하기 어려운데, 큰 변화를 기회 삼아 설계도 같이 정리한 느낌이었다.

Swift 플러그인 Noctule 작성자가 기존 공개 API로는 원하는 수준의 제어가 불가능해서 커스텀 LSP 클라이언트를 직접 만들 수밖에 없었다는 사례도 언급됐다. "커스텀 클라이언트가 과도한 선택이 아니라, 유일한 방법이었다"는 표현이 남았다. 열려 있는 API로는 닿을 수 없는 부분이 있었다는 건데, 이번 변화가 그 부분을 어느 정도 채워주는지는 지금 단계에서는 판단하기 어렵다.

> 💡 **여기서 드는 질문**: LSP 클라이언트 API가 열리면, 플러그인 개발자와 언어 서버 개발자 사이의 역할 경계가 어떻게 달라질까?

기존에 LSP4IJ라는 별도 구현을 쓰는 플러그인이라면 지금 당장 마이그레이션이 필수는 아니라고 한다. IDE 버전 지원 범위, Android Studio 호환 여부 등을 따져보고 결정하면 된다는 안내였다. 플러그인 개발자 입장에서 보면 선택지가 늘어난 것이지, 당장 뭔가를 고쳐야 하는 건 아니라는 게 흥미로웠다.

## ⭐️ 마지막으로, 공부하면서 정리해보니

이 글을 읽으면서 자꾸 비슷한 구조가 떠올랐다. "하나의 공통 레이어를 두면 여러 클라이언트가 가져다 쓴다" — 이건 LSP만의 얘기가 아니라 인터페이스 설계에서 반복되는 패턴에 가까운 것 같았다.

공부 끝에 남은 건 LSP 오픈소스화 자체보다 "공개 API를 어디까지 열어야 서드파티가 자유롭게 쓸 수 있는가"라는 질문 쪽이었다.

---

> 참고 원문: [Open-Sourcing the LSP Client API in IntelliJ IDEA 2026.2](https://blog.jetbrains.com/platform/2026/06/open-sourcing-the-lsp-client-api-in-intellij-idea-2026-2/)
