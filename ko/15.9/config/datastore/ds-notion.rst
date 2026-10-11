==================================
Notion 커넥터
==================================

개요
====

Notion 커넥터는 Notion의 페이지와 데이터베이스 행을 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.
Notion 내부 통합(internal integration)으로 인증하고, 그 통합에 공유된 모든 콘텐츠를 색인 대상으로 합니다.

이 기능을 사용하려면 ``fess-ds-notion`` 플러그인이 필요합니다.

지원 콘텐츠
===========

- 페이지(블록의 텍스트)
- 데이터베이스 행(속성 값 포함)
- Notion에 호스팅된 파일 블록과 PDF 블록의 첨부 파일(각각 독립된 문서로 색인)
- 페이지의 미해결 댓글(페이지 문서에 포함)

다음은 대상에서 제외됩니다:

- Notion에서 링크만 걸려 있는 파일(외부 파일). 다운로드하는 것은 Notion에 호스팅된 ``file`` 블록과 ``pdf`` 블록뿐입니다
- Notion 휴지통에 있는 페이지와 데이터베이스 행
- 페이지 단위의 접근 제어(아래 "권한" 참조)

전제조건
========

1. 플러그인 설치가 필요합니다
2. Notion 내부 통합 생성이 필요합니다
3. 크롤링 대상 페이지와 데이터베이스를 통합에 공유해야 합니다

플러그인 설치
-------------

관리 화면의 "시스템" → "플러그인"에서 설치하거나, ``bin/fess-setup install plugin fess-ds-notion`` 을 실행한 후
|Fess| 를 재시작합니다.
자세한 내용은 :doc:`../../admin/plugin-guide` 를 참조하세요.

Notion 통합 설정
----------------

1. Notion에서 내부 통합을 생성하고 "Internal Integration Secret"을 복사합니다.
2. 통합의 설정 페이지(Configuration)에서 다음 기능(capability)을 활성화합니다:

   .. list-table::
      :header-rows: 1
      :widths: 25 25 50

      * - 기능
        - 필수
        - 용도
      * - Read content
        - 항상 필수
        - 페이지, 블록, 데이터베이스, 데이터베이스 행 읽기. 활성화하지 않으면 모든 요청이 ``401 unauthorized`` 로 실패하고 크롤링이 즉시 중단됩니다
      * - Read comments
        - ``include_comments=true`` (기본값)인 경우만
        - 페이지 댓글 가져오기. 활성화하지 않으면 경고를 한 번 로그에 출력하고 해당 크롤링의 나머지 동안 댓글 크롤링을 비활성화합니다. 크롤링 자체는 실패하지 않습니다
      * - Read user information
        - 선택
        - 사용자 ID(``created_by``, ``last_edited_by``, ``people`` 속성)를 표시 이름으로 변환. 활성화하지 않으면 이름 대신 사용자 ID가 색인됩니다

3. 크롤링 대상 페이지와 데이터베이스를 모두 Notion에서 통합에 공유합니다.
   기능을 추가하는 것만으로는 어떤 콘텐츠에도 접근할 수 없습니다.

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
     - Company Notion
   * - 핸들러 이름
     - NotionDataStore
   * - 활성화
     - 켬

파라미터 설정
-------------

::

    token=secret_************************************

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
     - 내부 통합 시크릿(Internal Integration Secret). 스크립트에 전달되지 않으며 로그에도 출력되지 않습니다
   * - ``root_page_ids``
     - 아니오
     - 크롤링의 시작점으로 삼을 페이지 ID의 쉼표 구분 목록. 이 파라미터와 ``database_ids`` 가 모두 비어 있으면 Notion 검색으로 통합에 공유된 모든 페이지와 데이터베이스를 탐색합니다
   * - ``database_ids``
     - 아니오
     - 크롤링의 시작점으로 삼을 데이터베이스 ID의 쉼표 구분 목록. 각 데이터베이스의 모든 행을 색인합니다
   * - ``include_comments``
     - 아니오
     - 각 페이지의 미해결 댓글을 가져와서 그 텍스트를 ``notion.content`` 와 ``notion.comments`` 에 포함합니다(기본값: ``true``)
   * - ``include_files``
     - 아니오
     - Notion에 호스팅된 ``file`` 블록과 ``pdf`` 블록의 첨부 파일을 다운로드해 텍스트를 추출하고, 각각을 독립된 문서로 색인합니다(기본값: ``true``)
   * - ``max_file_size``
     - 아니오
     - 이 바이트 수를 초과하는 첨부 파일은 빈 콘텐츠로도 색인하지 않고 완전히 건너뜁니다(기본값: ``10485760``)
   * - ``include_pattern``
     - 아니오
     - 문서의 ``notion.url`` 이 일치해야 색인되는 정규식("크롤링 범위" 참조)
   * - ``exclude_pattern``
     - 아니오
     - 문서의 ``notion.url`` 이 일치하면 안 되는 정규식("크롤링 범위" 참조)
   * - ``request_interval``
     - 아니오
     - Notion의 속도 제한(초당 약 3회 요청)을 넘지 않도록 각 API 요청 전에 대기하는 밀리초(기본값: ``350``)
   * - ``max_retry_count``
     - 아니오
     - ``429``, ``5xx``, ``529`` 응답 또는 타임아웃 같은 통신 오류가 발생한 요청의 최대 재시도 횟수(기본값: ``5``)
   * - ``connection_timeout``
     - 아니오
     - 각 API 요청의 연결 타임아웃(밀리초, 기본값: ``10000``)
   * - ``read_timeout``
     - 아니오
     - 각 API 요청의 읽기 타임아웃(밀리초, 기본값: ``30000``)
   * - ``ignore_error``
     - 아니오
     - 다운로드한 첨부 파일의 텍스트 추출에 실패했을 때 문서를 실패로 처리하지 않고 빈 콘텐츠로 색인합니다(기본값: ``true``). 다운로드 실패는 이 설정과 관계없이 항상 문서의 실패가 됩니다

