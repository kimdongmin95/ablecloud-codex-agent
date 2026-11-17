# ABLESTACK Docs 자동 동기화

- GitHub Actions: `Sync ABLESTACK Docs`
- 일정: 매주 월요일 09:17 KST (GitHub 일정 실행은 지연될 수 있음)
- 수동 실행: Actions → Sync ABLESTACK Docs → Run workflow
- 동작: 공식 Markdown 문서 스냅샷을 `knowledge/docs/`에 저장하고 변경분만 커밋
- 검색: `scripts/search_knowledge.py`는 스냅샷 우선, 없으면 로컬 공식 체크아웃 사용
- 원본 소스: https://github.com/ablecloud-team/ablestack-docs

## 공개 재배포 전 확인

공식 저장소에서 명시적인 LICENSE 파일을 확인하지 못했습니다.
공식 문서를 개인의 **공개 GitHub 저장소에 복제/재배포**할 권한이 있는지
ABLECLOUD 또는 문서 권리자에게 확인하세요.

확인 전에는 워크플로 잡이 **실행되지 않습니다**.
권한 확인 후 저장소 Settings → Secrets and variables → Actions → Variables에
`ALLOW_DOCS_REPUBLISH` 이름으로 `true`를 설정하면 동작합니다.

## 주의사항

- 코드와 출처 정보 외에 고객사 로그, 접속 정보, 비밀번호를 넣지 마세요.
- 이미지, PDF 및 백서는 자동 복제하지 않습니다.
- GitHub Actions의 `contents: write` 권한이 허용되어야 자동 커밋됩니다.
- 브랜치 보호 규칙이 직접 push를 차단하면 별도의 PR 흐름이 필요합니다.
- 공개 저장소에 60일간 활동이 없으면 GitHub가 scheduled workflow를 자동 비활성화할 수 있습니다.
- upstream 저장소가 매우 크므로 최초 clone 및 갱신에 시간이 들 수 있습니다.
