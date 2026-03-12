==================================
Google Workspace 커넥터
==================================

개요
====

Google Workspace 커넥터는 Google Drive(구 G Suite)에서 파일을 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-gsuite`` 플러그인이 필요합니다.

지원 서비스
============

- Google Drive(마이 드라이브, 공유 드라이브)
- Google 문서, 스프레드시트, 프레젠테이션, 설문지 등

전제조건
========

1. 플러그인 설치가 필요합니다
2. Google Cloud Platform 프로젝트 생성이 필요합니다
3. 서비스 계정 생성과 인증 정보 취득이 필요합니다
4. Google Workspace 도메인 전체 위임 설정이 필요합니다

플러그인 설치
------------------------

방법 1: JAR 파일 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # 배치
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

방법 2: 관리 화면에서 설치

1. "시스템" → "플러그인" 열기
2. JAR 파일 업로드
3. |Fess| 재시작

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
     - Company Google Drive
   * - 핸들러 이름
     - GSuiteDataStore
   * - 활성화
     - 켬

파라미터 설정
----------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``private_key``
     - 예
     - 서비스 계정의 비밀 키(PEM 형식, 줄바꿈은 ``\n``)
   * - ``private_key_id``
     - 예
     - 비밀 키 ID
   * - ``client_email``
     - 예
     - 서비스 계정의 이메일 주소

스크립트 설정
--------------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.url
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

사용 가능한 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``file.name``
     - 파일명
   * - ``file.description``
     - 파일 설명
   * - ``file.contents``
     - 파일 텍스트 콘텐츠
   * - ``file.mimetype``
     - 파일 MIME 타입
   * - ``file.filetype``
     - 파일 타입
   * - ``file.created_time``
     - 생성 일시
   * - ``file.modified_time``
     - 최종 수정 일시
   * - ``file.web_view_link``
     - 브라우저에서 열기 링크
   * - ``file.url``
     - 파일 URL
   * - ``file.thumbnail_link``
     - 썸네일 링크(단기간 유효)
   * - ``file.size``
     - 파일 크기(바이트)
   * - ``file.roles``
     - 액세스 권한

