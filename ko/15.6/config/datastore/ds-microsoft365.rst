==================================
Microsoft 365 커넥터
==================================

개요
====

Microsoft 365 커넥터는 Microsoft 365 서비스(OneDrive, OneNote, Teams, SharePoint)에서 데이터를 가져와서
|Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-microsoft365`` 플러그인이 필요합니다.

지원 서비스
============

- **OneDrive**: 사용자 드라이브, 그룹 드라이브, 공유 문서
- **OneNote**: 노트북(사이트, 사용자, 그룹)
- **Teams**: 채널, 메시지, 채팅
- **SharePoint Document Libraries**: 문서 라이브러리 메타데이터
- **SharePoint Lists**: 목록과 목록 항목
- **SharePoint Pages**: 사이트 페이지, 뉴스 기사

전제조건
========

1. 플러그인 설치가 필요합니다
2. Azure AD 애플리케이션 등록이 필요합니다
3. Microsoft Graph API 권한 설정과 관리자 동의가 필요합니다
4. Java 21 이상, Fess 15.2.0 이상

플러그인 설치
------------------------

방법 1: JAR 파일 직접 배치

::

    # Maven Central에서 다운로드
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # 배치
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 또는
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

방법 2: 소스에서 빌드

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

설치 후 |Fess|를 재시작하세요.

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
     - Microsoft 365 OneDrive
   * - 핸들러 이름
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - 활성화
     - 켬

파라미터 설정(공통)
------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

공통 파라미터 목록
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``tenant``
     - 예
     - Azure AD 테넌트 ID
   * - ``client_id``
     - 예
     - 앱 등록 클라이언트 ID
   * - ``client_secret``
     - 예
     - 앱 등록 클라이언트 시크릿
   * - ``number_of_threads``
     - 아니오
     - 병렬 처리 스레드 수(기본값: 1)
   * - ``ignore_error``
     - 아니오
     - 오류 시에도 처리 계속(기본값: false)
   * - ``include_pattern``
     - 아니오
     - 포함할 콘텐츠의 정규표현식 패턴
   * - ``exclude_pattern``
     - 아니오
     - 제외할 콘텐츠의 정규표현식 패턴
   * - ``default_permissions``
     - 아니오
     - 기본 역할 할당

Azure AD 애플리케이션 등록
============================

1. Azure Portal에서 애플리케이션 등록
---------------------------------------

https://portal.azure.com 에서 Azure Active Directory를 열기:

1. "앱 등록" → "새 등록" 클릭
2. 애플리케이션 이름 입력
3. 지원되는 계정 유형 선택
4. "등록" 클릭

2. 클라이언트 시크릿 생성
---------------------------------

"인증서 및 비밀"에서:

1. "새 클라이언트 시크릿" 클릭
2. 설명과 유효기간 설정
3. 시크릿 값 복사(나중에 확인 불가하므로 주의)

3. API 권한 추가
----------------

"API 권한"에서:

1. "권한 추가" 클릭
2. "Microsoft Graph" 선택
3. "애플리케이션 권한" 선택
4. 필요한 권한 추가(아래 참조)
5. "관리자 동의 부여" 클릭

데이터 스토어별 필요 권한
==========================

OneDriveDataStore
-----------------

필수 권한:

- ``Files.Read.All``

조건부 권한:

- ``User.Read.All`` - user_drive_crawler=true인 경우
- ``Group.Read.All`` - group_drive_crawler=true인 경우
- ``Sites.Read.All`` - shared_documents_drive_crawler=true인 경우

OneNoteDataStore
----------------

필수 권한:

- ``Notes.Read.All``

조건부 권한:

- ``User.Read.All`` - user_note_crawler=true인 경우
- ``Group.Read.All`` - group_note_crawler=true인 경우
- ``Sites.Read.All`` - site_note_crawler=true인 경우

TeamsDataStore
--------------

필수 권한:

