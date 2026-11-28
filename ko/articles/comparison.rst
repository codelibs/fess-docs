============================
Fess와 다른 검색 솔루션 비교
============================

들어가며
========

사내 문서나 사이트 내 검색을 마련할 때, 후보로는 Fess 같은 검색 시스템 외에도 OpenSearch나 Apache Solr 등의 검색 엔진을 이용한 자체 개발, 외부 웹 검색 서비스, 상용 엔터프라이즈 검색 제품이 있습니다.
이 글에서는 먼저 Fess 15.9가 제공하는 것을 확인하기 쉬운 형태로 정리한 다음, 다른 선택지와의 역할 차이를 비교합니다.

.. note::

   Fess에 관한 내용은 15.9 시점 기준입니다.
   다른 제품이나 서비스에 대해서는 잘 바뀌지 않는 구성상의 차이만 다룹니다. 기능, 요금, 제공 상황은 바뀔 수 있으므로 각 제품의 최신 자료에서 확인하십시오.

Fess가 제공하는 것
==================

Fess는 OpenSearch를 검색 엔진으로 사용하는 검색 시스템입니다.
크롤러, 관리 화면, 검색 화면, API를 하나의 애플리케이션으로 제공하며, 인덱스와 크롤링 설정은 OpenSearch에 저장합니다.
Elasticsearch나 Solr를 검색 엔진으로 사용할 수는 없습니다.
라이선스는 Apache License 2.0입니다.

기능의 대부분은 플러그인으로 제공되며, 필요한 것만 설치합니다.
다음 표에서 "필요한 것"이 비어 있는 항목은 Fess 본체만으로 사용할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - 항목
     - 15.9에서 제공되는 것
     - 필요한 것
   * - 웹 크롤링
     - HTTP/HTTPS 사이트를 크롤링합니다. 웹 인증, 요청 헤더, 경로 매핑을 설정할 수 있습니다
     -
   * - 파일 크롤링
     - ``file``, ``smb``, ``smb1``, ``ftp`` 경로를 크롤링합니다
     -
   * - 클라우드 스토리지 크롤링
     - ``s3://``\ (Amazon S3 및 S3 호환 스토리지), ``gcs://``\ (Google Cloud Storage)
     - ``fess-storage-s3``, ``fess-storage-gcs``
   * - 데이터베이스나 SaaS
     - 데이터스토어 커넥터로 가져옵니다(목록은 다음 절)
     - ``fess-ds-*`` 플러그인
   * - 문서 형식
     - Office 문서, PDF, HTML, 텍스트, 압축 파일 등. 이미지나 스캔한 PDF의 OCR은 기본적으로 비활성화되어 있습니다
     - OCR에는 ``tesseract`` 명령
   * - 접근 제어
     - 역할·그룹·사용자 단위로 검색 결과를 다르게 보여 줍니다. SMB와 파일 크롤링에서는 파일의 접근 권한을 역할로 가져옵니다. LDAP(Active Directory 포함)와의 연동은 본체 기능입니다
     -
   * - 싱글 사인온
     - OpenID Connect, SAML, SPNEGO(Kerberos), Microsoft Entra ID
     - ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``
   * - 검색 화면
     - 정적 테마(HTML·CSS·JavaScript를 ZIP으로 묶은 것)로 표시합니다. 동봉된 테마는 ``bootstrap``\ 입니다
     -
   * - API
     - 검색, 라벨, 추천어, 인기 검색어, 헬스 체크, AI 검색 모드 등의 ``/api/v2``, 관리용 ``/api/admin``
     -
   * - 구 형식 API
     - ``/api/v1``, ``/json``\ ·\ ``/suggest``
     - ``fess-webapp-v1-api``, ``fess-webapp-classic-api``
   * - 시맨틱 검색
     - 본문을 청크로 나누어 벡터화하고, 키워드 검색 결과와 Rank Fusion으로 통합합니다. 기본적으로 비활성화되어 있습니다
     - 임베딩 모델(OpenSearch의 ML Commons 또는 ``fess-llm-*`` 플러그인)
   * - AI 검색 모드(RAG)
     - 검색 결과를 근거로 LLM이 답변합니다. 기본적으로 비활성화되어 있습니다
     - ``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock`` 중 하나
   * - MCP 서버
     - AI 에이전트가 ``/mcp``\ 로 Fess를 검색할 수 있게 합니다
     - ``fess-webapp-mcp``
   * - 이미지 검색
     - 문장으로 이미지(GIF·JPEG·PNG)를 찾는 멀티모달 검색입니다
     - ``fess-webapp-multimodal``\ 과 CLIP 서버

