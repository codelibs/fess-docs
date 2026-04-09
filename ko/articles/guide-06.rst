============================================================
제6회 개발팀의 지식 허브 -- 코드·Wiki·티켓의 통합 검색 환경
============================================================

들어가며
========

소프트웨어 개발팀에서는 일상 업무에서 다양한 도구를 사용합니다.
코드는 Git 리포지토리에, 사양서는 Confluence에, 태스크는 Jira에, 일상적인 커뮤니케이션은 Slack에.
각 도구에는 검색 기능이 있지만, "그 논의는 어디서 했더라?"라는 질문에 대해 모든 도구를 개별적으로 검색하는 것은 비효율적입니다.

본 기사에서는 개발팀이 일상적으로 사용하는 도구의 정보를 Fess에 집약하여 통합 검색이 가능한 지식 허브를 구축합니다.

대상 독자
========

- 소프트웨어 개발팀의 리더나 인프라 담당자
- 개발 관련 도구의 정보를 횡단 검색하고 싶은 분
- 데이터스토어 플러그인의 기본적인 사용법을 알고 싶은 분

시나리오
========

개발팀(20명)의 정보를 통합 검색할 수 있도록 합니다.

.. list-table:: 대상 데이터 소스
   :header-rows: 1
   :widths: 20 30 50

   * - 도구
     - 용도
     - 검색하고 싶은 정보
   * - Git 리포지토리
     - 소스 코드 관리
     - 코드, README, 설정 파일
   * - Confluence
     - 문서 관리
     - 설계서, 회의록, 절차서
   * - Jira
     - 티켓 관리
     - 버그 보고, 태스크, 스토리
   * - Slack
     - 커뮤니케이션
     - 기술적인 논의, 의사결정 기록

데이터스토어 크롤이란
========================

웹 크롤이나 파일 크롤은 URL이나 파일 경로를 따라 문서를 수집합니다.
반면 SaaS 도구의 정보를 수집하려면 "데이터스토어 크롤"을 사용합니다.

데이터스토어 크롤은 각 도구의 API를 통해 데이터를 가져와 Fess의 인덱스에 등록합니다.
Fess에서는 도구별로 데이터스토어 플러그인이 제공됩니다.

플러그인 설치
========================

데이터스토어 플러그인은 Fess의 관리 화면에서 설치할 수 있습니다.

1. 관리 화면의 [시스템] > [플러그인]을 선택
2. 설치된 플러그인 목록을 확인
3. [설치] 버튼에서 설치 화면으로 이동하여 [리모트] 탭에서 필요한 플러그인을 설치

이번 시나리오에서는 다음 플러그인을 사용합니다.

- ``fess-ds-git``: Git 리포지토리 크롤
- ``fess-ds-atlassian``: Confluence / Jira 크롤
- ``fess-ds-slack``: Slack 메시지 크롤

각 데이터 소스의 설정
====================

Git 리포지토리 설정
---------------------

Git 리포지토리를 크롤하여 코드나 문서를 검색 대상으로 합니다.

1. [크롤러] > [데이터스토어] > [새로 만들기]
2. 핸들러명: GitDataStore를 선택
3. 파라미터 설정

**파라미터 설정 예**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**스크립트 설정 예**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

``uri`` 에 리포지토리 URL을, ``username`` / ``password`` 에 인증 정보를 지정합니다. 프라이빗 리포지토리의 경우 액세스 토큰을 ``password`` 에 설정합니다. ``include_pattern`` 으로 크롤 대상 파일 확장자를 정규 표현식으로 필터링할 수 있습니다.

Confluence 설정
------------------

Confluence의 페이지나 블로그 기사를 검색 대상으로 합니다.

1. [크롤러] > [데이터스토어] > [새로 만들기]
2. 핸들러명: ConfluenceDataStore를 선택
3. 파라미터 설정

**파라미터 설정 예**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**스크립트 설정 예**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

``home`` 에 Confluence URL을 지정하고 ``auth_type`` 으로 인증 방식을 선택합니다. Confluence Cloud의 경우 ``basic`` 인증으로, ``basic.password`` 에 API 토큰을 설정합니다.

Jira 설정
------------

Jira의 티켓(Issue)을 검색 대상으로 합니다.

같은 ``fess-ds-atlassian`` 플러그인에 포함된 JiraDataStore 핸들러를 사용합니다.
JQL(Jira Query Language)을 사용하여 크롤 대상 티켓을 필터링할 수도 있습니다.
예를 들어 특정 프로젝트의 티켓만 대상으로 하거나 특정 상태(Closed 이외)의 티켓만 대상으로 할 수 있습니다.

1. [크롤러] > [데이터스토어] > [새로 만들기]
2. 핸들러명: JiraDataStore를 선택
3. 파라미터 설정

