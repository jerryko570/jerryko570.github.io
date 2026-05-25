---
title: "Nemotron-Labs Diffusion LM 공부 정리 | 토큰을 동시에 만든다는 게 무슨 말인가"
description: "NVIDIA가 공개한 확산 언어 모델, 기존 자회귀 방식과 뭐가 다른지 정리해봤다."
date: 2026-05-25 12:00:00 +0900
categories: [DevTools]
tags: [nvidia, llm, diffusion, inference, ai]
image:
  path: /assets/img/thumbnail/nemotron-labs-diffusion-lm-study-note.png
  alt: "Nemotron-Labs Diffusion LM 공부 정리 | 토큰을 동시에 만든다는 게 무슨 말인가"
---

HuggingFace 블로그에 NVIDIA의 Nemotron-Labs Diffusion 발표가 올라왔다. 제목에 "speed-of-light"가 붙어 있어서 처음엔 마케팅 문구겠거니 싶었는데, 읽다 보니 텍스트를 만드는 방식 자체가 달라서 정리해봤다.

핵심은 토큰을 생성하는 순서에 있다. 지금 쓰는 LLM들은 "나는 → 학교에 → 간다"처럼 왼쪽에서 오른쪽으로 하나씩 확정한다. 이번 모델은 그 방식이 다르다.

## 1️⃣ 이게 뭐냐?

Nemotron-Labs Diffusion LM은 여러 토큰 묶음을 동시에 만든다. 처음엔 노이즈에 가까운 상태에서 시작해서, 여러 번 반복하며 의미 있는 텍스트로 좁혀간다. 이미지 생성 모델에서 쓰던 확산(Diffusion) 개념을 텍스트에 가져온 건데, 텍스트는 연속값이 아니라 이산값이라 구현 방식이 다르다고 설명되어 있었다.

기존 자회귀(Autoregressive) 방식과 비교하면 가장 큰 차이는 GPU가 노는 시간이다. 기존 방식은 한 토큰이 완성될 때까지 다음 걸 시작 못 해서 GPU가 자주 대기 상태에 들어간다. 블록 단위로 동시에 처리하면 이 대기 시간이 줄어들고, 같은 GPU로 더 많은 요청을 다룰 수 있다는 게 주요 이점이었다.

하나의 모델 안에 3가지 생성 모드가 있는 것도 눈에 띄었다. 기존 AR 모드, 순수 확산(FastDiffuser) 모드, 그리고 Self-Speculation 모드다. Self-Speculation은 확산으로 후보 토큰을 여러 개 만들고 AR로 검증하는 방식인데, 속도와 정확도를 같이 가져가려는 시도로 읽혔다. 배포 설정만 바꾸면 기존 애플리케이션 코드는 그대로 쓸 수 있다는 설명도 있었다.

## 2️⃣ 내가 든 생각

디자이너 관점에서 봤을 때 가장 먼저 든 질문은, 텍스트가 블록 단위로 나온다면 사용자에게 어떻게 보여줄 수 있을까였다. 지금 AI 채팅 UI는 대부분 토큰이 하나씩 흘러들어오는 패턴인데, 블록 단위 생성이라면 이 흐름이 달라질 수 있다는 생각이 들었다.

👉🏻 "더 빠른 응답"이라는 말 뒤에, 응답을 어떻게 표현할지의 설계 질문이 같이 붙는다는 게 흥미로웠다.

> 💡 **여기서 드는 질문?**
> 블록 단위로 생성되는 텍스트를 사용자에게 어떤 방식으로 자연스럽게 표현할 수 있을까?

확산 방식을 텍스트에 쓴다는 것도 처음엔 잘 상상이 안 됐다. 이미지는 픽셀이 연속값이라 노이즈에서 정제하는 게 직관적인데, 텍스트는 개별 단어가 이산적이라 다른 방식이 필요하다는 걸 문서를 읽으면서 조금씩 이해했다. 단어들 사이의 연속성을 확률 분포로 근사해서 다룬다는 것까지 이해한 수준이고, 더 깊은 구현은 기술 보고서를 봐야 알 것 같다.

## ⭐️ 마지막으로

이런 류의 발표를 볼 때 자꾸 같은 질문을 하게 되는 것 같다 — 속도가 빨라지면 그게 사용자 경험에서 어떤 다른 가능성을 만들어낼 수 있을까.

---

> 참고 원문: [Towards Speed-of-Light Text Generation with Nemotron-Labs Diffusion Language Models](https://huggingface.co/blog/nvidia/nemotron-labs-diffusion)
