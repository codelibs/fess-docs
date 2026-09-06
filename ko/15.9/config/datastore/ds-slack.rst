==================================
Slack 커넥터
==================================

개요
====

Slack 커넥터는 Slack 워크스페이스의 채널 메시지를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-slack`` 플러그인이 필요합니다.

지원 콘텐츠
===========

- 퍼블릭 채널 메시지
- 프라이빗 채널 메시지
- 스레드 답글 메시지(``conversations.replies`` 로 가져옵니다)
- 파일 첨부(옵션)

다음은 대상 외입니다:

- 시스템 이벤트 메시지(``channel_join``, ``channel_topic``, ``pinned_item`` 등)는 기본적으로
  색인 대상에서 제외됩니다(``ignore_system_events``)
- 다이렉트 메시지(DM) 및 그룹 DM
- Huddle의 녹취록과 Clips(Slack에 공개 API가 없어 크롤링할 수 없습니다)

전제조건
========

1. 플러그인 설치가 필요합니다
2. Slack App 생성과 권한 설정이 필요합니다
3. OAuth Access Token 취득이 필요합니다

플러그인 설치
-------------

관리 화면의 "시스템" → "플러그인"에서 설치합니다:

1. Maven Central에서 ``fess-ds-slack-X.X.X.jar``\ 를 다운로드
2. 플러그인 관리 화면에서 업로드하여 설치
3. |Fess| 재시작

또는 자세한 내용은 :doc:`../../admin/plugin-guide` 를 참조하세요.

설정 방법
=========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 설정합니다.

기본 설정
---------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - Company Slack
   * - 핸들러 이름
     - SlackDataStore
   * - 활성화
     - 켬

파라미터 설정
-------------

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=false
    include_private=false

파라미터 목록
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``token``
     - 예
     - Slack 앱의 OAuth Access Token
   * - ``channels``
     - 아니오
     - 크롤링 대상 채널(쉼표 구분 또는 ``*all``). 미지정 시 모든 채널을 가져옵니다(``*all`` 과 동일한 동작).
   * - ``file_crawl``
     - 아니오
     - 파일도 크롤링(기본값: ``false``)
   * - ``include_private``
     - 아니오
     - 프라이빗 채널도 포함(기본값: ``false``)
   * - ``number_of_threads``
     - 아니오
     - 병렬 처리 스레드 수(기본값: ``1``)
   * - ``max_filesize``
     - 아니오
     - 크롤링할 파일의 최대 크기(바이트 단위, 기본값: ``10000000``)
   * - ``ignore_error``
     - 아니오
     - 오류 발생 시 처리 계속(기본값: ``true``)
   * - ``supported_mimetypes``
     - 아니오
     - 크롤링 대상 MIME 타입(정규식, 기본값: ``.*``)
   * - ``include_pattern``
     - 아니오
     - 크롤링 대상 URL의 정규식 패턴
   * - ``exclude_pattern``
     - 아니오
     - 크롤링 제외 URL의 정규식 패턴
   * - ``proxy_host``
     - 아니오
     - HTTP 프록시 호스트
   * - ``proxy_port``
     - 아니오
     - HTTP 프록시 포트(``proxy_host`` 지정 시 필수)
   * - ``file_types``
     - 아니오
     - Slack API의 파일 타입 필터(기본값: ``all``)
   * - ``channel_count``
     - 아니오
     - 채널 목록의 페이지당 가져오기 건수(기본값: ``100``)
   * - ``message_count``
     - 아니오
     - 메시지의 페이지당 가져오기 건수(기본값: ``100``)
   * - ``file_count``
     - 아니오
     - 파일의 페이지당 가져오기 건수(기본값: ``20``)
   * - ``user_count``
     - 아니오
     - API 페이지당 사용자 수(기본값: ``100``)
   * - ``user_cache_size``
     - 아니오
     - 사용자 정보 캐시의 최대 항목 수(기본값: ``10000``)
   * - ``bot_cache_size``
     - 아니오
     - 봇 정보 캐시의 최대 항목 수(기본값: ``10000``)
   * - ``channel_cache_size``
     - 아니오
     - 채널 정보 캐시의 최대 항목 수(기본값: ``10000``)

