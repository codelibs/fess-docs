==================================
데이터스토어 커넥터 개요
==================================

개요
====

|Fess| 의 데이터스토어 커넥터는 웹사이트나 파일 시스템 이외의 데이터 소스에서
콘텐츠를 가져와 인덱싱하는 기능을 제공합니다.

데이터스토어 커넥터를 사용하여 다음과 같은 소스에서 데이터를 검색 가능하게 만들 수 있습니다:

- 클라우드 스토리지 (Box, Dropbox, Google Drive, OneDrive)
- 협업 도구 (Confluence, Jira, Slack)
- 데이터베이스 (MySQL, PostgreSQL, Oracle 등)
- 기타 시스템 (Git, Salesforce, Elasticsearch 등)

사용 가능한 커넥터
==================

|Fess| 는 다양한 데이터 소스에 대응하는 커넥터를 제공합니다.
많은 커넥터는 플러그인으로 제공되며, 필요에 따라 설치할 수 있습니다.

클라우드 스토리지
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 커넥터
     - 플러그인
     - 설명
   * - :doc:`ds-box`
     - fess-ds-box
     - Box.com의 파일 및 폴더를 크롤링
   * - :doc:`ds-dropbox`
     - fess-ds-dropbox
     - Dropbox의 파일 및 폴더를 크롤링
   * - :doc:`ds-gsuite`
     - fess-ds-gsuite
     - Google Drive, Gmail 등을 크롤링
   * - :doc:`ds-microsoft365`
     - fess-ds-office365
     - OneDrive, SharePoint 등을 크롤링

협업 도구
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 커넥터
     - 플러그인
     - 설명
   * - :doc:`ds-atlassian`
     - fess-ds-atlassian
     - Confluence, Jira를 크롤링
   * - :doc:`ds-slack`
     - fess-ds-slack
     - Slack의 메시지 및 파일을 크롤링

개발·운영 도구
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 커넥터
     - 플러그인
     - 설명
   * - :doc:`ds-git`
     - fess-ds-git
     - Git 리포지토리의 소스 코드를 크롤링
   * - :doc:`ds-elasticsearch`
     - fess-ds-elasticsearch
     - Elasticsearch/OpenSearch에서 데이터를 가져옴
   * - :doc:`ds-salesforce`
     - fess-ds-salesforce
     - Salesforce 오브젝트를 크롤링

데이터베이스·파일
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 커넥터
     - 플러그인
     - 설명
   * - :doc:`ds-database`
     - (내장)
     - JDBC 호환 데이터베이스에서 데이터를 가져옴
   * - :doc:`ds-csv`
     - fess-ds-csv
     - CSV 파일에서 데이터를 가져옴
   * - :doc:`ds-json`
     - fess-ds-json
     - JSON 파일에서 데이터를 가져옴

커넥터 설치
======================

플러그인 설치
------------------------

데이터스토어 커넥터 플러그인은 관리 화면 또는 `plugin` 명령으로 설치할 수 있습니다.

관리 화면에서
~~~~~~~~~~~~

1. 관리 화면에 로그인
2. "시스템" → "플러그인"으로 이동
3. "Available" 탭에서 대상 플러그인 검색
4. "설치"를 클릭
5. |Fess| 재시작

명령줄
~~~~~~~~~~~~~~

::

    # 플러그인 설치
    ./bin/fess-plugin install fess-ds-box

    # 설치된 플러그인 확인
    ./bin/fess-plugin list

Docker 환경
~~~~~~~~~~

::

    # 시작 시 플러그인 설치
    docker run -e FESS_PLUGINS="fess-ds-box,fess-ds-dropbox" codelibs/fess:15.5.0

데이터스토어 설정 기본
======================

데이터스토어 커넥터 설정은 관리 화면의 "크롤러" → "데이터스토어"에서 수행합니다.

공통 설정 항목
------------

모든 데이터스토어 커넥터에 공통되는 설정 항목:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설명
   * - 이름
     - 설정의 식별명
   * - 핸들러 이름
     - 사용할 커넥터의 핸들러 이름 (예: ``BoxDataStore``)
   * - 파라미터
     - 커넥터 고유의 설정 파라미터 (key=value 형식)
   * - 스크립트
     - 인덱스 필드 매핑 스크립트
   * - 부스트
     - 검색 결과 우선순위
   * - 사용
     - 이 설정을 활성화할지 여부

파라미터 설정
----------------

파라미터는 개행 구분의 ``key=value`` 형식으로 지정합니다:

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

스크립트 설정
--------------

스크립트에서는 가져온 데이터를 |Fess| 의 인덱스 필드에 매핑합니다:

::

    url=data.url
    title=data.name
    content=data.content
    mimetype=data.mimetype
    filetype=data.filetype
    filename=data.filename
    created=data.created
    lastModified=data.lastModified
    contentLength=data.contentLength

인증 설정
========

많은 데이터스토어 커넥터는 OAuth 2.0 또는 API 키에 의한 인증이 필요합니다.

OAuth 2.0 인증
-------------

일반적인 OAuth 2.0 설정 파라미터:

::

    client.id=클라이언트ID
    client.secret=클라이언트시크릿
    refresh.token=리프레시토큰

또는:

::

    access.token=액세스토큰

API 키 인증
-----------

::

    api.key=API키
    api.secret=API시크릿

서비스 계정 인증
----------------------

::

    service.account.email=서비스계정의이메일주소
    service.account.key=비밀키(JSON형식 또는 키 파일 경로)

성능 튜닝
==========================

대량의 데이터를 처리할 때의 설정:

::

    # 배치 크기
    batch.size=100

    # 요청 간 대기 시간 (밀리초)
    interval=1000

    # 병렬 처리 수
    thread.size=1

    # 타임아웃 (밀리초)
    timeout=30000

문제 해결
======================

커넥터가 표시되지 않음
----------------------

1. 플러그인이 올바르게 설치되었는지 확인
2. |Fess| 재시작
3. 로그에서 오류가 없는지 확인

인증 오류
----------

1. 인증 정보가 올바른지 확인
2. 토큰 유효 기간 확인
3. 필요한 권한이 부여되었는지 확인
4. 서비스 측에서 API 액세스가 허용되었는지 확인

데이터를 가져올 수 없음
--------------------

1. 파라미터 형식이 올바른지 확인
2. 대상 폴더/파일에 대한 액세스 권한 확인
3. 필터 설정 확인
4. 로그에서 자세한 오류 메시지 확인

디버그 설정
------------

문제를 조사할 때는 로그 레벨을 조정합니다:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

참고 정보
========

- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
- :doc:`../../admin/plugin-guide` - 플러그인 관리 가이드
- :doc:`../../api/admin/api-admin-dataconfig` - 데이터스토어 설정 API