.. note::

   숫자 파라미터에 빈 값이나 숫자가 아닌 값을 지정하면 경고를 로그에 출력하고 기본값을 사용합니다.
   ``request_interval`` 과 ``max_retry_count`` 에 음수를 지정한 경우(``0`` 은 둘 다 유효)와
   ``true`` / ``false`` 파라미터에 다른 값을 지정한 경우도 마찬가지입니다.

스크립트 설정
-------------

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time
    created=notion.created_time

사용 가능한 필드
~~~~~~~~~~~~~~~~

페이지, 데이터베이스 행, 첨부 파일 등 모든 문서는 스크립트에서 ``notion`` 객체로 참조할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``notion.type``
     - 페이지 또는 데이터베이스 행은 ``page``, 첨부 파일은 ``file``
   * - ``notion.id``
     - 페이지 ID. 첨부 파일의 경우 블록 ID
   * - ``notion.title``
     - 페이지 제목(이름에 관계없이 유형이 ``title`` 인 속성). 첨부 파일의 경우 파일 이름
   * - ``notion.content``
     - 페이지의 경우: 제목 이외의 속성 값(데이터베이스 행만), 블록의 텍스트, 댓글 텍스트를 연결한 것. 첨부 파일의 경우: 추출한 텍스트
   * - ``notion.url``
     - 페이지의 Notion URL. 첨부 파일의 경우 포함된 페이지의 URL 끝에 ``#<블록 ID>`` 를 붙인 것
   * - ``notion.mimetype``
     - 페이지는 ``text/html``, 첨부 파일은 감지된 MIME 타입
   * - ``notion.created_time``
     - 페이지의 생성 일시. 첨부 파일에서는 사용할 수 없습니다
   * - ``notion.last_edited_time``
     - 페이지(또는 첨부 파일 블록)의 마지막 편집 일시
   * - ``notion.created_by``
     - 페이지 작성자. Notion이 이름을 반환한 경우 이름, 그렇지 않으면 사용자 ID. 첨부 파일에서는 사용할 수 없습니다
   * - ``notion.last_edited_by``
     - 마지막 편집자(같은 형식). 첨부 파일에서는 사용할 수 없습니다
   * - ``notion.parent_id``
     - 상위 페이지, 데이터베이스, 데이터 소스, 블록의 ID. 워크스페이스 바로 아래의 페이지는 비어 있음. 첨부 파일에서는 사용할 수 없습니다
   * - ``notion.properties``
     - 데이터베이스 행의 열 이름에서 서식이 적용된 텍스트로의 맵. 일반 페이지는 비어 있음. 첨부 파일에서는 사용할 수 없습니다
   * - ``notion.comments``
     - 페이지의 댓글 텍스트를 연결한 것. ``include_comments=false`` 이거나 댓글이 없으면 비어 있음. 첨부 파일에서는 사용할 수 없습니다
   * - ``notion.page_url``
     - 포함된 페이지의 URL. 첨부 파일 전용
   * - ``notion.page_title``
     - 포함된 페이지의 제목. 첨부 파일 전용
   * - ``notion.size``
     - 첨부 파일의 바이트 수(Notion이 반환한 경우). 첨부 파일 전용

크롤링 범위
===========

- ``root_page_ids`` 와 ``database_ids`` 를 모두 지정하지 않으면 Notion 검색으로 통합에 공유된 모든 페이지와 데이터베이스를 탐색합니다.
  Notion 검색은 모든 것을 빠짐없이 반환한다고 보장되지 않습니다. 색인에 없는 콘텐츠가 있으면 ``root_page_ids`` 또는 ``database_ids`` 를 명시적으로 지정하세요.
