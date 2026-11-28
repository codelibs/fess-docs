=========================================
Google Drive·SharePoint·Box 파일 검색하기
=========================================

들어가며
========

부서마다 Google Drive, SharePoint Online, Box를 나누어 쓰고 있으면 "그 자료를 어디에 두었더라"를 찾는 시간이 늘어납니다.
Fess의 데이터 저장소 플러그인을 사용하면 3개 서비스의 파일을 하나의 검색 화면에서 찾을 수 있게 됩니다.

다만 클라우드 스토리지에는 열람 권한이 서로 다른 파일이 섞여 있습니다.
설정을 잘못하면 계약서와 같은 기밀 파일이 로그인하지 않은 사용자의 검색 결과에도 나오게 됩니다.
이 글에서는 서비스별로 "그대로 옮겨 적으면 동작하는 최소 구성"과, 원래의 권한을 Fess로 가져오는 방법을 설명합니다.

플러그인 설치, 핸들러 이름·파라미터·스크립트 작성법, 작업 만드는 법 등 데이터 저장소에 공통된 절차는 :doc:`datastore-basics`\ 에 정리되어 있습니다.
먼저 그 글을 읽은 다음 진행하십시오.
글에 나오는 설정값은 Fess 15.9와 각 플러그인의 15.9.0 버전에 맞추었습니다.

이 글에서 만드는 구성
=====================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - 서비스
     - 플러그인
     - 핸들러 이름
     - 서비스 측에서 준비할 것
   * - Google Drive
     - ``fess-ds-gsuite``
     - ``GoogleDriveDataStore``
     - 서비스 계정의 JSON 키와 도메인 전체 위임
   * - SharePoint Online
     - ``fess-ds-microsoft365``
     - ``OneDriveDataStore``
     - Entra ID의 앱 등록(클라이언트 시크릿)과 Microsoft Graph의 애플리케이션 권한
   * - Box
     - ``fess-ds-box``
     - ``BoxDataStore``
     - JWT 인증을 사용하는 Box 커스텀 앱

Docker로 실행하는 경우에는 환경 변수 ``FESS_PLUGINS``\ 에 플러그인 이름과 버전을 공백으로 구분해 나열하면 시작할 때 한꺼번에 설치할 수 있습니다.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-gsuite:15.9.0 fess-ds-microsoft365:15.9.0 fess-ds-box:15.9.0

관리 화면이나 ``fess-setup``\ 으로 설치한 경우에는 설치 후 Fess를 재시작해야 합니다(\ ``FESS_PLUGINS``\ 는 Fess가 시작되기 전에 설치하므로 재시작이 필요 없습니다).

먼저 정할 것: 검색 결과를 누구에게 보여 줄 것인가
=================================================

데이터 저장소 설정을 새로 만들면 "권한" 칸에는 처음부터 ``{role}guest``\ 가 들어 있습니다.
이 값이 남아 있으면 가져온 파일이 로그인하지 않은 사용자에게도 검색됩니다.
3개 플러그인 모두 원래의 공유 설정으로부터 만든 롤을 ``file.roles``\ 에 넣습니다.
그래서 설정 방법은 3개 모두 다음 2가지가 공통입니다.

- "권한" 칸의 ``{role}guest``\ 를 지우고 비워 둔다
- 스크립트에 ``role=file.roles``\ 를 쓴다

이 2가지가 필요한 이유는 플러그인마다 "권한" 칸을 다루는 방식이 다르기 때문입니다.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 플러그인
     - "권한" 칸의 값
     - ``default_permissions`` 파라미터
   * - Google Drive
     - ``role=file.roles``\ 를 쓰면 사용되지 않는다. 쓰지 않으면 칸의 값(초기값은 ``{role}guest``)이 그대로 모든 파일에 붙는다
     - Drive의 ACL에서 아무것도 얻지 못한 파일에만 사용한다. 그것도 설정되어 있지 않으면 그 파일은 가져오지 않는다
   * - SharePoint(OneDriveDataStore)
     - ``file.roles``\ 에 합쳐진다. ``{role}guest``\ 를 남기면 모든 파일이 공개된다
     - 모든 파일에 추가한다
   * - Box
     - ``file.roles``\ 에 합쳐진다. ``{role}guest``\ 를 남기면 모든 파일이 공개된다
     - 모든 파일에 추가한다

