==================================
Dropbox 커넥터
==================================

개요
====

Dropbox 커넥터는 Dropbox 클라우드 스토리지에서 파일을 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-dropbox`` 플러그인이 필요합니다.

지원 서비스
============

- Dropbox (파일 스토리지)
- Dropbox Paper (문서)

전제 조건
=========

1. 플러그인 설치가 필요합니다
2. Dropbox 개발자 계정과 애플리케이션 생성이 필요합니다
3. 액세스 토큰 취득이 필요합니다

플러그인 설치
-------------

관리 화면의 "시스템" → "플러그인"에서 설치합니다:

1. Maven Central에서 ``fess-ds-dropbox-X.X.X.jar`` 를 다운로드
2. 플러그인 관리 화면에서 업로드하여 설치
3. |Fess| 를 재시작

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
     - Company Dropbox
   * - 핸들러 이름
     - DropboxDataStore 또는 DropboxPaperDataStore
   * - 활성화
     - 켬

파라미터 설정
-------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

파라미터 목록
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``access_token``
     - 예
     - Dropbox 액세스 토큰 (App Console에서 생성)
   * - ``basic_plan``
     - 아니오
     - 개인 계정인 경우 ``true``, 팀 계정인 경우 ``false`` (기본값: ``false``)
   * - ``max_size``
     - 아니오
     - 인덱싱 대상 최대 파일 크기 (바이트) (기본값: ``10000000``)
   * - ``number_of_threads``
     - 아니오
     - 크롤링에 사용할 스레드 수 (기본값: ``1``)
   * - ``ignore_folder``
     - 아니오
     - 폴더 메타데이터를 건너뛸지 여부 (기본값: ``true``)
   * - ``ignore_error``
     - 아니오
     - 콘텐츠 추출 중 오류를 무시할지 여부 (기본값: ``true``)
   * - ``supported_mimetypes``
     - 아니오
     - 허용할 MIME 타입의 정규식 패턴 (쉼표 구분) (기본값: ``.*``)
   * - ``include_pattern``
     - 아니오
     - 크롤링에 포함할 URL 패턴
   * - ``exclude_pattern``
     - 아니오
     - 크롤링에서 제외할 URL 패턴
   * - ``default_permissions``
     - 아니오
     - 인덱싱된 문서의 기본 권한 (쉼표 구분)
   * - ``max_cached_content_size``
     - 아니오
     - 메모리에 캐시할 콘텐츠 최대 크기 (바이트). 이 크기를 초과하는 콘텐츠는 임시 파일에 기록됩니다 (기본값: ``1048576``)
   * - ``readInterval``
     - 아니오
     - 각 레코드를 처리하는 사이에 삽입할 대기 시간 (밀리초) (기본값: ``0``)

스크립트 설정
-------------

Dropbox 파일의 경우
~~~~~~~~~~~~~~~~~~~

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

사용 가능한 필드:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``file.url``
     - 파일 미리보기 링크
   * - ``file.contents``
     - 파일 텍스트 콘텐츠
   * - ``file.mimetype``
     - 파일 MIME 타입
   * - ``file.filetype``
     - 파일 타입
   * - ``file.name``
     - 파일명
   * - ``file.path_display``
     - 파일 경로
   * - ``file.size``
     - 파일 크기 (바이트)
   * - ``file.client_modified``
     - 클라이언트 측 최종 수정 일시
   * - ``file.server_modified``
     - 서버 측 최종 수정 일시
   * - ``file.roles``
     - 파일 액세스 권한
   * - ``file.id``
     - Dropbox 파일 ID
   * - ``file.path_lower``
     - 소문자 파일 경로
   * - ``file.parent_shared_folder_id``
     - 상위 공유 폴더 ID
   * - ``file.content_hash``
     - 콘텐츠 해시
   * - ``file.rev``
     - 파일 리비전

Dropbox Paper의 경우
~~~~~~~~~~~~~~~~~~~~

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

