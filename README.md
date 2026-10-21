# 전기산업기사 필기 CBT

React·TypeScript·Vite로 구현한 비공식 학습용 정적 웹앱입니다. 전기기능사 CBT의 MIT 코드를 고정 커밋 `b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`에서 재사용하고 전기산업기사 설정과 새 문제은행으로 분리했습니다. [CBT 표준 스킬](.agents/skills/cbt-site-standard/SKILL.md) 전체와 references를 복사했으며 [AGENTS.md](AGENTS.md)에서 연결합니다. 기존 대상 저장소에는 AGENTS.md나 앱·workflow가 없었습니다.

## 구현 기능

- 실전 모의시험: 100문항, 150분 절대 종료 시각, 과목별 추출, 답안 수정·번호 이동, 새로고침 복원, 만료 자동 제출, 중복 제출 방지, 과락 포함 채점, 모든 보기·정답·해설과 시험 오답 재학습.
- 랜덤 문제풀이: 전체/과목 선택, 한 순회 ID 중복 방지, 즉시 채점, 연속 정답·세션 정답률·이어하기.
- 오답노트, 정답 재학습 시 오답 제거, 북마크, 과목별 통계·최근 시험과 취약 과목.
- JSON/CSV 양식·가져오기, 중복 제거, 검증 대기·근거 입력 후 로컬 승인, 검색·상태 필터·페이지 목록·JSON 내보내기.
- 답안 선택 후 두 모드에서 Space로 다음 문제 이동. 마지막 시험 문제에서는 자동 제출하지 않습니다. 입력·IME·수정키·길게 누르기·메뉴·대화상자를 보호합니다.
- PC/모바일 반응형 화면, 작은 높이·가로 화면에서도 독립 스크롤 가능한 메뉴. 상단 상시 면책 배너와 학습 기준/연도 버전 선택 메뉴는 없습니다. 비공식 고지는 사이드바·푸터에, 검수 한계는 문제은행 관리·해설·문서에 표시합니다. 실제 저장 오류 경고는 유지합니다.

## 공식 시험 규칙

