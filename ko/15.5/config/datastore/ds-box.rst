==================================
Box 커넥터
==================================

개요
====

Box 커넥터는 Box.com의 클라우드 스토리지에서 파일을 가져와
|Fess| 의 인덱스에 등록하는 기능을 제공합니다.

이 기능에는 ``fess-ds-box`` 플러그인이 필요합니다.

전제 조건
========

1. 플러그인 설치가 필요합니다
2. Box 개발자 계정 및 애플리케이션 생성이 필요합니다
3. JWT(JSON Web Token) 인증 또는 OAuth 2.0 인증 설정이 필요합니다

플러그인 설치
------------------------

방법 1: JAR 파일 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # 배치
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

방법 2: 관리 화면에서 설치

1. "시스템" → "플러그인" 열기
2. JAR 파일 업로드
3. |Fess| 재시작

설정 방법
========

관리 화면에서 "크롤러" → "데이터스토어" → "신규 작성"으로 설정합니다.

기본 설정
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - Company Box Storage
   * - 핸들러 이름
     - BoxDataStore
   * - 사용
     - 켜기

파라미터 설정
----------------

JWT 인증 예(권장):

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

파라미터 목록
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``client_id``
     - 예
     - Box 앱의 클라이언트 ID
   * - ``client_secret``
     - 예
     - Box 앱의 클라이언트 시크릿
   * - ``public_key_id``
     - 예
     - 공개키 ID
   * - ``private_key``
     - 예
     - 비밀키 (PEM 형식, 개행은 ``\n`` 으로 표현)
   * - ``passphrase``
     - 예
     - 비밀키의 패스프레이즈
   * - ``enterprise_id``
     - 예
     - Box 엔터프라이즈 ID

스크립트 설정
--------------

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

사용 가능한 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``file.url``
     - 브라우저에서 파일을 여는 링크
   * - ``file.contents``
     - 파일의 텍스트 콘텐츠
   * - ``file.mimetype``
     - 파일의 MIME 타입
   * - ``file.filetype``
     - 파일 타입
   * - ``file.name``
     - 파일명
   * - ``file.size``
     - 파일 크기 (바이트)
   * - ``file.created_at``
     - 생성일시
   * - ``file.modified_at``
     - 최종 업데이트 일시

자세한 내용은 `Box File Object <https://developer.box.com/reference#file-object>`_ 를 참조하세요.

Box 인증 설정
=============

JWT 인증 설정 절차
-----------------

1. Box Developer Console에서 애플리케이션 생성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://app.box.com/developers/console 에 접속:

1. "Create New App" 클릭
2. "Custom App" 선택
3. 인증 방법에서 "Server Authentication (with JWT)" 선택
4. 앱 이름 입력 후 생성

2. 애플리케이션 설정
~~~~~~~~~~~~~~~~~~~~~~~~~

"Configuration" 탭에서 설정:

**Application Scopes**:

- "Read all files and folders stored in Box" 체크

**Advanced Features**:

- "Generate a Public/Private Keypair" 클릭
- 생성된 JSON 파일 다운로드 (중요!)

**App Access Level**:

- "App + Enterprise Access" 선택

3. 엔터프라이즈에서 승인
~~~~~~~~~~~~~~~~~~~~~~~~~

Box 관리 콘솔에서:

1. "Apps" → "Custom Apps" 열기
2. 생성한 앱 승인

4. 인증 정보 취득
~~~~~~~~~~~~~~~~~

다운로드한 JSON 파일에서 다음 정보를 취득:

::

    {
      "boxAppSettings": {
        "clientID": "hdf8a7sd...",         // client_id
        "clientSecret": "kMN7sd8f...",      // client_secret
        "appAuth": {
          "publicKeyID": "4tg5h6j7",        // public_key_id
          "privateKey": "-----BEGIN...",    // private_key
          "passphrase": "7ba8sd9f..."       // passphrase
        }
      },
      "enterpriseID": "1923456"             // enterprise_id
    }

비밀키 형식
~~~~~~~~~~~~

``private_key`` 는 개행을 ``\n`` 으로 치환하여 한 줄로 만듭니다:

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n


사용 예
======

기업 Box 스토리지 전체 크롤링
---------------------------------

파라미터:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789

스크립트:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

문제 해결
======================

인증 오류
----------

**증상**: ``Authentication failed`` 또는 ``Invalid grant``

**확인 사항**:

1. ``client_id`` 와 ``client_secret`` 이 올바른지 확인
2. 비밀키가 올바르게 복사되었는지 확인 (개행이 ``\n`` 으로 되어 있는지)
3. 패스프레이즈가 올바른지 확인
4. Box 관리 콘솔에서 앱이 승인되었는지 확인
5. ``enterprise_id`` 가 올바른지 확인

비밀키 형식 오류
--------------------------

**증상**: ``Invalid private key format``

**해결 방법**:

비밀키의 개행이 올바르게 ``\n`` 으로 변환되었는지 확인:

::

    # 올바른 형식
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # 잘못된 형식 (실제 개행이 포함됨)
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

파일을 가져올 수 없음
----------------------

**증상**: 크롤링은 성공하지만 파일이 0건

**확인 사항**:

1. Application Scopes에서 "Read all files and folders"가 활성화되어 있는지 확인
2. App Access Level이 "App + Enterprise Access"로 되어 있는지 확인
3. Box 스토리지에 실제로 파일이 존재하는지 확인
4. 서비스 계정에 적절한 권한이 있는지 확인

참고 정보
========

- :doc:`ds-overview` - 데이터스토어 커넥터 개요
- :doc:`ds-dropbox` - Dropbox 커넥터
- :doc:`ds-gsuite` - Google Workspace 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
