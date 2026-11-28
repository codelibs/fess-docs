===========================
Fess 활용 사례와 유스케이스
===========================

들어가며
========

이 페이지에서는 Fess가 자주 쓰이는 상황을 업종별, 규모별, 기술적 목적별로 소개합니다.
각 사례마다 해결하려는 과제, 사용하는 Fess의 기능과 플러그인, 절차를 설명하는 글을 제시합니다.
설정 절차 자체는 각 글에 있으므로, 자신의 상황과 가까운 사례부터 읽을 글을 고르십시오.

이 글의 기능과 플러그인 이름은 Fess 15.9에 맞추었습니다.
15.9에서는 데이터베이스와 SaaS의 수집, SSO, S3·GCS 크롤링이 플러그인으로 제공됩니다.
플러그인 버전은 Fess와 같은 15.9.x를 사용하고, 설치한 뒤에는 Fess를 재시작합니다.
설치 방법은 `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__\ 을 참조하십시오.

.. note::

   아래는 일반적인 활용 패턴입니다. 실제 도입 사례는 `상용 지원 <../support-services.html>`__\ 에 문의하십시오.

목적으로 기능 찾기
==================

.. list-table::
   :header-rows: 1
   :widths: 34 38 28

   * - 하고 싶은 일
     - 사용하는 기능·플러그인
     - 읽을 글
   * - 먼저 로컬에서 실행해 보기
     - Docker Compose(docker-fess)
     - :doc:`guide-02`
   * - 사내 사이트와 파일 서버를 한꺼번에 검색하기
     - 웹 크롤링, 파일 시스템 크롤링, 파일 인증, 라벨
     - :doc:`guide-04`, :doc:`file-server-search`
   * - 부서나 직위에 따라 보이는 문서를 다르게 하기
     - 권한, 역할·그룹, LDAP(Active Directory)
     - :doc:`guide-05`
   * - 기존 사이트에 검색창 두기
     - 검색 폼, Fess Site Search(``fess-webapp-v1-api``), 테마
     - :doc:`guide-03`
   * - Git·Confluence·Jira·Slack 검색하기
     - ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack``
     - :doc:`datastore-basics`, :doc:`guide-06`
   * - Google Drive·SharePoint Online·Box 검색하기
     - ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box``
     - :doc:`datastore-basics`, :doc:`guide-07`
   * - 데이터베이스·CSV·Salesforce 검색하기
     - ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce``
     - :doc:`datastore-basics`, :doc:`guide-12`
   * - 업무 시스템에서 검색하기
     - 검색 API(``/api/v2``), 액세스 토큰
     - :doc:`guide-11`
   * - 사내 로그인으로 검색하게 하기
     - ``fess-sso-entraid``, ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``
     - :doc:`guide-15`
   * - 하나의 Fess를 여러 조직에서 나눠 쓰기
     - 가상 호스트, 역할, 라벨
     - :doc:`guide-13`
   * - 검색되지 않는 단어나 사용 방식을 조사해 개선하기
     - [시스템 정보] > [검색 로그]
     - :doc:`guide-08`
   * - 의미가 가까운 문서 찾기, AI가 답하게 하기
     - 시맨틱 검색, AI 검색 모드, ``fess-webapp-mcp``
     - :doc:`guide-18`, :doc:`guide-19`, :doc:`guide-20`
   * - 문서 수와 사용자 증가에 대비하기
     - OpenSearch 분리·클러스터화, Fess 여러 대 구성
     - :doc:`guide-14`
   * - 운영 환경에서 안정적으로 운영하기
     - ``/api/v2/health``, 백업, 로그
     - :doc:`guide-10`

업종별 유스케이스
=================

제조업: 흩어진 기술 문서 찾기
-----------------------------

**과제**: 설계서, 사양서, 품질 기록이 부문별 파일 서버에 나뉘어 있어, 도면 번호나 모델 번호로 관련 자료를 찾는 데 시간이 걸린다.

**사용하는 기능**:

- 파일 서버를 ``smb://``\ 로 크롤링하여 PDF나 Office 문서의 본문을 검색할 수 있게 합니다. Windows의 접근 권한(ACL)은 기본적으로 문서의 권한으로 수집됩니다
- 표시 이름이 "설계", "품질"과 같은 라벨을 만들고 대상 경로로 문서를 분류하여, 검색 화면에서 범위를 좁힐 수 있게 합니다
- 스캔한 종이 기록은 OCR을 활성화하면 본문을 검색할 수 있습니다. OCR은 기본적으로 비활성화되어 있으며, 크롤러가 실행되는 호스트에 ``tesseract``\ 가 필요합니다(`OCR 설정 <https://fess.codelibs.org/ko/stable/config/crawler-ocr.html>`__)

