# 🤖 블로그 자동화 시스템 설치 가이드

Jerry의 블로그에 2일마다 자동으로 디자인/프론트엔드/백엔드/AI 주제의 글을 올려주는 시스템입니다.

**인증 방식**: Claude Max 구독을 이용한 OAuth 인증 (API 키 불필요, 추가 비용 없음)

---

## 📂 파일 구조

```
jerryko570.github.io/
├── .github/
│   └── workflows/
│       └── auto-blog.yml          # 2일마다 실행되는 워크플로우
├── scripts/
│   ├── prepare.py                 # 크롤링 + 카테고리 선택
│   ├── crawler.py                 # RSS 파싱 라이브러리
│   ├── thumbnail.py               # 썸네일 생성 라이브러리
│   ├── make_thumbnail.py          # 썸네일 CLI (Claude Code가 호출)
│   ├── state_manager.py           # 상태 관리 라이브러리
│   ├── update_state.py            # 상태 업데이트 CLI (Claude Code가 호출)
│   ├── sources.yml                # 크롤링 소스 목록
│   ├── requirements.txt           # Python 패키지
│   ├── state.json                 # (자동 생성) 진행 상태
│   └── candidates.json            # (런타임) 크롤링 결과
├── prompts/
│   ├── style_guide.md             # 문체 규칙
│   ├── author_context.md          # 작성자 페르소나
│   └── claude_instructions.md     # Claude Code 지시사항
├── CLAUDE.md                      # 레포 컨텍스트
└── _posts/                        # 포스트가 자동 저장됨
```

---

## 🚀 설치 단계 (총 5단계, 약 15분)

### 1단계: 파일 복사

이 `blog-automation` 폴더의 모든 파일을 **레포 최상위**로 복사합니다.

```bash
# 예시
cd ~/projects/jerryko570.github.io
cp -r ~/다운로드/blog-automation/* .
cp -r ~/다운로드/blog-automation/.github .
```

`.github/`, `scripts/`, `prompts/`, `CLAUDE.md`가 레포 루트에 있어야 해요.

### 2단계: Claude Code 설치 (로컬)

터미널에서 Claude Code CLI 설치:

```bash
# npm 사용 (가장 간단)
npm install -g @anthropic-ai/claude-code

# 또는 homebrew (Mac)
brew install anthropic/tap/claude-code
```

### 3단계: Claude Code 로그인

```bash
cd ~/projects/jerryko570.github.io
claude
```

Claude Code가 실행되면 내부에서 로그인 명령어 실행:

```
/login
```

→ 브라우저가 열리며 Claude.ai 로그인 → Max 구독 계정으로 인증

### 4단계: GitHub App 설치 (핵심!)

Claude Code 안에서 다음 명령어 실행:

```
/install-github-app
```

이 명령어가 자동으로 해주는 것:
1. Claude GitHub App을 레포에 설치
2. **장기 OAuth 토큰** 생성 (단기 토큰 이슈 해결된 버전)
3. 레포의 GitHub Secrets에 `CLAUDE_CODE_OAUTH_TOKEN` 자동 등록
4. 기본 워크플로우 파일 생성 (우리가 만든 `auto-blog.yml`과는 별개)

> ⚠️ **주의**: `/install-github-app`이 `.github/workflows/claude.yml`을 생성할 수 있어요.
> 이건 `@claude` 멘션 응답용 워크플로우고, 우리 `auto-blog.yml`과는 별개로 공존 가능합니다.
> 원치 않으면 `claude.yml`만 삭제하세요.

### 5단계: GitHub Actions 권한 확인

레포 → **Settings** → **Actions** → **General** → 하단 **Workflow permissions**
- ✅ "Read and write permissions" 선택
- ✅ "Allow GitHub Actions to create and approve pull requests" 체크
- **Save**

### 6단계: 커밋 & 푸시

```bash
git add .github scripts prompts CLAUDE.md SETUP.md
git commit -m "feat: 블로그 자동화 시스템 추가 (Max OAuth 인증)"
git push
```

### 7단계: 수동 테스트 실행 🧪

첫 실행은 수동으로 해서 잘 동작하는지 확인하세요:

1. 레포 → **Actions** 탭
2. 좌측 **Auto Blog Post** 워크플로우 클릭
3. 우측 **Run workflow** 버튼 → **Run workflow** 확인
4. 실행 로그 확인 (각 단계별로)
5. 성공 시 `_posts/`에 새 MD 파일이 자동 커밋됩니다

