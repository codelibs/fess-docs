==================================
Google Workspace 커넥터
==================================

개요
====

Google Workspace 커넥터는 Google Drive(구 G Suite)에서 파일을 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-gsuite`` 플러그인이 필요합니다.

15.9 변경 사항
==============

|Fess| 15.9에서 커넥터가 대폭 재작성되었습니다. 기존 데이터 스토어 설정을 업그레이드하기 전에
이 절을 읽어 주세요.

.. warning::

   ``crawl_target``\ 의 기본값이 ``shared_drives``\ 가 되었고, ``legacy`` 이외의 값에서는
   ``impersonate_user``\ 가 필수가 되었습니다. 따라서 기존 설정을 그대로 업그레이드하면
   실행되지 않고 ``DataStoreException``\ 과 함께 **시작 시점에 실패합니다** .

   이는 의도된 동작입니다. 기존 동작으로는 서비스 계정에 명시적으로 공유된 파일에만 도달할 수
   있으므로, 그대로 두면 아무것도 인덱싱하지 않는 크롤링이 조용히 성공해 버립니다.
   ``impersonate_user``\ 에 도메인 관리자 계정을 설정하거나, 기존 동작을 유지하려면
   ``crawl_target=legacy``\ 를 설정하세요.

동작 변경
---------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 변경 사항
     - 필요한 조치
   * - ``crawl_target``\ 의 기본값이 ``shared_drives``\ 가 되고 ``impersonate_user``\ 가 필수가 됨
     - ``impersonate_user``\ 를 설정하거나 ``crawl_target=legacy``\ 를 설정합니다. 그렇지 않으면 크롤링이 시작 시점에 실패합니다.
   * - 기본 OAuth 범위가 ``https://www.googleapis.com/auth/drive``\ 에서 ``https://www.googleapis.com/auth/drive.readonly``\ 로 축소됨
     - Google Workspace 관리 콘솔의 도메인 전체 위임 설정은 범위를 명시적으로 나열하므로 업데이트가 필요합니다.
   * - ``crawl_target=users`` 및 ``crawl_target=both``\ 에서 ``https://www.googleapis.com/auth/admin.directory.user.readonly``\ 가 추가로 필요해짐
     - ``scopes`` 파라미터와 관리 콘솔의 위임 설정 양쪽에 범위를 추가합니다. 이는 시작 시점에 검증됩니다.
   * - 인덱싱되는 URL이 다운로드 링크에서 브라우저에서 열 수 있는 링크(``webViewLink``)로 변경됨
     - 새 URL을 반영하려면 전체 재크롤링이 필요합니다.
   * - ``default_permissions``\ 가 추가가 아니라 대체값이 됨
     - ACL이 해결된 문서에는 해당 ACL만 부여되며, ``default_permissions``\ 와의 합집합이 아닙니다. 결과적으로 권한이 더 엄격해집니다.
   * - 링크 공유만으로는 검색 역할이 부여되지 않음
     - ``allowFileDiscovery=false``\ 인 ``domain`` 및 ``anyone`` 권한은 "링크가 있는 모든 사용자"를 의미하며, Drive 자체도 이를 검색으로 찾을 수 있게 하지 않습니다.
   * - ACL이 아무것도 해결되지 않은 문서는 역할 없이 인덱싱되지 않고 건너뜀
     - 계속 인덱싱하려면 ``default_permissions``\ 를 설정합니다. 기존에는 역할 목록이 비어 있으면 권한 필터가 비활성화되어 모든 사용자에게 보였습니다.
   * - ``fields``\ 의 기본값이 ``*``\ 가 아니라 명시적인 필드 목록이 됨
     - 잘 쓰이지 않는 필드를 참조하는 크롤링 스크립트에서는 null이 반환됩니다. 기존 동작으로 되돌리려면 ``fields=*``\ 를 설정합니다.
   * - Google 문서가 일반 텍스트 대신 Markdown으로, 스프레드시트가 CSV 대신 TSV로 내보내짐
     - 모든 Google 문서의 인덱싱 텍스트에 Markdown 구문 문자가 포함됩니다. 전체 재크롤링이 필요합니다.
   * - ``refresh_token_interval``\ 이 무시됨
     - 토큰 갱신은 인증 라이브러리가 처리합니다. 기존 설정은 그대로 동작하며 경고가 로그에 출력됩니다.
   * - Google 설문지와 Google 사이트 도구는 메타데이터만 인덱싱됨
     - Drive API에 내보내기 형식이 없기 때문입니다. 기존에는 이러한 파일이 모두 크롤링 오류가 되었습니다.

새로운 기능
-----------