Docker 이미지에는 SSO 플러그인 4종, ``fess-storage-s3``, ``fess-storage-gcs``, ``fess-script-groovy``\ 가 동봉되어 있습니다.
그 밖의 플러그인은 [시스템] > [플러그인]에서 설치하고 Fess를 재시작합니다.
플러그인 버전은 Fess와 같은 마이너 버전(15.9라면 15.9.x)을 선택합니다.

데이터스토어 커넥터
-------------------

15.9용으로는 다음 데이터스토어 플러그인이 공개되어 있습니다.
설정 방법은 각 커넥터의 레퍼런스에 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 분류
     - 플러그인(대상)
   * - 클라우드 스토리지
     - ``fess-ds-box``\ (Box), ``fess-ds-dropbox``\ (Dropbox), ``fess-ds-gsuite``\ (Google 드라이브), ``fess-ds-microsoft365``\ (OneDrive, SharePoint Online, Teams 등)
   * - 협업
     - ``fess-ds-atlassian``\ (Confluence, Jira), ``fess-ds-slack``\ (Slack), ``fess-ds-notion``\ (Notion), ``fess-ds-backlog``\ (Backlog), ``fess-ds-sharepoint``\ (온프레미스 SharePoint Server)
   * - 개발·업무 시스템
     - ``fess-ds-git``\ (Git 저장소), ``fess-ds-salesforce``\ (Salesforce)
   * - 데이터
     - ``fess-ds-db``\ (JDBC로 접속할 수 있는 데이터베이스), ``fess-ds-csv``\ (CSV), ``fess-ds-json``\ (JSON), ``fess-ds-wikipedia``\ (Wikipedia 덤프)

여기에 없는 데이터 소스는 데이터스토어 플러그인을 직접 만들거나(:doc:`guide-17`), 관리용 API로 문서를 등록하여(:doc:`guide-11`) 검색 대상으로 만들 수 있습니다.

검색 엔진(OpenSearch·Apache Solr)을 이용한 자체 개발과의 차이
=============================================================

OpenSearch와 Apache Solr는 검색 엔진입니다.
인덱스 생성과 검색을 담당하지만, 데이터를 수집하는 크롤러나 이용자가 사용하는 검색 화면, 문서별 접근 제어는 포함하지 않습니다.
이러한 부분은 직접 개발하거나 다른 소프트웨어를 조합합니다.
예를 들어 웹 크롤링에는 Apache Nutch 같은 별도의 프로젝트가 있습니다.

Fess는 OpenSearch 위에 이러한 부분을 갖춘 애플리케이션입니다.
차이는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - 관점
     - Fess
     - 검색 엔진을 이용한 자체 개발
   * - 데이터 수집
     - 웹·파일·데이터스토어 크롤링을 관리 화면에서 설정합니다
     - 크롤러나 가져오기 처리를 만들거나, 다른 소프트웨어를 조합합니다
   * - 검색 화면
     - 테마로 표시합니다. 모양을 바꾸려면 테마를 만들거나, API를 사용해 독자적인 화면을 만듭니다
     - 자유롭게 만들 수 있지만, 모두 개발해야 합니다
   * - 접근 제어
     - 역할과 파일의 접근 권한을 문서에 기록하고, 검색 시 로그인 사용자로 필터링합니다
     - 문서 권한의 가져오기와 검색 시 필터링을 설계하고 구현합니다
   * - 인덱스 설계
     - Fess가 정의한 인덱스를 사용합니다. 한국어를 포함한 다국어 분석기가 설정되어 있습니다
     - 용도에 맞게 자유롭게 설계할 수 있습니다
   * - 운영하는 것
     - Fess와 OpenSearch
     - 검색 엔진과 자체 개발한 부분 전체

