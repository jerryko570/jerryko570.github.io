# Jerry's Blog

> 프론트엔드 공부하는 앱디자이너의 학습 저널.

🔗 **Live**: [jerryko570.github.io](https://jerryko570.github.io)

---

## 👋 about

UI/UX 디자인 환경에서 프론트엔드를 공부하고 있는 **Jerry**의 개인 자동화 기술 블로그입니다.

UI/UX 디자이너로 일하다가 프론트엔드를 본격적으로 파보고 있는 Jerry입니다. 
처음엔 "내가 디자인한 걸 직접 만들고 싶다"는 생각으로 시작했는데, 막상 들어와 보니 모르는 게 산더미고 배워도 어렵기만 합니다.
그래서 대부분 "공부 정리" 같은 학습 노트 톤으로 운영하고 있습니다. 깔끔한 결론은 거의 없고, 헤맨 흔적이 더 많이 남아있습니다.
다루는 건 React, TypeScript, Next.js 같은 프론트엔드 기본기, 그리고 디자이너 시절부터 만지던 도구들(Figma, Webflow, 요즘은 Claude까지)이 변해가는 모습을 함께 적어보려고 합니다.

---

## 🤖 매일 글이 자동으로 올라옵니다

이 블로그는 사람이 쓴 글과 함께, **매일 한국시간 오전 9시에 자동으로 새 학습 노트가 한 편 발행**됩니다. 직접 짠 워크플로우가 RSS를 돌고, Claude Code가 글을 쓰고, GitHub Actions가 푸시·빌드까지 합니다.

### 흐름

```
오전 9시 (KST)
    │
    ▼
┌───────────────────────────────┐
│ 1. RSS 크롤 (prepare.py)      │  공식 블로그 피드만 수집 (60일 이내)
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│ 2. 카테고리 선정 + 폴백       │  오늘 차례 카테고리에 새 글이 없으면
│                               │  자동으로 다음 카테고리로 넘어감
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│ 3. Claude Code 학습 노트 작성 │  Jerry의 톤·스타일 가이드를 읽고
│                               │  1500자 내외 한국어로 재구성
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│ 4. 썸네일 생성                │  카테고리 컬러 + 키워드 라벨
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│ 5. 커밋 + 푸시 → Pages 빌드   │  사이트에 자동 반영
└───────────────────────────────┘
```

### 카테고리 (4일 주기로 순환)

| ID | 표시명 | 다루는 내용 |
|---|---|---|
| `design-tools` | Design | Figma · Webflow · Notion 같은 디자인 도구의 공식 업데이트 |
| `design-craft` | DesignCraft | 토스 · PXD 등 한국 IT 기업의 프로덕트 디자인 케이스 |
| `frontend` | Frontend | React · Vercel · Tailwind · Astro · Svelte 공식 릴리스 |
| `dev-tools` | DevTools | OpenAI · GitHub · JetBrains · Hugging Face 등 |

### 글이 안 겹치게 하는 장치

- `scripts/state.json` 에 발행한 글 URL 해시를 누적 저장
- `prepare.py` 가 매일 그 목록과 비교해 이미 발행한 글은 후보에서 제외
- 카테고리도 마지막 발행 시점을 기억해서 한 카테고리만 반복 발행되지 않도록 순환

---

## 🛠️ 기술 스택

**블로그 자체**
- [Jekyll](https://jekyllrb.com/) + [Chirpy 테마](https://github.com/cotes2020/jekyll-theme-chirpy)
- GitHub Pages 호스팅
- Pretendard / Noto Sans CJK 폰트

**자동화 파이프라인**
- Python 3.11 (`feedparser`, `requests`, `beautifulsoup4`, `pyyaml`, `Pillow`)
- GitHub Actions (스케줄·디스패치 트리거)
- [Claude Code Action](https://github.com/anthropics/claude-code-action) — 글 생성 엔진

---

## 📁 디렉토리 구조

```
.
├── _posts/                    # 블로그 포스트 (.md)
├── _config.yml                # Jekyll 설정
├── assets/img/thumbnail/      # 포스트 썸네일
│
├── scripts/
│   ├── sources.yml            # 카테고리별 RSS 소스 정의
│   ├── prepare.py             # RSS 크롤 → 후보 선정 (폴백 포함)
│   ├── crawler.py             # RSS/Atom 파싱 라이브러리
│   ├── state_manager.py       # 중복 방지 + 카테고리 순환 상태
│   ├── update_state.py        # 포스트 발행 후 state 갱신 (stdin JSON)
│   ├── make_thumbnail.py      # 썸네일 생성 CLI
│   └── state.json             # 누적 상태 (자동 갱신)
│
├── prompts/
│   ├── claude_instructions.md # Claude Code가 따르는 작업 지시서
│   ├── style_guide.md         # 글쓰기 톤·블랙리스트 정의
│   └── author_context.md      # Jerry 페르소나·말투
│
└── .github/workflows/
    └── auto-blog-post.yml     # 일 1회 자동 발행 워크플로우
```

---

## 🧪 로컬에서 돌려보기

자동화 파이프라인을 손볼 일이 있으면 아래 순서로 테스트할 수 있습니다.

```bash
# 1. 의존성 설치
pip install -r scripts/requirements.txt

# 2. 후보 수집만 돌려보기
python scripts/prepare.py

# 3. 결과 확인
cat scripts/candidates.json | head -30
```

워크플로우 전체를 한 번에 돌리고 싶으면 GitHub 저장소 → **Actions** → **Auto Blog Post** → **Run workflow** 버튼.

---

## 📝 글쓰기 원칙

자동 발행 글이 AI 티 안 나게 하는 게 가장 어려운 부분이었습니다. `prompts/style_guide.md` 에 블랙리스트로 다음을 못 쓰게 막아두고 있어요.

- "완전히 / 혁명적 / 반드시" 같은 호들갑
- "여러분" 같은 대중 호칭
- 권위 인용 ("OO 연구에 따르면", 출처 없는 수치)
- 거창한 결론 선언

대신 권장하는 톤은:

- "써봐야 알겠지만"
- "이게 흥미로웠다"
- "~에 가까웠다"

원문을 번역·요약하지 않고, 읽은 뒤 **Jerry의 언어로 재구성**하는 걸 핵심 규칙으로 둡니다.

---

## 📮 연락처

- **Email**: jerry.narae@gmail.com
- **GitHub**: [@jerryko570](https://github.com/jerryko570)

---

<sub>이 README도 사람이 직접 작성했습니다. 자동 생성된 글에는 본문 하단에 "참고 원문" 링크가 항상 붙어있어요.</sub>