사용 가능한 필드:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``paper.url``
     - Paper 문서 미리보기 링크
   * - ``paper.contents``
     - Paper 문서 텍스트 콘텐츠
   * - ``paper.mimetype``
     - MIME 타입
   * - ``paper.filetype``
     - 파일 타입
   * - ``paper.title``
     - Paper 문서 제목
   * - ``paper.owner``
     - Paper 문서 소유자
   * - ``paper.roles``
     - 문서 액세스 권한
   * - ``paper.revision``
     - Paper 문서 리비전

Dropbox 인증 설정
=================

계정 종류와 액세스 토큰
-----------------------

이 커넥터는 ``basic_plan`` 파라미터에 따라 두 가지 동작 모드로 전환됩니다.
생성해야 할 앱과 액세스 토큰의 종류가 다르므로 먼저 확인하세요.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 모드
     - ``basic_plan``
     - 설명
   * - 팀 계정 (기본값)
     - ``false``
     - Dropbox Business (팀) 계정용입니다. 팀 관리자 권한을 가진 액세스 토큰이 필요하며, 팀 멤버의 파일과 팀 폴더를 전체에 걸쳐 크롤링합니다.
   * - 개인 계정
     - ``true``
     - 개인 (비팀) 계정용입니다. 일반 범위 지정 액세스 토큰을 사용하여 해당 계정 내 파일을 직접 크롤링합니다.

.. note::
   기본값 (``basic_plan=false``) 에서는 팀 관리용 API (팀 멤버 목록, 멤버 단위 파일 액세스, 팀 폴더) 를 사용하므로
   Dropbox Business 계정과 팀 관리자 권한을 가진 토큰이 필수입니다. 개인 계정을 사용하는 경우 반드시 ``basic_plan=true`` 를 설정하세요.

액세스 토큰 취득 절차
---------------------

1. Dropbox App Console에서 앱 생성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://www.dropbox.com/developers/apps 에 접속:

1. "Create app"을 클릭
2. API 타입에서 "Scoped access"를 선택
3. 액세스 타입을 선택 (팀 계정을 전체에 걸쳐 크롤링하는 경우 "Full Dropbox" 권장)
4. 앱 이름을 입력하고 생성

2. 권한 설정
~~~~~~~~~~~~

"Permissions" 탭에서 필요한 권한을 선택:

**파일 및 Paper 크롤링에 필요한 권한**:

- ``files.metadata.read`` - 파일 메타데이터 읽기
- ``files.content.read`` - 파일 및 Paper 문서 콘텐츠 읽기
- ``sharing.read`` - 공유 정보 읽기

**팀 계정 (``basic_plan=false``) 에서 추가로 필요한 권한**:

- ``members.read`` - 팀 멤버 목록 읽기
- 팀 데이터/팀 스페이스 액세스 권한 (멤버 단위 파일 및 팀 폴더 크롤링에 필요)

.. note::
   팀 계정 모드에서는 팀 관리자로서 각 멤버와 팀 폴더에 액세스합니다.
   Permissions 탭에서 위의 팀 관련 권한을 활성화하고 팀 관리자 토큰을 생성하세요.

3. 액세스 토큰 생성
~~~~~~~~~~~~~~~~~~~

"Settings" 탭에서:

1. "Generated access token" 섹션까지 스크롤
2. "Generate" 버튼을 클릭
3. 생성된 토큰을 복사 (이 토큰은 한 번만 표시됩니다)

.. warning::
   액세스 토큰은 안전하게 보관하세요. 이 토큰이 있으면
   Dropbox 계정에 액세스할 수 있습니다.

4. 토큰 설정
~~~~~~~~~~~~

취득한 토큰을 파라미터에 설정:

::

    access_token=sl.your-dropbox-token-here

개인 계정 설정
==============

개인 계정 사용
--------------

개인 계정 (팀 계정이 아닌 경우) 에서는
``basic_plan`` 파라미터를 ``true`` 로 설정하세요:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

``false`` (기본값) 인 경우 팀 계정으로 동작하여 팀 멤버와 팀 폴더의 파일을 크롤링합니다.
``true`` 인 경우 개인 계정으로 동작하여 계정 내 파일을 직접 크롤링합니다.

