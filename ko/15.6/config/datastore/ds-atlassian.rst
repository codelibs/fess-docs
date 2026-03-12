==================================
Atlassian 커넥터
==================================

개요
====

Atlassian 커넥터는 Atlassian 제품(Jira, Confluence)에서 데이터를 가져와
|Fess| 의 인덱스에 등록하는 기능을 제공합니다.

이 기능에는 ``fess-ds-atlassian`` 플러그인이 필요합니다.

지원 제품
========

- Jira (Cloud / Server / Data Center)
- Confluence (Cloud / Server / Data Center)

전제 조건
========

1. 플러그인 설치가 필요합니다
2. Atlassian 제품에 대한 적절한 인증 정보가 필요합니다
3. Cloud 버전의 경우 OAuth 2.0, Server 버전의 경우 OAuth 1.0a 또는 Basic 인증을 사용할 수 있습니다

플러그인 설치
------------------------

관리 화면의 "시스템" → "플러그인"에서 설치합니다:

1. Maven Central에서 ``fess-ds-atlassian-X.X.X.jar`` 다운로드
2. 플러그인 관리 화면에서 업로드하여 설치
3. |Fess| 재시작

설정 방법
========

관리 화면에서 "크롤러" → "데이터스토어" → "신규 작성"으로 설정합니다.

기본 설정
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - Company Jira/Confluence
   * - 핸들러 이름
     - JiraDataStore 또는 ConfluenceDataStore
   * - 사용
     - 켜기

파라미터 설정
----------------

Cloud 버전(OAuth 2.0) 예:

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Server 버전(Basic 인증) 예:

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Server 버전(OAuth 1.0a) 예:

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=oauth
    oauth.consumer_key=OauthKey
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...=\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``home``
     - 예
     - Atlassian 인스턴스의 URL
   * - ``is_cloud``
     - 예
     - Cloud 버전인 경우 ``true``, Server 버전인 경우 ``false``
   * - ``auth_type``
     - 예
     - 인증 유형: ``oauth``, ``oauth2``, ``basic``
   * - ``oauth.consumer_key``
     - OAuth 1.0a의 경우
     - 컨슈머 키 (보통 ``OauthKey``)
   * - ``oauth.private_key``
     - OAuth 1.0a의 경우
     - RSA 비밀키 (PEM 형식)
   * - ``oauth.secret``
     - OAuth 1.0a의 경우
     - 검증 코드
   * - ``oauth.access_token``
     - OAuth 1.0a의 경우
     - 액세스 토큰
   * - ``oauth2.client_id``
     - OAuth 2.0의 경우
     - 클라이언트 ID
   * - ``oauth2.client_secret``
     - OAuth 2.0의 경우
     - 클라이언트 시크릿
   * - ``oauth2.access_token``
     - OAuth 2.0의 경우
     - 액세스 토큰
   * - ``oauth2.refresh_token``
     - 아니요
     - 리프레시 토큰 (OAuth 2.0)
   * - ``oauth2.token_url``
     - 아니요
     - 토큰 URL (OAuth 2.0, 기본값 있음)
   * - ``basic.username``
     - Basic 인증의 경우
     - 사용자명
   * - ``basic.password``
     - Basic 인증의 경우
     - 비밀번호
   * - ``issue.jql``
     - 아니요
     - JQL (Jira만, 고급 검색 조건)

스크립트 설정
--------------

Jira의 경우
~~~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\n" + issue.comments
    last_modified=issue.last_modified

사용 가능한 필드:

- ``issue.view_url`` - 이슈의 URL
- ``issue.summary`` - 이슈 요약
- ``issue.description`` - 이슈 설명
- ``issue.comments`` - 이슈 코멘트
- ``issue.last_modified`` - 최종 업데이트 일시

Confluence의 경우
~~~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n" + content.comments
    last_modified=content.last_modified

사용 가능한 필드:

- ``content.view_url`` - 페이지 URL
- ``content.title`` - 페이지 제목
- ``content.body`` - 페이지 본문
- ``content.comments`` - 페이지 코멘트
- ``content.last_modified`` - 최종 업데이트 일시

