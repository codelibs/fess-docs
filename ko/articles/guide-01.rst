================================
Fess로 할 수 있는 일과 도입 방법
================================

들어가며
========

사내 문서는 웹 사이트, 파일 서버, 클라우드 스토리지, 채팅이나 티켓 관리 같은 SaaS, 데이터베이스에 나뉘어 저장되어 있습니다.
각 도구에 검색 기능이 있더라도, 여러 위치를 가로질러 한 번에 찾을 수는 없습니다.
Fess는 이러한 위치에서 문서를 모아 하나의 인덱스로 정리하고, 하나의 검색 화면이나 API에서 찾을 수 있게 해 주는 검색 서버입니다.

이 글은 Fess 도입을 검토하고 있는 정보 시스템 부서의 담당자와 개발자를 대상으로 다음 내용을 설명합니다.

- Fess가 무엇으로 구성되어 있고 어떻게 동작하는지
- 기본으로 사용할 수 있는 기능과 플러그인을 추가해야 사용할 수 있는 기능의 구분
- 목적에 따라 어느 글부터 읽어 나가면 되는지

각 기능의 설정 절차는 해당 글에서 다룹니다.

이 실천 가이드가 대상으로 하는 버전
===================================

실천 가이드의 각 글은 Fess 15.9를 대상으로 합니다.
화면의 항목명, 설정 키, 기본값은 15.9에서 확인한 것입니다.
15.10 이후에서만 사용할 수 있는 기능을 소개할 때는 글 안에 그 사실을 명시합니다.

레퍼런스 링크는 ``https://fess.codelibs.org/ko/stable/``\ 로 시작하며, 현재 안정 버전의 문서를 가리킵니다.
다른 버전을 사용하는 경우에는 URL의 ``stable``\ 을 버전 번호(예: ``15.9``)로 바꾼 페이지에서 항목명과 기본값을 확인하십시오.

Fess란
======

Fess는 Java로 작성된 오픈 소스 전문 검색 서버입니다.
라이선스는 Apache License 2.0이며, 상용 환경에서도 무상으로 사용할 수 있습니다.

문서의 저장과 검색에는 OpenSearch를 사용합니다.
Fess 15.9는 기동 시 연결 대상을 확인하고, OpenSearch 3 이상이 아니면 기동을 중단합니다.
OpenSearch 2 이하나 Elasticsearch에는 연결할 수 없습니다.
15.9에서는 본체에 내장되어 있던 검색 엔진이 제거되었으므로, OpenSearch는 반드시 별도로 준비해야 합니다(Docker 구성에서는 OpenSearch 컨테이너도 함께 기동합니다).

하나의 Fess에 다음 요소가 모두 갖추어져 있습니다.

- 문서를 수집하는 크롤러(웹, 파일 서버, 플러그인을 통한 각종 서비스)
- 크롤링 설정, 사용자, 권한, 사전, 스케줄 등을 설정하는 관리 화면
- 사용자가 이용하는 검색 화면
- 검색이나 추천을 외부 시스템에서 호출하기 위한 API(``/api/v2/``)

검색 화면은 HTML, CSS, JavaScript를 묶은 정적 테마로 표시됩니다.
Fess에는 ``bootstrap`` 테마가 포함되어 있으며, 다른 테마는 ZIP 파일로 [시스템] > [테마]에서 추가합니다.

Fess의 구성
===========

Fess를 동작시킬 때 등장하는 요소는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 요소
     - 역할
   * - Fess 본체(웹 애플리케이션)
     - 검색 화면, 관리 화면, API를 제공합니다. 스케줄러도 여기서 동작하며, 설정된 시각에 크롤링 등의 작업을 기동합니다
   * - 크롤러(별도 프로세스)
     - 크롤링 작업은 Fess 본체와는 별개의 Java 프로세스로 기동됩니다. 웹 페이지나 파일을 가져와 본문을 추출하고 OpenSearch에 등록합니다. 추천어 생성, 썸네일 생성, 시맨틱 검색용 벡터 생성 작업도 마찬가지로 별도 프로세스에서 동작합니다
   * - OpenSearch
     - 검색 대상 문서의 인덱스를 보관하고 검색을 실행합니다. 크롤링 설정이나 사용자, 작업 로그, 검색 로그 등 관리 화면에서 등록한 정보의 대부분도 여기에 저장됩니다

크롤러는 별도의 Java 프로세스이므로, 사용하는 메모리도 Fess 본체와 별도로 설정합니다(:doc:`guide-14`\ 에서 다룹니다).

문서를 검색할 수 있게 되기까지의 흐름은 다음과 같습니다.