``file.roles``\ 에 들어가는 것은 각 서비스의 사용자나 그룹을 나타내는 문자열입니다.

- Google Drive: 사용자와 그룹은 이메일 주소이고, 파일 소유자도 같은 형식입니다. 도메인 공유는 ``{group}<도메인 이름>``\ (\ ``domain_permission_format``\ 으로 변경 가능), 검색으로 찾을 수 있는 일반 공개(\ ``anyone``)는 ``guest`` 롤이 됩니다. 링크를 아는 사람에게만 공유한 설정은 롤이 되지 않습니다.
- SharePoint: 사용자는 개체 ID와 UPN, 그룹은 ID와 표시 이름입니다. "조직 내 모든 사용자"용 공유 링크는 그룹 ``EVERYONE_IN_TENANT``\ 가 됩니다.
- Box: 사용자는 Box 사용자 ID와 로그인(이메일 주소), 그룹은 Box 그룹 ID입니다. 파일 자체의 협업에 더해 상위 폴더의 협업과 소유자도 포함됩니다.

검색할 때 이 값들과 대조되는 것은 Fess에 로그인한 사용자의 사용자 이름과 그룹 이름입니다.
예를 들어 Google Drive의 사용자 권한을 적용하려면 Fess의 사용자 이름이 이메일 주소와 일치해야 합니다.
롤의 개념은 :doc:`guide-05`\ , SSO를 통한 로그인은 :doc:`guide-15`\ 를 참조하십시오.

서비스별로 검색 결과를 좁힐 수 있게 하는 라벨은 데이터 저장소 설정에 전용 칸이 없습니다.
스크립트에 ``label="box"`` 같은 줄을 추가하거나, URL에 일치하는 라벨을 만듭니다(자세한 내용은 :doc:`datastore-basics`).
라벨 값에 사용할 수 있는 것은 영숫자와 ``_``\ 뿐이므로, ``google-drive``\ 처럼 하이픈을 포함한 값은 만들 수 없습니다.

Google Drive: 공유 드라이브 가져오기
====================================

Google 측 준비
--------------

15.9의 ``fess-ds-gsuite``\ 는 기본적으로 ``crawl_target=shared_drives``\ 로 동작합니다.
도메인 안의 모든 공유 드라이브를 도메인 관리자로 가장하여 읽는 방식입니다.

1. Google Cloud 콘솔에서 프로젝트를 만들고 Google Drive API를 사용 설정한다
2. 서비스 계정을 만들고 [Keys] 탭에서 JSON 형식의 키를 만들어 다운로드한다
3. 서비스 계정에서 도메인 전체 위임을 사용 설정하고 OAuth 2 클라이언트 ID를 적어 둔다
4. Google Workspace 관리 콘솔의 [Security] > [Access and data control] > [API controls] > [Domain-wide delegation]\ 에서 그 클라이언트 ID에 범위 ``https://www.googleapis.com/auth/drive.readonly``\ 를 허용한다

``impersonate_user``\ 에 지정하는 계정은 Google Workspace의 도메인 관리자여야 합니다.
``crawl_target``\ 이 ``legacy`` 이외인데 ``impersonate_user``\ 가 없으면 크롤링을 시작할 때 오류로 멈춥니다.

파라미터와 스크립트
-------------------

[크롤러] > [데이터 저장소] > [새로 만들기]에서 "핸들러 이름"으로 ``GoogleDriveDataStore``\ 를 선택하고 "권한" 칸을 비웁니다.
``private_key``, ``private_key_id``, ``client_email``\ 에는 JSON 키의 같은 이름의 값을 옮겨 적습니다.
``private_key``\ 의 줄바꿈은 ``\n`` 그대로 두고 한 줄로 씁니다.

.. code-block:: properties

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com
    crawl_target=shared_drives
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_time
    last_modified=file.modified_time
    role=file.roles

``file.url``\ 은 파일의 ``webViewLink``\ 입니다.
삭제 반영은 인덱싱된 URL에 Drive의 파일 ID가 포함되어 있다는 것을 전제로 합니다.
그러므로 ``url``\ 은 바꿔 쓰지 말고 그대로 사용합니다.

다른 가져오기 범위는 다음과 같습니다.

