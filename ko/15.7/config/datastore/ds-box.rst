==================================
Box 커넥터
==================================

개요
====

Box 커넥터는 Box.com의 클라우드 스토리지에서 파일을 가져와
|Fess| 의 인덱스에 등록하는 기능을 제공합니다.

이 커넥터는 JWT（서버 인증）를 사용하여 엔터프라이즈에 연결하고,
엔터프라이즈에 소속된 각 사용자를 가장（impersonation）하여
각 사용자가 접근할 수 있는 파일을 재귀적으로 크롤링합니다.
크롤링 대상 사용자는 ``filter_term`` 파라미터로 좁힐 수 있습니다.

이 기능에는 ``fess-ds-box`` 플러그인이 필요합니다.

전제 조건
=========

1. 플러그인 설치가 필요합니다
2. Box 개발자 계정 및 애플리케이션 생성이 필요합니다
3. JWT（JSON Web Token）인증 설정이 필요합니다

플러그인 설치
------------------------

방법1: JAR 파일을 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # 배치
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

방법2: 관리 화면에서 설치

1. 「시스템」→「플러그인」 열기
2. JAR 파일 업로드
3. |Fess| 재시작

설정 방법
=========

관리 화면에서 「크롤러」→「데이터스토어」→「신규 작성」으로 설정합니다.

기본 설정
---------

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
-------------

JWT 인증 예:

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

파라미터 목록
~~~~~~~~~~~~~

인증 파라미터（필수）
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

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
     - 공개 키 ID
   * - ``private_key``
     - 예
     - 비밀 키（PEM 형식, 개행은 ``\n`` 으로 표현）
   * - ``passphrase``
     - 예
     - 비밀 키의 패스프레이즈
   * - ``enterprise_id``
     - 예
     - Box 엔터프라이즈 ID

크롤링 파라미터（임의）
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - 파라미터
     - 기본값
     - 설명
   * - ``max_size``
     - ``10000000``
     - 크롤링 대상 최대 파일 크기（바이트）. 기본값은 10MB.
   * - ``supported_mimetypes``
     - ``.*``
     - 크롤링 대상 MIME 타입（정규 표현식）. 쉼표로 구분하여 복수 지정 가능.
   * - ``include_pattern``
     - （없음）
     - 크롤링 대상에 포함할 URL 패턴
   * - ``exclude_pattern``
     - （없음）
     - 크롤링 대상에서 제외할 URL 패턴
   * - ``number_of_threads``
     - ``1``
     - 크롤링 처리 스레드 수
   * - ``ignore_folder``
     - ``true``
     - 폴더를 인덱싱 대상에서 제외할지 여부. 현재 구현에서는 폴더 자체는 인덱싱되지 않으므로（파일만 대상），이 파라미터는 효과가 없습니다.
   * - ``ignore_error``
     - ``true``
     - 오류 발생 시 처리를 계속할지 여부
   * - ``filter_term``
     - （없음）
     - 크롤링 대상 엔터프라이즈 사용자를 좁히는 필터 조건. 지정하지 않으면 모든 엔터프라이즈 사용자가 대상이 됩니다.
   * - ``fields``
     - （전체 필드）
     - Box API에서 가져올 필드 지정

접속 파라미터（임의）
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - 파라미터
     - 기본값
     - 설명
   * - ``base_url``
     - ``https://app.box.com``
     - 브라우저에서 파일을 열 URL（``file.url``）을 구성하기 위한 기본 URL. Box SDK가 사용하는 API 엔드포인트에는 영향을 주지 않습니다.
   * - ``max_retry_count``
     - ``10``
     - API 호출 최대 재시도 횟수
   * - ``proxy_host``
     - （없음）
     - HTTP 프록시 호스트명
   * - ``proxy_port``
     - （없음）
     - HTTP 프록시 포트 번호
   * - ``refresh_token_interval``
     - ``3540``
     - 토큰 갱신 간격（초）. 기본값은 59분.

스크립트 설정
-------------

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
~~~~~~~~~~~~~~~~

주요 필드
^^^^^^^^^

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
     - 파일 크기（바이트）
   * - ``file.created_at``
     - 생성 일시
   * - ``file.modified_at``
     - 최종 수정 일시
   * - ``file.download_url``
     - Box 직접 다운로드 URL
   * - ``file.id``
     - Box 아이템 ID
   * - ``file.description``
     - 파일 설명
   * - ``file.extension``
     - 파일 확장자
   * - ``file.sha1``
     - 파일의 SHA1 해시
   * - ``file.path_collection``
     - 폴더 경로 목록

메타데이터 필드
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``file.type``
     - 아이템 타입（"file" 또는 "folder"）
   * - ``file.file_version``
     - 파일 버전 정보
   * - ``file.sequence_id``
     - 시퀀스 ID
   * - ``file.etag``
     - ETag 해시
   * - ``file.trashed_at``
     - 휴지통 이동 일시
   * - ``file.purged_at``
     - 완전 삭제 일시
   * - ``file.content_created_at``
     - 콘텐츠 생성 일시
   * - ``file.content_modified_at``
     - 콘텐츠 수정 일시
   * - ``file.created_by``
     - 생성자 정보
   * - ``file.modified_by``
     - 수정자 정보
   * - ``file.owned_by``
     - 소유자 정보
   * - ``file.shared_link``
     - 공유 링크 정보
   * - ``file.parent``
     - 상위 폴더 정보
   * - ``file.item_status``
     - 아이템 상태
   * - ``file.version_number``
     - 버전 번호
   * - ``file.comment_count``
     - 댓글 수
   * - ``file.permissions``
     - 권한 정보
   * - ``file.tags``
     - 태그 정보
   * - ``file.lock``
     - 잠금 정보
   * - ``file.is_package``
     - 패키지 플래그
   * - ``file.is_watermark``
     - 워터마크 플래그
   * - ``file.collections``
     - 컬렉션 정보
   * - ``file.representations``
     - 표현 형식 정보
   * - ``file.api``
     - Box 파일 API 객체（협업 및 권한 정보 취득용）