1. 관리 화면에서 크롤링 설정(대상 URL이나 경로, 검색 결과를 보여 줄 대상을 정하는 권한 등)을 등록합니다
2. 스케줄러가 크롤링 작업을 기동합니다. 관리 화면에서 [지금 시작]으로 수동 기동할 수도 있습니다
3. 크롤러가 문서를 가져와 본문을 추출하고, 권한과 함께 OpenSearch에 등록합니다
4. 사용자가 검색하면, Fess는 사용자의 역할과 그룹으로 결과를 걸러 낸 다음 반환합니다

Docker로 기동하여 크롤링하고 검색하기까지의 일련의 조작은 :doc:`guide-02`\ 에서 직접 해 볼 수 있습니다.

본체 기능과 플러그인
====================

Fess 15.9에서는 많은 기능이 플러그인으로 본체와 분리되어 제공됩니다.
필요한 플러그인이 미리 들어 있는지는 도입 방법에 따라 다릅니다.

- ZIP, RPM, DEB로 도입한 Fess에는 플러그인이 하나도 들어 있지 않습니다
- Docker 표준 이미지(``ghcr.io/codelibs/fess:15.9.0`` 등)에는 다음 7개 플러그인이 미리 들어 있습니다: ``fess-script-groovy``, ``fess-storage-s3``, ``fess-storage-gcs``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``, ``fess-sso-oidc``
- Docker slim 이미지(``15.9.0-slim`` 등)에는 플러그인이 들어 있지 않습니다

주요 기능과 필요한 플러그인을 다음 표에 정리합니다.

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - 기능
     - 본체만으로 사용할 수 있는 것
     - 플러그인이 필요한 것
   * - 크롤링
     - 웹(http, https), 파일 시스템, 파일 서버(SMB), FTP
     - Amazon S3(``fess-storage-s3``), Google Cloud Storage(``fess-storage-gcs``), 브라우저에서 JavaScript를 실행하여 가져오는 웹 크롤링(``fess-crawler-playwright``)
   * - SaaS, 데이터베이스 등
     - 데이터 저장소 설정 화면과 실행 구조
     - 가져올 대상별 데이터 저장소 플러그인(``fess-ds-*``). Slack, Confluence와 Jira, Google Drive, Microsoft 365, Box, 데이터베이스, CSV, Git 등
   * - 로그인과 권한
     - Fess에 등록한 사용자, 역할, 그룹, LDAP / Active Directory와의 연동
     - SSO(OpenID Connect는 ``fess-sso-oidc``, SAML은 ``fess-sso-saml``, Entra ID는 ``fess-sso-entraid``, SPNEGO는 ``fess-sso-spnego``)
   * - 스크립트
     - JavaScript
     - Groovy(``fess-script-groovy``), OGNL(``fess-script-ognl``)
   * - 검색 화면
     - 포함된 테마 ``bootstrap``
     - 플러그인이 아니라 테마 ZIP 파일을 추가합니다
   * - API
     - ``/api/v2/``\ (검색, 라벨, 추천어, 인기 검색어, 헬스 체크 등)와 관리 API
     - ``/api/v1/``\ (``fess-webapp-v1-api``), ``/json``\ 과 ``/suggest``\ (``fess-webapp-classic-api``). Fess Site Search는 ``/api/v1/``\ 을 사용하므로 ``fess-webapp-v1-api``\ 가 필요합니다
   * - AI 관련
     - 시맨틱 검색과 AI 검색 모드(RAG)의 구조. OpenSearch에 배포한 임베딩 모델을 사용하는 경우, 시맨틱 검색에는 플러그인이 필요 없습니다
     - LLM이나 외부 임베딩 모델과의 연결(``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``), MCP 서버(``fess-webapp-mcp``), 이미지 검색(``fess-webapp-multimodal``)

표의 "플러그인이 필요한 것" 가운데 Docker 표준 이미지에 들어 있는 것은 S3와 GCS, SSO 4종류, Groovy뿐입니다.
그 밖의 플러그인은 어떤 도입 방법이든 추가로 설치해야 합니다.

스크립트 종류로 Groovy를 지정한 설정과, 이전 버전에서 이어받은 설정 중 스크립트 종류가 기록되어 있지 않은 설정은 Groovy로 실행됩니다.
이들을 사용하려면 ``fess-script-groovy``\ 가 필요합니다.
새로 만드는 데이터 저장소 설정에서는 스크립트 종류의 초깃값이 JavaScript입니다.

플러그인은 다음 중 한 가지 방법으로 설치합니다.
설치하거나 삭제한 후에는 Fess를 재시작합니다.
플러그인 버전은 Fess 버전에 맞춥니다(Fess 15.9라면 15.9.x).

