===========================================
개발팀의 Git·Confluence·Jira·Slack 검색하기
===========================================

들어가며
========

개발팀의 정보는 코드와 README는 Git, 설계서는 Confluence, 이슈는 Jira, 논의는 Slack처럼 도구마다 나뉘어 있습니다.
"그 사양은 어디에서 정해졌는가"를 찾을 때마다 4개의 도구를 차례로 검색하는 것은 번거롭습니다.
Fess의 데이터 저장소 플러그인을 사용하면 4개 도구의 정보를 하나의 검색 화면에서 찾을 수 있게 됩니다.

다만 설정을 잘못하면 다음과 같은 상태가 됩니다.

- Git 파일이 모두 URL이 빈 상태로 등록되어, 검색 결과에서 원래 파일을 열 수 없다
- Slack 메시지가 모두 제목 없이 표시된다
- 프라이빗 채널의 발언이 로그인하지 않은 사용자의 검색 결과에도 나온다
- Git 파일이 며칠 후 인덱스에서 사라진다

이 글에서는 도구마다 "그대로 옮겨 적으면 동작하는 최소 구성"을 제시하고, 각 설정에서 위의 함정을 어떻게 피하는지 설명합니다.
플러그인 설치, 핸들러 이름·파라미터·스크립트 작성법, 작업 만드는 법과 같은 데이터 저장소 공통 절차는 :doc:`datastore-basics`\ 에 정리되어 있습니다.
먼저 그 글을 읽은 후 진행하십시오.
글 속의 설정값은 Fess 15.9와 각 플러그인의 15.9.0 버전에 맞추었습니다.

이 글에서 만드는 구성
=====================

.. list-table::
   :header-rows: 1
   :widths: 14 20 26 40

   * - 도구
     - 플러그인
     - 핸들러 이름
     - 도구 측에서 준비할 것
   * - Git
     - ``fess-ds-git``
     - ``GitDataStore``
     - 읽기 권한이 있는 액세스 토큰(HTTPS로 clone할 수 있어야 함)
   * - Confluence / Jira
     - ``fess-ds-atlassian``
     - ``ConfluenceDataStore`` / ``JiraDataStore``
     - 크롤링용 계정의 API 토큰
   * - Slack
     - ``fess-ds-slack``
     - ``SlackDataStore``
     - Slack App의 Bot User OAuth Token(\ ``xoxb-``\ )

Docker로 실행하는 경우, 환경 변수 ``FESS_PLUGINS``\ 에 플러그인 이름과 버전을 공백으로 구분해 나열하면 시작할 때 한꺼번에 설치할 수 있습니다.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-git:15.9.0 fess-ds-atlassian:15.9.0 fess-ds-slack:15.9.0

관리 화면이나 ``fess-setup``\ 으로 설치한 경우에는 설치 후 Fess를 재시작합니다.

먼저 정할 것: 검색 결과를 누구에게 보여 줄 것인가
=================================================

데이터 저장소 설정을 새로 만들면 "권한" 칸에는 처음부터 ``{role}guest``\ 가 들어 있습니다.
이대로 두면 가져온 정보는 로그인하지 않은 사용자에게도 검색됩니다.

Git, Confluence, Jira 플러그인은 원래 도구의 접근 권한을 Fess로 가져오지 않습니다.
크롤링에 사용하는 계정이 읽을 수 있는 것은 모두 가져오며, "권한" 칸에 적은 역할이나 그룹을 가진 사람에게 보입니다.
따라서 다음 2가지를 조합해 범위를 정합니다.

- "권한" 칸의 ``{role}guest``\ 를 보여 주고 싶은 상대(예: ``{group}developers``\ )로 바꿔 쓴다
- 크롤링용 계정의 권한이나, 뒤에서 설명하는 ``jira.jql``\ 과 ``include_pattern``\ 으로 가져오는 범위를 그 상대에게 보여 줘도 되는 것으로 좁힌다

Slack 플러그인만은 프라이빗 채널의 멤버를 권한으로 가져올 수 있습니다(후술).
그룹과 역할의 개념은 :doc:`guide-05`\ 를 참조하십시오.

Git 저장소
==========

준비
----