자세한 내용은 `Box File Object <https://developer.box.com/reference#file-object>`_ 를 참조하세요.

Box 인증 설정
=============

JWT 인증 설정 절차
------------------

1. Box Developer Console에서 애플리케이션 생성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://app.box.com/developers/console 에 접속:

1. 「Create New App」 클릭
2. 「Custom App」 선택
3. 인증 방법에서 「Server Authentication (with JWT)」 선택
4. 앱 이름 입력 후 생성

2. 애플리케이션 설정
~~~~~~~~~~~~~~~~~~~~~

「Configuration」 탭에서 설정:

**Application Scopes**:

- 「Read all files and folders stored in Box」 체크

**Advanced Features**:

- 「Generate a Public/Private Keypair」 클릭
- 생성된 JSON 파일 다운로드（중요！）

**App Access Level**:

- 「App + Enterprise Access」 선택

3. 엔터프라이즈에서 승인
~~~~~~~~~~~~~~~~~~~~~~~~~

Box 관리 콘솔에서:

1. 「Apps」→「Custom Apps」 열기
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

비밀 키 형식
~~~~~~~~~~~~

``private_key`` 는 개행을 ``\n`` 으로 치환하여 한 줄로 만듭니다:

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n

사용 예
=======

기업 Box 스토리지 전체 크롤링
------------------------------

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

특정 폴더만 크롤링
------------------

``include_pattern`` 파라미터로 폴더 경로에 의한 필터링이 가능합니다.

파라미터:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    include_pattern=.*Documents/Projects/.*

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

PDF 파일만 크롤링
-----------------

``supported_mimetypes`` 파라미터로 MIME 타입에 의한 필터링이 가능합니다.

파라미터:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    supported_mimetypes=application/pdf

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
=========

인증 오류
---------

**증상**: ``Authentication failed`` 또는 ``Invalid grant``

**확인 사항**:

1. ``client_id`` 와 ``client_secret`` 이 올바른지 확인
2. 비밀 키가 올바르게 복사되었는지 확인（개행이 ``\n`` 으로 되어 있는지）
3. 패스프레이즈가 올바른지 확인
4. Box 관리 콘솔에서 앱이 승인되었는지 확인
5. ``enterprise_id`` 가 올바른지 확인

비밀 키 형식 오류
-----------------

**증상**: ``Invalid private key format``

**해결 방법**:

비밀 키의 개행이 올바르게 ``\n`` 으로 변환되었는지 확인:

::

    # 올바른 형식
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # 잘못된 형식（실제 개행이 포함된 경우）
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

파일을 가져올 수 없음
---------------------

**증상**: 크롤링은 성공하지만 파일이 0건

**확인 사항**:

1. Application Scopes에서 「Read all files and folders」가 활성화되어 있는지 확인
2. App Access Level이 「App + Enterprise Access」로 되어 있는지 확인
3. Box 스토리지에 실제로 파일이 존재하는지 확인
4. 서비스 계정에 적절한 권한이 있는지 확인

파일이 대량으로 있는 경우
-------------------------

**증상**: 크롤링에 시간이 걸리거나 타임아웃 발생

**해결 방법**:

데이터스토어 설정에서 처리를 분할:

1. 크롤링 간격 조정
2. 복수의 데이터스토어로 나누어 설정（폴더 단위 등）
3. ``number_of_threads`` 파라미터로 스레드 수 증가
4. 스케줄 설정으로 부하 분산

권한과 접근 제어
================

Box 협업 권한 반영
------------------

``file.api`` 필드가 제공하는 ``BoxFileAPI`` 객체를 통해,
Box의 협업 정보를 |Fess| 의 검색 롤에 매핑할 수 있습니다.
``file.api.collaborationRoles`` 는 파일에 접근할 수 있는 사용자 및
그룹에 해당하는 검색 롤 목록을 반환합니다.

스크립트에서 권한을 설정:

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.api.collaborationRoles
    mimetype=file.mimetype
    filename=file.name
    created=file.created_at
    last_modified=file.modified_at

.. note::
   ``file.api.collaborationRoles`` 는 파일마다 협업 정보를
   가져오기 때문에, Box API 호출 횟수가 증가하여 크롤링에 시간이 걸릴 수 있습니다.

모든 파일에 고정 롤을 할당하는 경우에는 다음과 같이 지정합니다:

::

    role="{role}box-users"

참고 정보
=========

- :doc:`ds-overview` - 데이터스토어 커넥터 개요
- :doc:`ds-dropbox` - Dropbox 커넥터
- :doc:`ds-gsuite` - Google Workspace 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