Fess가 본문을 추출할 수 없는 형식의 파일은 파일 이름이나 경로로만 찾을 수 있습니다.
대상 형식은 `검색 대상 파일 <../supported-files.html>`__\ 에서 확인하십시오.

**읽을 글**: :doc:`guide-04`\ 로 구성을 만들고, :doc:`file-server-search`\ 에서 ACL의 전제를 확인한 뒤, :doc:`guide-05`\ 로 부서별 표시 범위를 설정합니다.

금융·보험업: 규정과 계약서를 권한에 따라 찾기
---------------------------------------------

**과제**: 사내 규정, 매뉴얼, 계약서가 대량으로 있어 문의나 감사가 있을 때마다 찾는 수고가 든다. 한편으로 열람할 수 있는 사람을 부서별로 엄격하게 나누고 싶다.

**사용하는 기능**:

- 문서별 권한으로 검색 결과에 표시할 대상을 한정합니다. 새 크롤링 설정의 권한에는 처음부터 ``{role}guest``\ 가 들어 있으므로, 공개하지 않는 문서에서는 지웁니다
- 로그인하지 않은 사용자가 검색하지 못하게 하려면 [일반]의 "로그인 필요"를 활성화합니다
- 사내 ID 기반으로 로그인하려면 SSO를 사용합니다. SAML이라면 ``fess-sso-saml``, Entra ID라면 ``fess-sso-entraid``\ 입니다(Docker 이미지에는 4개의 SSO 플러그인이 포함되어 있습니다)
- 업무 시스템에서 검색하는 경우에는 액세스 토큰을 서버 측에 두고 검색 API를 호출합니다

**읽을 글**: :doc:`guide-05`\ 에서 권한을 설계하고, :doc:`guide-15`\ 에서 SSO와 HTTPS를 설정합니다. 업무 시스템과의 연계는 :doc:`guide-11`\ 입니다.

교육 기관: 학내 사이트와 공유 드라이브를 가로질러 검색하기
----------------------------------------------------------

**과제**: 학부별 웹 사이트, 강의 자료, 학내 문서가 서로 다른 곳에 있어, 학생도 교직원도 원하는 정보에 도달하지 못한다.

**사용하는 기능**:

- 학내 웹 사이트를 웹 크롤링으로 수집합니다. 기관 리포지터리(DSpace 등)는 전용 커넥터가 없으므로 공개 페이지를 웹 크롤링합니다
- Google Drive의 공유 드라이브는 ``fess-ds-gsuite``, SharePoint Online은 ``fess-ds-microsoft365``\ 로 수집합니다
- 학생용과 교직원용으로 보이는 범위를 나누려면 역할과 권한으로 구분합니다. 사이트 자체를 나누려면 가상 호스트를 사용합니다

**읽을 글**: :doc:`guide-04`, :doc:`guide-07`, :doc:`guide-05`. 사이트를 나누는 경우는 :doc:`guide-13`\ 입니다.

IT·소프트웨어업: 개발 정보를 한곳에서 찾기
------------------------------------------

**과제**: 코드는 Git, 설계는 Confluence, 이슈는 Jira, 논의는 Slack이나 Teams에 나뉘어 있어 과거의 경위를 찾기 어렵다.

**사용하는 기능**:

- ``fess-ds-git``\ 으로 리포지터리의 파일을, ``fess-ds-atlassian``\ 으로 Confluence와 Jira를, ``fess-ds-slack``\ 으로 Slack 메시지를 수집합니다
- Teams의 채널과 채팅은 ``fess-ds-microsoft365``\ 의 ``TeamsDataStore``\ 로 수집할 수 있습니다(`Microsoft 365 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-microsoft365.html>`__)
- 소스 코드 검색에 특화된 구성으로 `docker-codesearch <https://github.com/codelibs/docker-codesearch>`__\ 가 공개되어 있습니다
- 사내 도구에 검색을 넣으려면 검색 API를, AI 에이전트가 검색하게 하려면 ``fess-webapp-mcp``\ 를 사용합니다

**읽을 글**: :doc:`datastore-basics` 다음에 :doc:`guide-06`. AI 에이전트와의 연계는 :doc:`guide-20`\ 입니다.

규모별 유스케이스
=================

필요한 서버 대수나 메모리는 사용자 수나 문서 수만으로 정해지지 않습니다.
본문의 길이, 첨부 파일의 비율, 로그인해서 사용하는지 여부에 따라 부하가 달라지므로, 먼저 작게 실행해서 측정하고 부족한 것을 늘립니다.
판단 절차는 :doc:`guide-14`\ 의 규모 기준에 관한 절에 정리되어 있습니다.
운영 환경 서버의 권장 요건(CPU 4코어 이상, 메모리 8GB 이상 등)은 `시스템 요구사항 <https://fess.codelibs.org/ko/stable/install/prerequisites.html>`__\ 을 참조하십시오.

