# 오승환 개발자 포트폴리오

GitHub Pages에서 제공할 수 있는 정적 HTML 포트폴리오입니다. 메인 페이지와 프로젝트 상세 페이지 6개, 기존에 검증한 Archify 다이어그램을 포함합니다. 서버나 npm 패키지 설치 없이 작동합니다.

## 미리보기

이 폴더에서 다음 명령을 실행하고 `http://127.0.0.1:4173/portfolio/`를 엽니다.

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

## 내용 수정

`content.json`의 소개, 기술 스택, 프로젝트 내용을 수정한 뒤 다음 명령으로 HTML을 다시 생성합니다.

```powershell
python build.py
python verify.py
```

스타일은 `portfolio/assets/style.css`, 테마 전환과 분야 필터는 `portfolio/assets/site.js`에서 관리합니다. 실제 사이트는 `portfolio/` 아래에 생성됩니다. 내부 경로는 상대 경로여서 프로젝트 상세 페이지와 다이어그램 링크도 같은 경로 아래에서 작동합니다.

## GitHub Pages 배포

1. 공개 저장소는 기존 `osh8242/osh8242.github.io`를 유지하며, 사이트 주소는 `https://osh8242.github.io/portfolio/`입니다.
2. **이 폴더의 내용만** 저장소 루트에 올립니다. 상위 폴더의 경력 기록, 지원서, 소스 프로젝트는 업로드 대상이 아닙니다.
3. 저장소의 **Settings → Pages → Build and deployment**에서 **Deploy from a branch**, `main`, `/(root)`를 선택하고 저장합니다.
4. 배포가 완료되면 `https://osh8242.github.io/portfolio/`로 접근합니다. 이후 수정은 같은 저장소의 `main` 브랜치에 반영합니다.

### 주소 변경 방식 (2026-10-04)

- 저장소 이름이나 GitHub Pages 설정을 바꾸지 않고, 기존 사이트 파일을 `portfolio/` 폴더로 옮겼습니다.
- `build.py`도 같은 폴더에 HTML을 생성하도록 바꿨습니다. 소개·프로젝트 내용과 디자인은 유지합니다.
- 계정 루트 `/`, 오타 경로 `/portpolio/`, 기존 `/projects/*.html` 및 HTML 다이어그램 주소는 새 경로로 자동 이동합니다. JavaScript를 사용할 수 있으면 검색 조건과 본문 위치(`#...`)도 유지하며, 사용할 수 없으면 HTML 자동 이동과 수동 링크가 동작합니다.
- 사이트와 저장소의 공개 설정은 변경하지 않았습니다. 주소 변경은 접근 제한 기능이 아닙니다.

[GitHub 공식 배포 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 원문과 근거

콘텐츠는 사용자의 개발자 포트폴리오 및 연결된 프로젝트 상세 문서에서 가져왔습니다. 파일 워커의 중복 실행 방지 주장은 후속 코드 점검에서 확인한 범위에 맞춰 제외했습니다. Impala는 인수 후 분석·검증 역할로 표기하며 환경 변화로 단축된 시간을 구현 성과로 주장하지 않습니다.

- [개발자 포트폴리오 원문](https://app.notion.com/p/3b9361f185c381e7a1d0ea37d4cc8db3)
- 콘텐츠 스냅샷 확인일: 2026-10-04

전화번호와 지원서 PDF는 사이트에 추가하지 않았습니다. 이름과 연락용 이메일, GitHub·Notion 공개 링크만 사용합니다. Google Fonts와 Shields.io는 표시용 외부 리소스이며, 글꼴이나 배지를 읽지 못해도 본문과 링크는 사용할 수 있습니다.