- ``Team.ReadBasic.All``
- ``Group.Read.All``
- ``Channel.ReadBasic.All``
- ``ChannelMessage.Read.All``
- ``ChannelMember.Read.All``
- ``User.Read.All``

조건부 권한:

- ``Chat.Read.All`` - chat_id를 지정하는 경우
- ``Files.Read.All`` - append_attachment=true인 경우

SharePointDocLibDataStore
-------------------------

필수 권한:

- ``Files.Read.All``
- ``Sites.Read.All``

또는 ``Sites.Selected`` (site_id 지정 시, 사이트마다 설정 필요)

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

필수 권한:

- ``Sites.Read.All``

또는 ``Sites.Selected`` (site_id 지정 시, 사이트마다 설정 필요)

스크립트 설정
==============

OneDrive
--------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

사용 가능한 필드:

- ``file.name`` - 파일명
- ``file.description`` - 파일 설명
- ``file.contents`` - 텍스트 콘텐츠
- ``file.mimetype`` - MIME 타입
- ``file.filetype`` - 파일 타입
- ``file.created`` - 생성 일시
- ``file.last_modified`` - 최종 수정 일시
- ``file.size`` - 파일 크기
- ``file.web_url`` - 브라우저에서 열 URL
- ``file.roles`` - 액세스 권한

OneNote
-------

::

    title=notebook.name
    content=notebook.contents
    created=notebook.created
    last_modified=notebook.last_modified
    url=notebook.web_url
    role=notebook.roles
    size=notebook.size

사용 가능한 필드:

- ``notebook.name`` - 노트북 이름
- ``notebook.contents`` - 섹션과 페이지의 통합 콘텐츠
- ``notebook.size`` - 콘텐츠 크기(문자 수)
- ``notebook.created`` - 생성 일시
- ``notebook.last_modified`` - 최종 수정 일시
- ``notebook.web_url`` - 브라우저에서 열 URL
- ``notebook.roles`` - 액세스 권한

Teams
-----

::

    title=message.title
    content=message.content
    created=message.created_date_time
    last_modified=message.last_modified_date_time
    url=message.web_url
    role=message.roles

사용 가능한 필드:

- ``message.title`` - 메시지 제목
- ``message.content`` - 메시지 콘텐츠
- ``message.created_date_time`` - 생성 일시
- ``message.last_modified_date_time`` - 최종 수정 일시
- ``message.web_url`` - 브라우저에서 열 URL
- ``message.roles`` - 액세스 권한
- ``message.from`` - 발신자 정보

SharePoint Document Libraries
------------------------------

::

    title=doclib.name
    content=doclib.content
    created=doclib.created
    last_modified=doclib.modified
    url=doclib.url
    role=doclib.roles

사용 가능한 필드:

- ``doclib.name`` - 문서 라이브러리 이름
- ``doclib.description`` - 라이브러리 설명
- ``doclib.content`` - 검색용 통합 콘텐츠
- ``doclib.created`` - 생성 일시
- ``doclib.modified`` - 최종 수정 일시
- ``doclib.url`` - SharePoint URL
- ``doclib.site_name`` - 사이트 이름

SharePoint Lists
----------------

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

사용 가능한 필드:

- ``item.title`` - 목록 항목 제목
- ``item.content`` - 텍스트 콘텐츠
- ``item.created`` - 생성 일시
- ``item.modified`` - 최종 수정 일시
- ``item.url`` - SharePoint URL
- ``item.fields`` - 모든 필드의 맵
- ``item.roles`` - 액세스 권한

SharePoint Pages
----------------

::

    title=page.title
    content=page.content
    created=page.created
    last_modified=page.modified
    url=page.url
    role=page.roles

사용 가능한 필드:

