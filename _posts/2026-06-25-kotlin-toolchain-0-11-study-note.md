---
title: "Kotlin Toolchain 0.11 공부 정리 | Amper는 어디로 갔을까"
description: "Amper가 Kotlin Toolchain으로 이름을 바꾸고 Alpha 단계에 진입했다. 브랜드 변경 뒤에 뭐가 달라졌는지 문서를 읽어보며 정리했다."
date: 2026-06-25 10:00:00 +0900
categories: [DevTools]
tags: [kotlin, jetbrains, build-tools, cli]
image:
  path: /assets/img/thumbnail/kotlin-toolchain-0-11-study-note.png
  alt: "Kotlin Toolchain 0.11 공부 정리 | Amper는 어디로 갔을까"
---

JetBrains 블로그에 Kotlin Toolchain 0.11 릴리스 글이 올라왔다. 메인은 Amper라고 불리던 빌드 도구가 이름을 바꾸고 Alpha 단계에 진입했다는 내용이었다.

처음엔 "리브랜딩인데 뭘 공부하나"라는 생각이었는데, 왜 이름이 바뀌었는지 읽어보다 보니 단순히 마케팅 차원의 변화는 아닌 것 같았다. 조금 더 들여다봤다.

## 1️⃣ 이게 뭐냐?

Amper는 JetBrains가 만든 빌드 도구였다. Gradle이나 Maven이 있던 자리에서, 설정 방식을 더 단순하게 만들겠다는 방향으로 시작된 프로젝트다.

0.11 버전부터 이름이 Kotlin Toolchain으로 바뀌었다. 핵심은 "빌드 도구 하나"에서 "Kotlin 개발 전체의 진입점"으로 포지션을 재정의했다는 점이다. `kotlin`이라는 단일 명령어로 프로젝트 생성, 빌드, 테스트, 배포를 전부 처리하는 흐름을 만들겠다는 방향인 것 같다.

Alpha 전환도 중요한 포인트였다. JetBrains 기준에서 Alpha가 정확히 어느 수준인지는 모르지만, 실험 단계를 벗어나 프로덕션 환경에서도 쓸 수 있다는 공식 입장을 낸 것이라는 건 읽을 수 있었다.

새 기능 중 눈에 띈 건 JVM 라이브러리를 Maven Central에 직접 배포할 수 있게 된 것이다. PGP 서명, 체크섬 같은 걸 자동으로 처리해준다고 한다. 기존에 이 과정이 번거로웠던 모양이다. 글로벌 CLI 설치도 지원해서 `kotlin` 명령어를 프로젝트 밖에서도 쓸 수 있게 됐다.

기존 Amper 사용자는 래퍼 스크립트(`amper` → `kotlin`)와 IDE 플러그인을 새 버전으로 교체해야 한다.

## 2️⃣ 내가 든 생각

이름 변경이 단순 리브랜딩으로 안 읽힌 이유가 있었다. "빌드 도구"와 "Toolchain"은 담는 범위가 다르다. 이름이 바뀌면서 도구가 책임지는 범위 자체가 달라진 거라는 느낌이 들었다.

👉🏻 단일 명령어로 전 주기를 처리하는 방향은 프론트엔드에서도 비슷한 흐름이 있다고 느꼈다. Vite나 Bun 같은 도구들이 빌드만이 아니라 런타임, 패키징, 개발 서버까지 아우르는 방향으로 가고 있는 것과 비슷한 결이라는 생각이 들었다.

> 💡 **그러면 Kotlin Toolchain이 Kotlin 생태계에서 Bun 같은 포지션을 노리는 걸까?**  
> 문서만 본 입장에서는 정확히 가늠하기 어렵다. 실제 사용 예시를 더 찾아봐야 알 수 있을 것 같다.

마이그레이션 공지가 꽤 명시적이라는 점도 인상적이었다. 명령어와 플러그인 이름이 바뀐다는 건 기존 사용자 입장에서 귀찮은 작업이지만, 인터페이스가 통일되면 장기적으론 낫지 않을까 싶었다.

## ⭐️ 마지막으로, 빌드 도구를 공부하면서 든 생각

공부 끝에 남은 건 이거였다. 도구가 이름을 바꿀 때는 대개 "어디까지 책임질 것인가"라는 선 긋기가 들어있다는 것. Amper에서 Kotlin Toolchain으로의 전환도 그 선이 달라진 거라는 한 줄짜리 인상이다.

---

> 참고 원문: [Kotlin Toolchain 0.11: The Next Step for Amper](https://blog.jetbrains.com/amper/2026/06/kotlin-toolchain-0-11/)