OAuth 2.0 인증 설정
===================

Cloud 버전의 경우(권장)
---------------------

1. Atlassian Developer Console에서 애플리케이션 생성
2. OAuth 2.0 인증 정보 취득
3. 필요한 스코프 설정:

   - Jira: ``read:jira-work``, ``read:jira-user``
   - Confluence: ``read:confluence-content.all``, ``read:confluence-user``

4. 액세스 토큰 및 리프레시 토큰 취득

OAuth 1.0a 인증 설정
====================

Server 버전의 경우
--------------

1. Jira 또는 Confluence에서 Application Link 생성
2. RSA 키 쌍 생성:

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. 공개키를 Application Link에 등록
4. 비밀키를 파라미터에 설정

Basic 인증 설정
===============

Server 버전의 간단한 설정
------------------------

.. warning::
   Basic 인증은 보안상 권장되지 않습니다. 가능한 한 OAuth 인증을 사용하세요.

Basic 인증을 사용할 경우:

1. 관리자 권한을 가진 사용자 계정 준비
2. 사용자명과 비밀번호를 파라미터에 설정
3. HTTPS를 사용하여 보안 연결 확보

JQL을 통한 고급 검색
===================

Jira 이슈를 JQL로 필터링
--------------------------

특정 조건에 맞는 이슈만 크롤링:

::

    # 특정 프로젝트만
    issue.jql=project = "MYPROJECT"

    # 특정 상태 제외
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # 기간 지정
    issue.jql=updated >= -30d

    # 복수 조건 조합
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

JQL 자세한 내용은 `Atlassian JQL 문서 <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_ 를 참조하세요.

사용 예
======

Jira Cloud 크롤링
--------------------

파라미터:

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=Abc123DefGhi456
    oauth2.client_secret=xyz789uvw456rst123
    oauth2.access_token=eyJhbGciOiJIUzI1...
    oauth2.refresh_token=def456ghi789jkl012
    issue.jql=project = "SUPPORT" AND status != "Closed"

스크립트:

::

    url=issue.view_url
    title="[" + issue.key + "] " + issue.summary
    content=issue.description + "\n\n코멘트:\n" + issue.comments
    last_modified=issue.last_modified

Confluence Server 크롤링
---------------------------

파라미터:

::

    home=https://wiki.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=crawler_user
    basic.password=secure_password

스크립트:

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n코멘트:\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

문제 해결
======================

인증 오류
----------

**증상**: ``401 Unauthorized`` 또는 ``403 Forbidden``

**확인 사항**:

1. 인증 정보가 올바른지 확인
2. Cloud 버전의 경우, 적절한 스코프가 설정되어 있는지 확인
3. Server 버전의 경우, 사용자에게 적절한 권한이 있는지 확인
4. OAuth 2.0의 경우, 토큰 유효 기간 확인

연결 오류
----------

**증상**: ``Connection refused`` 또는 연결 타임아웃

**확인 사항**:

1. ``home`` URL이 올바른지 확인
2. 방화벽 설정 확인
3. Atlassian 인스턴스가 가동 중인지 확인
4. ``is_cloud`` 파라미터가 올바르게 설정되어 있는지 확인

데이터를 가져올 수 없음
--------------------

**증상**: 크롤링은 성공하지만 문서가 0건

**확인 사항**:

1. JQL로 너무 많이 필터링하지 않았는지 확인
2. 사용자에게 읽기 권한이 있는 프로젝트/스페이스인지 확인
3. 스크립트 설정이 올바른지 확인
4. 로그에서 오류가 발생하지 않았는지 확인

OAuth 2.0 토큰 갱신
-----------------------

**증상**: 얼마 후 인증 오류 발생

**해결 방법**:

OAuth 2.0의 액세스 토큰은 유효 기간이 있습니다. 리프레시 토큰을 설정하면 자동 갱신이 가능합니다:

::

    oauth2.refresh_token=your_refresh_token

참고 정보
========

- :doc:`ds-overview` - 데이터스토어 커넥터 개요
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
- `Atlassian Developer <https://developer.atlassian.com/>`_