``fess-ds-git``\ 은 HTTPS로 clone합니다.
SSH URI(\ ``git@...`` 형식)는 지원하지 않습니다.
프라이빗 저장소의 경우에는 읽기용 액세스 토큰을 만듭니다.
GitHub의 classic 토큰이라면 ``repo`` 스코프, GitLab이라면 ``read_repository`` 스코프입니다.

파라미터와 스크립트
-------------------

[크롤러] > [데이터 저장소] > [새로 만들기]에서 "핸들러 이름"으로 ``GitDataStore``\ 를 선택합니다.

.. code-block:: properties

    script_type=javascript
    uri=https://github.com/example/dev-platform.git
    username=fess-crawler
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    base_url=https://github.com/example/dev-platform/blob/main/
    include_pattern=.*\.(md|rst|txt|java|py|ts|yml|yaml)$
    time_to_live=5256000

.. code-block:: properties

    url=url
    title=path
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp
    label="code"

각 줄의 의미는 다음과 같습니다.

- ``base_url``\ : 스크립트의 ``url``\ 은 ``base_url``\ 과 저장소 내 경로를 그대로 연결한 값입니다. 생략하면 ``url``\ 이 빈 문자열이 되어, 모든 파일이 같은 문서 ID가 되어 서로 덮어씁니다. 끝은 ``/``\ 로 마치고, 브랜치 이름은 크롤링하는 브랜치(기본값은 원격의 기본 브랜치, 바꿀 때는 ``commit_id``\ )와 맞춥니다.
- ``username`` / ``password``\ : 둘 다 지정했을 때만 인증에 사용됩니다. 토큰은 ``uri``\ 에 넣지 말고 ``password``\ 에 적습니다(\ ``password``\ 는 저장 시 암호화되지만 ``uri``\ 는 암호화되지 않습니다).
- ``include_pattern``\ : 저장소 내 경로(예: ``docs/setup.md``\ ) 전체와 일치하는 정규 표현식입니다. URL이 아닙니다.
- ``title=path``\ : 파일 이름만 담긴 ``name``\ 으로 하면 ``README.md``\ 처럼 이름이 같은 파일을 검색 결과에서 구별할 수 없으므로 경로를 사용합니다.

차분 크롤링과 유효 기간
-----------------------

``fess-ds-git``\ 은 크롤링이 성공하면 그 커밋 ID를 "파라미터" 칸의 ``prev_commit_id``\ 에 다시 기록합니다.
2회차부터는 이전 커밋과의 차분에 있는 파일만 등록하고, 삭제·이름 변경된 파일의 문서를 지웁니다(삭제를 반영하려면 ``base_url``\ 이 필요합니다).

이 차분 크롤링은 Fess 문서의 유효 기간과 궁합이 나쁘기 때문에, 위의 예에서는 ``time_to_live``\ 를 지정하고 있습니다.
데이터 저장소의 문서에는 등록 시 유효 기간이 붙습니다.
기본적으로는 [시스템] > [일반]의 "이전 문서 삭제"(기본값 3일)로 정해지며, 기한이 지난 문서는 매분 실행되는 작업 "Doc Purger"가 삭제합니다.
차분 크롤링에서는 변경이 없는 파일이 다시 등록되지 않으므로 유효 기간이 연장되지 않고, 첫 크롤링 후 며칠 만에 사라져 버립니다.
``time_to_live``\ 는 이 설정의 문서 유효 기간을 분 단위로 지정하는 파라미터로, ``5256000``\ 은 약 10년입니다.

이 때문에 스크립트, ``base_url``\ , ``include_pattern``\ , "권한" 칸을 바꿔도 변경이 없는 파일에는 반영되지 않습니다.
모든 파일을 다시 등록하려면 다음 절차를 따릅니다.

1. [시스템 정보] > [검색]에서 ``label:code``\ 를 검색하고 [이 쿼리로 모두 삭제]로 오래된 문서를 지운다
2. "파라미터" 칸의 ``prev_commit_id=`` 값을 지우고 저장한다
3. 작업을 실행한다

"권한" 칸이나 ``base_url``\ 을 바꾼 경우에는 문서 ID가 바뀌므로, 절차 1을 생략하면 오래된 문서가 남습니다.
이 데이터 저장소 설정을 삭제할 때도 먼저 절차 1로 문서를 지우십시오.

Confluence
==========