- ``crawl_target=users``: 모든 사용자의 내 드라이브를 읽습니다. Admin SDK API 사용 설정과 범위 ``https://www.googleapis.com/auth/admin.directory.user.readonly`` 추가(위임 설정과 ``scopes`` 파라미터 양쪽)가 필요합니다.
- ``crawl_target=legacy``: 서비스 계정의 주소에 직접 공유된 파일만 읽습니다. 위임과 ``impersonate_user``\ 는 필요 없습니다.

증분 크롤링
-----------

``incremental=true``\ 를 추가하면 두 번째 이후에는 Drive의 변경 피드만 읽습니다.
이때 ``delete_old_docs``\ 는 강제로 ``false``\ 가 되어, Drive에서 삭제된 파일이 인덱스에 남을 수 있습니다.
또한 변경되지 않은 파일은 다시 등록되지 않으므로, 그대로 두면 "이전 문서 삭제"의 일수(초기값 3일)가 지나면 검색 결과에서 사라집니다(\ :doc:`datastore-basics`\ 의 문서 유효 기간에 관한 절).

증분 크롤링을 사용하는 경우에는 다음과 같이 조합합니다.

- ``incremental``\ 을 붙이지 않은 전체 크롤링용 설정도 만들어 주 1회 등 정기적으로 실행한다
- 두 설정 모두에 전체 크롤링 간격보다 조금 긴 ``time_to_live``\ 를 지정한다(주 1회 전체 크롤링이라면 ``time_to_live=11520``, 8일)

Drive에서 삭제된 파일은 이 기한이 지나는 시점에 검색 결과에서 사라집니다.
변경 피드의 위치는 플러그인이 "파라미터" 칸에 다시 써 넣으므로, 다시 써 넣은 값은 편집하지 마십시오.

SharePoint Online: 문서 라이브러리의 파일 가져오기
==================================================

어떤 핸들러를 사용할 것인가
---------------------------

SharePoint 문서 라이브러리에 있는 파일의 본문을 검색하려면 ``fess-ds-microsoft365``\ 의 ``OneDriveDataStore``\ 를 사용합니다.

- ``SharePointDocLibDataStore``\ 는 라이브러리 하나를 1건으로 등록할 뿐, 안의 파일은 가져오지 않습니다.
- ``fess-ds-sharepoint``\ (\ ``SharePointDataStore``)는 온프레미스 SharePoint Server용입니다. Microsoft Graph를 지원하지 않으며, SharePoint Online에는 ``fess-ds-microsoft365``\ 를 사용하도록 안내되어 있습니다.

Entra ID 측 준비
----------------

1. Azure Portal의 [App registrations]\ 에서 새로 등록한다
2. [Certificates & secrets]\ 에서 새 클라이언트 시크릿을 만들고 값을 적어 둔다(유효 기간은 여기서 정합니다)
3. [API permissions] > [Microsoft Graph] > [Application permissions]\ 에서 아래 4개를 추가한다
4. [Grant admin consent]\ 를 실행한다

추가할 애플리케이션 권한은 다음과 같습니다.

- ``Files.Read.All``
- ``User.Read.All``, ``Group.Read.All``: ACL의 사용자 이름·그룹 이름을 조회하기 위해 어느 가져오기 범위에서든 필요
- ``Sites.Read.All``: ``shared_documents_drive_crawler=true``\ 로 사이트를 열거하기 위해 필요

파라미터와 스크립트
-------------------

``OneDriveDataStore``\ 는 아무것도 지정하지 않으면 SharePoint의 모든 사이트에 더해 모든 사용자의 OneDrive와 모든 Microsoft 365 그룹의 드라이브도 읽습니다.
SharePoint만 대상으로 하려면 3개의 플래그를 명시합니다.

.. code-block:: properties

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your-client-secret
    shared_documents_drive_crawler=true
    user_drive_crawler=false
    group_drive_crawler=false
    script_type=javascript

.. code-block:: properties

    url=file.web_url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created
    last_modified=file.last_modified
    role=file.roles

특정 라이브러리만으로 좁히고 싶다면 3개의 플래그를 모두 ``false``\ 로 하고 ``drive_id``\ 에 드라이브 ID를 지정합니다.
드라이브 ID는 Microsoft Graph의 ``GET /sites/{site-id}/drives``\ 로 확인할 수 있습니다.
``drive_id``\ 만 지정하고 플래그를 남겨 두면, 그 드라이브는 전체 가져오기에 "추가"될 뿐입니다.

권한 누락과 재시도
------------------