고급 파라미터
~~~~~~~~~~~~~

아래 파라미터는 연결·재시도 동작, 세밀한 크롤링 범위 제어, 권한 동기화를 다룹니다:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 파라미터
     - 설명
   * - ``connection_timeout``
     - 각 Slack API 요청의 연결 타임아웃(밀리초, 기본값: ``20000``)
   * - ``read_timeout``
     - 각 Slack API 요청의 읽기 타임아웃(밀리초, 기본값: ``20000``)
   * - ``max_retry_count``
     - ``429``\ (레이트 리밋) 또는 ``5xx`` 응답을 받았을 때의 최대 재시도 횟수(기본값: ``3``)
   * - ``retry_interval``
     - 응답에 ``Retry-After`` 헤더가 없는 경우, 첫 재시도까지의 대기 시간(밀리초, 기본값:
       ``3000``). 재시도할 때마다 두 배로 늘어나며 ``60000`` 밀리초에서 상한에 도달합니다.
       ``Retry-After`` 헤더가 있으면 해당 값(초)이 우선합니다
   * - ``executor_timeout``
     - 크롤링 종료 시 대기열에 남은 작업이 완료될 때까지 기다리는 시간(초, 기본값: ``60``).
       이 시간을 초과하면 강제 종료됩니다
   * - ``exclude_archived``
     - ``conversations.list`` 의 결과에서 아카이브된 채널을 제외할지 여부(기본값: ``false``).
       ``true`` 로 설정하면 ``channels`` 에 채널명으로 지정한 아카이브된 채널을 이름으로
       확인할 수 없게 됩니다(자세한 내용은 문제 해결 참조)
   * - ``ignore_system_events``
     - Slack이 자동 생성하는 채널 관리 계열 메시지(``channel_join``, ``channel_topic``,
       ``pinned_item`` 등)를 색인 대상에서 제외할지 여부(기본값: ``true``)
   * - ``read_interval``
     - 메시지 또는 파일을 1건 처리할 때마다 대기하는 시간(밀리초, 기본값: ``0`` = 대기 없음).
       레이트 리밋이 엄격한 워크스페이스에 대해 크롤링 속도를 늦출 때 사용합니다
   * - ``max_content_length``
     - 콘텐츠 추출(Tika)이 파일 1건에서 추출할 수 있는 최대 문자 수(기본값: 미설정 = MIME
       타입별 |Fess| 기본 상한을 따름). ``max_filesize`` 는 다운로드 전에 파일 크기로 걸러내는
       전송량의 상한이고, ``max_content_length`` 는 다운로드 후 추출하는 텍스트양의 상한으로,
       각각 독립적으로 동작합니다. ``max_filesize`` 를 줄여도 ``max_content_length`` 를
       대신할 수는 없습니다(예: 1MB의 압축 파일이라도 압축 해제 후에는 훨씬 많은 텍스트가
       될 수 있습니다)
   * - ``permission_sync``
     - 프라이빗 채널의 멤버십을 검색용 권한(역할)으로 변환할지 여부(기본값: ``false``).
       자세한 내용은 뒤에 나오는 "권한 동기화(ACL)"를 참조하세요
   * - ``default_permissions``
     - 채널 멤버십과 무관하게 색인되는 모든 문서에 부여할 추가 권한(``{user}``/``{group}``/
       ``{role}`` 형식, 쉼표 구분, 기본값: 비어 있음). ``permission_sync`` 가 활성화된 경우에만
       적용됩니다

.. note::

   ``ignore_system_events`` 의 기본값은 ``true`` 입니다. 이 파라미터를 지정하지 않은 기존
   크롤링 설정이라도, |Fess| 를 업그레이드하면 ``channel_join`` 등의 시스템 이벤트 메시지가
   더 이상 색인되지 않게 되어, 오류나 경고 없이 색인되는 문서 수가 줄어듭니다. 이전과 동일하게
   시스템 이벤트도 색인하려면 ``ignore_system_events=false`` 를 명시적으로 지정하세요.

