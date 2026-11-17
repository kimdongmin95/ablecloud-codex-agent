# ABLECLOUD Codex Technical Q&A Agent

Codex에서 ABLESTACK 기술 문서를 검색하고 근거·그림·점검 절차를 포함한 답변을 작성하는 개인용 프로젝트입니다.

## 처음 실행 (Windows PowerShell)

```powershell
cd C:\Projects\ablecloud-codex-agent
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\sync_docs.py
.\.venv\Scripts\python.exe scripts\ingest_pdfs.py
.\.venv\Scripts\python.exe scripts\search_knowledge.py "Glue 스토리지 구성" --limit 5
codex
```

`git` CLI와 인터넷 연결이 필요합니다. `sync_docs.py`는 공식 문서 저장소를 `knowledge/upstream/ablestack-docs`로 clone/pull 합니다. `ingest_pdfs.py`는 `config/sources.json`에서 지정한 **공식 PDF만** 받아 텍스트를 추출합니다. 웹페이지 PDF 링크 탐색 및 임의 크롤링은 구현하지 않았습니다.

Codex에서 이렇게 질문하세요:

> $ablecloud-expert ABLESTACK HCI에서 Cell, Glue, Mold의 역할을 비교하고 Mermaid 구성도와 공식 문서 출처를 포함해 설명해줘.

## 자료 출처

- https://docs.ablecloud.io/latest/
- https://github.com/ablecloud-team/ablestack-docs
- https://www.ablecloud.io/resource/ebook

공식 GitHub 문서의 **현재 기본 브랜치**를 가져옵니다. 배포 사이트의 latest 버전과 일치하지 않을 수 있으므로 답변 시 버전 차이를 확인하세요. PDF 등 콘텐츠의 저작권은 원저작자에게 있습니다. 공개 GitHub에 수집한 문서/PDF 또는 내부 운영 정보를 커밋하지 마세요.

## 답변 동작

1. Codex가 질문을 읽고 `search_knowledge.py`를 실행합니다.
2. 검색 결과는 출처 파일, 제목, URL, 짧은 발췌를 제공합니다.
3. 답변은 반드시 원문을 추가로 열어 검증하고 공식 페이지 URL을 링크합니다.
4. 공식 이미지가 있다면 공식 URL로 연결하거나 사용자가 확인할 수 있는 위치를 안내합니다.
5. 새로운 개념도를 설명할 때 Mermaid 도식을 포함합니다. Mermaid는 렌더링 가능한 환경에서 이미지처럼 표시됩니다.

## 제한 사항

- 공식 백서 검색 전용 API를 확인한 것은 아닙니다. 현재 PDF 직접 요청 방식입니다.
- 본 프로젝트는 로컬 자료 검색과 Codex를 위한 지침입니다. 별도 LLM API나 독립형 챗봇 서버가 아닙니다.
- Markdown의 상대 이미지 링크는 경우에 따라 사이트 주소로 별도 확인해야 합니다.
- 검색 알고리즘은 기본 키워드 검색이며, 고급 의미 검색(RAG embedding)은 미구현입니다.
- 공개 소스의 라이선스와 이용 조건을 확인하고 사용하세요.
