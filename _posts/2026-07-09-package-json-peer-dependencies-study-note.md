---
title: "package.json 공부 정리 | 공통 컴포넌트 패키지를 만들면서 마주친 설정들"
description: "공통 컴포넌트를 별도 패키지로 배포하는 상황에서 처음 제대로 마주친 peerDependencies, files, engines 필드를 정리한 기록"
date: 2026-07-09 10:00:00 +0900
categories: [DesignCraft]
tags: [javascript, package-json, peerdependencies, npm, component-library]
image:
  path: /assets/img/thumbnail/package-json-peer-dependencies-study-note.png
  alt: "package.json 공부 정리 | 공통 컴포넌트 패키지를 만들면서 마주친 설정들"
---

PXD Story에서 package.json에 관한 글을 읽었다. 공통 컴포넌트를 별도 패키지로 배포해본 경험을 정리한 글인데, 특히 `peerDependencies`라는 필드가 처음 등장하는 맥락이 흥미로웠다.

평소에 `dependencies`랑 `devDependencies` 정도만 봐왔는데, 공통 컴포넌트를 다른 서비스에서 설치해 쓰는 구조로 만들어야 하는 순간 판단해야 할 것들이 달라진다는 게 이번에 정리됐다.

## 1️⃣ peerDependencies가 뭐냐

`peer`는 '동등한 위치'라는 의미다. 이 패키지를 사용하는 쪽에서 직접 설치해야 하는 의존성을 선언하는 방식인데, 쉽게 말하면 "React는 내가 따로 번들하지 않을게, 너희가 가진 걸 쓸게"라고 명시하는 거다.

이게 왜 필요한지는 React를 생각하면 이해가 됐다. 만든 패키지가 React를 직접 번들해버리면, 그걸 쓰는 프로젝트에 React가 두 개 공존하게 된다. 그러면 Hooks 오류나 Context가 분리되는 문제가 생긴다고 한다. 공통 컴포넌트에서 react, react-dom, styled-components 같은 건 `peerDependencies`로 관리해야 한다는 이유가 여기서 온다.

```json
{
  "peerDependencies": {
    "react": "^18.0.0 || ^19.0.0",
    "react-dom": "^18.0.0 || ^19.0.0"
  },
  "devDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

글에서 권장한 방식은 개발 단계에서는 `devDependencies`에도 같이 넣어두고, `peerDependencies`로 버전 호환성 조건을 명시하는 구조였다. 두 군데 동시에 선언하는 게 처음엔 이상해 보였는데, 각자 역할이 다르다는 걸 이해하고 나서 납득이 됐다.

## 2️⃣ 내가 든 생각

"나중에 제외하는 방식"은 실수할 가능성이 높다는 표현이 인상적이었다. 선언을 미리 정확하게 나눠두는 게, 번들 결과물에서 예상치 못한 것들이 끼어 있는 상황을 피하는 방법이라는 것이다.

👉🏻 한 가지 놓치기 쉬운 부분이 있었는데, `rollupOptions`에서 `external` 설정을 빠뜨리면 `peerDependencies`로 선언해도 번들에 포함될 수 있다는 거였다. 선언하는 것과 실제로 제외되는 것이 자동으로 연결되지 않는다는 게 처음 알게 된 포인트였다.

> 💡 **여기서 드는 질문?**
> 단일 프로젝트에서 쓸 때는 잘 몰라도 됐던 것들이 패키지 배포 순간 전부 다 의미를 갖게 되는 건데, 그럼 이 설정들을 언제부터 챙겨야 하는 걸까.

`files` 필드도 처음 제대로 봤다. npm에 배포할 때 `dist`와 `README.md`만 포함시키는 설정인데, 이 필드 없이 배포하면 소스 파일, 테스트 코드 같은 것들까지 올라간다. 배포 대상을 명시적으로 좁히는 방식이 의도치 않은 파일 노출을 막는다는 것도 새로 정리됐다.

`engines` 필드는 이 패키지가 어떤 Node.js 버전과 패키지 매니저에서 동작하는지를 명시하는 거다. 여러 개발 환경이 혼재하는 팀에서 빌드 오류를 사전에 막는 용도라고 한다. 공부만 한 입장에서는 협업 환경일수록 이런 명시가 중요해진다는 인상이었다.

## ⭐️ 마지막으로, package.json을 공부하며 든 생각

결국 핵심은 package.json이 "패키지 목록을 적어두는 파일"이 아니라, 이 코드가 어떤 환경에서 어떻게 쓰이길 원하는지를 선언하는 파일에 가깝다는 쪽인 것 같다. 혼자 쓸 때는 굳이 몰라도 넘어가던 설정들이, 다른 서비스에서 설치해 쓰는 순간 전부 의미를 갖게 된다. 프론트 공부를 하다 보면 이런 식으로 "이 필드가 왜 있는 건지"가 하나씩 풀리는 순간이 있는데, 이번이 그런 경우였다.

---

> 참고 원문: [package.json 어디까지 알고 계신가요? (peerDependencies, files, engines, version)](https://story.pxd.co.kr/1906)