2026-10-21 [Q-Net 전기산업기사 시험정보](https://www.q-net.or.kr/crf005.do?id=crf00503s02&jmCd=2140&jmInfoDivCcd=B0)의 취득방법을 직접 확인했습니다.

| 항목 | 설정 |
| --- | --- |
| 과목 | 전기자기학·전력공학·전기기기·회로이론·전기설비기술기준 |
| 방식 | 객관식 4지선다, 과목당 20문항·30분 |
| 합계 | 100문항·150분 |
| 합격 | 과목별 40점 이상 **그리고** 전체 평균 60점 이상 |
| 미응답 | 오답으로 처리하고 오답노트에 포함 |

자격증 규칙과 저장 namespace는 [qualification.json](src/qualification.json)에서 관리합니다. [공식 확인 기록](docs/official-rules.md)과 [응답 해시·확인 범위](docs/official-evidence.json)를 남겼습니다. 공식 시험 규칙의 확인과 개별 문항의 공식 출제기준 대조는 별개입니다. 실기는 제공하지 않습니다.

## 실제 문제 수와 한계

| 과목 | 자체 제작 | 원문 기출 | 복원 |
| --- | ---: | ---: | ---: |
| 전기자기학 | 200 | 0 | 0 |
| 전력공학 | 200 | 0 | 0 |
| 전기기기 | 200 | 0 | 0 |
| 회로이론 | 200 | 0 | 0 |
| 전기설비기술기준 | 200 | 0 | 0 |
| 합계 | **1,000** | **0** | **0** |

기본 JSON에 등록된 내부 검수 완료 1,000개, 검증 대기·제외·정규화 중복 0개, 목표 부족 0개입니다. **25개의 계산 원고 × 조건 40개로 구성한 수치 변형 은행**이며 1,000개의 독립 개념·기출이 아닙니다. 기준 조건 25개와 추가 조건 변형 975개, 비계산 개념형 0개입니다. 사용자 개인 등록분은 집계하지 않습니다.

`reviewed`는 AI 보조 원고 25개의 질문·조건·공식·단위·해설 내부 검토와 모든 변형의 독립 계산 검사를 뜻합니다. 외부 전문가나 독립적인 사람의 전수 검수는 받지 않았습니다. 출제 연도·회차는 모두 `null`입니다. 저장소 URL은 작성 위치·검수 기록이지 외부 정답 증빙이 아닙니다. 읽지 않은 자료를 출처로 표기하지 않았습니다.

**전체 출제범위 대비용으로는 보완이 필요합니다.** 전기설비기술기준은 설비 기초 계산만 있고 최신 법규·KEC 문항은 없습니다. Q-Net 세부 출제기준의 항목별 매핑, 다양한 개념·응용 원고 확대와 전문가 검수가 남아 있습니다. 기출 원문·공식 정답·연도·회차·재배포 권한을 확보하지 않아 기출을 등록하지 않았습니다. [유형·문항 검수 기록](docs/question-review.md)에 정확한 범위를 설명합니다.

한 회 시험은 과목마다 먼저 서로 다른 family 5개에서 1개씩 선택한 뒤 나머지 15개를 고유 ID로 보충합니다. 따라서 현재 은행은 같은 계산 유형이 한 시험에 반복되며, 실제 시험의 난이도·주제 분포를 재현하지 않습니다.

## 로컬 개발·검증

Node.js 24.19.0(`.node-version`), npm 11.9.0으로 확인했습니다. package engines의 최소 버전은 Node 22.12입니다. 서버·로그인·유료 API·비밀키는 필요 없습니다.

```bash
cd /workspace/Industrial-Engineer-Electricity-CBT
npm ci --cache /tmp/iee-npm-cache --no-audit --no-fund
npm run dev -- --port 5173 --strictPort
```

```bash
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

현재 클라우드처럼 Chromium이 이미 설치되어 있으면 다운로드 대신 다음을 사용합니다.

```bash
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e
```

문항 원고의 재생성은 `python scripts/generate_bank.py`입니다. 결정적 입력·순서·고정 ID로 동일한 JSON을 생성합니다. 생성 코드와 다른 TypeScript 식으로 재검산하며 테스트는 바이트 단위 재현도 확인합니다. Python 3은 재생성 검사에 필요합니다. 앱 커밋 `8c65bc6`의 [배포 없는 GitHub CI](https://github.com/YunSangYeong/Industrial-Engineer-Electricity-CBT/actions/runs/39538039191)도 성공했습니다. 자세한 결과는 [검증 기록](docs/validation.md)에 있습니다.

## 기록 보관과 가져오기

저장 키는 `industrial-engineer-electricity-cbt:v1`이며 전기기능사 앱과 충돌하지 않습니다. localStorage에 시험·연습·북마크·오답·개인 등록 문항을 보관합니다. 응답은 최근 5,000개, 시험은 최근 30회입니다. 저장 실패는 경고하고, 손상 데이터는 자동 덮어쓰지 않습니다. 초기화에는 확인이 필요하며 기본 문제는 보존합니다.

학습 기록 JSON **백업 내보내기**를 지원하지만 백업 복원 UI는 없습니다. 문제은행 JSON 가져오기와 학습 기록 복원을 혼동하지 마세요. origin·브라우저·기기가 다르면 기록은 분리되고, 시크릿/iframe의 저장 제한이 적용될 수 있습니다. 문제은행 등록·승인은 현재 브라우저에만 저장되며 GitHub 공용 데이터로 자동 게시하지 않습니다.

## 사용자가 직접 GitHub Pages 배포하기

**에이전트는 Pages를 활성화하거나 배포·재배포하지 않았습니다. 배포 workflow·배포 API도 실행하지 않았습니다.** 신규 `pages.yml`은 오직 `workflow_dispatch`이며 deploy job도 수동 이벤트·`main` 조건과 검증 성공을 요구합니다. push/PR의 `ci.yml`은 읽기 권한으로 검증만 수행합니다.

반영 브랜치는 `codex/electricity-cbt-20261021`입니다. GitHub API에서 기존 Pages Source 설정을 읽는 요청이 네트워크 403으로 차단되어, 확인되지 않은 브랜치 배포를 피하려고 기존 `main` 대신 원격에 없던 새 브랜치에 푸시합니다. 기존 `main`에는 README만 있고 workflow가 없음을 Git 트리에서 확인했습니다. API로 기존 Pages의 활성화 여부나 외부 배포 연계까지 확인했다고 주장하지 않습니다.

사용자 배포 순서:

1. 저장소 **Settings → Pages**를 확인합니다. 기존 브랜치 기반 자동 게시가 있다면 **먼저 Source를 GitHub Actions로 변경**하여 병합만으로 배포되지 않게 합니다. Pages 최초 활성화나 설정 변경은 사용자가 직접 진행합니다. 다른 외부 배포 연계도 있으면 자동 실행을 먼저 해제합니다.
2. `codex/electricity-cbt-20261021`의 변경을 검토하여 `main`에 병합합니다. 이 코드의 push/PR CI는 배포하지 않습니다. Actions 검증 결과를 확인합니다.
3. Pages Source가 **GitHub Actions**인지 확인하고, **Actions → Publish Pages (user manual only) → Run workflow → main**을 직접 실행합니다. 이 작업은 테스트·브라우저 검사·빌드 성공 후에만 아티팩트를 배포합니다. 필요한 environment 승인이 있으면 직접 처리합니다.
4. 배포 커밋과 실행 성공을 확인하고, PC/모바일 두 모드·과락·새로고침·Space·메뉴 스크롤을 공개 주소에서 확인합니다. 이 공개 검증은 아직 실행하지 않았습니다.

예상 기본 주소: `https://YunSangYeong.github.io/Industrial-Engineer-Electricity-CBT/` (미배포). Vite base도 이 저장소 경로로 지정했습니다. 기본 URL은 이후에도 유지하며 블로그 iframe에는 이 주소를 사용합니다. 실제 블로그의 iframe·서드파티 저장 제한은 사용자 배포 후 별도 확인이 필요합니다.

## 라이선스

기준 앱 코드는 MIT 고지를 보존했습니다. 새 자체 제작 문제·등록 양식은 CC BY 4.0입니다. 외부 가져오기 자료의 이용 권한은 별도로 확인해야 합니다. [LICENSE](LICENSE)를 참고하세요.