Atlassian Cloud에서는 크롤링용 계정으로 API 토큰을 만들어 Basic 인증의 비밀번호로 사용합니다.
가져오는 대상은 이 계정이 열람할 수 있는 스페이스의 페이지와 블로그 게시물입니다.
"핸들러 이름"으로 ``ConfluenceDataStore``\ 를 선택합니다.

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    include_pattern=https://example\.atlassian\.net/wiki/spaces/(DEV|OPS)/.*

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body + content.comments
    last_modified=content.last_modified
    label="docs"

- ``home``\ 은 ``/wiki``\ 를 붙여도 붙이지 않아도 동작합니다. Cloud에서는 Confluence용으로 ``/wiki``\ 가 보완됩니다.
- ``deployment``\ 는 생략하면 호스트 이름이 ``.atlassian.net``\ 으로 끝나는 경우 ``cloud``\ , 그 외에는 ``datacenter``\ 로 간주됩니다.
- ``content.comments``\ 를 더하면 페이지의 댓글도 본문으로 검색할 수 있습니다. 각 댓글은 빈 줄로 구분되어 연결되어 있습니다.
- ``include_pattern``\ 은 문서의 URL 전체와의 일치로 판정됩니다. Cloud 페이지의 URL은 ``https://<사이트>/wiki/spaces/<스페이스키>/pages/<페이지ID>``\ 이므로 스페이스 키로 좁힐 수 있습니다. Data Center의 URL(\ ``/pages/viewpage.action?pageId=...``\ )에는 스페이스 키가 포함되지 않으므로 이 방법은 사용할 수 없습니다.

Data Center에서는 ``deployment=datacenter``\ 로 하고, 개인용 액세스 토큰을 사용하는 경우에는 ``auth_type=pat``\ 과 ``pat.token``\ 을 지정합니다.

Jira
====

인증은 Confluence와 같습니다.
"핸들러 이름"으로 ``JiraDataStore``\ 를 선택하고, 가져올 이슈를 JQL로 좁힙니다.

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    jira.jql=project in (DEV, OPS)

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description + issue.comments
    last_modified=issue.last_modified
    label="tickets"

JQL 파라미터 이름은 ``jira.jql``\ 입니다.
예전 이름인 ``issue.jql``\ 도 아직 동작하지만, 로그에 ``Parameter "issue.jql" is deprecated``\ 라는 경고가 나옵니다.
예전 이름은 16.0에서 삭제될 예정입니다.
``jira.jql``\ 을 생략하면 ``created is not empty``\ , 즉 계정이 열람할 수 있는 모든 이슈가 대상이 됩니다.

``issue.comments``\ 를 더하면 이슈의 댓글도 빈 줄로 구분되어 본문에 들어가 검색할 수 있습니다.
댓글은 이슈마다 API로 가져오므로 호출 횟수가 늘어납니다(뒤에서 설명하는 속도 제한 참조).

Slack
=====

Slack App 준비
--------------

https://api.slack.com/apps 에서 App을 만들고, [OAuth & Permissions]의 Bot Token Scopes에 다음 스코프를 추가한 후 워크스페이스에 설치합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 스코프
     - 필요한 경우
   * - ``channels:read``, ``channels:history``, ``users:read``, ``team:read``
     - 항상 필요
   * - ``groups:read``, ``groups:history``
     - 프라이빗 채널을 가져온다(\ ``include_private=true``\ )
   * - ``users:read.email``
     - 프라이빗 채널의 멤버를 권한으로 사용한다(\ ``permission_sync=true``\ )
   * - ``files:read``
     - 파일도 가져온다(\ ``file_crawl=true``\ )

``team:read``\ 가 없으면 메시지마다 ``chat.getPermalink``\ 를 호출하게 되어 API 호출이 크게 늘어납니다.
설치 후, 가져올 채널마다 App을 추가합니다.
App이 참여하지 않은 채널은 경고가 나오고 건너뜁니다.

공개 채널과 프라이빗 채널은 데이터 저장소 설정을 나누어 2개 만듭니다.
이유는 "프라이빗 채널" 절에서 설명합니다.

공개 채널
---------

"핸들러 이름"으로 ``SlackDataStore``\ 를 선택하고, "권한" 칸은 공개 채널을 보여 주고 싶은 상대로 합니다.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=*all
    include_private=false

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    label="slack"

