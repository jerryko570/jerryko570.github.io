---
title: "git worktree 공부 정리 | 브랜치 전환 없이 병렬 작업하기"
description: "GitHub 블로그에서 git worktree 소개 글을 읽었다. 2015년부터 있던 기능인데 왜 이제야 주목받는 건지 정리해봤다."
date: 2026-06-17 09:00:00 +0900
categories: [DevTools]
tags: [git, worktree, github-copilot]
image:
  path: /assets/img/thumbnail/git-worktree-study-note.png
  alt: "git worktree 공부 정리 | 브랜치 전환 없이 병렬 작업하기"
---

GitHub 블로그에 `git worktree`를 소개하는 글이 올라왔다. 제목만 봤을 때는 브랜치 관련 팁 글 정도겠거니 했는데, 읽어보니 좀 다른 개념이었다.

`git worktree`는 2015년부터 있던 기능이라는데, 최근 들어 갑자기 주목받기 시작했다고 한다. 오랫동안 거의 쓰이지 않다가 이제야 관심이 생긴 이유가 뭔지 궁금해서 좀 더 읽어봤다.

## 1️⃣ 이게 뭐냐?

핵심만 정리하면, 하나의 git 저장소에서 여러 작업 폴더를 동시에 열 수 있는 기능이다. 각 폴더는 서로 다른 브랜치를 체크아웃한 상태로 독립적으로 존재한다.

기존 방식과 비교하면 차이가 더 와닿는다. `feature-A` 브랜치에서 작업 중인데 갑자기 버그 수정이 들어왔다면, 보통은 `git stash → checkout → pull → 수정 → stash pop` 흐름을 타야 한다. 단계 자체는 어렵지 않은데, 그 과정에서 작업 흐름이 끊기는 느낌이 생각보다 불편하다.

worktree를 쓰면 새 폴더를 만들어서 거기서 따로 작업하면 된다:

```bash
git worktree add ../hotfix-workspace -b hotfix-bug main
```

`../hotfix-workspace` 폴더가 생기고, 거기서 `hotfix-bug` 브랜치 작업을 독립적으로 할 수 있다. 원래 폴더의 편집기 상태는 건드려지지 않는다.

한계도 있다. 같은 브랜치를 두 worktree에서 동시에 체크아웃하는 건 안 된다. `node_modules` 같은 의존성도 worktree마다 따로 설치해야 해서 디스크를 더 쓰게 된다. 저장소 내부에 worktree를 만들면 `.gitignore`에 따로 추가해줘야 하는 것도 챙겨야 할 부분이다.

## 2️⃣ 내가 든 생각

오래된 기능이 최근에야 주목받는 이유가 흥미로웠다. AI 기반 병렬 개발 세션이 늘면서 여러 컨텍스트를 동시에 다뤄야 하는 상황이 많아졌기 때문이라고 한다. GitHub Copilot 앱도 지금은 새 작업을 시작할 때 worktree를 기본값으로 쓴다고 했다.

그 배경이 납득이 갔다. AI 에이전트가 병렬로 여러 작업을 돌리는 패턴이 늘면서, 사람 쪽 작업 흐름도 비슷한 구조를 필요로 하게 됐다는 이야기.

디자이너 입장에서 보면 Figma에서 컴포넌트를 복사해 별도 파일에서 수정하는 방식이랑 비슷하다는 느낌이 들었다. 원본은 그대로 두고 분리된 공간에서 실험하는 패턴.

👉🏻 브랜치 전환의 실제 비용이 파일 변경 자체보다 "머릿속 컨텍스트 재로드"에 있는 것 같다는 생각이 들었다. `stash`하고 `checkout`하고 돌아오는 과정이 짧아도, 그 사이 집중이 흩어지는 감이 있다. worktree는 그걸 폴더 단위로 잘라낸다.

> 💡 **여기서 드는 질문?**
> 의존성을 각 worktree마다 따로 설치해야 한다면, 가볍게 hotfix 하나 수정하고 끝낼 때는 그냥 stash가 더 빠르지 않을까. 어떤 상황에서 worktree를 선택하고 어떤 상황에서 stash를 선택하는 게 맞는지, 기준을 아직 잘 못 잡겠다.

## ⭐️ 마지막으로, 이번 공부를 끝내고

공부 끝에 남은 건 이 정도다 — worktree는 "병렬 작업 도구"라기보다 "작업 흐름을 끊기지 않게 보호하는 도구"에 가깝다는 인상. 기능을 먼저 소개받으면 "굳이?"가 나오는데, 왜 쓰는지를 먼저 알고 나면 납득이 되는 종류였다.

---

> 참고 원문: [What are git worktrees, and why should I use them?](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them/)
