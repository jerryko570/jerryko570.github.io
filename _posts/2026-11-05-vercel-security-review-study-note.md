---
title: "Vercel Security Review 공부 정리 | push할 때마다 보안 검사가 돌아간다는 게"
description: "GitHub push마다 취약점을 자동 검사하는 Vercel Security Review가 public beta. PR이 아닌 push 기반이라는 점이 흥미로웠다."
date: 2026-11-05 10:00:00 +0900
categories: [Frontend]
tags: [vercel, security, ci, dev-workflow]
image:
  path: /assets/img/thumbnail/vercel.png
  alt: "Vercel Security Review 공부 정리 | push할 때마다 보안 검사가 돌아간다는 게"
---

Vercel 블로그에서 Security Review라는 기능이 public beta로 공개됐다는 소식을 읽었다. 처음엔 이름만 보고 외부 감사 서비스 같은 걸 연동하는 건가 했는데, 읽어보니 GitHub에 코드를 push할 때마다 소스 코드를 자동으로 훑어서 취약점을 찾는 기능이었다.

보안 쪽은 솔직히 아직 잘 모르는 영역이라서 처음엔 그냥 넘겼다. 그런데 push 이벤트 기반이라는 점이 걸려서 다시 돌아와 공부해봤다.

## 1️⃣ 이게 뭐냐?

Security Review는 GitHub 저장소에 push가 일어날 때마다 소스 코드에서 취약점을 자동 검사하고, 결과를 Vercel 대시보드와 GitHub check에 돌려주는 기능이다. Pro/Enterprise 팀을 대상으로 public beta 단계이고, Vercel GitHub App이 설치된 저장소에서 쓸 수 있다.

내가 흥미로웠던 건 트리거가 PR이 아니라 push라는 점이었다. 보통 CI 검사는 PR 올릴 때 돌린다고 이해하고 있었는데, push 기반이면 프로덕션 브랜치에 직접 push하거나 force push해도 검사가 돌아간다. 한 번의 push가 여러 프로젝트에 영향을 줄 경우엔 함께 검토된다.

검사 결과에는 어느 프로젝트, 어느 브랜치, 어느 커밋인지와 함께 취약점 요약, 수정 제안, AI가 매긴 심각도 등급이 담긴다. PR이 열려있으면 finding 링크가 달린 리뷰 코멘트도 자동으로 달린다.

수정은 두 가지다. 대시보드에서 "Fix with Vercel Agent"를 누르면 Agent가 수정안을 만들어 PR을 열어준다. 단, 사람이 직접 승인하기 전에는 머지되지 않는다. CLI에서는 `vercel security vulnerabilities`로 결과를 조회할 수 있고, Markdown이나 JSON으로 내보내서 다른 에이전트에 넘기는 것도 된다.

## 2️⃣ 내가 든 생각

여러 가지가 걸렸는데, 그중 하나는 "자연어로 보안 정책을 작성할 수 있다"는 점이었다. 팀 단위나 프로젝트 단위로 "우리는 이렇게 빌드한다"는 맥락을 문장으로 알려주면, Security Review가 그 맥락을 반영해 검사한다고 한다.

👉🏻 디자이너로서 처음 든 생각은 이런 인터페이스가 왠지 익숙하다는 것이었다. 기술 용어가 아닌 자연어로 의도를 전달하고, AI가 그걸 해석해 동작하는 흐름이 최근 AI 도구들이 가는 방향과 겹쳐 보였다. 보안 도구가 꼭 보안 전문가만 쓰는 형태가 아닐 수도 있겠다는 생각도 들었다.

> 💡 **여기서 든 질문**: AI가 심각도를 매기는 기준이 궁금해졌다. 같은 취약점이라도 프로젝트 맥락에 따라 위험도가 다를 텐데, 자연어 정책이 그 차이를 얼마나 반영해줄 수 있는지는 문서만 봐선 잘 모르겠다.

다만 문서에 한계가 명시되어 있다는 점도 인상적이었다. 소스 코드 분석이지 보안 감사나 런타임 테스트가 아니며, 취약점이 없다는 걸 보장하지는 않는다고 적혀있다. 도구가 커버하는 범위를 솔직하게 선 그어두는 방식이 오히려 신뢰가 가는 느낌이었다.

Agent가 수정 PR을 열어도 사람이 승인해야 머지된다는 원칙도 그 연장선에 있는 것 같았다. AI가 제안을 하되, 최종 판단은 사람이 한다는 흐름인 것 같다.

## ⭐️ 마지막으로

공부 끝에 남은 건 "보안 점검도 린터처럼 쓸 수 있겠다"는 한 줄짜리 인상이다. push마다 자동으로 돌고, GitHub check로 결과가 붙고, Agent가 수정 PR을 여는 흐름이 CI의 다른 단계들과 별로 달라 보이지 않았다. 보안이 따로 챙기는 항목이 아니라 개발 흐름 안에 녹아있는 형태로 가고 있구나 싶었다.

---

> 참고 원문: [Vercel Security Review now in public beta](https://vercel.com/changelog/vercel-security-review-public-beta)
