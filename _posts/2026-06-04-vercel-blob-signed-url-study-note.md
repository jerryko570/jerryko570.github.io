---
title: "Vercel Blob Signed URL 공부 정리 | 서버가 열쇠를 쥐는 구조"
description: "Vercel Blob에 추가된 Signed URL 기능을 읽어봤다. 전체 권한 대신 좁게 잘라낸 URL을 발급하는 구조가 흥미로웠다."
date: 2026-06-04 10:00:00 +0900
categories: [Frontend]
tags: [vercel, blob, signed-url, security]
image:
  path: /assets/img/thumbnail/vercel-blob-signed-url-study-note.png
  alt: "Vercel Blob Signed URL 공부 정리 | 서버가 열쇠를 쥐는 구조"
---

Vercel 블로그를 보다가 Blob에 Signed URL이 추가됐다는 공지를 봤다. 처음엔 "URL에 서명이 붙는 거구나" 정도로 지나치려 했는데, 어떻게 동작하는지가 궁금해서 좀 더 읽어봤다.

Vercel Blob은 Next.js 같은 환경에서 파일 저장을 간단하게 연결할 수 있게 해주는 스토리지 서비스다. 지금까지는 `BLOB_READ_WRITE_TOKEN`이라는 하나의 긴 토큰으로 권한을 관리해야 했는데, 이번 업데이트로 그 방식이 달라졌다.

## 1️⃣ 이게 뭐냐?

핵심은 "전체 권한이 담긴 토큰을 클라이언트에 넘기지 않는다"는 쪽에 가깝다. 대신 서버가 `issueSignedToken()`으로 서명 토큰을 만들고, `presignUrl()`로 시간 제한 URL을 발급한다. 이 URL은 딱 하나의 작업(`put`, `get`, `head`, `delete` 중 하나)에만 쓸 수 있고, 지정한 경로의 단일 객체에만 유효하다. 만료 시간은 최대 7일.

```ts
// 서버에서 발급
const uploadUrl = await presignUrl('uploads/avatar.png', {
  operation: 'put',
  expiresIn: 3600
})
// 이 URL만 브라우저에 넘김
```

`put` URL은 multipart를 지원한다고 한다. 브라우저가 대용량 파일을 서버를 경유하지 않고 Blob에 직접 스트리밍할 수 있는 구조다. 이전 방식이라면 서버가 중간에서 파일을 받아 다시 올려야 했을 텐데, 그 과정을 건너뛸 수 있는 셈이다.

`delete` URL에는 `ifMatch` 옵션도 있다. URL을 발급한 뒤 다른 파일로 덮어씌워졌다면 삭제 자체를 건너뛰는 조건을 걸 수 있다. 이런 세밀한 제어가 가능하다는 게 문서를 읽으면서 꽤 흥미로웠다.

## 2️⃣ 내가 든 생각

Signed URL이라는 개념 자체는 AWS S3 같은 클라우드 스토리지에서 익숙한 패턴이다. Vercel Blob에 이게 붙었다는 점보다, "그럼 이전까진 어떻게 했지?"라는 질문에서 공부가 시작됐다.

👉🏻 가장 인상적이었던 건 "범위 제한" 구조였다. URL 하나는 get이면 get만, put이면 put만 허용한다. 같은 URL로 다른 작업을 시도할 수 없고, 경로도 발급 시점에 고정된다. 서명이 "작업 + 경로 + 만료"를 한꺼번에 묶어두니까, 유출되더라도 피해 범위가 그 안에 머무는 편이다.

> 💡 **여기서 드는 질문?**  
> OIDC 인증과 연동하면 서버가 `BLOB_READ_WRITE_TOKEN` 없이 동작한다고 하는데, 로컬 개발 환경에서 이 흐름이 어떻게 구성되는 건지 아직 잘 모르겠다.

디자이너 관점으로 보면, "클라이언트에게 최소한만 준다"는 구조가 UI 권한 설계와 닮아 있다는 생각이 들었다. 사용자에게 보여주는 액션 범위와 실제 시스템 권한을 분리하는 방식이라고 하면 비슷한 방향인 것 같다.

## ⭐️ 마지막으로, 이 기능을 공부하며 남은 것

정리해보니, 이 기능이 해결하는 건 "어떻게 파일을 올릴까"라기보다 "전체 권한 없이 최소한만 줄 수 있을까" 쪽에 가까운 것 같다. 구현 편의보다 설계 의도가 더 눈에 들어온 공부였다.

---

> 참고 원문: [Signed URLs are now available for Vercel Blob](https://vercel.com/changelog/signed-urls-are-now-available-for-vercel-blob)