1대로 시작하기
--------------

부서 단위 도입이나 시험 운영에서는 Fess와 OpenSearch를 서버 1대에서 실행합니다.
Docker Compose를 사용하는 경우 ``compose.yaml``\ 과 ``compose-opensearch3.yaml`` 두 파일로 기동합니다.
절차는 :doc:`guide-02`\ 에 있습니다.

1대 구성이라도 다음 두 가지는 처음부터 정해 둡니다.

- 백업 방법. 설정은 [시스템 정보] > [백업]에서 받을 수 있지만, 사전은 포함되지 않습니다(:doc:`guide-10`)
- Docker의 경우 [시스템] > [일반]에서 바꾼 설정은 컨테이너 안의 ``system.properties``\ 에 저장되며, 컨테이너를 다시 만들면 원래대로 돌아갑니다(:doc:`guide-02`\ 의 정지와 재시작에 관한 절)

사용 부서가 늘어나면
--------------------

검색이나 크롤링이 느려지면, 먼저 원인이 Fess 본체인지, 크롤러인지, OpenSearch인지 확인합니다.
대부분의 경우 다음 순서로 확장합니다.

1. 1대 그대로 Fess·크롤러·OpenSearch의 힙과 크롤링 병렬도를 조정한다
2. OpenSearch를 별도 서버로 분리한다
3. OpenSearch를 3대 클러스터로 만든다
4. Fess를 여러 대로 늘리고 로드 밸런서로 분배한다

Fess를 여러 대로 운영하는 경우 [일반]의 설정, ``fess_config.properties``\ 의 ``app.cipher.key``, 설치한 플러그인을 모든 서버에서 맞춥니다.
Fess 15.9의 로그인 세션은 각 서버의 메모리에 저장되므로, 로그인해서 사용하는 화면을 분배할 때는 로드 밸런서에서 스티키 세션을 활성화합니다.
세션을 OpenSearch에 저장해 서버 간에 공유하는 기능은 15.10 이후에 사용할 수 있습니다.

**읽을 글**: :doc:`guide-14`, :doc:`guide-10`.

전사적으로 사용하기
-------------------

전사 규모에서는 위 구성에 더해 다음을 검토합니다.

- 크롤링을 담당하는 Fess를 1대로 정합니다(``scheduler.target.name``\ 과 작업의 "대상"). 검색을 받는 서버에 크롤링 부하를 주지 않기 위해서입니다
- ``/api/v2/health``\ 를 로드 밸런서와 모니터링에 사용합니다. OpenSearch 클러스터가 ``RED``\ 인 경우나 연결할 수 없는 경우에는 503을 반환합니다
- 조직별로 검색 화면이나 대상을 나누려면 가상 호스트를 사용하거나 Fess 인스턴스를 나눕니다(:doc:`guide-13`)
- 검색 로그에서 결과가 0건인 단어나 클릭되지 않는 단어를 정기적으로 확인합니다(:doc:`guide-08`)

Kubernetes에서 실행할 수도 있지만, 공식 Helm 차트는 제공되지 않습니다.
Docker Compose 파일을 변환하거나 매니페스트를 직접 만듭니다(`Docker 설치 (상세) <https://fess.codelibs.org/ko/stable/install/install-docker.html>`__\ 의 FAQ).

대규모 환경에 도입할 때는 `상용 지원 <../support-services.html>`__ 이용도 검토하십시오.

기술적 유스케이스
=================

사내 Wiki·지식 베이스 통합 검색
-------------------------------

Wiki의 종류에 따라 수집 방법이 달라집니다.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 대상
     - 수집 방법
     - 참고
   * - Confluence
     - ``fess-ds-atlassian``\ (``ConfluenceDataStore``)
     - :doc:`guide-06`
   * - Notion
     - ``fess-ds-notion``
     - `Notion 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-notion.html>`__
   * - Backlog
     - ``fess-ds-backlog``
     - `Backlog 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-backlog.html>`__
   * - MediaWiki 등 웹에서 열람할 수 있는 Wiki
     - 웹 크롤링(로그인이 필요하면 웹 인증도 설정)
     - :doc:`guide-04`

데이터 저장소로 수집한 문서에도 권한에 ``{role}guest``\ 가 처음부터 들어 있습니다.
한정된 사람만 읽을 수 있는 스페이스를 수집하는 경우에는 :doc:`guide-06`\ 에서 검색 결과를 누구에게 보여 줄지 정하는 절을 먼저 읽으십시오.