- ``page.title`` - 페이지 제목
- ``page.content`` - 페이지 콘텐츠
- ``page.created`` - 생성 일시
- ``page.modified`` - 최종 수정 일시
- ``page.url`` - SharePoint URL
- ``page.type`` - 페이지 타입(news/article/page)
- ``page.roles`` - 액세스 권한

데이터 스토어별 추가 파라미터
================================

OneDrive
--------

::

    max_content_length=-1
    ignore_folder=true
    supported_mimetypes=.*
    drive_id=
    shared_documents_drive_crawler=true
    user_drive_crawler=true
    group_drive_crawler=true

OneNote
-------

::

    site_note_crawler=true
    user_note_crawler=true
    group_note_crawler=true

Teams
-----

::

    team_id=
    exclude_team_ids=
    include_visibility=
    channel_id=
    chat_id=
    ignore_replies=false
    append_attachment=true
    ignore_system_events=true
    title_dateformat=yyyy/MM/dd'T'HH:mm:ss
    title_timezone_offset=Z

SharePoint Document Libraries
-----------------------------

::

    site_id=
    exclude_site_id=
    ignore_system_libraries=true

SharePoint Lists
----------------

::

    site_id=hostname,siteCollectionId,siteId
    list_id=
    exclude_list_id=
    list_template_filter=
    ignore_system_lists=true

SharePoint Pages
----------------

::

    site_id=
    exclude_site_id=
    ignore_system_pages=true
    page_type_filter=

사용 예
======

OneDrive 전체 드라이브 크롤링
----------------------------

파라미터:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    user_drive_crawler=true
    group_drive_crawler=true
    shared_documents_drive_crawler=true

스크립트:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

특정 팀의 Teams 메시지 크롤링
------------------------------------

파라미터:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    team_id=19:abc123def456@thread.tacv2
    ignore_replies=false
    append_attachment=true
    title_timezone_offset=+09:00

스크립트:

::

    title=message.title
    content=message.content
    created=message.created_date_time
    url=message.web_url
    role=message.roles

SharePoint 목록 크롤링
--------------------------

파라미터:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    site_id=contoso.sharepoint.com,686d3f1a-a383-4367-b5f5-93b99baabcf3,12048306-4e53-420e-bd7c-31af611f6d8a
    list_template_filter=100,101
    ignore_system_lists=true

스크립트:

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

문제 해결
======================

인증 오류
----------

**증상**: ``Authentication failed`` 또는 ``Insufficient privileges``

**확인 사항**:

1. 테넌트 ID, 클라이언트 ID, 클라이언트 시크릿이 올바른지 확인
2. Azure Portal에서 필요한 API 권한이 부여되었는지 확인
3. 관리자 동의가 부여되었는지 확인
4. 클라이언트 시크릿 유효기간 확인

API 속도 제한 오류
-------------------

**증상**: ``429 Too Many Requests``

**해결 방법**:

1. ``number_of_threads``를 줄임(1 또는 2로 설정)
2. 크롤링 간격을 늘림
3. ``ignore_error=true``를 설정하여 계속 처리

데이터를 가져올 수 없음
--------------------

**증상**: 크롤링은 성공하지만 문서가 0개

**확인 사항**:

1. 대상 데이터가 존재하는지 확인
2. API 권한이 올바르게 설정되었는지 확인
3. 사용자/그룹 드라이브 크롤러 설정 확인
4. 로그에서 오류 메시지 확인

SharePoint 사이트 ID 확인 방법
----------------------------

PowerShell로 확인:

::

    Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive
    Get-PnPSite | Select Id

또는 Microsoft Graph API로:

::

    GET https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/yoursite

대량 데이터 크롤링
--------------------

**해결 방법**:

1. 여러 데이터 스토어로 분할(사이트 단위, 드라이브 단위 등)
2. 스케줄 설정으로 부하 분산
3. ``number_of_threads``를 조정하여 병렬 처리
4. 특정 폴더/사이트만 크롤링

참고 정보
========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-gsuite` - Google Workspace 커넥터
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