스크립트 설정
-------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

사용 가능한 필드
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``message.title``
     - 타이틀(메시지의 경우 빈 문자열, 파일의 경우 파일명과 타이틀)
   * - ``message.text``
     - 메시지 텍스트 콘텐츠(파일 항목의 경우, 파일명과 추출된 파일 본문)
   * - ``message.user``
     - 메시지 발신자의 표시 이름(미설정 시 실제 이름, 사용자 이름, 사용자 ID 순으로 해결)
   * - ``message.channel``
     - 메시지가 전송된 채널명
   * - ``message.timestamp``
     - 메시지 전송 일시
   * - ``message.permalink``
     - 메시지의 퍼머링크
   * - ``message.attachments``
     - 첨부 파일의 폴백 정보
   * - ``message.roles``
     - 이 메시지 또는 파일을 볼 수 있는 검색 권한(역할) 목록. ``permission_sync=true`` 인
       경우에만 존재하는 필드입니다. 스크립트에서 ``role=message.roles`` 를 지정하지 않으면
       계산된 권한은 색인되는 문서에 반영되지 않습니다

Slack App 설정
==============

1. Slack App 생성
-----------------

https://api.slack.com/apps 에 접속:

1. "Create New App" 클릭
2. "From scratch" 선택
3. 앱 이름 입력(예: Fess Crawler)
4. 워크스페이스 선택
5. "Create App" 클릭

2. OAuth & Permissions 설정
---------------------------

"OAuth & Permissions" 메뉴에서:

**Bot Token Scopes**\ 에 다음을 추가:

기본 스코프(항상 필요):

- ``channels:history`` - 퍼블릭 채널 메시지 읽기
- ``channels:read`` - 퍼블릭 채널 정보 읽기
- ``users:read`` - 사용자 정보 읽기(표시 이름 해결에 필요)
- ``team:read`` - 워크스페이스 정보 읽기. ``team.info`` 를 크롤링할 때마다 호출하므로 이
  스코프는 필수입니다. 이 스코프가 없으면 이 커넥터는 메시지 1건마다 ``chat.getPermalink``
  를 추가로 호출하게 되어 API 호출 수가 크게 늘어납니다

프라이빗 채널도 포함하는 경우(``include_private=true``)에 추가:

- ``groups:history`` - 프라이빗 채널 메시지 읽기
- ``groups:read`` - 프라이빗 채널 정보 읽기

파일도 크롤링하는 경우(``file_crawl=true``)에 추가:

- ``files:read`` - 파일 콘텐츠 읽기

프라이빗 채널의 권한을 동기화하는 경우(``permission_sync=true``)에 추가:

- ``users:read.email`` - 멤버의 이메일 주소 읽기(권한 동기화에 필수)

3. 앱 설치
----------

"Install App" 메뉴에서:

1. "Install to Workspace" 클릭
2. 권한 확인 후 "허용" 클릭
3. "Bot User OAuth Token" 복사(``xoxb-``\ 로 시작)

.. note::
   보통은 ``xoxb-``\ 로 시작하는 Bot User OAuth Token을 사용하지만,
   파라미터에서는 ``xoxp-``\ 로 시작하는 User OAuth Token도 사용 가능합니다.

4. 채널에 추가
--------------

크롤링 대상 채널에 App을 추가:

1. Slack에서 채널 열기
2. 채널 이름 클릭
3. "통합" 탭 선택
4. "앱 추가" 클릭
5. 생성한 앱 추가

권한 동기화(ACL)
================

Slack 커넥터는 프라이빗 채널의 멤버십을 |Fess| 의 검색 권한(역할)으로 변환하여, 해당 채널의
멤버만 콘텐츠를 검색할 수 있도록 하는 기능을 제공합니다. 기본값은 비활성화입니다.

.. note::

   ``permission_sync`` 는 권한(역할)을 계산할 뿐, 자동으로 적용하지는 않습니다. 스크립트에
   ``role=message.roles`` 를 추가해야만 계산된 권한이 색인되는 문서에 반영됩니다. 이 매핑을
   잊으면 ``permission_sync=true`` 로 인한 API 호출 증가와 프라이빗 채널 건너뛰기만 발생할
   뿐, 접근 제어는 전혀 이루어지지 않습니다.