- ``crawl_target``\ 으로 크롤링 대상을 선택할 수 있습니다. 서비스 계정 자신의 시점(``legacy``),
  도메인 내의 모든 공유 드라이브(``shared_drives``), 디렉터리 전체 사용자의 마이 드라이브
  (``users``), 또는 둘 다(``both``)입니다. `크롤링 대상`_\ 을 참조하세요.
- 공유 드라이브 항목에 올바른 ACL이 부여됩니다. `권한과 액세스 제어`_\ 를 참조하세요.
- Drive 변경 피드를 이용한 증분 크롤링을 지원합니다. `증분 크롤링`_\ 을 참조하세요.
- ``Retry-After``\ 를 존중하는 지수 백오프 기반의 속도 제한 대응과, 하나의 공유 드라이브나
  사용자의 실패가 전체 크롤링을 중단시키지 않는 구조를 추가했습니다.
  `속도 제한과 재시도`_\ 를 참조하세요.
- 인증이 필요한 프록시를 위해 ``proxy_username``\ 과 ``proxy_password``\ 를 추가했습니다.

지원 서비스
===========

- Google Drive(마이 드라이브, 공유 드라이브)
- Google 문서, 스프레드시트, 프레젠테이션, 그림, Apps Script
- Google 설문지, Google 사이트 도구(내보내기 형식이 없어 메타데이터만 인덱싱)

전제조건
========

1. 플러그인 설치가 필요합니다
2. Google Cloud Platform 프로젝트 생성이 필요합니다
3. 서비스 계정 생성과 인증 정보 취득이 필요합니다
4. Google Workspace 도메인 전체 위임 설정이 필요합니다
5. ``crawl_target=legacy`` 이외를 사용하는 경우, 대신 액세스할 Google Workspace 관리자 계정이
   필요합니다

플러그인 설치
-------------

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
     - Company Google Drive
   * - 핸들러 이름
     - GoogleDriveDataStore
   * - 활성화
     - 켬

파라미터 설정
-------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com

파라미터 목록
~~~~~~~~~~~~~

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
   * - ``impersonate_user``
     - 조건부
     - 도메인 전체 위임으로 대신 액세스할 Google Workspace 계정. ``crawl_target=legacy`` 이외에서는 필수이며, 설정하지 않으면 크롤링이 시작 시점에 실패합니다. ``shared_drives``\ 와 ``both``\ 는 도메인 관리자 권한으로 공유 드라이브를 열거하므로, 이 계정은 도메인 관리자여야 합니다.
   * - ``crawl_target``
     - 아니오
     - 크롤링 대상. ``legacy``, ``shared_drives``, ``users``, ``both`` 중 하나. 기본값: ``shared_drives``. `크롤링 대상`_\ 을 참조하세요.
   * - ``scopes``
     - 아니오
     - OAuth 범위(쉼표 구분). 기본값: ``https://www.googleapis.com/auth/drive.readonly``. ``crawl_target=users`` 및 ``both``\ 에서는 ``https://www.googleapis.com/auth/admin.directory.user.readonly``\ 가 추가로 필요합니다.
   * - ``user_query``
     - 아니오
     - ``crawl_target=users`` 및 ``both``\ 에서 열거할 사용자를 좁히는 Admin SDK의 ``query``. 기본값: 지정 안 함(고객 계정의 전체 사용자)
   * - ``query``
     - 아니오
     - Google Drive API 검색 쿼리 문자열. 증분 크롤링에서 사용하는 변경 피드에는 적용되지 않습니다
   * - ``corpora``
     - 아니오
     - 검색 대상 코퍼스. 기본값: ``allDrives``. ``crawl_target=legacy``\ 에서만 사용되므로 기본 크롤링 대상에서는 효과가 없습니다. ``shared_drives``\ 는 각 드라이브를 ``drive``\ 로, ``users``\ 는 각 마이 드라이브를 ``user``\ 로 열거하며 둘 다 고정입니다
   * - ``spaces``
     - 아니오
     - 검색 대상 공간(Google Drive API의 ``spaces`` 매개변수, 예: ``drive``, ``appDataFolder``). 기본값: 지정 안 함(API 기본값). ``crawl_target=legacy``\ 와 ``users``\ 에서 사용되며 ``shared_drives``\ 에서는 무시됩니다
   * - ``fields``
     - 아니오
     - Google Drive API에서 가져올 파일 필드 지정. 기본값은 ``*``\ 가 **아니라** 명시적인 필드 목록입니다. 스크립트 컨텍스트, ACL 해결, 인덱스 URL, 증분 크롤링에 필요한 필드를 모두 포함하지만, 목록에 없는 필드는 크롤링 스크립트에서 null이 됩니다. 기존처럼 모든 필드를 가져오려면 ``fields=*``\ 를 설정합니다
   * - ``default_permissions``
     - 아니오
     - 문서의 Drive ACL이 아무것도 해결되지 않았을 때 사용할 권한(쉼표 구분, 예: ``{role}drive-users``). 추가가 아니라 대체값이며, ACL이 해결된 문서에는 해당 ACL만 부여됩니다
   * - ``max_size``
     - 아니오
     - 인덱스 대상 최대 파일 크기(바이트). 기본값: ``10000000`` (약 10MB)
   * - ``number_of_threads``
     - 아니오
     - 병렬 처리 스레드 수. 기본값: ``1``
   * - ``incremental``
     - 아니오
     - 전부 열거하는 대신 Drive 변경 피드로 크롤링할지 여부. 기본값: ``false``. 크롤링 시작 전에 데이터 스토어 설정의 파라미터 항목에서 직접 읽습니다. `증분 크롤링`_\ 을 참조하세요