자세한 내용은 `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_를 참조하세요.

Google Cloud Platform 설정
=========================

1. 프로젝트 생성
---------------------

https://console.cloud.google.com/ 에 접속:

1. 새 프로젝트 생성
2. 프로젝트 이름 입력
3. 조직과 위치 선택

2. Google Drive API 활성화
---------------------------

"API 및 서비스" → "라이브러리"에서:

1. "Google Drive API" 검색
2. "사용 설정" 클릭

3. 서비스 계정 생성
---------------------------

"API 및 서비스" → "사용자 인증 정보"에서:

1. "사용자 인증 정보 만들기" → "서비스 계정" 선택
2. 서비스 계정 이름 입력(예: fess-crawler)
3. "만들기 및 계속" 클릭
4. 역할은 설정 불필요(건너뛰기)
5. "완료" 클릭

4. 서비스 계정 키 생성
-------------------------------

생성한 서비스 계정에서:

1. 서비스 계정 클릭
2. "키" 탭 열기
3. "키 추가" → "새 키 만들기"
4. JSON 형식 선택
5. 다운로드된 JSON 파일 저장

5. 도메인 전체 위임 활성화
-----------------------------

서비스 계정 설정에서:

1. "도메인 전체 위임 활성화" 체크
2. "저장" 클릭
3. "OAuth 2 클라이언트 ID" 복사

6. Google Workspace 관리 콘솔에서 승인
---------------------------------------

https://admin.google.com/ 에 접속:

1. "보안" → "액세스 및 데이터 관리" → "API 제어" 열기
2. "도메인 전체 위임" 선택
3. "새로 추가" 클릭
4. 클라이언트 ID 입력
5. OAuth 범위 입력:

   ::

       https://www.googleapis.com/auth/drive.readonly

6. "승인" 클릭

인증 정보 설정
==============

JSON 파일에서 정보 취득
--------------------------

다운로드한 JSON 파일:

::

    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...\n-----END PRIVATE KEY-----\n",
      "client_email": "fess-crawler@your-project.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
    }

다음 정보를 파라미터에 설정:

- ``private_key_id`` → ``private_key_id``
- ``private_key`` → ``private_key`` (줄바꿈은 그대로 ``\n``)
- ``client_email`` → ``client_email``

비밀 키 형식
~~~~~~~~~~~~

``private_key``는 줄바꿈을 ``\n``으로 유지합니다:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

사용 예
======

Google Drive 전체 크롤링
--------------------------

파라미터:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com

스크립트:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    filename=file.name

권한 포함 크롤링
----------------

파라미터:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

스크립트:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    role=file.roles
    filename=file.name

특정 파일 타입만 크롤링
--------------------------------

Google 문서만:

::

    if (file.mimetype == "application/vnd.google-apps.document") {
        title=file.name
        content=file.description + "\n" + file.contents
        mimetype=file.mimetype
        created=file.created_time
        last_modified=file.modified_time
        url=file.web_view_link
    }

문제 해결
======================

인증 오류
----------

**증상**: ``401 Unauthorized`` 또는 ``403 Forbidden``

**확인 사항**:

1. 서비스 계정 인증 정보가 올바른지 확인:

   - ``private_key``의 줄바꿈이 ``\n``으로 되어 있는지
   - ``private_key_id``가 올바른지
   - ``client_email``이 올바른지

2. Google Drive API가 활성화되어 있는지 확인
3. 도메인 전체 위임이 설정되어 있는지 확인
4. Google Workspace 관리 콘솔에서 승인되었는지 확인
5. OAuth 범위가 올바른지 확인(``https://www.googleapis.com/auth/drive.readonly``)

도메인 전체 위임 오류
------------------------

**증상**: ``Not Authorized to access this resource/api``

**해결 방법**:

1. Google Workspace 관리 콘솔에서 승인 확인:

   - 클라이언트 ID가 올바르게 등록되어 있는지
   - OAuth 범위가 올바른지(``https://www.googleapis.com/auth/drive.readonly``)

2. 서비스 계정에서 도메인 전체 위임이 활성화되어 있는지 확인

파일을 가져올 수 없음
----------------------

**증상**: 크롤링은 성공하지만 파일이 0개

**확인 사항**:

1. Google Drive에 파일이 존재하는지 확인
2. 서비스 계정에 읽기 권한이 있는지 확인
3. 도메인 전체 위임이 올바르게 설정되어 있는지 확인
4. 대상 사용자의 Drive에 액세스 가능한지 확인

API 할당량 오류
-----------------

**증상**: ``403 Rate Limit Exceeded`` 또는 ``429 Too Many Requests``

**해결 방법**:

1. Google Cloud Platform에서 할당량 확인
2. 크롤링 간격을 늘림
3. 필요 시 할당량 증가 요청

비밀 키 형식 오류
--------------------------

**증상**: ``Invalid private key format``

**해결 방법**:

줄바꿈이 올바르게 ``\n``으로 되어 있는지 확인:

::

    # 올바름
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # 잘못됨(실제 줄바꿈이 포함되어 있음)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

공유 드라이브 크롤링
----------------------

.. note::
   서비스 계정으로 공유 드라이브를 크롤링하는 경우,
   공유 드라이브에 서비스 계정을 멤버로 추가해야 합니다.

1. Google Drive에서 공유 드라이브 열기
2. "멤버 관리" 클릭
3. 서비스 계정 이메일 주소 추가
4. 권한 수준을 "뷰어"로 설정

대량의 파일이 있는 경우
------------------------

**증상**: 크롤링에 시간이 오래 걸리거나 타임아웃됨

**해결 방법**:

1. 데이터 스토어를 여러 개로 분할
2. 스케줄 설정으로 부하 분산
3. 크롤링 간격 조정
4. 특정 폴더만 크롤링

권한과 액세스 제어
==================

Google Drive 공유 권한 반영
----------------------------

Google Drive 공유 설정을 Fess 권한에 반영:

파라미터:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

스크립트:

::

    title=file.name
    content=file.description + "\n" + file.contents
    role=file.roles
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link

``file.roles``에 Google Drive 공유 정보가 포함됩니다.

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-microsoft365` - Microsoft 365 커넥터
- :doc:`ds-box` - Box 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