**파라미터 설정 예**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**스크립트 설정 예**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

``issue.jql`` 에 JQL 쿼리를 지정하여 크롤 대상 티켓을 필터링합니다.

Slack 설정
-------------

Slack의 메시지를 검색 대상으로 합니다.

1. [크롤러] > [데이터스토어] > [새로 만들기]
2. 핸들러명: SlackDataStore를 선택
3. 파라미터 설정

**파라미터 설정 예**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**스크립트 설정 예**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

``token`` 에 Slack Bot의 OAuth 토큰을 지정합니다. ``channels`` 로 크롤 대상 채널을 지정할 수 있으며, 모든 채널을 대상으로 하려면 ``*all`` 을 설정합니다. 프라이빗 채널을 대상으로 하려면 ``include_private=true`` 를 설정하고 Bot을 해당 채널에 초대해 두어야 합니다.

라벨 활용
============

라벨로 정보 출처를 구분하기
------------------------

각 데이터 소스에 라벨을 설정하여 검색 시 정보 출처를 전환할 수 있도록 합니다.

- ``code``: Git 리포지토리의 코드
- ``docs``: Confluence 문서
- ``tickets``: Jira 티켓
- ``discussions``: Slack 메시지

이용자는 "전체"로 횡단 검색하고 필요에 따라 라벨로 필터링할 수 있습니다.

검색 품질 향상
===============

문서 부스트 활용
--------------------------

개발팀의 지식 허브에서는 모든 문서가 동일한 중요도를 갖지는 않습니다.
예를 들어 다음과 같은 우선순위를 생각할 수 있습니다.

1. Confluence 문서(공식 사양서·절차서)
2. Jira 티켓(최신 과제·진행 중인 태스크)
3. Git 리포지토리(코드·README)
4. Slack 메시지(논의 기록)

문서 부스트를 사용하면 특정 조건에 일치하는 문서의 검색 스코어를 높일 수 있습니다.
관리 화면의 [크롤러] > [문서 부스트]에서 URL 패턴이나 라벨에 기반하여 부스트 값을 설정할 수 있습니다.

관련 콘텐츠 활용
--------------------

검색 결과에 "관련 콘텐츠"를 표시하여 이용자가 원하는 정보에 도달하는 것을 지원할 수 있습니다.
예를 들어 Confluence의 설계서를 검색했을 때 관련된 Jira 티켓이 "관련 콘텐츠"로 표시되면 편리합니다.

운용상의 고려 사항
===============

크롤 스케줄
--------------------

데이터 소스별로 적절한 크롤 빈도를 설정합니다.

.. list-table:: 스케줄 예
   :header-rows: 1
   :widths: 25 25 50

   * - 데이터 소스
     - 권장 빈도
     - 이유
   * - Confluence
     - 4시간마다
     - 문서 업데이트 빈도가 중간 정도
   * - Jira
     - 2시간마다
     - 티켓 업데이트가 빈번
   * - Git
     - 일 1회
     - 릴리스 주기에 맞춤
   * - Slack
     - 4시간마다
     - 실시간성은 불필요하나 신선도는 중요

API 레이트 제한 대응
----------------------

SaaS 도구의 API에는 레이트 제한이 있습니다.
크롤 간격(인터벌)을 적절히 설정하여 API의 레이트 제한에 저촉되지 않도록 합니다.
특히 Slack API는 레이트 제한이 엄격하므로 크롤 간격에 여유를 두는 것이 중요합니다.

액세스 토큰 관리
----------------------

데이터스토어 플러그인 설정에는 각 도구의 API 액세스 토큰이 필요합니다.
보안 관점에서 다음 사항에 유의하십시오.

- 최소 권한 원칙: 읽기 전용 액세스 토큰을 사용
- 정기적인 로테이션: 토큰을 정기적으로 갱신
- 전용 계정 사용: 개인 계정이 아닌 서비스 계정을 사용

정리
======

본 기사에서는 개발팀이 일상적으로 사용하는 도구의 정보를 Fess에 집약하여 통합 검색이 가능한 지식 허브를 구축했습니다.

- 데이터스토어 플러그인으로 Git, Confluence, Jira, Slack의 데이터를 수집
- 라벨로 개발자에게 사용하기 편리한 검색 경험을 제공
- 문서 부스트로 정보의 우선순위를 제어
- API 레이트 제한이나 토큰 관리 등 운용상의 고려 사항

개발팀의 지식 허브를 통해 "그 논의는 어디서?", "이 사양서는?"이라는 질문에 신속하게 답할 수 있는 환경이 실현됩니다.

다음 회에서는 클라우드 스토리지의 횡단 검색에 대해 다룹니다.

참고 자료
========

- `Fess 데이터스토어 설정 <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess 플러그인 관리 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