고급 파라미터
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 파라미터
     - 설명
   * - ``domain_permission_format``
     - ``type=domain``\ 인 Drive 권한에 적용할 역할 형식. ``{domain}``\ 이 도메인 이름으로 치환됩니다. 기본값: ``{group}{domain}``
   * - ``thread_pool_timeout_seconds``
     - 크롤링 종료 시 작업 스레드의 종료를 기다리는 시간(초). 기본값: ``60``
   * - ``page_size``
     - ``files.list``\ 와 ``changes.list``\ 의 페이지 크기. 기본값: ``1000``. ``1000``\ 을 넘는 값은 자동으로 축소됩니다
   * - ``permission_page_size``
     - ``permissions.list``\ 와 ``drives.list``\ 의 페이지 크기. 기본값: ``100``. ``100``\ 을 넘는 값은 자동으로 축소됩니다
   * - ``max_cached_content_size``
     - 메모리에 유지하는 콘텐츠의 최대 크기(바이트). 이를 초과하는 콘텐츠는 임시 파일로 저장됩니다. 기본값: ``1048576`` (1MB)
   * - ``max_retries``
     - Drive API의 속도 제한이나 일시적인 실패에 대한 최대 재시도 횟수. 기본값: ``5``
   * - ``retry_initial_interval_ms``
     - 첫 재시도까지의 백오프 간격(밀리초). 기본값: ``1000``
   * - ``max_backoff_ms``
     - 한 번의 대기 시간 상한(밀리초). 기본값: ``32000``
   * - ``read_timeout``
     - HTTP 읽기 타임아웃(밀리초). 기본값: ``20000``
   * - ``connect_timeout``
     - HTTP 연결 타임아웃(밀리초). 기본값: ``20000``
   * - ``proxy_host``
     - 프록시 서버 호스트명. 프록시는 ``proxy_host``\ 와 ``proxy_port``\ 가 모두 설정된 경우에만 사용되며, 한쪽만으로는 효과가 없습니다
   * - ``proxy_port``
     - 프록시 서버 포트 번호. ``proxy_host``\ 를 참조하세요
   * - ``proxy_username``
     - 인증이 필요한 프록시의 사용자 이름. 설정하면 모든 요청에 ``Proxy-Authorization`` 헤더가 추가됩니다. 무엇이 인증되고 무엇이 인증되지 않는지는 `제한 사항`_\ 을 참조하세요
   * - ``proxy_password``
     - 인증이 필요한 프록시의 비밀번호
   * - ``ignore_folder``
     - 폴더를 건너뛸지 여부. 기본값: ``true``
   * - ``ignore_error``
     - 오류 발생 시 처리를 계속할지 여부. 기본값: ``true``
   * - ``supported_mimetypes``
     - 인덱스 대상 MIME 타입(정규식, 쉼표 구분). 기본값: ``.*`` (전체 타입)
   * - ``include_pattern``
     - 인덱스 대상 URL의 정규식 패턴
   * - ``exclude_pattern``
     - 제외할 URL의 정규식 패턴
   * - ``refresh_token_interval``
     - 15.9부터 무시됩니다. 액세스 토큰 갱신은 인증 라이브러리가 처리합니다. 기존 설정은 그대로 동작하며 경고가 로그에 출력됩니다

.. note::

   ``private_key``, ``private_key_id``, ``client_email``, ``proxy_username``,
   ``proxy_password``\ 는 스크립트 평가 컨텍스트에서 제거되므로, 크롤링 스크립트로 인덱스에
   등록할 수 없고 검색 결과로 노출되지도 않습니다.