- 각 시작점에서 도달할 수 있는 하위 페이지와 하위 데이터베이스도 모두 크롤링하므로, 보통은 루트 페이지 하나만 지정해도 워크스페이스의 한 섹션 전체에 도달합니다.
- ``include_pattern`` 과 ``exclude_pattern`` 이 결정하는 것은 해당 페이지(또는 첨부 파일) 자신의 문서를 색인할지 여부뿐입니다.
  하위 항목의 탐색은 멈추지 않습니다. 페이지의 블록은 페이지 자신의 URL에 패턴을 적용하기 전에 항상 순회하므로,
  제외된 페이지의 하위 페이지도 각자의 URL로 계속 크롤링되어 색인됩니다.
  하위 트리 전체를 제외하려면 루트뿐 아니라 그 아래의 모든 URL에 일치하는 패턴을 지정하세요.
- Notion 휴지통에 있는 페이지와 데이터베이스 행은 건너뜁니다.

권한
====

Notion API는 페이지의 공유 설정을 제공하지 않으므로, 이 커넥터는 페이지 단위의 접근 제어를 동기화할 수 없습니다.
모든 문서는 데이터 스토어 설정의 "권한" 필드에 설정한 권한만으로 색인됩니다.

.. warning::

   통합에 공유한 모든 콘텐츠는 Notion에서 누가 볼 수 있는지와 관계없이, 이 필드에서 허용한 역할이 검색할 수 있게 됩니다.
   그 역할이 검색해도 되는 페이지와 데이터베이스만 통합에 공유하세요.

오류 처리
=========

- 크롤링이 중단되는 것은 HTTP ``401`` (토큰으로 인증할 수 없음) 또는 ``public_api_request_blocked`` 를 나타내는 ``429`` 응답
  (Notion의 속도 제한이 통합을 차단함)인 경우뿐입니다.
  ``root_page_ids`` 도 ``database_ids`` 도 지정하지 않았을 때 Notion 검색이 실패하면 시작점이 없으므로 크롤링이 중단됩니다.
- 그 외의 실패는 문서 단위로 처리됩니다. 하나의 페이지, 데이터베이스, 댓글 스레드, 블록에 대한 ``404`` 나 ``403``,
  하나의 요청에서 ``max_retry_count`` 를 모두 소진한 경우는 로그에 기록하고 건너뛰며 크롤링을 계속합니다.
- 문서 단위의 실패는 해당 문서의 URL(페이지는 Notion URL, 첨부 파일은 ``<페이지 URL>#<블록 ID>``)로
  "크롤러" → "장애 URL"에 기록됩니다.
  첨부 파일의 서명된 다운로드 URL은 기록되지도 로그에 출력되지도 않습니다.
- 파라미터에 ``keep_expires_docs=false`` 를 지정하면 크롤링에서 다시 색인되지 않은 데이터 스토어의 문서는 크롤링이 끝날 때 삭제됩니다.
  중단된 크롤링도 마찬가지입니다.
  기본적으로 문서에는 유효 기간이 지정되며, 그 기간이 지날 때까지 인덱스에 남습니다.

사용 예
=======

특정 페이지 트리를 크롤링
-------------------------

파라미터:

::

    token=secret_************************************
    root_page_ids=0123456789abcdef0123456789abcdef
    include_comments=false

스크립트:

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time

데이터베이스를 크롤링
---------------------

파라미터:

::

    token=secret_************************************
    database_ids=fedcba9876543210fedcba9876543210
    include_files=false

스크립트:

::

    title=notion.title
    content=notion.content
    url=notion.url
    created=notion.created_time
    last_modified=notion.last_edited_time

통합에 공유된 모든 것을 크롤링
------------------------------

파라미터:

::

    token=secret_************************************
    request_interval=500

문제 해결
=========

크롤링이 ``401`` 로 즉시 중단됨
-------------------------------

토큰이 통합의 "Internal Integration Secret"인지, "Read content" 기능이 활성화되어 있는지 확인하세요.

색인에 없는 페이지가 있음
-------------------------

1. 페이지 또는 데이터베이스가 통합에 공유되어 있는지 확인합니다
2. 자동 탐색에 의존하고 있다면 Notion 검색이 모든 것을 반환한다고 보장되지 않으므로 ``root_page_ids`` 또는 ``database_ids`` 를 명시적으로 지정합니다
3. ``include_pattern`` 과 ``exclude_pattern`` 을 확인합니다
4. "크롤러" → "장애 URL"에서 개별적으로 실패한 문서를 확인합니다

댓글이 색인되지 않음
--------------------

통합의 "Read comments" 기능을 활성화하세요. 활성화하지 않으면 경고를 한 번 로그에 출력하고 해당 크롤링에서는 댓글을 건너뜁니다.
색인되는 것은 미해결 댓글뿐입니다.

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-slack` - Slack 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../../admin/failureurl-guide` - 장애 URL
- :doc:`../../admin/plugin-guide` - 플러그인 관리 가이드
- `Notion API Documentation <https://developers.notion.com/>`_