검색 구조를 처음부터 설계하고 싶거나 독자적인 데이터 구조를 검색하고 싶다면 검색 엔진을 직접 사용하는 편이 적합합니다.
반면 문서를 모아 사내에서 검색할 수 있게 하는 것이 목적이라면, Fess로 시작하고 부족한 부분을 API나 플러그인으로 보완하는 편이 개발 범위를 줄일 수 있습니다.

Fess를 기존 OpenSearch 클러스터에 연결할 수도 있습니다.
CodeLibs 플러그인을 설치할 수 없는 Amazon OpenSearch Service 등에서는 ``search_engine.type``\ 에 ``aws`` 또는 ``vanilla``\ 를 지정합니다.
이 경우 사전 관리나 중복 문서 검출 등 일부 기능은 사용할 수 없습니다(`검색 엔진 종류 <https://fess.codelibs.org/ko/stable/config/search-engine-type.html>`__ 참조).

외부 웹 검색 서비스를 이용한 사이트 내 검색과의 차이
====================================================

검색 서비스 사업자의 인덱스를 이용해 사이트 내 검색을 제공하는 방법도 있습니다.
이 방법에서는 검색할 수 있는 것이 사업자의 크롤러가 가져온 공개 페이지로 한정됩니다.
로그인이 필요한 페이지나 사내 파일 서버는 대상으로 할 수 없으며, 언제 크롤링되는지, 어떤 순서로 표시되는지도 사업자에 따라 달라집니다.

Fess에서는 크롤링 대상과 시기를 직접 정하고, 인덱스를 자사 환경에 둡니다.
검색 결과 조정에는 키 매치(특정 단어로 특정 문서를 상위에 표시), 문서 부스트, 관련 쿼리 등을 사용할 수 있습니다.
기존 사이트에 넣는 방법은 두 가지입니다.

- 검색 폼을 두고 Fess의 검색 화면(테마)으로 이동시킨다
- Fess Site Search(FSS)의 JavaScript를 삽입하여 페이지 안에 검색 결과를 표시한다

FSS는 ``/api/v1``\ 을 호출하므로 15.9에서는 ``fess-webapp-v1-api`` 플러그인이 필요합니다.
절차는 :doc:`guide-03`\ 을 참조하십시오.

상용 엔터프라이즈 검색 제품과의 차이
====================================

상용 제품과 비교할 경우, 제품마다 지원 범위가 크게 다르므로 일반론으로 우열을 정할 수는 없습니다.
다음 관점에서 후보 제품과 Fess를 같은 조건으로 확인할 것을 권장합니다.

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 관점
     - Fess의 경우
   * - 대상 데이터 소스
     - 앞 절의 표와 데이터스토어 커넥터 목록에서 확인합니다. 부족한 경우 플러그인을 직접 만들 수 있습니다
   * - 접근 제어
     - 역할·그룹·사용자 단위로, LDAP와 SSO 4가지 방식에 대응합니다
   * - 생성형 AI
     - AI 검색 모드(RAG), 시맨틱 검색, MCP 서버. LLM은 Ollama(자체 운영), OpenAI, Gemini, Amazon Bedrock 중에서 선택합니다
   * - 데이터 보관 위치
     - 인덱스는 자체 운영하는 OpenSearch에 둡니다. LLM이나 임베딩에 외부 서비스를 사용하는 경우 질문이나 문서 본문이 해당 서비스로 전송됩니다
   * - 운영 형태
     - 자체 운영하는 소프트웨어입니다. Docker, Linux(ZIP·RPM·DEB), Windows에 설치할 수 있습니다. Kubernetes에서도 실행할 수 있지만 공식 Helm 차트는 없습니다
   * - 비용과 지원
     - 라이선스 비용은 들지 않습니다. 비용은 서버와 운영 공수입니다. 상용 지원은 `상용 지원 <https://fess.codelibs.org/ko/support-services.html>`__\ 에서 안내하고 있습니다
   * - 변경의 자유도
     - 소스 코드가 공개되어 있으며, 테마, 플러그인, API로 확장할 수 있습니다

상용 제품이 적합한 것은 필요한 커넥터나 관리 기능이 제품에 갖추어져 있고 운영을 벤더에 맡기고 싶은 경우입니다.
Fess가 적합한 것은 자사 환경에 데이터를 둔 채 필요한 기능을 조합하여 검색 기반을 만들고 싶은 경우입니다.