.. note::

   증분 크롤링을 활성화하면 커넥터가 ``start_page_tokens``\ 와 ``crawl_signature``\ 를
   데이터 스토어 설정의 파라미터 항목에 다시 기록합니다. 이 값들은 커넥터가 관리하며 사용자가
   설정한 파라미터와 함께 표시되지만, 수정하지 마세요. 수정하거나 삭제하면 다음 실행에서
   모든 스코프가 전체 크롤링이 됩니다.

크롤링 대상
-----------

서비스 계정은 자신의 Drive를 갖지 않고 어떤 Google 그룹에도 속하지 않으므로, 서비스 계정
자신으로 인증하는 크롤링은 서비스 계정 주소에 명시적으로 공유된 파일에만 도달할 수 있습니다.
따라서 ``crawl_target``\ 은 누구의 시점으로 Drive를 크롤링할지를 선택합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 값
     - 설명
   * - ``legacy``
     - 기존 버전과 마찬가지로 서비스 계정 자신의 시점으로 크롤링합니다. ``impersonate_user``\ 는 필요하지 않습니다. 서비스 계정에 명시적으로 공유된 파일만 찾을 수 있습니다
   * - ``shared_drives``
     - 기본값. 도메인 내의 모든 공유 드라이브를 열거하고 각각을 개별적으로 순회합니다
   * - ``users``
     - Admin SDK로 디렉터리의 전체 사용자를 열거하고, 각 사용자를 대신하여 마이 드라이브를 순회합니다
   * - ``both``
     - ``shared_drives`` 다음에 ``users``\ 를 실행합니다. 여러 스코프에 나타나는 파일은 한 번만 인덱싱됩니다

다음 항목은 크롤링 시작 시점에 검증되며, 잘못된 조합이면 실행되지 않고
``DataStoreException``\ 이 발생합니다.

1. ``crawl_target``\ 은 ``legacy``, ``shared_drives``, ``users``, ``both`` 중 하나여야 합니다
2. ``crawl_target=legacy`` 이외인 경우 ``impersonate_user``\ 가 설정되어 있어야 합니다
3. ``crawl_target``\ 이 ``users`` 또는 ``both``\ 인 경우 ``scopes``\ 에
   ``https://www.googleapis.com/auth/admin.directory.user.readonly``\ 가 포함되어 있어야 합니다

.. note::

   ``shared_drives``\ 와 ``both``\ 는 도메인 관리자 권한으로 공유 드라이브를 열거하므로,
   ``impersonate_user``\ 에 지정하는 계정은 Google Workspace의 도메인 관리자여야 합니다.
   이 열거는 크롤링 범위 전체를 결정하므로, 영구적인 실패는 기록하고 건너뛰는 대신 크롤링을
   중단합니다. 공유 드라이브를 하나도 열거하지 못한 크롤링은 부분적인 성공이 아니며, 아무것도
   인덱싱하지 않은 채 성공으로 보고해서는 안 되기 때문입니다.

증분 크롤링
-----------

``incremental=true``\ 를 설정하면 각 스코프(공유 드라이브 하나, 또는 대신 액세스하는 사용자
한 명의 시점)가 전부 열거하는 대신 Drive의 변경 피드를 읽습니다. 토큰이 저장되어 있지 않은
스코프는 전체를 크롤링하고, 다음 실행을 위해 변경 피드의 시작 위치를 기록합니다.

::

    crawl_target=shared_drives
    impersonate_user=admin@example.com
    incremental=true

.. warning::

   증분 크롤링 실행에서는 ``delete_old_docs``\ 가 강제로 ``false``\ 가 되며, 명시적으로
   ``delete_old_docs=true``\ 를 지정해도 존중되지 않고 덮어써집니다(경고가 로그에 출력됩니다).
   오래된 문서 삭제 처리는 이번 크롤링에서 등록되지 않은 이 데이터 설정의 모든 문서를 삭제하는
   것으로, 전체 크롤링을 전제로 합니다. 증분 크롤링은 변경된 문서만 처리하므로, 이 삭제 처리는
   인덱스의 나머지 전부를 삭제하게 됩니다.

   Drive에서 사라진 문서를 삭제하려면 ``incremental=false``\ 인 별도의 데이터 스토어 설정을
   스케줄링하세요.

변경 피드의 시작 위치는 크롤링이 완료되고 작업 스레드가 모두 종료된 경우에만 저장됩니다.
도중에 중지된 크롤링에서는 저장되지 않으며, 다음 실행은 같은 변경을 다시 읽습니다.

스코프가 반환하는 대상을 결정하는 설정, 즉 ``crawl_target``, ``impersonate_user``,
``user_query``, ``query``, ``corpora``, ``spaces`` 중 하나가 변경된 경우에도 저장된 시작
위치는 폐기되고 모든 스코프가 전체 크롤링이 됩니다. 저장된 시작 위치는 그것을 취득한 시점의
대상 범위만 나타내므로, 설정 변경 후에 거기서 재개하면 인덱스에 영구적인 누락이 생기기
때문입니다.