사용 예
=======

Dropbox 파일 전체 크롤링
------------------------

파라미터:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

스크립트:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified

Dropbox Paper 문서 크롤링
-------------------------

파라미터:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

스크립트:

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

권한 포함 크롤링
----------------

파라미터:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    default_permissions={role}admin

스크립트 (Dropbox 파일):

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

스크립트 (Dropbox Paper):

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

특정 파일 타입만 크롤링
-----------------------

특정 MIME 타입만을 인덱싱 대상으로 하려면 ``supported_mimetypes`` 파라미터에
허용할 MIME 타입의 정규식을 쉼표로 구분하여 지정합니다.

.. note::
   데이터 스토어 스크립트는 한 줄씩 ``필드명=식`` 의 독립된 식으로 평가됩니다.
   따라서 여러 줄에 걸친 ``if`` 블록으로 여러 필드를 한꺼번에 대입할 수 없습니다.
   MIME 타입에 따른 필터링은 스크립트가 아닌 ``supported_mimetypes`` 파라미터로 수행하세요.

파라미터 (PDF 및 Word 파일만):

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    supported_mimetypes=application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document

스크립트:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

문제 해결
=========

인증 오류
---------

**증상**: ``Invalid access token`` 또는 ``401 Unauthorized``

**확인 사항**:

1. 액세스 토큰이 올바르게 복사되었는지 확인
2. 토큰 유효기간이 만료되지 않았는지 확인 (장기 토큰 사용)
3. Dropbox App Console에서 필요한 권한이 부여되었는지 확인
4. 앱이 비활성화되지 않았는지 확인

파일을 가져올 수 없음
---------------------

**증상**: 크롤링은 성공하지만 파일이 0건

**확인 사항**:

1. 앱의 "Access type"이 적절한지 확인:

   - "Full Dropbox": Dropbox 전체에 액세스 가능
   - "App folder": 특정 폴더만 액세스 가능

2. 필요한 권한이 부여되었는지 확인:

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Dropbox 계정에 파일이 존재하는지 확인

API 속도 제한 오류
------------------

**증상**: ``429 Too Many Requests`` 오류

**해결 방법**:

1. ``readInterval`` 을 설정하여 각 파일 처리 간격을 벌림
2. ``number_of_threads`` 를 줄여 동시 요청 수를 감소
3. 데이터 스토어를 폴더 단위 등으로 여러 개로 분할하고 스케줄을 분산하여 실행

.. note::
   ``basic_plan`` 은 계정 종류 (팀/개인) 를 전환하는 파라미터이며
   속도 제한 조정에는 영향을 미치지 않습니다. 계정에 맞게 올바르게 설정하세요.

Paper 문서를 가져올 수 없음
---------------------------

**증상**: Paper 문서가 크롤링되지 않음

**확인 사항**:

1. 핸들러 이름이 ``DropboxPaperDataStore`` 인지 확인
2. 권한에 ``files.content.read`` 가 포함되어 있는지 확인
3. Paper 문서가 실제로 존재하는지 확인

대량의 파일이 있는 경우
-----------------------

**증상**: 크롤링에 시간이 오래 걸리거나 타임아웃됨

**해결 방법**:

1. 데이터 스토어를 여러 개로 분할 (폴더 단위 등)
2. 스케줄 설정으로 부하 분산
3. Basic 플랜인 경우 API 속도 제한에 주의

권한과 액세스 제어
==================

Dropbox 공유 권한 반영
----------------------

Dropbox 공유 설정을 Fess 권한에 반영할 수 있습니다:

파라미터:

::

    access_token=sl.your-dropbox-token-here
    default_permissions={role}dropbox-users

스크립트:

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.roles
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

``file.roles`` 또는 ``paper.roles`` 에 Dropbox 공유 정보가 포함됩니다.

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-box` - Box 커넥터
- :doc:`ds-gsuite` - Google Workspace 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
