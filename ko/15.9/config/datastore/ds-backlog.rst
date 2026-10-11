==================================
Backlog 커넥터
==================================

개요
====

Backlog 커넥터는 Backlog 스페이스의 이슈, Wiki 페이지, 문서, 파일을 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.
API 키로 스페이스에 인증합니다.
색인된 각 문서는 해당 Backlog 프로젝트의 멤버만 검색할 수 있도록 제한됩니다(아래 "권한" 참조).

이 기능을 사용하려면 ``fess-ds-backlog`` 플러그인이 필요합니다.

지원 콘텐츠
===========

- 이슈(댓글 포함)
- Wiki 페이지
- 문서
- 이슈, Wiki 페이지, 문서의 첨부 파일
- 프로젝트의 공유 파일

크롤링은 매번 전체 크롤링입니다. 기본적으로 Backlog에서 사라진 문서는 크롤링이 끝날 때 삭제되지 않고,
유효 기간이 지났을 때 삭제됩니다("삭제된 콘텐츠와 취소된 접근 권한" 참조).

전제조건
========

1. 플러그인 설치가 필요합니다
2. 크롤링 전용 Backlog 사용자와 그 API 키가 필요합니다
3. 그 사용자를 크롤링 대상의 모든 프로젝트 멤버로 추가해야 합니다

플러그인 설치
-------------

관리 화면의 "시스템" → "플러그인"에서 설치하거나, ``bin/fess-setup install plugin fess-ds-backlog`` 을 실행한 후
|Fess| 를 재시작합니다.
자세한 내용은 :doc:`../../admin/plugin-guide` 를 참조하세요.

Backlog 측 설정
---------------

1. 크롤링 전용 Backlog 사용자를 만들고 그 API 키를 발급합니다("개인 설정" → "API").
   크롤링에는 이 사용자에게 보이는 것이 그대로 보입니다.
2. 크롤링 대상의 모든 프로젝트에 그 사용자를 추가합니다. 커넥터는 사용자가 참여하지 않은 프로젝트를 가져오지 않습니다.
   스페이스 관리자라도 마찬가지입니다.
3. 제한이 없는 역할(관리자 또는 일반 사용자)을 사용자에게 부여합니다. 제한이 있는 역할에서는 기능에 따라 Backlog가 HTTP 403을 반환합니다.
   "보기만 가능" 사용자는 이슈의 첨부 파일을 다운로드할 수 없고, 공유 파일을 다운로드할 수 있는 것은 제한이 없는 사용자뿐입니다.
   이런 403에서는 커넥터가 프로젝트와 기능마다 경고를 한 건 로그에 출력하고, 해당 프로젝트의 그 기능
   (이슈 첨부 파일, Wiki 첨부 파일, 문서 첨부 파일, 공유 파일)을 건너뛰고 나머지 크롤링을 계속합니다.
4. 스페이스가 API 접근에 2단계 인증을 요구하는 경우 Backlog는 오류 코드 12
   (RequiredMFAError)를 반환하며 크롤링은 중단됩니다.

API 키는 ``Backlog-API-Key`` 요청 헤더로만 전송됩니다. 스크립트에 전달되지 않고,
이 커넥터가 로그에 출력하지도 않습니다. HTTP 리디렉션은 따르지 않으므로 키가 스페이스의 호스트 밖으로 나가는 일은 없습니다.

.. warning::

   ``org.codelibs.curl`` 로거의 ``FINE`` 로그를 활성화하지 마세요. HTTP 클라이언트는 그 레벨에서 요청 헤더를 로그에 출력하며,
   마스킹하는 것은 ``Authorization`` 이나 ``Cookie`` 같은 헤더뿐이므로 ``Backlog-API-Key`` 헤더가 로그에 기록됩니다.

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
     - Company Backlog
   * - 핸들러 이름
     - BacklogDataStore
   * - 권한
     - (비워 둡니다. "권한" 참조)
   * - 활성화
     - 켬

파라미터 설정
-------------

::

    api_key=**********************************************
    space_url=https://example.backlog.com