속도 제한과 재시도
------------------

Drive API의 속도 제한이나 일시적인 실패는 ``max_retries``, ``retry_initial_interval_ms``,
``max_backoff_ms`` 범위에서 지수 백오프로 재시도됩니다. ``Retry-After`` 헤더는 지수 백오프보다
우선하지만, 잘못된 값으로 크롤링이 몇 시간씩 멈추지 않도록 ``max_backoff_ms``\ 로 상한이
적용됩니다. ``Retry-After``\ 는 초 단위 형식만 유효하며, HTTP 날짜 형식인 경우에는 지수
백오프로 대체됩니다.

``429``, ``500``, ``502``, ``503``, ``504``\ 는 항상 재시도됩니다. ``403``\ 은 속도 제한
오류인 경우에만 재시도되며, 그 밖의 ``403``\ 은 재시도해도 해결되지 않는 인가 실패이므로 즉시
기록됩니다.

파일 목록 조회에 실패해도 더 이상 전체 크롤링이 중단되지 않습니다. 남은 공유 드라이브와
사용자의 크롤링은 계속되며, 실패는 크롤러 로그와 관리 화면의 실패 URL 목록에 기록됩니다.

스크립트 설정
-------------

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
~~~~~~~~~~~~~~~~

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
     - 파일 URL. ``webViewLink``\ 가 사용되며, 없는 경우에는 ``https://drive.google.com/open?id=<파일 ID>``\ 가 사용됩니다
   * - ``file.thumbnail_link``
     - 썸네일 링크(단기간 유효)
   * - ``file.size``
     - 파일 크기(바이트)
   * - ``file.roles``
     - 액세스 권한

.. note::

   값이 채워지는 것은 ``fields`` 파라미터에 지정한 필드뿐입니다. 요청하지 않은 필드는
   스크립트에서 null이 됩니다. 기존처럼 모든 필드를 가져오려면 ``fields=*``\ 를 설정하세요.