---

## ⚙️ 실행 주기

- 2일마다 한국시간 오전 9시(UTC 0시)에 자동 실행
- 필요시 Actions 탭에서 **Run workflow**로 수동 실행 가능
- 카테고리 순환: 디자인 → 프론트엔드 → 백엔드 → AI → 디자인 ...

---

## 🛠️ 커스터마이징

### 문체 바꾸기
`prompts/style_guide.md`와 `prompts/author_context.md`를 수정 → 커밋하면 다음 실행부터 즉시 반영.

### 소스 추가/제거
`scripts/sources.yml`에서 RSS URL을 추가/제거.

### 주기 변경
`.github/workflows/auto-blog.yml`의 cron 표현식:
- 매일: `'0 0 * * *'`
- 3일마다: `'0 0 */3 * *'`
- 주 1회 월요일: `'0 0 * * 1'`

### Claude 모델 변경
`.github/workflows/auto-blog.yml`의 `claude_args`:
- `--model claude-sonnet-4-6` (기본, 권장)
- `--model claude-opus-4-7` — 최고 품질 (Max 할당량 더 많이 씀)
- `--model claude-haiku-4-5-20251001` — 빠르지만 품질 낮음

---

## 💰 비용

**$0/월!** 🎉

Claude Max 5x 구독만으로 모든 GitHub Actions 실행이 무료입니다.
GitHub Actions 자체도 **Public 레포는 무제한 무료**라서 추가 비용 없어요.

---

## ❓ 문제 해결

### 인증 실패: `Invalid OAuth token`
- `/install-github-app`을 다시 실행하세요 (토큰 재발급)
- 또는 Claude Code에서 `/logout` 후 다시 `/login`

### 토큰이 만료됨
- `/install-github-app`은 **장기 토큰**을 발급하지만, 간혹 갱신이 필요할 수 있어요
- GitHub → Settings → Secrets → Actions → `CLAUDE_CODE_OAUTH_TOKEN` 삭제 후 다시 `/install-github-app` 실행

### 실행은 됐는데 포스트가 안 생겼어요
- Actions 탭 → 해당 실행 클릭 → 로그 확인
- "후보 없음" 메시지 = 모든 RSS가 이미 본 글이거나 피드가 비어있음. 다음 실행 기다리거나 수동 재실행.

### Claude가 엉뚱한 형식으로 저장했어요
- `prompts/claude_instructions.md`의 해당 부분을 더 명확히 수정
- 또는 해당 포스트만 수동으로 삭제 (`state.json`의 `seen_url_hashes`에는 기록되어 있어서 중복 안 됨)

### 한글 썸네일이 깨져 나와요
- `auto-blog.yml`의 `fonts-noto-cjk` 설치 단계 로그 확인

### 푸시 실패
- 6단계의 Workflow permissions 설정 확인

### Claude Code 할당량 초과
- Max 5x도 시간당 제한이 있어요. 2일에 1회 실행이니 문제 없을 거예요.
- 만약 할당량 이슈 발생 시 Pro로 낮추거나, 모델을 Haiku로 변경.

---

## 🔄 API 방식으로 전환하고 싶다면

OAuth 방식이 불안정하거나 문제가 생기면, 언제든 API 방식으로 전환 가능:

1. [Anthropic 콘솔](https://console.anthropic.com)에서 API 키 발급
2. `ANTHROPIC_API_KEY`를 GitHub Secrets에 등록
3. 워크플로우의 `claude_code_oauth_token` → `anthropic_api_key`로 변경
4. 비용: 월 $1 미만

필요하면 도움 요청하세요!

---

## 📝 기타

- 원문 저작권 존중을 위해 **번역이 아닌 재해석**을 원칙으로 하며, 글 끝에 원문 출처가 링크됩니다
- 자동 포스트가 마음에 안 들면 `_posts/`에서 그냥 지우면 됩니다. `state.json`에는 이미 기록돼 있어서 같은 원문이 다시 뽑히진 않아요.
- Jerry의 기존 수기 포스트와 구분하기 쉽게 썸네일 파일명에 `auto-` 접두사가 붙어요.

즐거운 자동화 되세요! 🚀