파라미터 목록
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``api_key``
     - 예
     - Backlog API 키. 스크립트에 전달되지 않으며 로그에도 출력되지 않습니다
   * - ``space_url``
     - 예
     - 스페이스의 URL(예: ``https://example.backlog.com``). ``https`` 만 지정할 수 있으며 스킴과 호스트만 지정합니다(끝의 슬래시는 무시됩니다). 지정하지 않았거나 형식이 잘못되었거나 ``http`` 이면 크롤링이 중단됩니다
   * - ``project_keys``
     - 아니오
     - 크롤링 대상 프로젝트 키의 쉼표 구분 목록(대소문자 구분 없음). 비어 있으면 사용자에게 보이는 모든 프로젝트를 크롤링합니다. 사용자에게 보이지 않는 키는 경고로 로그에 출력됩니다
   * - ``include_archived``
     - 아니오
     - 보관된 프로젝트도 크롤링합니다(기본값: ``false``)
   * - ``include_issues``
     - 아니오
     - 이슈를 색인합니다(기본값: ``true``)
   * - ``include_comments``
     - 아니오
     - 이슈의 댓글을 이슈 문서에 포함합니다(기본값: ``true``)
   * - ``include_wikis``
     - 아니오
     - Wiki가 활성화된 프로젝트에서 Wiki 페이지를 색인합니다(기본값: ``true``)
   * - ``include_documents``
     - 아니오
     - 문서가 활성화된 프로젝트에서 문서를 색인합니다(기본값: ``true``)
   * - ``include_attachments``
     - 아니오
     - 이슈, Wiki 페이지, 문서의 첨부 파일을 다운로드해서 색인합니다(기본값: ``true``)
   * - ``include_shared_files``
     - 아니오
     - 파일 공유가 활성화된 프로젝트에서 공유 파일을 다운로드해서 색인합니다(기본값: ``true``)
   * - ``permission_sync``
     - 아니오
     - 프로젝트의 각 문서에 프로젝트 멤버마다 하나의 ``{user}`` 역할을 부여합니다(기본값: ``true``). "권한"을 참조하세요
   * - ``default_permissions``
     - 아니오
     - 모든 문서에 추가할 권한의 쉼표 구분 목록(``{user}name``, ``{group}name``, ``{role}name``)
   * - ``max_file_size``
     - 아니오
     - 이 바이트 수를 초과하는 파일은 건너뛰고 색인하지 않습니다(기본값: ``10485760``)
   * - ``include_pattern``
     - 아니오
     - ``backlog.url`` 이 일치해야 색인되는 정규식
   * - ``exclude_pattern``
     - 아니오
     - ``backlog.url`` 이 일치하면 안 되는 정규식. 이슈, Wiki 페이지, 문서가 제외되면 그 첨부 파일도 건너뜁니다
   * - ``request_interval``
     - 아니오
     - 각 API 요청 전에 대기하는 밀리초(기본값: ``200``)
   * - ``search_request_interval``
     - 아니오
     - 검색형 요청(이슈 목록, Wiki 목록) 사이의 최소 간격(밀리초). Backlog는 클라이언트에 1초 이상 간격을 두도록 요청합니다(기본값: ``1000``)
   * - ``max_retry_count``
     - 아니오
     - HTTP 429, 5xx, 연결 실패의 재시도 횟수(기본값: ``5``)
   * - ``connection_timeout``
     - 아니오
     - 연결 타임아웃(밀리초, 기본값: ``10000``)
   * - ``read_timeout``
     - 아니오
     - 읽기 타임아웃(밀리초, 기본값: ``30000``)
   * - ``ignore_error``
     - 아니오
     - 다운로드한 파일의 텍스트 추출에 실패했을 때 실패로 기록하지 않고 빈 콘텐츠로 색인합니다(기본값: ``true``)

.. note::

   잘못된 값(숫자가 아닌 값, 음수인 간격이나 재시도 횟수, 0 이하의 타임아웃이나 ``max_file_size``, ``true`` / ``false`` 이외의 불리언 값)은
   경고를 로그에 출력하고 기본값을 사용합니다.
   ``request_interval``, ``search_request_interval``, ``max_retry_count`` 에서는 ``0`` 도 유효합니다.

스크립트 설정
-------------

::

    title=backlog.title
    content=backlog.content
    url=backlog.url
    mimetype=backlog.mimetype
    created=backlog.created
    last_modified=backlog.updated
    role=backlog.roles

.. important::

   프로젝트 멤버로의 제한을 적용하려면 ``role=backlog.roles`` 가 필수입니다.
   지정하지 않으면 인덱스에 반영되는 것은 데이터 스토어 설정의 "권한" 필드 값뿐입니다.

사용 가능한 필드
~~~~~~~~~~~~~~~~

모든 문서는 스크립트에서 ``backlog`` 객체로 참조할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 필드
     - 유형
     - 설명
   * - ``backlog.type``
     - 전체
     - ``issue``, ``wiki``, ``document``, ``attachment``, ``file`` 중 하나
   * - ``backlog.id``
     - 전체
     - 이슈, Wiki 페이지, 문서, 첨부 파일, 공유 파일의 Backlog상 ID
   * - ``backlog.project_key``, ``backlog.project_name``
     - 전체
     - 프로젝트
   * - ``backlog.title``
     - 전체
     - 이슈는 ``[KEY-1] 요약``. 그 외에는 페이지 이름, 문서 제목, 파일 이름
   * - ``backlog.content``
     - 전체
     - 이슈: 설명, 속성, 사용자 정의 필드, 댓글. Wiki 페이지: 페이지 내용. 문서: 일반 텍스트. 첨부 파일과 파일: 추출한 텍스트
   * - ``backlog.url``
     - 전체
     - "URL" 참조
   * - ``backlog.mimetype``
     - 전체
     - 이슈, Wiki 페이지, 문서는 ``text/plain``. 파일은 감지된 유형
   * - ``backlog.created``, ``backlog.updated``
     - 전체
     - ISO 8601 형식의 UTC 일시(Backlog가 반환한 경우)
   * - ``backlog.created_by``, ``backlog.updated_by``
     - 전체
     - 사용자 이름(Backlog가 반환한 경우)
   * - ``backlog.roles``
     - 전체
     - 검색 역할("권한" 참조)
   * - ``backlog.issue_key``, ``backlog.issue_type``, ``backlog.status``, ``backlog.priority``, ``backlog.assignee``
     - 이슈
     - 이슈의 속성(이름)
   * - ``backlog.categories``, ``backlog.milestones``, ``backlog.versions``
     - 이슈
     - 이름의 목록
   * - ``backlog.custom_fields``
     - 이슈
     - 사용자 정의 필드 이름에서 값 텍스트로의 맵
   * - ``backlog.comments``
     - 이슈
     - ``작성자: 내용`` 형식의 댓글 텍스트(빈 줄로 구분)
   * - ``backlog.tags``
     - Wiki 페이지, 문서
     - 태그 이름의 목록
   * - ``backlog.parent_type``, ``backlog.parent_url``, ``backlog.parent_title``
     - 첨부 파일
     - 첨부 파일이 속한 이슈, Wiki 페이지, 문서
   * - ``backlog.size``
     - 첨부 파일, 파일
     - 다운로드한 바이트 수
   * - ``backlog.path``
     - 파일
     - 공유 파일의 경로(예: ``/docs/spec.pdf``)

URL
---

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 유형
     - URL
   * - 이슈
     - ``{space_url}/view/{ISSUE-KEY}``
   * - Wiki 페이지
     - ``{space_url}/alias/wiki/{ID}``
   * - 문서
     - ``{space_url}/document/{PROJECT}/{ID}``
   * - 파일
     - ``{space_url}/file/{PROJECT}{디렉터리}{이름}`` (경로의 각 세그먼트는 퍼센트 인코딩됩니다)
   * - 첨부 파일
     - ``{상위 항목의 URL}#attachment-{ID}``

.. note::

   문서와 공유 파일의 URL 형식, 그리고 문서 첨부 파일의 다운로드용 엔드포인트는
   실제 Backlog 스페이스에서 확인되지 않았습니다. 링크가 기대한 페이지를 열지 않더라도
   문서는 색인되어 검색할 수 있습니다. 잘못된 것은 링크 대상뿐입니다.

권한
====

``permission_sync=true`` (기본값)이면 프로젝트의 모든 문서에 다음 역할이 부여됩니다:

- 프로젝트 각 멤버의 ``mailAddress`` 에 대한 ``{user}`` 역할과 ``userId`` 에 대한 ``{user}`` 역할(빈 값은 제외).
  멤버는 둘 중 어느 쪽으로든 |Fess| 에 로그인할 수 있습니다
- ``default_permissions`` 의 값
- 데이터 스토어 설정의 "권한" 필드 값

프로젝트 멤버를 가져올 수 없거나 멤버 중 누구도 사용 가능한 ``mailAddress`` 또는 ``userId`` 를 갖고 있지 않으면
프로젝트 전체를 건너뛰고 "크롤러" → "장애 URL"에 기록합니다. 멤버 역할 없이 색인되는 일은 없습니다.

``permission_sync=false`` 이면 ``default_permissions`` 와 "권한" 필드만 적용됩니다.

.. warning::

   데이터 스토어 설정의 "권한" 필드를 비워 두세요. 관리 화면은 이 필드에 ``{role}guest`` 를 미리 채워 두는데,
   이 역할은 익명 검색 사용자를 포함한 모든 사용자가 가지고 있습니다. 그대로 두면 모든 문서의 역할에 합쳐져서
   Backlog의 모든 콘텐츠를 누구나 검색할 수 있게 됩니다.
   ``permission_sync=true`` 일 때, 게스트 역할이 포함된 프로젝트마다 커넥터가 경고를 로그에 출력합니다.

멤버 역할에 의존하기 전에 다음 점에 유의하세요:

- 멤버의 식별자는 |Fess| 의 로그인 이름으로 취급됩니다. Backlog의 ``userId`` 가 ``tanaka`` 이면 |Fess| 의 로그인 이름이 ``tanaka`` 인 사람에게 접근이 허용되지만,
  같은 사람이라는 보장은 없습니다(예: LDAP이나 Active Directory의 계정 이름). ``mailAddress`` 역할에는 이 문제가 없습니다.
  ``permission_sync`` 는 |Fess| 의 로그인 이름이 Backlog의 사용자 ID 또는 메일 주소와 일치하는 환경에서만 사용하세요.
- 게스트 역할이나 다른 로그인에 대응되어 버리는 식별자를 가진 멤버는 프로젝트와 멤버 ID를 알리는 경고를 출력하고 무시됩니다.
  ``userId`` 가 ``guest`` 인 경우와 백슬래시를 포함하는 식별자가 해당됩니다(|Fess| 는 사용자 이름에서 백슬래시까지를 제거합니다).
- 프로젝트 멤버는 모두 첨부 파일과 공유 파일을 포함해 프로젝트의 색인된 모든 항목을 검색으로 찾을 수 있습니다.
  Backlog 자체가 그 멤버에게 다운로드를 허용하지 않는 경우("보기만 가능" 사용자는 이슈 첨부 파일을 다운로드할 수 없음)에도 마찬가지입니다.
  역할은 기능 단위가 아니라 프로젝트 단위입니다.

삭제된 콘텐츠와 취소된 접근 권한
================================

기본적으로 |Fess| 는 각 문서에 유효 기간(일반 설정의 "이전 문서 삭제", 기본값 3일)을 지정하고,
유효 기간이 있는 문서는 크롤링이 끝날 때 삭제하지 않습니다. 유효 기간이 지난 문서는 Doc Purger 가 삭제합니다. 따라서 기본적으로 다음과 같이 동작합니다:

- Backlog에서 삭제한 콘텐츠는 최대 약 3일간 검색할 수 있는 상태로 남습니다
- 멤버가 프로젝트에서 빠져도 그 멤버는 이미 색인된 프로젝트의 문서에 최대 약 3일간 접근할 수 있습니다.
  다음 크롤링에서 같은 문서가 새 문서 ID로 색인되고(ID에는 역할 목록이 포함됩니다), 이전 역할을 가진 이전 문서는 유효 기간이 지날 때까지 남습니다.
  그동안 나머지 멤버에게는 중복된 검색 결과가 표시됩니다

크롤링이 끝날 때 이런 문서를 삭제하려면 데이터 스토어 설정의 파라미터에 ``keep_expires_docs=false`` 를 추가하세요.
|Fess| 는 그 크롤링에서 다시 색인되지 않은 해당 설정의 모든 문서를 삭제합니다. 이는 크롤링이 도달하지 못한 모든 문서에도 적용됩니다("오류 처리" 참조).

사용 예
=======

특정 프로젝트를 크롤링
----------------------

파라미터:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    project_keys=PROJ,DOCS
    include_shared_files=false

이슈와 Wiki 페이지만(첨부 파일 제외)
------------------------------------

파라미터:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    include_documents=false
    include_attachments=false
    include_shared_files=false

Backlog에서 삭제한 문서를 크롤링이 끝날 때 삭제
-----------------------------------------------

파라미터:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    keep_expires_docs=false

오류 처리
=========

- 크롤링이 중단되는 것은 HTTP ``401``, Backlog 오류 코드 11 (AuthenticationError) 또는 12 (RequiredMFAError),
  ``api_key`` 또는 ``space_url`` 의 누락이나 오류, 프로젝트 목록 가져오기 실패인 경우뿐입니다.
- HTTP ``429`` 에서는 ``X-RateLimit-Reset`` 헤더가 나타내는 시각까지 대기한 후 재시도합니다(최대 120초. 헤더가 없으면 60초).
  HTTP ``5xx`` 와 연결 실패에서는 지수 백오프(1초, 2초, 4초, 최대 60초)로 재시도합니다.
  ``max_retry_count`` 만큼의 재시도를 소진하면 그 항목은 실패가 됩니다.
- 그 외의 실패(``403``, ``404``, 재시도 소진)는 해당 항목 하나에 대해 기록되며 크롤링은 계속됩니다.
- 항목의 실패로 크롤링 작업이 실패하지는 않습니다. 크롤링 후에 "크롤러" → "장애 URL"과 크롤러 로그를 확인하세요.
- ``keep_expires_docs=false`` 이면 실패한 부분의 콘텐츠는 다시 색인되지 않으므로 그 크롤링이 끝날 때 삭제됩니다.
  실패한 목록 가져오기, 건너뛴 프로젝트, 403으로 건너뛴 기능 아래의 모든 콘텐츠가, 실패 없이 크롤링이 완료될 때까지 인덱스에서 사라집니다.
  크롤링이 중단된 경우도 마찬가지입니다. 기본적으로 이런 콘텐츠는 유효 기간이 지날 때까지 검색할 수 있는 상태로 남습니다.

문제 해결
=========

크롤링이 시작할 때 중단됨
-------------------------

1. ``api_key`` 가 올바르고 이 스페이스의 사용자용으로 발급된 것인지 확인합니다
2. ``space_url`` 이 호스트만 있는 ``https`` URL(예: ``https://example.backlog.com``)인지 확인합니다
3. 스페이스가 API 접근에 2단계 인증을 요구하는 경우 크롤링은 RequiredMFAError로 중단됩니다

프로젝트가 색인되지 않음
------------------------

1. API 사용자가 그 프로젝트의 멤버인지 확인합니다
2. ``permission_sync=true`` 이면 멤버를 가져올 수 없는 프로젝트나, 멤버 중 누구도 사용 가능한 메일 주소 또는 사용자 ID를 갖고 있지 않은 프로젝트는 건너뜁니다. "크롤러" → "장애 URL"을 확인하세요
3. ``project_keys`` 와 ``include_archived`` 를 확인합니다

첨부 파일이나 공유 파일이 없음
------------------------------

제한이 없는 역할을 API 사용자에게 부여하세요. HTTP 403으로 건너뛴 프로젝트와 기능마다 로그에 경고가 한 건 출력됩니다.

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-atlassian` - Atlassian 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../../admin/failureurl-guide` - 장애 URL
- :doc:`../../admin/plugin-guide` - 플러그인 관리 가이드
- `Backlog API Documentation <https://developer.nulab.com/docs/backlog/>`_
