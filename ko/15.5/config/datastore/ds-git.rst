==================================
Git 커넥터
==================================

개요
====

Git 커넥터는 Git 리포지토리의 파일을 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-git`` 플러그인이 필요합니다.

지원 리포지토리
==============

- GitHub(퍼블릭/프라이빗)
- GitLab(퍼블릭/프라이빗)
- Bitbucket(퍼블릭/프라이빗)
- 로컬 Git 리포지토리
- 기타 Git 호스팅 서비스

전제조건
========

1. 플러그인 설치가 필요합니다
2. 프라이빗 리포지토리의 경우 인증 정보가 필요합니다
3. 리포지토리에 대한 읽기 액세스 권한이 필요합니다

플러그인 설치
------------------------

관리 화면의 "시스템" → "플러그인"에서 설치합니다.

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
     - Project Git Repository
   * - 핸들러 이름
     - GitDataStore
   * - 활성화
     - 켬

파라미터 설정
----------------

퍼블릭 리포지토리 예:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    prev_commit_id=
    delete_old_docs=false

프라이빗 리포지토리 예(인증 있음):

::

    uri=https://username:personal_access_token@github.com/company/private-repo.git
    base_url=https://github.com/company/private-repo/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    prev_commit_id=
    delete_old_docs=false

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``uri``
     - 예
     - Git 리포지토리의 URI(clone용)
   * - ``base_url``
     - 예
     - 파일 표시용 기본 URL
   * - ``extractors``
     - 아니오
     - MIME 타입별 추출기 설정
   * - ``prev_commit_id``
     - 아니오
     - 이전 커밋 ID(차등 크롤링용)
   * - ``delete_old_docs``
     - 아니오
     - 삭제된 파일을 인덱스에서 삭제(기본값: ``false``)

스크립트 설정
--------------

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    cache=""
    digest=author.toExternalString()
    anchor=
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

사용 가능한 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``url``
     - 파일 URL
   * - ``path``
     - 리포지토리 내 파일 경로
   * - ``name``
     - 파일명
   * - ``content``
     - 파일 텍스트 콘텐츠
   * - ``contentLength``
     - 콘텐츠 길이
   * - ``timestamp``
     - 최종 수정 일시
   * - ``mimetype``
     - 파일 MIME 타입
   * - ``author``
     - 최종 커밋자 정보

Git 리포지토리 인증
===================

GitHub Personal Access Token
-----------------------------

1. GitHub에서 Personal Access Token 생성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://github.com/settings/tokens 에 접속:

1. "Generate new token" → "Generate new token (classic)" 클릭
2. 토큰명 입력(예: Fess Crawler)
3. 범위에서 "repo" 체크
4. "Generate token" 클릭
5. 생성된 토큰 복사

2. URI에 인증 정보 포함
~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:ghp_abc123def456ghi789jkl012@github.com/company/repo.git

GitLab Private Token
--------------------

1. GitLab에서 Access Token 생성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GitLab의 User Settings → Access Tokens:

1. 토큰명 입력
2. 범위에서 "read_repository" 체크
3. "Create personal access token" 클릭
4. 생성된 토큰 복사

2. URI에 인증 정보 포함
~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:glpat-abc123def456@gitlab.com/company/repo.git

SSH 인증
-------

SSH 키를 사용하는 경우:

::

    uri=git@github.com:company/repo.git

.. note::
   SSH 인증을 사용하는 경우, |Fess|를 실행하는 사용자의 SSH 키를 설정해야 합니다.

추출기 설정
============

MIME 타입별 추출기
--------------------

``extractors`` 파라미터로 파일 타입별 추출기를 지정:

::

    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,application/json:textExtractor,

형식: ``<MIME 타입 정규표현식>:<추출기명>,``

기본 추출기
~~~~~~~~~~~~~~~~~~

- ``textExtractor`` - 텍스트 파일용
- ``tikaExtractor`` - 바이너리 파일용(PDF, Word 등)

텍스트 파일만 크롤링
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=text/.*:textExtractor,

모든 파일 크롤링
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=.*:tikaExtractor,

특정 파일 타입만
~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Markdown, YAML, JSON만
    extractors=text/markdown:textExtractor,text/yaml:textExtractor,application/json:textExtractor,

차등 크롤링
============

이전 커밋 이후 변경 사항만 크롤링
------------------------------------

초기 크롤링 후 ``prev_commit_id``에 이전 커밋 ID를 설정:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    prev_commit_id=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
    delete_old_docs=true

.. note::
   커밋 ID는 마지막 크롤링 시점의 커밋 ID를 설정합니다.
   이렇게 하면 해당 커밋 이후의 변경 사항만 크롤링됩니다.