``message.title``\ 은 메시지에서는 항상 빈 문자열이므로, ``title=message.title``\ 로 쓰면 모든 결과가 제목 없음이 됩니다.
위의 예처럼 작성자와 채널 이름으로 제목을 만듭니다.
스레드의 답글도 1건씩 문서로 등록됩니다.
``channel_join`` 등의 시스템 메시지는 기본값(\ ``ignore_system_events=true``\ )으로 제외됩니다.

프라이빗 채널
-------------

``permission_sync=true``\ 를 지정하면 프라이빗 채널 멤버의 이메일 주소로부터 멤버별 사용자 역할을 만들어 ``message.roles``\ 에 넣습니다.
다만 이 값에는 ``default_permissions``\ 와 "권한" 칸의 값도 더해집니다.
공개 채널은 자체 역할을 갖지 않으므로, 이 2가지가 비어 있으면 공개 채널의 문서는 아무에게도 보이지 않게 됩니다.
반대로 2가지 중 어느 한쪽에 공개 채널용 상대를 적으면, 그 상대에게 프라이빗 채널의 문서도 보여 버립니다.
하나의 설정으로 양쪽을 올바르게 다룰 수 없으므로, 프라이빗 채널은 별도의 설정으로 합니다.

두 번째 데이터 저장소 설정에서는 "권한" 칸의 ``{role}guest``\ 를 지워 비우고, 가져올 프라이빗 채널의 이름을 ``channels``\ 에 나열합니다.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=dev-security,dev-incident
    include_private=true
    permission_sync=true

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    role=message.roles
    label="slack"

- ``role=message.roles``\ 를 쓰지 않으면 계산한 역할은 사용되지 않습니다. 이때 크롤링 시작 시 ``no script value references message.roles``\ 라는 경고가 나옵니다.
- ``channels``\ 에 공개 채널을 섞으면 그 문서는 역할이 비어 아무에게도 보이지 않습니다.
- 이 설정에서는 크롤링 시작 시 ``default_permissions is not set and this crawl's DataConfig permission field is empty``\ 라는 경고가 나옵니다. 공개 채널을 포함하지 않았다면 문제없습니다.
- 멤버를 가져오지 못한 채널이나, 이메일 주소를 1건도 확인하지 못한 채널(\ ``users:read.email``\ 을 빠뜨린 경우 등)은 그 크롤링에서는 가져오지 않습니다. [시스템 정보] > [장애 URL]에 채널 ID와 채널 이름으로 기록됩니다.

검색할 때는 Fess에 로그인한 사용자의 사용자 이름이 이 이메일 주소와 대조됩니다.
따라서 Fess의 사용자 이름이 Slack의 이메일 주소와 일치해야 합니다.
Slack은 이메일 주소를 소문자로 다루므로 Fess의 사용자 이름도 소문자로 합니다.
일치하지 않는 사용자에게는 프라이빗 채널의 문서가 표시되지 않을 뿐이며, 다른 사람의 문서가 보이는 일은 없습니다.
SSO로 로그인한 경우 어떤 값이 사용자 이름이 되는지는 :doc:`guide-15`\ 를 참조하십시오.

이미 ``permission_sync`` 없이 프라이빗 채널을 가져온 경우, 그 문서는 유효 기간이 끝날 때까지 권한이 붙지 않은 채 남습니다.
[시스템 정보] > [검색]에서 해당 문서를 삭제한 후 이 설정으로 크롤링하십시오.

라벨·부스트 값·스케줄
=====================

라벨은 위의 각 스크립트의 ``label="..."`` 줄로 붙이고 있습니다.
검색 화면의 필터에 표시하려면 [크롤러] > [라벨]에서 같은 값(\ ``code``\ , ``docs``\ , ``tickets``\ , ``slack``\ )의 라벨을 만듭니다.
문서의 URL과 일치하는 "대상 경로"를 가진 라벨이 있으면 스크립트의 라벨이 사라진다는 점에 주의하십시오(\ :doc:`datastore-basics`\ ).

[크롤러] > [문서 부스트]의 규칙은 데이터 저장소의 문서에는 적용되지 않습니다.
Confluence의 설계서를 Slack의 발언보다 상위에 표시하고 싶은 경우에는 Confluence 데이터 저장소 설정의 "부스트 값"(초깃값 ``1.0``\ )을 올립니다.
값은 검색 점수에 곱해지므로 조금씩 바꾸면서 검색 결과를 비교해 보십시오.