선택 기준
=========

다음 질문에 차례로 답하면 Fess가 후보가 되는지 판단할 수 있습니다.

1. 검색하려는 데이터가 Fess의 크롤링 대상이나 데이터스토어 커넥터에 포함되어 있습니까?

   - 포함되어 있지 않다면 플러그인 자체 개발(:doc:`guide-17`)이나 API를 통한 등록(:doc:`guide-11`)에 필요한 개발량을 산정합니다.

2. 이용자마다 보여 줄 문서를 달리해야 합니까?

   - 파일 서버의 접근 권한을 사용한다면 :doc:`file-server-search`, 역할 설계는 :doc:`guide-05`, SSO는 :doc:`guide-15`\ 를 확인합니다.

3. 검색 화면은 Fess의 테마로 충분합니까?

   - 자사 애플리케이션에 검색을 넣는 경우에는 ``/api/v2``\ 를 사용합니다(:doc:`guide-11`).

4. Fess와 OpenSearch를 자체적으로 운영할 수 있습니까?

   - 운영할 수 없거나 운영을 벤더에 맡기고 싶다면 Fess의 상용 지원이나 상용 제품을 검토합니다.

5. 생성형 AI를 이용한 답변이나 의미 검색이 필요합니까?

   - 사용할 LLM을 정하고, :doc:`guide-19`\ 와 :doc:`guide-18`\ 에서 필요한 구성을 확인합니다.

1과 4의 답이 "예"라면 먼저 Fess를 사용해 보고 실제 문서로 검색 결과를 확인하는 것이 확실합니다.

직접 사용해 보고 확인하기
=========================

비교표만으로는 자사 문서를 어떻게 검색할 수 있는지 알 수 없습니다.
:doc:`guide-02`\ 의 절차로 Fess를 Docker로 기동하고, 검색하려는 대상의 일부를 크롤링한 다음 다음 사항을 확인합니다.

- 대상 문서가 수집되었는지([시스템 정보] > [작업 로그]와 [장애 URL]에서 오류가 난 URL이 없는지 확인합니다)
- 자주 쓰는 단어로 검색했을 때 기대하는 문서가 상위에 나오는지
- 로그인 사용자를 바꿨을 때 보이면 안 되는 문서가 표시되지 않는지(접근 제어가 필요한 경우)

다음에 읽을 글
==============

- Fess의 구성과 글 전체를 읽어 나가는 방법을 알고 싶다: :doc:`guide-01`
- 우선 직접 실행해 보고 싶다: :doc:`guide-02`
- 기존 사이트에 검색을 넣고 싶다: :doc:`guide-03`
- 데이터베이스나 SaaS의 데이터를 검색하고 싶다: :doc:`datastore-basics`
- 파일 서버의 접근 권한을 검색 결과에 반영하고 싶다: :doc:`file-server-search`
- 생성형 AI가 사내 문서를 바탕으로 답변하게 하고 싶다: :doc:`guide-19`
- 규모 확대에 대비하고 싶다: :doc:`guide-14`
- 활용 사례를 알고 싶다: :doc:`use-cases`

참고 자료
=========

- `데이터스토어 커넥터 개요 <https://fess.codelibs.org/ko/stable/config/datastore/ds-overview.html>`__
- `파일 크롤링(파일 서버 검색) <https://fess.codelibs.org/ko/stable/admin/fileconfig-guide.html>`__
- `검색 대상 파일 <https://fess.codelibs.org/ko/supported-files.html>`__
- `OCR 설정 <https://fess.codelibs.org/ko/stable/config/crawler-ocr.html>`__
- `테마 <https://fess.codelibs.org/ko/stable/admin/theme-guide.html>`__
- `API 개요 <https://fess.codelibs.org/ko/stable/api/api-overview.html>`__
- `시맨틱 검색 <https://fess.codelibs.org/ko/stable/config/search-semantic.html>`__
- `AI 검색(RAG) 및 LLM 통합 개요 <https://fess.codelibs.org/ko/stable/config/llm-overview.html>`__
- `검색 엔진 종류 <https://fess.codelibs.org/ko/stable/config/search-engine-type.html>`__
- `플러그인 <https://fess.codelibs.org/ko/stable/admin/plugin-guide.html>`__