- 관리 화면의 [시스템] > [플러그인]에서 [설치]를 클릭하고 목록에서 선택한다
- 명령줄에서 ``bin/fess-setup install plugin <플러그인 이름>:<버전>``\ 을 실행한다
- Docker에서는 환경 변수 ``FESS_PLUGINS``\ 에 ``fess-ds-slack:15.9.0 fess-webapp-mcp:15.9.0``\ 처럼 공백으로 구분하여 지정한다

데이터 저장소 플러그인의 사용법은 :doc:`datastore-basics`\ 에서, 플러그인을 직접 만드는 방법은 :doc:`guide-17`\ 에서 설명합니다.

검색할 수 있는 파일 형식
========================

파일에서 본문을 추출할 때는 Apache Tika 등의 추출 처리를 사용합니다.
HTML, PDF, Microsoft Office 문서, 텍스트, 압축 파일의 내용 등을 검색할 수 있습니다.
확인된 형식의 목록은 `검색 대상 파일 <https://fess.codelibs.org/ko/supported-files.html>`__\ 을 참조하십시오.

이미지나 스캔해서 만든 PDF 안의 문자는 기본적으로 검색할 수 없습니다.
크롤러가 동작하는 호스트에 ``tesseract``\ 를 설치하고 OCR을 활성화하면 검색할 수 있게 됩니다.
절차는 `OCR(이미지 내 문자 인식) 설정 <https://fess.codelibs.org/ko/stable/config/crawler-ocr.html>`__\ 을 참조하십시오.

도입 방법 선택하기
==================

Fess는 Docker, ZIP, RPM, DEB로 배포됩니다.
먼저 시험해 보려면 Fess와 OpenSearch를 한꺼번에 기동할 수 있는 Docker가 가장 빠른 방법입니다.
절차는 :doc:`guide-02`\ 에서 설명합니다.

운영 환경에서는 OpenSearch를 별도의 서버나 클러스터로 준비할 수도 있습니다.
필요한 Java와 OpenSearch 버전, CPU·메모리·디스크 기준은 `시스템 요구사항 <https://fess.codelibs.org/ko/stable/install/prerequisites.html>`__\ 을 확인하십시오.

목적별로 읽어 나가는 순서
=========================

글은 목적에 따라 읽어 나갈 수 있도록 나뉘어 있습니다.
목적에 가까운 행을 골라, 글을 왼쪽부터 차례로 읽으십시오.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 목적
     - 읽을 글
   * - 우선 시험해 보고 싶다
     - :doc:`guide-02`
   * - 파일 서버를 검색하고 싶다
     - :doc:`file-server-search` → :doc:`guide-04` → :doc:`guide-05`
   * - 클라우드나 SaaS의 데이터를 검색하고 싶다
     - :doc:`datastore-basics` → :doc:`guide-07` / :doc:`guide-06` / :doc:`guide-12`
   * - 기존 사이트나 시스템에 검색을 넣고 싶다
     - :doc:`guide-03` → :doc:`guide-11`
   * - 부서나 사용자별로 보여 줄 정보를 나누고 싶다
     - :doc:`guide-05` → :doc:`guide-15` → :doc:`guide-13`
   * - AI로 검색을 강화하고 싶다
     - :doc:`guide-18` → :doc:`guide-19` → :doc:`guide-20`
   * - 운영 환경에서 사용을 시작한다
     - :doc:`guide-10` → :doc:`guide-16` → :doc:`guide-14`

이 밖에 다음 글이 있습니다.

- 검색 품질 높이기: :doc:`guide-08`, :doc:`guide-09`, :doc:`guide-22`
- 이미지와 텍스트를 함께 검색하기: :doc:`guide-21`
- 플러그인 직접 만들기: :doc:`guide-17`
- 전사 확대 계획하기: :doc:`guide-23`
- 활용 사례와 다른 제품과의 비교: :doc:`use-cases`, :doc:`comparison`

글 목록은 :doc:`../guide` 페이지에도 정리되어 있습니다.

참고 자료
=========

- `Fess 문서(안정 버전) <https://fess.codelibs.org/ko/stable/>`__
- `시스템 요구사항 <https://fess.codelibs.org/ko/stable/install/prerequisites.html>`__
- `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__
- `플러그인 아키텍처 <https://fess.codelibs.org/ko/stable/dev/plugin-architecture.html>`__
- `테마 <https://fess.codelibs.org/ko/stable/admin/theme-guide.html>`__
- `검색 대상 파일 <https://fess.codelibs.org/ko/supported-files.html>`__
- `docker-fess(GitHub) <https://github.com/codelibs/docker-fess>`__
- `codelibs/fess(GitHub) <https://github.com/codelibs/fess>`__