삭제된 파일 처리
------------------------

``delete_old_docs=true``를 설정하면 Git 리포지토리에서 삭제된 파일이
인덱스에서도 삭제됩니다.

사용 예
======

GitHub 퍼블릭 리포지토리
--------------------------

파라미터:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    delete_old_docs=false

스크립트:

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    last_modified=timestamp
    mimetype=mimetype

GitHub 프라이빗 리포지토리
----------------------------

파라미터:

::

    uri=https://username:ghp_abc123def456ghi789jkl012@github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    delete_old_docs=false

스크립트:

::

    url=url
    title=name
    content=content
    digest=author.toExternalString()
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

GitLab(셀프 호스팅)
----------------------

파라미터:

::

    uri=https://username:glpat-abc123@gitlab.company.com/team/project.git
    base_url=https://gitlab.company.com/team/project/-/blob/main/
    extractors=text/.*:textExtractor,
    prev_commit_id=
    delete_old_docs=false

스크립트:

::

    url=url
    host="gitlab.company.com"
    site="gitlab.company.com/team/project/" + path
    title=name
    content=content
    last_modified=timestamp

문서만 크롤링(Markdown 파일)
--------------------------------------------

파라미터:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/markdown:textExtractor,text/plain:textExtractor,
    delete_old_docs=false

스크립트:

::

    if (mimetype.startsWith("text/")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
    }

특정 디렉토리만 크롤링
------------------------------

스크립트로 필터링:

::

    if (path.startsWith("docs/") || path.startsWith("README")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
        mimetype=mimetype
    }

문제 해결
======================

인증 오류
----------

**증상**: ``Authentication failed`` 또는 ``Not authorized``

**확인 사항**:

1. Personal Access Token이 올바른지 확인
2. 토큰에 적절한 권한이 있는지 확인(``repo`` 범위)
3. URI 형식이 올바른지 확인:

   ::

       # 올바름
       uri=https://username:token@github.com/company/repo.git

       # 잘못됨
       uri=https://github.com/company/repo.git?token=...

4. 토큰 유효기간 확인

리포지토리를 찾을 수 없음
------------------------

**증상**: ``Repository not found``

**확인 사항**:

1. 리포지토리 URL이 올바른지 확인
2. 리포지토리가 존재하고 삭제되지 않았는지 확인
3. 인증 정보가 올바른지 확인
4. 리포지토리에 대한 액세스 권한이 있는지 확인

파일을 가져올 수 없음
----------------------

**증상**: 크롤링은 성공하지만 파일이 0개

**확인 사항**:

1. ``extractors`` 설정이 적절한지 확인
2. 리포지토리에 파일이 존재하는지 확인
3. 스크립트 설정이 올바른지 확인
4. 대상 브랜치에 파일이 존재하는지 확인

MIME 타입 오류
----------------

**증상**: 특정 파일이 크롤링되지 않음

**해결 방법**:

추출기 설정 조정:

::

    # 모든 파일 대상
    extractors=.*:tikaExtractor,

    # 특정 MIME 타입 추가
    extractors=text/.*:textExtractor,application/json:textExtractor,application/xml:textExtractor,

대형 리포지토리
----------------

**증상**: 크롤링에 시간이 오래 걸리거나 메모리 부족

**해결 방법**:

1. ``extractors``로 대상 파일 제한
2. 스크립트로 특정 디렉토리만 필터링
3. 차등 크롤링 사용(``prev_commit_id`` 설정)
4. 크롤링 간격 조정

브랜치 지정
--------------

기본 브랜치 외를 크롤링하는 경우:

::

    uri=https://github.com/company/repo.git#develop
    base_url=https://github.com/company/repo/blob/develop/

``#`` 뒤에 브랜치명을 지정합니다.

URL 생성
=========

base_url 설정 패턴
----------------------

**GitHub**:

::

    base_url=https://github.com/user/repo/blob/master/

**GitLab**:

::

    base_url=https://gitlab.com/user/repo/-/blob/main/

**Bitbucket**:

::

    base_url=https://bitbucket.org/user/repo/src/master/

``base_url``과 파일 경로가 결합되어 URL이 생성됩니다.

스크립트에서 URL 생성
---------------------

::

    url=base_url + path
    title=name
    content=content

또는 커스텀 URL:

::

    url="https://github.com/mycompany/repo/blob/main/" + path
    title=name
    content=content

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-database` - 데이터베이스 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `GitHub Personal Access Tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
- `GitLab Personal Access Tokens <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_