자세한 내용은 `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_\ 를 참조하세요.

Google 형식 파일의 텍스트 추출
------------------------------

Google 형식 파일은 다운로드할 수 없으므로 내보내기가 필요합니다. 내보내기 형식은 고정된
대응표가 아니라 Drive API가 실제로 반환하는 형식에서 선택되며, 내보내기는 10MB가 상한입니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 종류
     - 내보내기 형식
   * - Google 문서
     - Markdown(``text/markdown``). 사용할 수 없으면 일반 텍스트, 그다음 HTML
   * - Google 스프레드시트
     - TSV(``text/tab-separated-values``). 사용할 수 없으면 CSV
   * - Google 프레젠테이션
     - 일반 텍스트
   * - Google 그림
     - PNG. 인덱싱할 텍스트가 없으므로 메타데이터만 등록됩니다
   * - Apps Script
     - 내보낸 JSON에서 스크립트 소스를 추출하여 인덱싱합니다
   * - Google 설문지, Google 사이트 도구
     - 내보내기 불가. 메타데이터만 등록되며 오류가 되지 않습니다

.. note::

   Google 문서가 Markdown으로 내보내지므로, 모든 Google 문서의 인덱싱 텍스트에 Markdown 구문
   문자가 포함됩니다. 이미 인덱싱된 문서에 반영하려면 전체 재크롤링이 필요합니다.

.. note::

   내보내기 형식은 크롤링마다 한 번 Drive API에서 가져옵니다. 이 호출에 실패하면 Drive가
   기존부터 지원해 온 변환(Google 문서는 일반 텍스트, Google 스프레드시트는 CSV)으로
   대체되며 경고가 로그에 출력됩니다.

Google Cloud Platform 설정
==========================

1. 프로젝트 생성
----------------

https://console.cloud.google.com/ 에 접속:

1. 새 프로젝트 생성
2. 프로젝트 이름 입력
3. 조직과 위치 선택

2. Google Drive API 활성화
--------------------------

"API 및 서비스" → "라이브러리"에서:

1. "Google Drive API" 검색
2. "사용 설정" 클릭
3. ``crawl_target``\ 이 ``users`` 또는 ``both``\ 인 경우 "Admin SDK API"도 사용 설정

3. 서비스 계정 생성
-------------------

"API 및 서비스" → "사용자 인증 정보"에서:

1. "사용자 인증 정보 만들기" → "서비스 계정" 선택
2. 서비스 계정 이름 입력(예: fess-crawler)
3. "만들기 및 계속" 클릭
4. 역할은 설정 불필요(건너뛰기)
5. "완료" 클릭

4. 서비스 계정 키 생성
----------------------

생성한 서비스 계정에서:

1. 서비스 계정 클릭
2. "키" 탭 열기
3. "키 추가" → "새 키 만들기"
4. JSON 형식 선택
5. 다운로드된 JSON 파일 저장

5. 도메인 전체 위임 활성화
--------------------------

서비스 계정 설정에서:

1. "도메인 전체 위임 활성화" 체크
2. "저장" 클릭
3. "OAuth 2 클라이언트 ID" 복사

6. Google Workspace 관리 콘솔에서 승인
--------------------------------------

https://admin.google.com/ 에 접속:

1. "보안" → "액세스 및 데이터 관리" → "API 제어" 열기
2. "도메인 전체 위임" 선택
3. "새로 추가" 클릭
4. 클라이언트 ID 입력
5. OAuth 범위 입력:

   ::

       https://www.googleapis.com/auth/drive.readonly

   ``crawl_target``\ 이 ``users`` 또는 ``both``\ 인 경우에는 두 범위를 모두 입력합니다:

   ::

       https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

6. "승인" 클릭

.. warning::

   위임 설정은 범위를 명시적으로 나열하므로, 이전 버전에서 업그레이드하는 경우 업데이트가
   필요합니다. 15.9에서 기본 범위가 ``https://www.googleapis.com/auth/drive``\ 에서
   ``https://www.googleapis.com/auth/drive.readonly``\ 로 변경되었으며, 여기서 허용하는 범위는
   데이터 스토어 설정의 ``scopes`` 파라미터와 일치해야 합니다.

인증 정보 설정
==============

JSON 파일에서 정보 취득
-----------------------

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

``private_key``\ 는 줄바꿈을 ``\n``\ 으로 유지합니다:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

사용 예
=======

모든 공유 드라이브 크롤링
-------------------------

파라미터:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com

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
    role=file.roles
    filename=file.name

전체 사용자의 마이 드라이브 크롤링
----------------------------------

파라미터:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=users
    impersonate_user=admin@example.com
    scopes=https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

사용자를 좁히려면 Admin SDK 쿼리를 추가합니다:

::

    user_query=orgUnitPath=/Sales

기존 동작을 유지하는 경우
-------------------------

``crawl_target=legacy``\ 는 15.9 이전의 동작을 유지하며, 서비스 계정에 명시적으로 공유된
파일만 찾을 수 있습니다. ``impersonate_user``\ 는 필요하지 않습니다.

파라미터:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=legacy

권한 포함 크롤링
----------------

파라미터:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

``default_permissions``\ 는 Drive ACL이 아무것도 해결되지 않은 문서에만 사용됩니다.

특정 파일 타입만 크롤링
-----------------------

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
=========

크롤링을 시작할 수 없음
-----------------------

**증상**: 크롤링이 ``DataStoreException``\ 과 함께 즉시 종료됨

**해결 방법**:

1. ``parameter 'crawl_target' must be one of ...`` : ``crawl_target``\ 의 값이 ``legacy``,
   ``shared_drives``, ``users``, ``both`` 중 어느 것도 아닙니다
2. ``parameter 'impersonate_user' is required when 'crawl_target' is not 'legacy'`` :
   ``impersonate_user``\ 에 도메인 관리자 계정을 설정하거나 ``crawl_target=legacy``\ 를
   설정합니다
3. ``parameter 'scopes' must include 'https://www.googleapis.com/auth/admin.directory.user.readonly'`` :
   ``scopes``\ 와 도메인 전체 위임 설정에 이 범위를 추가합니다

기존 설정을 그대로 업그레이드한 경우 이는 예상된 결과입니다. `15.9 변경 사항`_\ 을
참조하세요.

인증 오류
---------

**증상**: ``401 Unauthorized`` 또는 ``403 Forbidden``

**확인 사항**:

1. 서비스 계정 인증 정보가 올바른지 확인:

   - ``private_key``\ 의 줄바꿈이 ``\n``\ 으로 되어 있는지
   - ``private_key_id``\ 가 올바른지
   - ``client_email``\ 이 올바른지

2. Google Drive API가 활성화되어 있는지 확인
3. 도메인 전체 위임이 설정되어 있는지 확인
4. Google Workspace 관리 콘솔에서 승인되었는지 확인
5. OAuth 범위가 올바른지 확인(``https://www.googleapis.com/auth/drive.readonly``.
   ``crawl_target``\ 이 ``users`` 또는 ``both``\ 인 경우
   ``https://www.googleapis.com/auth/admin.directory.user.readonly``\ 도 필요)

도메인 전체 위임 오류
---------------------

**증상**: ``Not Authorized to access this resource/api``

**해결 방법**:

1. Google Workspace 관리 콘솔에서 승인 확인:

   - 클라이언트 ID가 올바르게 등록되어 있는지
   - OAuth 범위가 올바른지. 위임 설정은 범위를 명시적으로 나열하므로 15.9의 범위 변경에 맞춰
     업데이트가 필요합니다

2. 서비스 계정에서 도메인 전체 위임이 활성화되어 있는지 확인
3. ``crawl_target``\ 이 ``shared_drives`` 또는 ``both``\ 인 경우, ``impersonate_user``\ 에
   지정한 계정이 도메인 관리자인지 확인

파일을 가져올 수 없음
---------------------

**증상**: 크롤링은 성공하지만 파일이 0개

**확인 사항**:

1. ``crawl_target``\ 이 의도한 값인지 확인합니다. ``legacy``\ 인 경우 서비스 계정은 자신의
   Drive를 갖지 않고 어떤 그룹에도 속하지 않으므로, 명시적으로 공유된 파일만 찾을 수 있습니다
2. Google Drive에 파일이 존재하는지 확인
3. 서비스 계정에 읽기 권한이 있는지 확인
4. 도메인 전체 위임이 올바르게 설정되어 있는지 확인
5. 대상 사용자의 Drive에 액세스 가능한지 확인

문서가 건너뛰어짐
-----------------

**증상**: 크롤러 로그에 ``Skipped ... because no permission could be resolved``\ 가 출력됨

**해결 방법**:

문서의 Drive ACL에서 검색 역할이 하나도 해결되지 않아 인덱싱되지 않고 건너뛰었습니다. 역할
없이 인덱싱하면 해당 문서에서 |Fess| 의 권한 필터가 비활성화되어 모든 사용자에게 보이므로
건너뜁니다. 건너뛰기는 크롤링 실패가 아니므로 크롤러 로그에만 출력되고 실패 URL 목록에는
표시되지 않습니다.

1. 대체 권한을 부여해 인덱싱하려면 ``default_permissions``\ 를 설정합니다
2. 공유 드라이브의 ACL을 읽을 수 있도록, ``impersonate_user``\ 에 지정한 계정이 도메인
   관리자인지 확인합니다
3. 문서가 링크 공유만으로 되어 있지 않은지 확인합니다. ``allowFileDiscovery=false``\ 인
   ``domain`` 및 ``anyone`` 권한에는 검색 역할이 부여되지 않습니다. Drive 자체도 그러한
   문서를 검색으로 찾을 수 있게 하지 않기 때문입니다

API 할당량 오류
---------------

**증상**: ``403 Rate Limit Exceeded`` 또는 ``429 Too Many Requests``

**해결 방법**:

1. 이러한 실패는 지수 백오프로 자동 재시도됩니다. 그래도 실패하는 경우 ``max_retries``
   또는 ``max_backoff_ms``\ 를 크게 설정합니다
2. ``number_of_threads``\ 를 줄여 요청 빈도를 낮춥니다
3. Google Cloud Platform에서 할당량 확인
4. 크롤링 간격을 늘림
5. 필요 시 할당량 증가 요청

비밀 키 형식 오류
-----------------

**증상**: ``Invalid private key format``

**해결 방법**:

줄바꿈이 올바르게 ``\n``\ 으로 되어 있는지 확인:

::

    # 올바름
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # 잘못됨(실제 줄바꿈이 포함되어 있음)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

공유 드라이브 크롤링
--------------------

.. note::
   ``crawl_target=shared_drives``\ (기본값)에서는 도메인 관리자 권한으로 공유 드라이브를
   열거하므로, 개별 공유 드라이브에 서비스 계정을 멤버로 추가할 필요가 없습니다. 대신
   ``impersonate_user``\ 에 도메인 관리자를 지정하세요.

``crawl_target=legacy``\ 인 경우에는 각 공유 드라이브에 서비스 계정을 추가해야 합니다.

1. Google Drive에서 공유 드라이브 열기
2. "멤버 관리" 클릭
3. 서비스 계정 이메일 주소 추가
4. 권한 수준을 "뷰어"로 설정

대량의 파일이 있는 경우
-----------------------

**증상**: 크롤링에 시간이 오래 걸리거나 타임아웃됨

**해결 방법**:

1. ``incremental=true``\ 를 활성화하여 이전 실행 이후의 변경만 크롤링합니다
2. ``crawl_target=both``\ 를 사용하지 않고 공유 드라이브와 사용자를 별도의 데이터 스토어
   설정으로 분할합니다
3. ``query``, ``user_query``, ``supported_mimetypes``\ 로 대상을 좁힙니다
4. 스케줄 설정으로 부하 분산
5. 크롤링 간격 조정

권한과 액세스 제어
==================

Drive 권한에서 Fess 역할로의 변환
---------------------------------

문서의 ACL은 추가 API 호출 횟수가 파일 수가 아니라 공유 드라이브 수에 비례하도록 다음 세
단계로 해결됩니다.

1. 파일 목록에 포함된 인라인 권한. 추가 비용이 들지 않습니다
2. 인라인 권한이 반환되지 않는 공유 드라이브 항목에 대해서는 공유 드라이브 자체의 ACL.
   도메인 관리자 권한으로 드라이브마다 한 번만 가져와 캐시합니다
3. 개별적으로 추가 권한을 가진 항목에 대해서는 그 항목 자신의 권한

각 Drive 권한은 다음과 같이 |Fess| 의 검색 역할로 변환됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Drive 권한
     - 검색 역할
   * - ``user``
     - 해당 사용자의 이메일 주소에 대응하는 검색 역할. 파일의 소유자도 항상 이 형식으로 추가됩니다
   * - ``group``
     - 해당 그룹의 이메일 주소에 대응하는 검색 역할. Google 그룹의 멤버는 전개되지 않으며, |Fess| 측에서 SSO나 LDAP로 해결하는 것을 전제로 합니다
   * - ``domain``
     - ``domain_permission_format``\ 의 ``{domain}``\ 을 도메인 이름으로 치환한 것. 기본값: ``{group}{domain}``
   * - ``anyone``
     - ``guest`` 역할
   * - 위 항목 중 ``allowFileDiscovery=false``\ 인 것과 삭제된 권한
     - 역할 없음. 링크 공유는 Drive 자체에서도 검색으로 찾을 수 없기 때문입니다

해결 결과가 비어 있으면 추가가 아니라 대체값으로 ``default_permissions``\ 가 사용됩니다.
``default_permissions``\ 도 설정되어 있지 않으면 문서는 건너뜁니다.

Google Drive 공유 권한 반영
---------------------------

Google Drive 공유 설정을 Fess 권한에 반영:

파라미터:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

``file.roles``\ 에 Google Drive 공유 정보가 포함됩니다.

제한 사항
=========

- Drive의 "삭제됨"을 나타내는 변경 알림에는 삭제뿐 아니라 액세스 권한의 상실도 포함됩니다.
  ``crawl_target=users`` 또는 ``both``\ 인 경우, 한 사용자의 액세스 권한을 회수하면 다른
  사용자가 아직 읽을 수 있는 문서라도 인덱스에서 삭제됩니다. 해당 파일에 다음 변경이 있을 때,
  또는 다음 전체 크롤링에서 복구됩니다.
- 증분 크롤링 중에 스코프가 전체 크롤링으로 대체된 경우에도 오래된 문서 삭제 처리는 계속
  억제되므로, 스코프의 시작 위치가 기록되지 않은 동안 Drive에서 삭제된 문서는 인덱스에
  남습니다. 이를 삭제하려면 ``incremental=false``\ 인 별도의 데이터 스토어 설정이 필요합니다.
- 삭제의 반영은 인덱싱된 URL에 Drive 파일 ID가 포함되어 있음을 전제로 합니다. ``webViewLink``\ 와
  대체 URL은 이 조건을 만족하지만, 크롤링 스크립트에서 ``url``\ 을 파일 ID가 포함되지 않은
  값으로 바꾸는 경우 삭제는 반영되지 않습니다.
- 변경 피드는 ``query``\ 로 좁혀지지 않습니다. ``query``\ 를 설정하고 ``incremental=true``\ 로
  한 경우, 쿼리에 일치하지 않는 변경된 파일도 인덱싱됩니다.
- 대규모 도메인에서 ``crawl_target=both``\ 를 사용하면 대략
  ``2 + 공유 드라이브 수 + 사용자 수`` 회의 목록 조회가 발생합니다. 공유 드라이브와 사용자를
  별도의 데이터 스토어 설정으로 분할하는 것이 현실적인 완화책입니다.
- ``proxy_username``\ 과 ``proxy_password``\ 는 ``Proxy-Authorization`` 요청 헤더로 전송되므로
  평문 HTTP 요청만 인증할 수 있습니다. Google API 통신은 모두 HTTPS이며, 인증이 필요한 프록시를
  경유하는 HTTPS 연결은 ``CONNECT``\ 로 성립되는데 이는 요청 헤더가 아니라 JDK의
  ``java.net.Authenticator``\ 가 처리합니다. 이러한 환경에서는 JVM 옵션
  ``-Djdk.http.auth.tunneling.disabledSchemes=``\ 와 ``Authenticator`` 설정이 필요합니다.

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-microsoft365` - Microsoft 365 커넥터
- :doc:`ds-box` - Box 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
