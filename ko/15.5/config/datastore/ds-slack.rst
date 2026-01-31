==================================
Slack 커넥터
==================================

개요
====

Slack 커넥터는 Slack 워크스페이스의 채널 메시지를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-slack`` 플러그인이 필요합니다.

지원 콘텐츠
==============

- 퍼블릭 채널 메시지
- 프라이빗 채널 메시지
- 파일 첨부(옵션)

전제조건
========

1. 플러그인 설치가 필요합니다
2. Slack App 생성과 권한 설정이 필요합니다
3. OAuth Access Token 취득이 필요합니다

플러그인 설치
------------------------

관리 화면의 "시스템" → "플러그인"에서 설치합니다:

1. Maven Central에서 ``fess-ds-slack-X.X.X.jar``를 다운로드
2. 플러그인 관리 화면에서 업로드하여 설치
3. |Fess| 재시작

또는 자세한 내용은 :doc:`../../admin/plugin-guide` 를 참조하세요.

설정 방법
========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 설정합니다.

기본 설정
--------

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
----------------

::

    token=xoxp-your-token-here
    channels=general,random
    file_crawl=false
    include_private=false

파라미터 목록
~~~~~~~~~~~~~~~~

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
     - 예
     - 크롤링 대상 채널(쉼표 구분 또는 ``*all``)
   * - ``file_crawl``
     - 아니오
     - 파일도 크롤링(기본값: ``false``)
   * - ``include_private``
     - 아니오
     - 프라이빗 채널도 포함(기본값: ``false``)

스크립트 설정
--------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

사용 가능한 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``message.text``
     - 메시지 텍스트 콘텐츠
   * - ``message.user``
     - 메시지 발신자의 표시 이름
   * - ``message.channel``
     - 메시지가 전송된 채널명
   * - ``message.timestamp``
     - 메시지 전송 일시
   * - ``message.permalink``
     - 메시지의 퍼머링크
   * - ``message.attachments``
     - 첨부 파일의 폴백 정보

Slack App 설정
=============

1. Slack App 생성
------------------

https://api.slack.com/apps 에 접속:

1. "Create New App" 클릭
2. "From scratch" 선택
3. 앱 이름 입력(예: Fess Crawler)
4. 워크스페이스 선택
5. "Create App" 클릭

2. OAuth & Permissions 설정
----------------------------

"OAuth & Permissions" 메뉴에서:

**Bot Token Scopes**에 다음을 추가:

퍼블릭 채널만의 경우:

- ``channels:history`` - 퍼블릭 채널 메시지 읽기
- ``channels:read`` - 퍼블릭 채널 정보 읽기

프라이빗 채널도 포함하는 경우(``include_private=true``):

- ``channels:history``
- ``channels:read``
- ``groups:history`` - 프라이빗 채널 메시지 읽기
- ``groups:read`` - 프라이빗 채널 정보 읽기

파일도 크롤링하는 경우(``file_crawl=true``):

- ``files:read`` - 파일 콘텐츠 읽기

3. 앱 설치
-----------------------

"Install App" 메뉴에서:

1. "Install to Workspace" 클릭
2. 권한 확인 후 "허용" 클릭
3. "Bot User OAuth Token" 복사(``xoxb-``로 시작)

.. note::
   보통은 ``xoxb-``로 시작하는 Bot User OAuth Token을 사용하지만,
   파라미터에서는 ``xoxp-``로 시작하는 User OAuth Token도 사용 가능합니다.

4. 채널에 추가
---------------------

크롤링 대상 채널에 App을 추가:

1. Slack에서 채널 열기
2. 채널 이름 클릭
3. "통합" 탭 선택
4. "앱 추가" 클릭
5. 생성한 앱 추가

사용 예
======

특정 채널 크롤링
--------------------------

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
----------------------------

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
--------------------------------------

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
------------------------

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
----------------------------

스크립트:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

문제 해결
======================

인증 오류
----------

**증상**: ``invalid_auth`` 또는 ``not_authed``

**확인 사항**:

1. 토큰이 올바르게 복사되었는지 확인
2. 토큰 형식 확인:

   - Bot User OAuth Token: ``xoxb-``로 시작
   - User OAuth Token: ``xoxp-``로 시작

3. 앱이 워크스페이스에 설치되어 있는지 확인
4. 필요한 권한이 부여되어 있는지 확인

채널을 찾을 수 없음
------------------------

**증상**: ``channel_not_found``

**확인 사항**:

1. 채널명이 올바른지 확인(#은 불필요)
2. 앱이 채널에 추가되어 있는지 확인
3. 프라이빗 채널인 경우 ``include_private=true`` 설정
4. 채널이 존재하고 아카이브되지 않았는지 확인

메시지를 가져올 수 없음
------------------------

**증상**: 크롤링은 성공하지만 메시지가 0개

**확인 사항**:

1. 필요한 범위가 부여되어 있는지 확인:

   - ``channels:history``
   - ``channels:read``
   - 프라이빗 채널인 경우: ``groups:history``, ``groups:read``

2. 채널에 메시지가 존재하는지 확인
3. 앱이 채널에 추가되어 있는지 확인
4. Slack 앱이 활성화되어 있는지 확인

권한 부족 오류
--------------

**증상**: ``missing_scope``

**해결 방법**:

1. Slack App 설정에서 필요한 범위 추가:

   **퍼블릭 채널**:

   - ``channels:history``
   - ``channels:read``

   **프라이빗 채널**:

   - ``groups:history``
   - ``groups:read``

   **파일**:

   - ``files:read``

2. 앱 재설치
3. |Fess| 재시작

파일을 크롤링할 수 없음
--------------------------

**증상**: ``file_crawl=true``인데도 파일이 가져와지지 않음

**확인 사항**:

1. ``files:read`` 범위가 부여되어 있는지 확인
2. 채널에 실제로 파일이 게시되어 있는지 확인
3. 파일의 액세스 권한 확인

API 속도 제한
-------------

**증상**: ``rate_limited``

**해결 방법**:

1. 크롤링 간격을 늘림
2. 채널 수를 줄임
3. 데이터 스토어를 여러 개로 분할하여 스케줄 분산

Slack API 제한:

- Tier 3 메서드: 50+ 요청/분
- Tier 4 메서드: 100+ 요청/분

대량의 메시지가 있는 경우
--------------------------

**증상**: 크롤링에 시간이 오래 걸리거나 타임아웃됨

**해결 방법**:

1. 채널을 분할하여 여러 데이터 스토어 설정
2. 크롤링 스케줄 분산
3. 오래된 메시지를 제외하는 설정 고려

스크립트 고급 사용 예
========================

메시지 필터링
--------------------------

특정 사용자의 메시지만 인덱싱:

::

    if (message.user == "홍길동") {
        title=message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

키워드를 포함하는 메시지만:

::

    if (message.text.contains("중요") || message.text.contains("장애")) {
        title="[중요] " + message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

메시지 가공
----------------

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
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-atlassian` - Atlassian 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
