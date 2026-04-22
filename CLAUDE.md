# Jerry's Blog — Repository Context

이 레포는 Jekyll + Chirpy 테마로 운영되는 개인 기술 블로그입니다.

## 디렉토리 구조

- `_posts/` — 블로그 포스트 마크다운 파일들. 파일명 형식: `YYYY-MM-DD-slug.md`
- `_config.yml` — Jekyll 설정
- `assets/img/thumbnail/` — 포스트 썸네일 이미지들
- `scripts/` — 자동 블로그 생성 스크립트 (Python)
- `prompts/` — AI가 글 쓸 때 참고하는 스타일/페르소나 가이드
- `.github/workflows/auto-blog.yml` — 2일마다 자동 포스트 생성 워크플로우

## 블로그 작성자 (Jerry)

- 프론트엔드 공부하는 앱디자이너 (UI/UX 디자인 배경)
- 반말(하다체)로 학습 저널 형식의 글을 씀
- 상세 문체 규칙: `prompts/style_guide.md`
- 작성자 페르소나: `prompts/author_context.md`

## 자동화 워크플로우

- `scripts/prepare.py`가 먼저 실행되어 RSS 피드를 크롤링하고 `scripts/candidates.json`을 생성
- 이후 Claude Code Action이 `prompts/claude_instructions.md`의 지시대로 포스트 작성
- Claude Code가 호출할 수 있는 Python CLI 도구:
  - `scripts/make_thumbnail.py` — 썸네일 자동 생성
  - `scripts/update_state.py` — 상태 업데이트

## 중요

- 모든 포스트는 **한국어**로 작성 (코드/기술 용어는 영문)
- 프론트매터는 Chirpy 테마 규격을 따름
- 원문 저작권 존중: 번역이 아닌 재해석, 출처 각주 필수