활성화 방법
-----------

1. Slack App에 ``users:read.email`` 스코프를 추가합니다(멤버의 이메일 주소 확인에 필수)
2. 파라미터에 ``permission_sync=true`` 를 설정합니다
3. 스크립트에 ``role=message.roles`` 를 추가합니다

파라미터:

::

    include_private=true
    permission_sync=true

스크립트:

::

    role=message.roles

페일 클로즈(Fail-Closed) 동작
-----------------------------

다음 중 하나에 해당하는 프라이빗 채널은 해당 크롤링에서 전혀 색인되지 않습니다(콘텐츠가
잘못 공개되는 대신 색인하지 않는 방향으로 처리하는 "페일 클로즈" 동작입니다):

- 채널의 멤버 목록 취득에 실패한 경우
- 멤버 목록이 0건이었던 경우(크롤링에 사용하는 토큰의 봇 사용자 자신이 해당 프라이빗 채널에
  참가하지 않은 경우 발생합니다)
- 멤버는 있지만 그중 누구의 이메일 주소도 확인할 수 없었던 경우(주로 ``users:read.email``
  스코프 부족이 원인입니다)

퍼블릭 채널은 ``conversations.members`` 를 호출하지 않으며 항상 모두가 볼 수 있는 것으로
간주됩니다.

프린시펄 이름 일치
------------------

검색 시 권한 판정은 |Fess| 의 로그인 이름(프린시펄 이름)으로 이루어집니다. 이 기능이
계산하는 권한은 Slack의 이메일 주소로부터 만들어지므로, |Fess| 의 로그인 이름과 Slack의
이메일 주소를 일치시켜야 합니다. Slack은 이메일 주소를 소문자로 정규화하므로, |Fess| 쪽의
로그인 이름도 소문자로 해 두십시오. 일치하지 않는 경우 다른 사람의 문서가 보이는 것이 아니라,
해당 사용자의 검색 결과가 항상 0건이 됩니다(원인을 파악하기 어려우므로 주의하세요).

기타 주의사항
-------------

- Slack의 사용자 그룹(User Group)은 사용하지 않습니다. 권한은 각 멤버의 이메일 주소로부터
  직접 계산합니다
- ``default_permissions`` 로 채널 멤버십과 무관하게 모든 문서에 부여할 추가 권한을 지정할
  수 있습니다(``permission_sync=true`` 인 경우에만 적용)
- ``permission_sync=false`` 인 채로 ``include_private=true`` 로 설정하면, 프라이빗 채널의
  콘텐츠는 데이터 스토어 설정의 "권한" 항목 설정만으로 색인됩니다. 이 항목이 비어 있으면
  사실상 모두에게 공개됩니다
- 이미 색인된 워크스페이스에서 ``permission_sync`` 를 나중에 활성화하더라도, 이전에 색인된
  문서에 소급하여 권한이 부여되지는 않습니다. 적용하려면 ``permission_sync=true`` 와
  ``role=message.roles`` 를 설정한 뒤 다시 크롤링하십시오. 마찬가지로 ``permission_sync``
  를 나중에 비활성화하더라도, 이미 적용된 권한이 색인된 문서에서 자동으로 제거되지는 않습니다

사용 예
=======

특정 채널 크롤링
----------------

파라미터:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random,tech-discussion
    file_crawl=false
    include_private=false

스크립트:

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

모든 채널 크롤링
----------------

파라미터:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=false

스크립트:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

프라이빗 채널 포함 크롤링
-------------------------

파라미터:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=true

스크립트:

::

    title=message.user + " #" + message.channel
    digest=message.text
    content=message.text + "\n첨부: " + message.attachments
    created=message.timestamp
    url=message.permalink

파일 포함 크롤링
----------------

파라미터:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=true
    include_private=false

스크립트:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

상세 메시지 정보 포함
---------------------

스크립트:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