파일의 ACL은 파일마다 Graph를 호출하여 가져옵니다.
이 호출이 실패했을 때의 처리는 ``permission_failure_policy``\ 로 정해집니다.
기본값인 ``skip``\ 에서는 그 파일을 등록하지 않고 [시스템 정보] > [장애 URL]과 WARN 로그에 기록합니다.
``index_without_acl``\ 로 바꾸면 ACL이 불완전한 채로 등록되므로, 기밀성이 높은 라이브러리에서는 기본값 그대로 두는 것이 안전합니다.

Graph 호출의 재시도는 ``max_retry_count``\ (기본값 3, 상한 10)와 ``retry_interval``\ (초, 기본값 3, 상한 180)로 조정할 수 있습니다.
``OneDriveDataStore``\ 에는 증분 크롤링 옵션이 없으며 매번 전체를 읽습니다.

Box: 계약서 폴더를 권한과 함께 가져오기
=======================================

Box 측 준비
-----------

``fess-ds-box``\ 는 JWT를 사용한 서버 인증만 지원합니다.

1. Box Developer Console에서 "Custom App"을 만들고 인증 방법으로 "Server Authentication (with JWT)"를 선택한다
2. [Configuration] 탭의 Application Scopes에서 "Read all files and folders stored in Box"를 사용 설정한다
3. App Access Level로 "App + Enterprise Access"를 선택한다
4. [Generate a Public/Private Keypair]\ 로 키 쌍을 만들고 JSON 파일을 저장한다
5. Box 관리 콘솔에서 앱을 승인한다

JSON 파일의 ``clientID``, ``clientSecret``, ``publicKeyID``, ``privateKey``, ``passphrase``, ``enterpriseID``\ 가 각각 ``client_id``, ``client_secret``, ``public_key_id``, ``private_key``, ``passphrase``, ``enterprise_id``\ 에 대응합니다.
6개 모두 필수입니다.

대상 폴더를 하나로 좁히기
-------------------------

법무팀의 계약서처럼 대상이 정해져 있는 경우에는 ``root_folder_id``\ 로 폴더를 하나만 읽습니다.
이 모드에서는 사용자로 가장하지 않고 앱의 서비스 계정으로 폴더를 읽습니다.
그러므로 서비스 계정을 대상 폴더의 협업자로 추가해 두어야 합니다.
폴더 ID는 Box 웹 화면에서 폴더를 열었을 때 URL 끝에 있는 숫자입니다.

.. code-block:: properties

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456
    root_folder_id=123456789
    default_permissions={group}legal
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at
    role=file.roles

"권한" 칸의 ``{role}guest``\ 는 반드시 지우십시오.
Box에서는 칸의 값이 ``file.roles``\ 에 합쳐지므로, 남겨 두면 계약서가 로그인하지 않은 사용자에게도 검색됩니다.

Box의 그룹은 그룹 ID로서 롤이 되므로 Fess 측의 그룹 이름과는 그대로는 일치하지 않습니다.
이 예에서는 ``default_permissions={group}legal``\ 로 Fess의 ``legal`` 그룹에 모든 파일을 보여 줍니다.
Box에서 개별적으로 공유된 사용자는 로그인(이메일 주소)이 Fess의 사용자 이름과 일치하면 이에 더해 검색할 수 있습니다.
사내 전체용 공유 링크가 붙은 파일에 롤을 추가하고 싶다면 ``company_shared_link_role``\ 을 사용합니다.

모든 사용자의 파일을 읽는 경우
------------------------------

``root_folder_id``\ 를 생략하면 엔터프라이즈의 모든 사용자를 열거하고, 한 명씩 가장하여 파일을 읽습니다.
대상 사용자는 ``filter_term``\ 으로 좁힐 수 있습니다.
가장을 통한 API 호출이 Box 측 앱 설정에서 허용되어 있어야 하므로, Box의 개발자용 문서에서 설정을 확인하십시오.

속도 제한 대응
--------------

``429``\ 와 ``5xx`` 응답의 재시도 횟수는 ``max_retry_attempts``\ (기본값 5)입니다.
``max_retry_count``\ (기본값 10)는 ``401`` 응답에서 연결을 다시 만드는 횟수로, 속도 제한과는 관계가 없습니다.
API 호출 간격을 벌리고 싶을 때는 ``readInterval``\ (밀리초)로 1건마다 대기 시간을 넣습니다.
``fess-ds-box``\ 에는 증분 크롤링 옵션이 없습니다.