파일 서버 통합 검색
-------------------

Fess 15.9의 파일 크롤링이 다루는 프로토콜은 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 경로 형식
     - 대상
   * - ``smb://``
     - Windows 공유 폴더나 SMB로 공유하는 NAS
   * - ``smb1://``
     - SMB1만 지원하는 오래된 서버
   * - ``file:``
     - Fess 서버에서 보이는 디렉터리. NFS 공유는 OS에서 마운트한 다음 이 형식으로 지정합니다
   * - ``ftp://``
     - FTP 서버
   * - ``s3://`` / ``gcs://``
     - Amazon S3 호환 스토리지 / Google Cloud Storage. ``fess-storage-s3`` / ``fess-storage-gcs``\ 가 필요합니다(Docker 이미지에는 포함)

기본적으로 활성화된 것은 ``file``, ``smb``, ``smb1``, ``ftp``\ 입니다(``crawler.file.protocols``).
SMB의 ACL을 검색 결과에 반영하려면 크롤링 설정의 권한에서 ``{role}guest``\ 를 지워야 합니다.
이유와 확인 방법은 :doc:`file-server-search`\ 에, 구체적인 설정은 :doc:`guide-04`\ 에 있습니다.

웹 사이트 내 검색
-----------------

공개 사이트에 검색 기능을 붙이는 방법은 3가지이며, 조합해서 사용할 수 있습니다.

- 검색 폼을 두고 Fess의 검색 화면으로 이동시킵니다. Fess 측의 추가 설정은 필요 없습니다
- Fess Site Search(FSS)로 기존 페이지 안에 검색 결과를 표시합니다. FSS는 ``/api/v1``\ 을 호출하므로 15.9에서는 플러그인 ``fess-webapp-v1-api``\ 가 필요합니다. FSS의 JavaScript는 Fess에서 제공되지 않으므로, FSS JS Generator로 생성해 자신의 사이트에 둡니다
- Fess의 검색 화면을 테마로 기존 사이트의 디자인에 맞춥니다

절차는 :doc:`guide-03`\ 에 있습니다.
독자적인 검색 화면을 만드는 경우에는 ``/api/v2/search``\ 를 사용합니다(:doc:`guide-11`).

데이터베이스 검색
-----------------

제품 마스터나 FAQ처럼 데이터베이스에 들어 있는 정보는 ``fess-ds-db``\ 로 수집합니다.
JDBC를 지원하는 데이터베이스(MySQL, PostgreSQL, Oracle, SQL Server 등)가 대상이며, 접속 대상에 맞는 JDBC 드라이버를 따로 준비합니다.
SELECT 문으로 가져온 열을 스크립트로 ``title``\ 이나 ``content`` 등의 필드에 대응시킵니다.

검색 결과의 링크는 원래 업무 화면의 URL을 조립해 ``url``\ 에 넣어 두면, 사용자가 원래 데이터를 바로 열 수 있습니다.
절차는 :doc:`guide-12`\ 에 있습니다.

생성형 AI와 조합하기
--------------------

- 키워드가 일치하지 않아도 의미가 가까운 문서 찾기: 시맨틱 검색(:doc:`guide-18`)
- 사내 문서를 근거로 AI가 답하게 하기: AI 검색 모드. 벡터 검색이 없어도 사용할 수 있습니다(:doc:`guide-19`)
- Claude Code 등의 AI 에이전트가 Fess를 검색하게 하기: ``fess-webapp-mcp``\ (:doc:`guide-20`)

어떤 방법이든 검색되는 문서는 일반 검색과 같은 권한으로 걸러집니다(AI 검색 모드는 로그인한 사용자, MCP는 액세스 토큰의 권한. MCP에서 인증을 사용하지 않는 경우는 게스트 권한).
AI에 전달되는 문서도 이 권한으로 정해지므로, 먼저 :doc:`guide-05`\ 의 권한 설계를 마쳐 둡니다.

도입 진행 방법
==============

1. :doc:`guide-02`\ 로 Fess를 기동하고, 대상의 일부를 크롤링해 검색을 시험한다
2. 위의 표에서 자신의 과제에 맞는 글을 골라 설정한다
3. 권한(:doc:`guide-05`)과 운영(:doc:`guide-10`)을 정한 뒤 사용자에게 공개한다

참고 자료
=========

- `빠른 시작 <../quick-start.html>`__
- `문서 <../documentation.html>`__
- `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__
- `데이터 저장소 커넥터 가이드 <https://fess.codelibs.org/ko/stable/config/datastore/index.html>`__
- `토론 포럼 <https://discuss.codelibs.org/c/FessEN/>`__
- `GitHub <https://github.com/codelibs/fess>`__