권한을 동기화하여 크롤링
------------------------

프라이빗 채널의 콘텐츠를 해당 채널의 멤버만 검색할 수 있도록 합니다. 사전에 Slack App에
``users:read.email`` 스코프를 추가하세요.

파라미터:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    include_private=true
    permission_sync=true

스크립트:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink
    role=message.roles

.. note::

   ``role=message.roles`` 를 빠뜨리면 계산된 권한이 색인되는 문서에 반영되지 않습니다.
   자세한 내용은 "권한 동기화(ACL)"를 참조하세요.

문제 해결
=========

오류 처리 방식
--------------

Slack 커넥터는 Slack API 오류를 다음 세 가지로 구분하여 처리합니다:

- **치명적 오류**\ (``invalid_auth``, ``token_revoked``, ``account_inactive``,
  ``missing_scope``, ``not_authed``, ``token_expired``): 토큰 자체를 사용할 수 없는
  상태이므로 크롤링 작업 전체를 실패로 처리합니다
- **일시적 오류**\ (``ratelimited``, ``internal_error``, ``fatal_error``,
  ``service_unavailable``, ``request_timeout``): 재시도해도 해소되지 않으면 크롤링 작업
  전체를 실패로 처리합니다(재시도 동작은 뒤의 "API 속도 제한" 참조)
- **채널 단위 오류**\ (``channel_not_found``, ``not_in_channel`` 등): 해당 채널만 경고와
  함께 건너뛰고, 다른 채널의 크롤링은 계속됩니다

이전 버전에서는 치명적 오류가 발생해도 크롤링이 "성공"으로 처리되어, 결과적으로 0건 또는
일부만 색인되는 "조용한 부분 성공"이 발생했습니다. 현재는 이 세 가지 분류에 따라 치명적·
일시적 오류는 반드시 작업 실패로 보고됩니다.

인증 오류
---------

**증상**: ``invalid_auth`` 또는 ``not_authed``

**확인 사항**:

1. 토큰이 올바르게 복사되었는지 확인
2. 토큰 형식 확인:

   - Bot User OAuth Token: ``xoxb-``\ 로 시작
   - User OAuth Token: ``xoxp-``\ 로 시작

3. 앱이 워크스페이스에 설치되어 있는지 확인
4. 필요한 권한이 부여되어 있는지 확인

채널을 찾을 수 없음
-------------------

**증상**: ``channel_not_found``

**확인 사항**:

1. 채널명이 올바른지 확인(#은 불필요)
2. 앱이 채널에 추가되어 있는지 확인
3. 프라이빗 채널인 경우 ``include_private=true`` 설정
4. ``exclude_archived=true`` 를 설정하지 않았는지 확인하세요. 기본값
   (``exclude_archived=false``)에서는 아카이브된 채널도 목록에 포함되어 크롤링됩니다.
   ``true`` 로 설정한 경우에만 ``channels`` 에 채널명으로 지정한 아카이브된 채널을 이름으로
   확인할 수 없게 됩니다

메시지를 가져올 수 없음
-----------------------

**증상**: 크롤링은 성공했지만 색인되는 문서가 적거나 0건

**확인 사항**:

1. ``ignore_system_events`` 의 기본값은 ``true`` 입니다. 채널 내 메시지가
   ``channel_join`` 등의 시스템 이벤트뿐인 경우, 해당 채널은 색인되는 문서가 0건이 됩니다
   ("고급 파라미터" 참조)
2. 채널에 실제로 메시지가 게시되어 있는지 확인
3. 앱이 채널에 추가되어 있는지 확인
4. ``permission_sync=true`` 인 경우, 프라이빗 채널의 멤버 취득에 실패하면 해당 채널은 이번
   크롤링에서 색인되지 않습니다(페일 클로즈. "권한 동기화(ACL)" 참조)

.. note::

   이전 버전에서는 스코프 부족(``missing_scope``)이 발생해도 크롤링이 성공한 채로 메시지
   0건이 되는 경우가 있었습니다. 현재는 ``missing_scope`` 를 포함한 치명적 오류가 발생하면
   크롤링 작업 자체가 실패합니다. 작업이 실패하고 있다면 이 절이 아니라 다음의 "권한 부족
   오류"를 확인하세요.

권한 부족 오류
--------------

**증상**: ``missing_scope``\ (크롤링 작업 전체가 실패합니다)

**해결 방법**:

1. Slack App 설정에서 필요한 스코프 추가:

   **기본**\ (항상 필요):

   - ``channels:history``
   - ``channels:read``
   - ``users:read``
   - ``team:read``

   **프라이빗 채널**:

   - ``groups:history``
   - ``groups:read``

   **파일**:

   - ``files:read``

   **권한 동기화**\ (``permission_sync=true``):

   - ``users:read.email``

2. 앱 재설치
3. |Fess| 재시작

파일을 크롤링할 수 없음
-----------------------

**증상**: ``file_crawl=true``\ 인데도 파일이 가져와지지 않음

**확인 사항**:

1. ``files:read`` 스코프가 부여되어 있는지 확인
2. 채널에 실제로 파일이 게시되어 있는지 확인
3. 파일의 액세스 권한 확인
4. ``max_filesize`` 를 초과하는 파일은 다운로드되지 않습니다(로그의 경고를 확인하세요)

API 속도 제한
-------------

**증상**: ``ratelimited``\ (크롤링 작업 전체가 실패합니다)

**해결 방법**:

1. ``max_retry_count``, ``retry_interval`` 의 기본값으로 해결되지 않으면 값을 늘림
2. ``read_interval`` 을 설정하여 크롤링 속도를 늦춤
3. 채널 수를 줄이거나, 데이터 스토어를 여러 개로 분할하여 스케줄을 분산

Slack API의 ``ratelimited`` 오류는 ``Retry-After`` 헤더가 있으면 그 초수, 없으면
``retry_interval`` 을 기점으로 두 배씩 늘어나는 백오프(``max_retry_count`` 회까지, 최대
60초)로 자동으로 재시도됩니다. 재시도를 모두 사용해도 속도 제한이 해소되지 않으면 크롤링
작업 전체가 실패합니다.

Slack API의 Tier(호출 가능 횟수의 상한):

- Tier 1: 1+ 요청/분
- Tier 2: 20+ 요청/분 — ``conversations.list``, ``users.list``\ (크롤링 시작 시 무조건
  전량 취득하므로 가장 고갈되기 쉽습니다)
- Tier 3: 50+ 요청/분 — ``conversations.history``, ``conversations.replies``,
  ``files.list``
- Tier 4: 100+ 요청/분 — ``conversations.members``\ (``permission_sync=true`` 일 때만),
  ``files.info``\ (이 커넥터의 크롤링에서는 현재 호출되지 않습니다)

.. note::

   2025년 5월 29일자 Slack의 레이트 리밋 강화(``conversations.history``,
   ``conversations.replies`` 두 메서드를 50+ 요청/분으로 제한)는 Slack Marketplace 등
   생성한 워크스페이스 밖으로 배포되는 앱에만 적용됩니다. |Fess| 용으로 만들어, 생성한
   워크스페이스에만 설치하는 사내 앱에는 적용되지 않습니다.

대량의 메시지가 있는 경우
-------------------------

**증상**: 크롤링에 시간이 오래 걸리거나 타임아웃됨

**해결 방법**:

1. 채널을 분할하여 여러 데이터 스토어 설정
2. 크롤링 스케줄 분산

스크립트 응용 예
================

메시지 가공
-----------

긴 메시지 요약:

::

    title=message.user + " #" + message.channel
    content=message.text
    digest=message.text.length() > 100 ? message.text.substring(0, 100) + "..." : message.text
    created=message.timestamp
    url=message.permalink

채널명 정리:

::

    title="[Slack: " + message.channel + "] " + message.user
    content=message.text
    created=message.timestamp
    url=message.permalink

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-atlassian` - Atlassian 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../security-role` - 역할 기반 검색 설정 가이드
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
- `Slack API Rate Limits <https://docs.slack.dev/apis/web-api/rate-limits>`_