도구마다 실행 빈도를 바꾸려면 각 데이터 저장소 설정의 상세 화면에서 [새 작업 작성]을 사용합니다(\ :doc:`datastore-basics`\ ).

API 속도 제한
=============

Slack과 Atlassian 플러그인은 ``429``\ 와 ``5xx`` 응답을 자동으로 재시도하고, ``Retry-After`` 헤더가 있으면 그 초만큼 기다립니다(Slack은 최대 60초).

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 플러그인
     - 조정할 수 있는 파라미터
   * - Slack
     - ``read_interval``\ (메시지 1건마다의 대기 시간, 밀리초, 기본값 ``0``\ ), ``max_retry_count``\ (기본값 ``3``\ ), ``retry_interval``\ (첫 재시도까지의 대기 시간, 밀리초, 기본값 ``3000``\ . 재시도할 때마다 2배가 되며 상한 60초)
   * - Atlassian
     - ``read_interval``\ (API 호출의 최소 간격, 밀리초, 기본값 ``0``\ . 스레드 간 공유). 재시도 횟수와 간격은 고정입니다

Slack에서 재시도를 다 쓰면 그 크롤링은 중단됩니다.
작업 로그의 상태는 "OK" 그대로이므로 다음 절의 절차로 확인합니다.

동작 확인
=========

작업 결과와 로그를 보는 방법은 :doc:`datastore-basics`\ 에서 설명합니다.
데이터 저장소 크롤링은 실패해도 작업이 "OK"로 표시되는 경우가 있으므로 건수와 로그로 판단하십시오.
이 글의 구성에서는 추가로 다음 사항을 확인합니다.

1. [시스템 정보] > [검색]에서 ``label:code``\ , ``label:docs``\ , ``label:tickets``\ , ``label:slack``\ 을 각각 검색해 건수가 0이 아닌지 확인한다
2. Git 문서의 URL을 열어 저장소의 파일이 표시되는지 확인한다. ``fess-crawler.log``\ 에 ``base_url is blank`` 경고가 나와 있으면 ``base_url``\ 을 다시 확인한다
3. Git 설정의 상세 화면을 열어 파라미터에 ``prev_commit_id``\ 가 다시 기록되었는지 확인한다
4. 로그아웃한 상태에서 프라이빗 채널에만 있는 단어를 검색해 1건도 나오지 않는지 확인한다
5. 그 채널의 멤버로 로그인하면 같은 단어로 찾을 수 있는지 확인한다

5에서 찾을 수 없는 경우에는 Fess의 사용자 이름과 Slack의 이메일 주소가 일치하는지, ``fess-crawler.log``\ 에 ``private channel(s) skipped`` 경고가 나와 있지 않은지 확인합니다.
인증 오류 등으로 설정 전체가 실패한 경우에는 [시스템 정보] > [장애 URL]에 설정 단위로 기록됩니다.

정리
====

- Git은 ``base_url``\ 을 반드시 지정하고, 차분 크롤링으로 문서가 기한 만료되지 않도록 ``time_to_live``\ 를 붙입니다.
- Confluence와 Jira는 ``content.comments`` / ``issue.comments``\ 로 댓글도 가져오고, JQL은 ``jira.jql``\ 에 씁니다.
- Slack의 제목은 ``message.user``\ 와 ``message.channel``\ 로 만듭니다.
- Git, Confluence, Jira는 원래의 권한을 가져오지 않으므로 "권한" 칸과 가져오는 범위로 공개 범위를 정합니다.
- Slack의 프라이빗 채널은 별도의 설정으로 하고, ``permission_sync=true``\ , ``role=message.roles``\ , 빈 "권한" 칸으로 가져옵니다.
- 정보원의 우선순위는 데이터 저장소 설정의 "부스트 값"으로 조정합니다.

참고 자료
=========

- `Git 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-git.html>`__
- `Atlassian 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-atlassian.html>`__
- `Slack 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-slack.html>`__
- `데이터 저장소 크롤링 <https://fess.codelibs.org/ko/stable/admin/dataconfig-guide.html>`__
- `일반 <https://fess.codelibs.org/ko/stable/admin/general-guide.html>`__
- `fess-ds-slack 15.9.0 README(스코프와 권한 동기화) <https://github.com/codelibs/fess-ds-slack/blob/fess-ds-slack-15.9.0/README.md>`__
