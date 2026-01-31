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

전제조건
========

1. 플러그인 설치가 필요합니다
2. Dropbox 개발자 계정과 애플리케이션 생성이 필요합니다
3. 액세스 토큰 취득이 필요합니다

플러그인 설치
------------------------

관리 화면의 "시스템" → "플러그인"에서 설치합니다:

1. Maven Central에서 ``fess-ds-dropbox-X.X.X.jar``를 다운로드
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
     - Company Dropbox
   * - 핸들러 이름
     - DropboxDataStore 또는 DropboxPaperDataStore
   * - 활성화
     - 켬

파라미터 설정
----------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

파라미터 목록
~~~~~~~~~~~~~~~~

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
     - Basic 플랜인 경우 ``true`` (기본값: ``false``)

스크립트 설정
--------------

Dropbox 파일의 경우
~~~~~~~~~~~~~~~~~~~~~

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

Dropbox Paper의 경우
~~~~~~~~~~~~~~~~~~~

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

Dropbox 인증 설정
=================

액세스 토큰 취득 절차
--------------------------

1. Dropbox App Console에서 앱 생성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://www.dropbox.com/developers/apps 에 접속:

1. "Create app"을 클릭
2. API 타입에서 "Scoped access"를 선택
3. 액세스 타입에서 "Full Dropbox" 또는 "App folder"를 선택
4. 앱 이름을 입력하고 생성

2. 권한 설정
~~~~~~~~~~~~~

"Permissions" 탭에서 필요한 권한을 선택:

**파일 크롤링에 필요한 권한**:

- ``files.metadata.read`` - 파일 메타데이터 읽기
- ``files.content.read`` - 파일 콘텐츠 읽기
- ``sharing.read`` - 공유 정보 읽기

**Paper 크롤링에 추가로 필요한 권한**:

- ``files.content.read`` - Paper 문서 읽기

3. 액세스 토큰 생성
~~~~~~~~~~~~~~~~~~~~~~~~~

"Settings" 탭에서:

1. "Generated access token" 섹션까지 스크롤
2. "Generate" 버튼 클릭
3. 생성된 토큰 복사 (이 토큰은 한 번만 표시됩니다)

.. warning::
   액세스 토큰은 안전하게 보관하세요. 이 토큰이 있으면
   Dropbox 계정에 액세스할 수 있습니다.

4. 토큰 설정
~~~~~~~~~~~~~~~~~

취득한 토큰을 파라미터에 설정:

::

    access_token=sl.your-dropbox-token-here

Basic 플랜 설정
=================

Dropbox Basic 플랜 제한
-------------------------

Dropbox Basic 플랜의 경우 API 제한이 다릅니다.
``basic_plan`` 파라미터를 ``true``로 설정하세요:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

이렇게 하면 API 속도 제한에 대응한 처리가 수행됩니다.

사용 예
======

Dropbox 파일 전체 크롤링
------------------------------

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
-----------------------------------

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
--------------------------------

스크립트로 필터링:

::

    # PDF와 Word 파일만
    if (file.mimetype == "application/pdf" || file.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        last_modified=file.client_modified
    }

문제 해결
======================

인증 오류
----------

**증상**: ``Invalid access token`` 또는 ``401 Unauthorized``

**확인 사항**:

1. 액세스 토큰이 올바르게 복사되었는지 확인
2. 토큰 유효기간이 만료되지 않았는지 확인 (장기 토큰 사용)
3. Dropbox App Console에서 필요한 권한이 부여되었는지 확인
4. 앱이 비활성화되지 않았는지 확인

파일을 가져올 수 없음
----------------------

**증상**: 크롤링은 성공하지만 파일이 0개

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
-------------------

**증상**: ``429 Too Many Requests`` 오류

**해결 방법**:

1. Basic 플랜인 경우 ``basic_plan=true`` 설정
2. 크롤링 간격을 늘림
3. 여러 액세스 토큰을 사용하여 부하 분산

Paper 문서를 가져올 수 없음
-------------------------------

**증상**: Paper 문서가 크롤링되지 않음

**확인 사항**:

1. 핸들러 이름이 ``DropboxPaperDataStore``인지 확인
2. 권한에 ``files.content.read``가 포함되어 있는지 확인
3. Paper 문서가 실제로 존재하는지 확인

대량의 파일이 있는 경우
------------------------

**증상**: 크롤링에 시간이 오래 걸리거나 타임아웃됨

**해결 방법**:

1. 데이터 스토어를 여러 개로 분할 (폴더 단위 등)
2. 스케줄 설정으로 부하 분산
3. Basic 플랜인 경우 API 속도 제한에 주의

권한과 액세스 제어
==================

Dropbox 공유 권한 반영
-----------------------

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

``file.roles`` 또는 ``paper.roles``에 Dropbox 공유 정보가 포함됩니다.

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-box` - Box 커넥터
- :doc:`ds-gsuite` - Google Workspace 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