운영에서 알아 둘 점
===================

인증 정보의 기한
----------------

- Entra ID의 클라이언트 시크릿에는 만들 때 정한 유효 기간이 있습니다. 기한이 지나면 인증 오류가 나서 가져올 수 없게 되므로, 기한 전에 새 시크릿을 만들어 파라미터의 ``client_secret``\ 을 교체합니다.
- Google의 액세스 토큰은 플러그인이 사용하는 라이브러리가 자동으로 갱신합니다. 15.9에서는 ``refresh_token_interval``\ 이 무시되고 경고가 로그에 출력됩니다.
- Box의 액세스 토큰은 ``refresh_token_interval``\ (기본값 3540초)마다 자동으로 갱신됩니다.

다 가져오지 못하는 경우
-----------------------

3개 플러그인 모두 크롤링 마지막에 작업 스레드의 종료를 기본 60초 기다리며, 끝나지 않은 부분은 가져오지 않습니다.
큰 테넌트에서 건수가 부족할 때는 대기 시간을 늘리십시오.
파라미터 이름은 Google Drive가 ``thread_pool_timeout_seconds``, SharePoint가 ``executor_shutdown_timeout``, Box가 ``thread_pool_await_timeout``\ 입니다(모두 초 단위).

Google Drive에서는 429, 500, 502, 503, 504 응답과 속도 제한으로 인한 403이 지수 백오프로 재시도됩니다.
재시도는 ``max_retries``\ (기본값 5), ``retry_initial_interval_ms``\ (기본값 1000), ``max_backoff_ms``\ (기본값 32000)로 조정할 수 있습니다.

동작 확인하기
=============

작업 결과와 로그를 보는 방법은 :doc:`datastore-basics`\ 에서 설명합니다.
데이터 저장소 크롤링은 파일 가져오기에 실패해도 작업이 "OK"로 표시될 수 있으므로, 건수와 로그로 판단하십시오.
이 글의 구성에서는 추가로 다음 3가지를 확인합니다.

1. 로그아웃한 상태에서 가져온 파일에 포함된 단어를 검색해, 1건도 나오지 않는 것을 확인한다("권한" 칸을 비우는 것을 잊지 않았는지)
2. 공유된 사용자로 로그인하면 같은 파일이 나오는 것을 확인한다
3. Google Drive 설정에서는 ``fess-crawler.log``\ 에 ``Skipped ... because no permission could be resolved``\ 가 나오지 않았는지 확인한다(ACL이 비어 있어 가져오지 않은 파일입니다)

2에서 나오지 않으면 사용자의 사용자 이름이나 그룹 이름이 ``file.roles``\ 의 값과 일치하는지 다시 확인합니다.

정리
====

- SharePoint의 파일 본문은 ``OneDriveDataStore``\ 로 가져오고, 필요 없다면 OneDrive와 그룹 드라이브를 ``false``\ 로 합니다.
- 3개 서비스 모두 "권한" 칸의 ``{role}guest``\ 를 지우고 스크립트에 ``role=file.roles``\ 를 씁니다.
- ``default_permissions``\ 는 Google Drive에서는 빈 ACL의 대체, SharePoint와 Box에서는 모든 파일에 대한 추가입니다.
- 증분 크롤링이 있는 것은 Google Drive(\ ``incremental=true``)뿐입니다. 사용하는 경우에는 전체 크롤링용 설정과 조합하고 양쪽에 ``time_to_live``\ 를 지정합니다.

참고 자료
=========

- `Google Workspace 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-gsuite.html>`__
- `Microsoft 365 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-microsoft365.html>`__
- `Box 커넥터 <https://fess.codelibs.org/ko/stable/config/datastore/ds-box.html>`__
- `데이터 저장소 설정 <https://fess.codelibs.org/ko/stable/admin/dataconfig-guide.html>`__
- `fess-ds-microsoft365 15.9.0 README(Graph 권한 목록) <https://github.com/codelibs/fess-ds-microsoft365/blob/fess-ds-microsoft365-15.9.0/README.md>`__
- `fess-ds-box 15.9.0 README(file.roles와 root_folder_id) <https://github.com/codelibs/fess-ds-box/blob/fess-ds-box-15.9.0/README.md>`__
