========================
SharePoint Server 커넥터
========================


개요
====

SharePoint Server 커넥터는 온프레미스 **SharePoint Server** (2013, 2016, 2019, Subscription
Edition)가 REST/OData API(2013의 경우 XML/Atom API)로 제공하는 문서 라이브러리 파일과 목록
항목을 가져와 |Fess| 인덱스에 등록하는 기능을 제공합니다.

이 기능을 사용하려면 ``fess-ds-sharepoint`` 플러그인이 필요합니다.

.. note::

   SharePoint Online(Microsoft 365)을 크롤링하려는 경우에는 이 커넥터가 아니라
   :doc:`ds-microsoft365` 를 사용하세요. 이 커넥터의 OAuth 인증은 Azure ACS의 애플리케이션
   전용 인증에만 대응하며, Microsoft Graph API와의 연동 기능은 없습니다.

지원 버전: SharePoint Server 2013 / 2016 / 2019 / Subscription Edition(SE)

지원 콘텐츠
===========

- 문서 라이브러리 파일
- 목록 항목
- 목록 항목의 첨부 파일

전제 조건
=========

1. 플러그인 설치가 필요합니다
2. 크롤링에 사용하는 계정에 크롤링 대상 사이트·목록·문서 라이브러리에 대한 읽기 권한이
   필요합니다
3. NTLM, Kerberos(SPNEGO), OAuth(ACS) 중 정확히 하나의 인증 방식을 선택하고 해당 자격
   증명을 준비해 두어야 합니다

플러그인 설치
-------------

관리 화면의 "시스템" → "플러그인"에서 설치합니다:

1. ``fess-ds-sharepoint-X.X.X.jar`` 다운로드
2. ``$FESS_HOME/app/WEB-INF/lib`` (또는 ``/usr/share/fess/app/WEB-INF/lib``)에 배치
3. |Fess| 재시작

자세한 내용은 :doc:`../../admin/plugin-guide` 를 참조하세요.

설정 방법
=========

관리 화면에서 "크롤러" → "데이터 스토어" → "새로 만들기"에서 이 커넥터를 설정합니다.

기본 설정
---------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 항목
     - 설정 예
   * - 이름
     - SharePoint
   * - 핸들러 이름
     - SharePointDataStore
   * - 활성화
     - 켬

파라미터 설정
-------------

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

파라미터 목록
~~~~~~~~~~~~~

**URL / 사이트**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``url``
     - 예
     - SharePoint 서버의 기본 URL(예: ``http://sharepoint.example.com/``)
   * - ``site.name``
     - 조건부
     - ``/sites/<site.name>/`` 하위에서 크롤링할 사이트 모음 이름. ``site.path`` 를 설정한
       경우 불필요
   * - ``site.path``
     - 아니오
     - 사이트의 서버 상대 관리되는 경로(예: ``/teams/eng``. 루트 사이트 모음은 ``/`` 를
       사용). 설정하면 하드코딩된 ``/sites/`` 프리픽스 대신 이 값이 그대로 사용되며,
       ``site.name`` 은 더 이상 필요하지 않음
   * - ``site.list_id``
     - 아니오
     - GUID로 목록 하나를 지정해 크롤링(목록 크롤 모드)
   * - ``site.list_name``
     - 아니오
     - 표시 이름으로 목록 하나를 지정해 크롤링(목록 크롤 모드)
   * - ``site.doclib_path``
     - 아니오
     - 사이트 하위의 문서 라이브러리 경로(문서 라이브러리 크롤 모드, 예:
       ``/Shared Documents``)
   * - ``site.exclude_list``
     - 아니오
     - 제외할 목록 엔터티 타입 이름의 정규식 패턴(쉼표 구분). 사이트 전체 크롤링에만
       적용됨
   * - ``site.exclude_folder``
     - 아니오
     - 제외할 최상위 폴더 이름의 정규식 패턴(쉼표 구분). 사이트 전체 크롤링에만 적용됨
   * - ``site.crawl_subsites``
     - 아니오
     - 사이트의 하위 사이트까지 재귀적으로 크롤링할지 여부(기본값: ``false``). 자세한
       내용은 `하위 사이트와 관리되는 경로`_ 참조
   * - ``site.max_depth``
     - 아니오
     - ``site.crawl_subsites`` 가 재귀적으로 탐색할 수 있는 하위 사이트 단계 수
       (기본값: ``10``). 루트는 깊이 0

**인증**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``auth.ntlm.user``
     - 아니오
     - NTLM 사용자 이름. 설정하면 NTLM 인증이 활성화됨(``DOMAIN\user`` 형식 가능)
   * - ``auth.ntlm.password``
     - 아니오
     - NTLM 비밀번호
   * - ``auth.ntlm.domain``
     - 아니오
     - Windows 도메인. NTLM의 독립된 필드로 전송됨
   * - ``auth.ntlm.workstation``
     - 아니오
     - NTLM 협상 과정에서 전송되는 워크스테이션 이름
   * - ``auth.kerberos.principal``
     - 아니오
     - 클라이언트 프린시펄(``user@REALM`` 형식). 설정하면 Kerberos/SPNEGO 인증이
       활성화됨
   * - ``auth.kerberos.keytab``
     - 아니오
     - 프린시펄의 키를 담은 키탭 파일 경로. ``auth.kerberos.password`` 와는 배타적
   * - ``auth.kerberos.password``
     - 아니오
     - 프린시펄의 비밀번호. 키탭이 설정되지 않은 경우에만 사용됨
   * - ``auth.kerberos.strip_port``
     - 아니오
     - 서비스 프린시펄 이름에서 포트를 제거할지 여부(기본값: ``true``)
   * - ``auth.kerberos.use_canonical_hostname``
     - 아니오
     - 서비스 프린시펄 이름을 만들기 전에 대상 호스트를 정규 이름으로 해석할지 여부
       (기본값: ``false``)
   * - ``auth.kerberos.krb5_conf``
     - 아니오
     - ``krb5.conf`` 경로. ``java.security.krb5.conf`` 가 아직 설정되지 않은 경우에만
       적용됨
   * - ``auth.kerberos.debug``
     - 아니오
     - ``Krb5LoginModule`` 의 디버그 출력을 활성화할지 여부(기본값: ``false``)
   * - ``auth.oauth.client_id``
     - 아니오
     - Azure ACS 애플리케이션 전용 OAuth 클라이언트 ID. 설정하면 OAuth 인증이 활성화됨
   * - ``auth.oauth.client_secret``
     - 아니오
     - OAuth 클라이언트 시크릿
   * - ``auth.oauth.tenant``
     - 아니오
     - 테넌트 이름(``.sharepoint.com`` 제외)
   * - ``auth.oauth.realm``
     - 아니오
     - Azure AD 렐름/디렉터리 ID

``auth.kerberos.principal``, ``auth.ntlm.user``, ``auth.oauth.client_id`` 중 **정확히
하나만** 설정할 수 있습니다. 자세한 내용은 `인증`_ 을 참조하세요.

**목록**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``list.items.number_per_page``
     - 아니오
     - ``GetListItems`` 의 페이지 크기(기본값: ``100``)
   * - ``list.item.content.include_fields``
     - 아니오
     - 필드 이름(쉼표 구분). 설정하면 이 목록 항목 필드들만 ``content`` 에 연결됨
   * - ``list.item.content.exclude_fields``
     - 아니오
     - 필드 이름 패턴(쉼표 구분, 각 요소는 정규식으로 처리됨). 내장된 다수의 표준
       필드에 더해 ``content`` 에서 제외됨
   * - ``list.is_sub_page``
     - 아니오
     - 목록 항목을 SitePages/wiki 하위 페이지로 취급할지 여부. 페이징 폴백과 웹 링크
       형식에 영향을 줌(기본값: ``false``)

**HTTP**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``http.connection_timeout``
     - 아니오
     - HTTP 연결 타임아웃(밀리초). 커넥션 풀 대기 타임아웃으로도 사용됨
       (기본값: ``30000``)
   * - ``http.socket_timeout``
     - 아니오
     - HTTP 소켓(읽기) 타임아웃(밀리초, 기본값: ``30000``)
   * - ``proxy_host``
     - 아니오
     - HTTP 프록시 호스트
   * - ``proxy_port``
     - 조건부
     - HTTP 프록시 포트. ``proxy_host`` 를 설정한 경우 필수(기본값: ``-1`` = 프록시 없음)

**필터링과 콘텐츠**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``include_pattern``
     - 아니오
     - 크롤링 대상이 되려면 항목의 값이 일치해야 하는 정규식. 여기서 말하는 "값"이
       무엇인지는 이 표 아래의 참고 사항을 확인
   * - ``exclude_pattern``
     - 아니오
     - 일치하는 항목을 크롤링 대상에서 제외하는 정규식
   * - ``supported_mimetypes``
     - 아니오
     - 파일의 MIME 타입이 하나 이상 일치해야 하는 정규식(쉼표 구분, 기본값: ``.*``)
   * - ``max_content_length``
     - 아니오
     - 파일의 최대 크기(바이트). 초과한 파일은 실패가 아니라 스킵됨
       (기본값: ``-1`` = 무제한)
   * - ``extractor_name``
     - 아니오
     - 익스트랙터 팩토리가 매핑하지 못하는 MIME 타입에만 사용되는 폴백 익스트랙터
       (기본값: ``tikaExtractor``)

**동작**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``sp.version``
     - 아니오
     - ``2013`` 을 지정하면 SharePoint 2013용 XML/Atom,
       ``GetXxxByServerRelativeUrl`` 계열 API로 전환됨(미설정 시 SharePoint Online /
       2016 이후 REST 방식)
   * - ``retry_limit``
     - 아니오
     - SharePoint 서버/클라이언트 예외 발생 시 크롤링 단위당 최대 재시도 횟수
       (기본값: ``2``)
   * - ``role.skip``
     - 아니오
     - 항목별 권한 가져오기를 완전히 건너뛸지 여부(기본값: ``false``). 자세한 내용은
       `권한`_ 참조
   * - ``ignore_error``
     - 아니오
     - 파일의 콘텐츠 추출에 실패했을 때 크롤링 대상을 실패시키는 대신 로그를 남기고
       건너뛸지 여부(기본값: ``false``)
   * - ``default_permissions``
     - 아니오
     - SharePoint가 반환한 권한에 더해, 모든 문서의 권한 목록에 병합할 권한 문자열
       (쉼표 구분)
   * - ``delete_old_docs``
     - 아니오
     - 이번 실행에서 다시 가져오지 못한 문서를 삭제할지 여부(코어 기본값: ``true``).
       이 플러그인은 크롤링 대상 중 하나라도 실패하면 이번 실행에 한해 이 값을 강제로
       ``false`` 로 설정함
   * - ``number_of_threads``
     - 아니오
     - 동시에 처리할 크롤링 대상 수(기본값: ``1`` = 스레드 풀 없음). 프로세서 수의
       2배가 상한. 자세한 내용은 `병렬 크롤링과 부하`_ 참조
   * - ``script_type``
     - 아니오
     - 데이터 설정 스크립트에 사용할 스크립트 엔진(기본값: ``groovy``)
   * - ``readInterval``
     - 아니오
     - 연속된 크롤링 결과 사이의 대기 시간(밀리초, 기본값: ``0``). 다른 파라미터와
       달리 camelCase 표기임에 유의

스크립트 설정
-------------

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

사용 가능한 필드
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 20 32 32

   * - 키
     - 목록 항목(ItemCrawl)
     - 문서 라이브러리 파일(FolderCrawl→FileCrawl)
     - 첨부 파일(ItemAttachmentsCrawl→FileCrawl)
   * - ``url``
     - 웹 링크
     - 파일 URL
     - 파일 URL
   * - ``host``
     - 호스트 이름
     - 호스트 이름
     - 호스트 이름
   * - ``site``
     - 서버 상대 경로(``FileRef``)
     - 서버 상대 경로
     - 서버 상대 경로
   * - ``title``
     - ``Title`` 필드, 없으면 ``FileLeafRef``/파일명
     - 문서 라이브러리 파일 자체의 ``Title`` 목록 값(있는 경우), 없으면 파일명
     - 파일명
   * - ``titleWithListName``
     - ``"[목록명] 제목"``
     - ``"[목록명] 파일명"`` (문서 라이브러리 크롤에서는 목록명이 항상 비어 있으므로
       실질적으로 파일명만 표시됨)
     - ``"[목록명] 파일명"``
   * - ``listName``
     - 목록 표시 이름, 또는 ``""``
     - 항상 ``""``
     - 실제 목록 이름
   * - ``content``
     - 필드 값의 연결
     - 추출된 텍스트
     - 추출된 텍스트
   * - ``digest``
     - ``content`` 의 요약
     - ``content`` 의 요약
     - ``content`` 의 요약
   * - ``content_length``
     - ``content.length()``
     - ``content.length()``
     - ``content.length()``
   * - ``last_modified``
     - 목록 조회 결과에서 가져옴
     - 목록 조회 결과에서 가져옴
     - 목록 조회 결과에서 가져옴
   * - ``created``
     - 목록 조회 결과에서 가져옴
     - 목록 조회 결과에서 가져옴
     - 목록 조회 결과에서 가져옴
   * - ``mimetype``
     - 항상 ``text/html``
     - 감지된 값
     - 감지된 값
   * - ``filetype``
     - ``mimetype`` 에서 파생
     - ``mimetype`` 에서 파생
     - ``mimetype`` 에서 파생
   * - ``role``
     - 권한 목록(비어 있지 않은 경우에만)
     - 권한 목록(비어 있지 않은 경우에만)
     - 권한 목록(비어 있지 않은 경우에만)
   * - ``list_name``
     - 있음
     - **없음**
     - 있음
   * - ``list_id``
     - 있음
     - **없음**
     - 있음
   * - ``item_id``
     - 있음
     - **없음**
     - 있음

.. note::

   ``content_length`` 는 ``content.length()``, 즉 추출·연결된 텍스트의 문자 수
   (UTF-16 코드 단위)이며 파일의 바이트 크기가 아닙니다. 이는 Box, Google Drive,
   Dropbox 커넥터의 ``file.size`` (각 서비스 자체의 파일 메타데이터에서 가져오는 실제
   바이트 크기)와는 값의 성격이 다르므로, 이 커넥터의 ``content_length`` 를 그것들과
   비교하지 마세요.

**동적 키: ``val_*``**

목록 항목의 ``FieldValuesAsText`` (SharePoint가 해당 항목에 대해 반환하는 원시 필드 값
맵으로, ``odata.metadata`` 등 OData 메타데이터 키도 포함됨)의 각 키는 두 가지 이름으로
노출됩니다: 프리픽스 없이(위의 고정 키와 이름이 겹치지 않는 경우에만) 한 번, 그리고
무조건 ``val_`` 프리픽스를 붙여서 한 번입니다. 예를 들어 ``Status`` 필드는 ``Status``
와 ``val_Status`` 양쪽 모두로 노출됩니다.

``val_*`` 키는 **목록 항목 크롤(ItemCrawl) 경로에서만** 존재합니다. 문서 라이브러리
파일(FolderCrawl→FileCrawl)이나 목록 항목의 첨부 파일(ItemAttachmentsCrawl→FileCrawl)
에서는 ``val_*`` 키가 전혀 생성되지 않습니다.

인증
====

인증 방식은 3가지가 있으며, **설정할 수 있는 것은 그중 하나뿐입니다**.
``auth.kerberos.principal``, ``auth.ntlm.user``, ``auth.oauth.client_id`` 중 2개 이상을
설정하면, 어떤 요청도 보내지기 전에 데이터 설정 잡이 유효성 검사 오류로 실패합니다. 이는
의도된 동작입니다: HTTP 클라이언트에 등록되는 자격 증명은 하나뿐이며, 그 자격 증명이
등록되는 스코프는 ``Negotiate`` 챌린지에도 ``NTLM`` 챌린지에도 똑같이 일치해 버리기
때문에, 여러 개를 설정하면 로그만 봐서는 원인을 알 수 없는 401이 반환될 뿐입니다.

NTLM
----

::

    auth.ntlm.user={SharePoint 사용자 이름}
    auth.ntlm.password={비밀번호}
    auth.ntlm.domain={Windows 도메인. 선택 사항, 기본값은 미설정}
    auth.ntlm.workstation={NTLM 협상에서 전송할 워크스테이션 이름. 선택 사항, 기본값은 미설정}

``auth.ntlm.domain`` 과 ``auth.ntlm.workstation`` 은 둘 다 기본값이 미설정이며, 이는 이
커넥터가 지금까지 항상 만들어 온 것과 정확히 같은 자격 증명을 구성합니다. 사용자 이름에
``DOMAIN\user`` 형식으로 도메인을 적어 넣는 방법도 계속 사용할 수 있습니다.
``auth.ntlm.domain`` 을 설정하면 도메인을 NTLM의 독립된 필드로 전송하게 되며, 이는
결합된 형식을 거부하는 서버에서 필요로 하는 방식입니다.

Kerberos(SPNEGO)
----------------

**지원 범위:** 크롤러 JVM 1개, Fess 인스턴스당 ``krb5.conf`` 1개, 키탭 또는 비밀번호,
위임(delegation) 없음, 채널 바인딩 없음, NTLM·OAuth와는 배타적 관계. 이 범위를 벗어나는
구성은 지원되지 않습니다.

::

    auth.kerberos.principal={클라이언트 프린시펄. user@REALM 형식으로 작성. 설정하면 Kerberos가 활성화됨}
    auth.kerberos.keytab={프린시펄의 키를 담은 키탭 파일 경로. auth.kerberos.password 와는 배타적}
    auth.kerberos.password={프린시펄의 비밀번호. 키탭이 설정되지 않은 경우에만 사용}
    auth.kerberos.strip_port={true 또는 false. 서비스 프린시펄 이름에서 포트를 제거할지 여부. 기본값은 true}
    auth.kerberos.use_canonical_hostname={true 또는 false. 서비스 프린시펄 이름을 위해 대상 호스트를 정규 이름으로 해석할지 여부. 기본값은 false}
    auth.kerberos.krb5_conf={krb5.conf 경로. java.security.krb5.conf 가 아직 설정되지 않은 경우에만 적용}
    auth.kerberos.debug={true 또는 false. Krb5LoginModule 디버그 출력. 기본값은 false}

- **``krb5.conf`` 는 ``jvm.crawler.options`` 에 설정합니다**
  (예: ``-Djava.security.krb5.conf=/path/to/krb5.conf``). 데이터 스토어 크롤링은
  크롤러의 **자식 프로세스** 에서 실행되므로, webapp 쪽에만 영향을 주는 설정을 해도
  효과가 없고, webapp을 재시작해도 반영되지 않습니다 — 반영하려면 크롤링 잡을 다시
  실행해야 합니다. ``auth.kerberos.krb5_conf`` 는 아직 이 프로퍼티가 설정되어 있지
  않을 때를 위한 편의 기능으로, **이미 설정된 값을 덮어쓰는 일은 절대 없습니다**
  (이 프로퍼티는 JVM 전역이며, 하나의 크롤러 JVM이 크롤링 잡의 모든 데이터 설정을
  실행하기 때문입니다). 덮어쓰지 않은 경우에는 두 경로를 모두 명시한 경고가 로그에
  출력됩니다.
- **``krb5.conf`` 의 ``[libdefaults]`` 에 ``udp_preference_limit = 1`` 을 설정하세요.**
  설정하지 않으면 JDK는 먼저 UDP로 시도하며, KDC가 응답하지 않는 경우(도달 불가,
  방화벽이 UDP 88을 차단, 응답이 데이터그램 크기를 초과 등) TCP로 폴백하기 전에 30초
  간격으로 3회 재시도합니다. 로그에 아무것도 남지 않은 채 인증 1회당 약 1분 반씩
  크롤링이 멈춘 것처럼 보인다면 대개 이것이 원인입니다.
- **프린시펄은 항상 ``user@REALM`` 형식으로 작성하세요.** ``default_realm`` 은 JVM
  전역 설정이며, 서로 다른 렐름에 속한 여러 SharePoint 팜이 하나의 ``krb5.conf`` 를
  공유해야 하는 경우도 있으므로, 렐름을 생략한 ``user`` 는 그 파일이 우연히 지정하고
  있는 렐름을 기준으로 해석되어 버립니다.
- **``auth.kerberos.use_canonical_hostname`` 은 기본값이 ``false``** 입니다. Apache
  HttpClient 자체의 기본값과는 의도적으로 다릅니다. 활성화하면 서비스 프린시펄 이름을
  만들기 전에 대상 호스트가 역방향 DNS 조회를 거치는데, 대체 액세스 매핑이나 로드
  밸런서 뒤에서는 어떤 SPN도 등록되어 있지 않은 이름이 만들어질 수 있으며, 그 결과로
  발생하는 실패는 DNS가 원인이라는 것을 전혀 알려주지 않습니다. SPN이 실제로 정규
  이름으로 등록되어 있는 경우에만 활성화하세요.
- **IIS Extended Protection이 ``tokenChecking=Require`` 로 설정되어 있으면 동작할 수
  없습니다.** Apache HttpClient는 4.5 계열과 5.x 계열 모두 채널 바인딩을 지원하지
  않습니다. IIS의 기본값은 ``None`` 이므로 보통은 문제가 되지 않지만, ``Require`` 로
  설정된 경우에는 우회 방법이 없습니다.
- **티켓은 크롤링용 HTTP 클라이언트를 만들 때 한 번만 획득되며, 이후 갱신되지
  않습니다.** 티켓 유효 기간보다 오래 걸리는 크롤링은 도중부터 인증에 실패하기
  시작합니다.
- **``auth.kerberos.password`` 는 ``auth.ntlm.password`` 와 마찬가지로 평문으로
  저장·표시됩니다.** Fess에는 데이터 스토어 핸들러 파라미터를 마스킹하는 기능이 없어,
  데이터 설정 편집 화면은 이를 일반 텍스트 영역으로 렌더링합니다. 가능하면
  ``auth.kerberos.keytab`` 을 사용하고, 키탭 파일에는 제한적인 권한을 설정하세요.
- ``auth.kerberos.debug=true`` 로 설정하면 ``Krb5LoginModule`` 은 Fess 로그가 아니라
  크롤러 프로세스의 표준 출력에 기록합니다.

OAuth(ACS)
----------

::

    auth.oauth.client_id={OAuth 클라이언트 ID}
    auth.oauth.client_secret={OAuth 클라이언트 시크릿}
    auth.oauth.tenant={테넌트 이름. .sharepoint.com 제외}
    auth.oauth.realm={Azure AD 렐름/디렉터리 ID}

``auth.oauth.client_id`` 를 설정하면 Windows Azure Access Control Service
(``https://accounts.accesscontrol.windows.net/{realm}/tokens/OAuth/2``)에 대한 클라이언트
자격 증명(애플리케이션 전용) 플로우가 활성화됩니다. 액세스 토큰은 크롤링용 HTTP
클라이언트를 만들 때 한 번만 취득되어 모든 요청에 ``Bearer`` ``Authorization`` 헤더로
부여되며, 401이 반환되면 한 번만 갱신하여 재시도합니다. **Microsoft는 ACS를 지원 중단
(deprecated) 처리했으며 폐지가 예정되어 있습니다.** OAuth를 설정한 크롤링을 실행할
때마다 이 사실을 알리는 경고가 로그에 출력됩니다. 이 플러그인에는 Entra ID 앱 등록
(인증서 또는 클라이언트 시크릿 방식) 플로우는 구현되어 있지 않으며, 레거시 ACS
애플리케이션 전용 인증만 지원합니다.

OAuth를 연결할지 판단할 때는 ``auth.oauth.client_id`` 의 존재 여부만 확인합니다.
``client_secret``, ``tenant``, ``realm`` 은 무조건 읽어 들이며, 생략하면 그대로 빈
값이 되어 전용 검증 메시지 없이 토큰 취득이 실패할 수 있습니다.

**``sp.version=2013`` 과 OAuth의 조합은 한 번도 동작한 적이 없습니다.** 이 플러그인이
SharePoint 2013을 대상으로 수행하는 모든 API 호출은 XML/Atom 클라이언트를 경유하는데,
그 클라이언트의 어떤 코드 경로도 OAuth 토큰을 요청에 부여하지 않습니다 — 따라서 둘 다
설정하면 모든 요청이 미인증 상태로 전송됩니다. 크롤링은 이 사실을 그대로 경고로 로그에
남기고 ``auth.ntlm.*`` 를 대안으로 명시하지만, 잡을 실패시키지는 않습니다. SharePoint
2013에는 ``auth.ntlm.*`` 를 사용하세요.

권한
====

``role.skip=true`` (기본값 ``false``)로 설정하면 항목별 권한 가져오기를 완전히
건너뜁니다: ``GetListItemRole`` 호출이 전혀 이루어지지 않고, 항목에 ``role`` 키가
설정되는 일도 없으며, 문서에는 데이터 설정 자체의 정적 Permission 설정과, 설정되어
있다면 ``default_permissions`` 만 반영됩니다 — SharePoint에서 유래한 권한은 전혀
반영되지 않습니다.

권한을 가져올 때는 SharePoint 자체의 사용자, 보안 그룹, SharePoint 그룹이 전개되어
Fess의 검색 권한으로 매핑됩니다:

- **온프레미스 AD** 계정이나 그룹(로그인 이름에 백슬래시를 포함하고, Azure 클레임
  프리픽스로 시작하지 않는 것)은 표준 AD 사용자/그룹 권한 헬퍼를 통해 매핑됩니다.
- **Azure AD(Entra ID)** 계정(로그인 이름이 ``i:0#.f|membership|`` 로 시작하는 것)은
  **두 가지 방식으로** 매핑됩니다 — Azure 클레임의 전체 값으로 한 번, 그 클레임의
  ``@`` 앞부분에 해당하는 AD 계정 부분으로 한 번, 이렇게 매핑되어 같은 사용자에 대해
  Entra ID 형식과 AD 형식 양쪽의 권한이 추가됩니다. 여러 클레임 형식 프리픽스 중
  하나(특별한 "전체 사용자" 그룹인 ``spo-grid-all-users`` 포함)로 Azure로 판별된 보안
  그룹도 동일하게 두 형식 모두로 매핑됩니다.
- **SharePoint 그룹** 은 자신의 멤버십(사용자, 보안 그룹, 중첩된 그룹)이 재귀적으로
  전개됩니다. 서로를 포함하는 그룹 사이의 무한 재귀를 막기 위한 방문 완료 그룹 가드도
  갖추고 있습니다.

``default_permissions`` (쉼표 구분)는 위의 모든 처리가 끝난 **뒤에** 병합되며,
SharePoint가 해당 항목에 대해 권한을 전혀 반환하지 않은 경우(``role.skip=true`` 인
경우와 "SharePoint가 아무것도 반환하지 않은" 경우 양쪽 모두에 해당)에도 적용됩니다.
최종 권한 목록은 데이터 설정 자체의 정적 Permission 설정, SharePoint에서 유래한 권한
(건너뛰지 않은 경우), 그리고 ``default_permissions`` 의 합집합에서 중복을 제거한
것입니다.

하위 사이트와 관리되는 경로
===========================

``site.path`` 를 설정하면 지정한 서버 상대 관리되는 경로가 하드코딩된 ``/sites/``
프리픽스 대신 그대로 사용되며, ``site.name`` 은 더 이상 필요하지 않습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 시나리오
     - 설정
   * - 루트 사이트 모음
     - ``site.path=/``
   * - ``/teams/eng`` 사이트
     - ``site.path=/teams/eng``
   * - 기존 방식의 ``/sites/mysite/`` 형태
     - ``site.name=mysite`` (``site.path`` 는 설정하지 않음)

``site.crawl_subsites`` (기본값 ``false``)를 설정하면, 사이트 전체 크롤링
(``site.list_name`` 도 ``site.doclib_path`` 도 설정하지 않은 크롤링)이
``_api/web/webinfos`` 로 찾아낸 사이트의 하위 사이트까지 재귀적으로 크롤링하게
됩니다. 설정하지 않은 채로 두면 크롤링은 지금까지와 정확히 같은 요청만 보내며,
``webinfos`` 자체를 전혀 요청하지 않는 것도 포함해 그대로 유지됩니다.

하위 사이트의 문서는 루트 사이트의 문서와 같은 데이터 설정 안에, 각자의 서버 상대
경로 아래에 색인됩니다 — 어떤 문서가 루트가 아니라 하위 사이트에서 왔는지를 나타내는
정보는 인덱스 어디에도 없습니다.

``site.max_depth`` (기본값 ``10``)는 ``site.crawl_subsites=true`` 일 때 루트
사이트로부터 몇 단계 아래의 하위 사이트까지 크롤링할지를 제한합니다. 루트 사이트
자체가 깊이 0이므로, ``site.max_depth=1`` 은 루트의 직계 하위 사이트까지만 크롤링하고
그 이상은 진행하지 않습니다. ``site.crawl_subsites=true`` 인 상태에서
``site.max_depth`` 를 ``1`` 미만으로 설정하면 이 기능은 사실상 다시 꺼진 상태가 되어
(하위 사이트가 전혀 크롤링되지 않음), 크롤링 시작 시 경고로 로그에 남습니다.

하위 사이트 크롤링을 켜면, 발견된 하위 사이트 수(``site.max_depth`` 로 제한됨)에
거의 비례해 **크롤링 전체 소요 시간이 늘어납니다**: 하위 사이트마다 자체적인 전체
폴더 목록 조회, 목록 조회, 그리고 (깊이 제한에 도달하지 않았다면) 자체적인
``webinfos`` 호출이, 루트 사이트 크롤링이 이미 수행하는 모든 작업에 더해서
발생하기 때문입니다.

`병렬 크롤링과 부하`_ 에서 설명하는 ``number_of_threads`` 와 ``readInterval`` 은,
하위 사이트를 재귀적으로 도는 크롤링에도 다른 어떤 크롤링과 마찬가지로 동일하게
적용됩니다.

병렬 크롤링과 부하
==================

``number_of_threads`` (기본값 ``1``)는 동시에 처리할 크롤링 대상의 수입니다.
기본값에서는 크롤링이 지금까지와 정확히 똑같이 동작합니다: 모든 대상이 크롤링
스레드 위에서 처리되며 **스레드 풀은 전혀 생성되지 않습니다.**

이 값은 Fess를 실행 중인 머신의 **프로세서 수의 2배를 상한** 으로 제한됩니다.
데이터 설정이 호스트가 처리할 수 있는 것보다 많은 동시성을 요구할 수 없도록 하기
위해서입니다. ``1`` 미만의 값, 또는 비어 있거나 해석할 수 없는 값은 그대로
반영되거나 잡을 실패시키는 대신 ``1`` 로 폴백합니다. 값이 상한에 걸렸거나 ``1``
미만이었던 경우에는 요청된 값과 실제 값이 함께 로그에 남고, 해석할 수 없는
값이었던 경우에는 경고가 로그에 남습니다. **비어 있는 값은 아무것도 로그에 남기지
않습니다** — 빈 값은 그 파라미터가 단순히 설정되지 않았음을 의미하기 때문입니다.

HTTP 커넥션 풀 크기도 이 값에 맞춰 조정됩니다. Apache HttpClient는 기본적으로
라우트당 2개의 커넥션만 허용하며, 크롤링 전체가 하나의 라우트로 취급됩니다: 이
값을 올리지 않으면 세 번째 이후의 스레드는 요청을 보내는 대신 커넥션을 기다리며
크롤링 시간을 소모하게 됩니다.

**``readInterval`` 은 이 값을 무엇으로 설정하든, 문서 전달 속도를 1건씩의 간격으로
계속 제어합니다.** 스레드는 크롤링의 탐색과 가져오기를 더 빠르게 하지만, 문서가
인덱서에 도달하는 속도를 더 빠르게 하지는 않습니다. 이는 의도된 설계입니다 —
운영자가 설정한 간격을 스레드 수로 나눠 버리면, 그 간격으로 제한하려던 부하를
오히려 그대로 배가시키게 되기 때문입니다. 앞선 문서들이 아직 전달 중일 때 한
문서의 처리를 끝낸 워커는 그냥 대기합니다.

``number_of_threads`` 를 올렸을 때 실제로 배가되는 것은 SharePoint에 대한 **요청
빈도** 입니다. 아래에서 설명하는 503 백오프와 ``X-SharePointHealthScore`` 대기는
크롤링 대상별로, 그것을 크롤링하는 스레드 위에서 적용되므로, ``n`` 개의 스레드는
단일 스레드 크롤링의 최대 ``n`` 배에 달하는 요청을 보내게 됩니다 — 팜이 "지금
바쁘다"고 신호를 보내는 동안도 예외는 아닙니다. 온프레미스 팜에서는 이 값을
단계적으로 올리세요.

스레드를 늘려도 실제로 얻을 수 있는 효과에는 다음 두 가지가 상한을 둡니다:

- **각 SharePoint 그룹의 멤버십은 처음 읽힐 때만 한 번에 하나의 스레드씩 순서대로
  읽힙니다.** 권한은 크롤링 전체가 공유하는 캐시를 통해 해결되며, 이 캐시는
  그룹의 멤버 조회 동안 유지되는 단일 잠금으로 보호됩니다. 이 잠금 덕분에, 어떤
  스레드가 멤버를 아직 읽는 중인 그룹을 다른 스레드에 넘겨서, 그 그룹이 보호하는
  항목을 권한 없이 색인해 버리는 사태를 막을 수 있습니다. 그룹이 한 번 캐시되면
  이후의 모든 참조는 저렴한 조회가 되므로, 이는 **콜드 캐시 비용** 입니다 —
  서로 다른 그룹이 많은 사이트의 크롤링은 초반 몇 분 동안 ``n`` 개 스레드보다는
  단일 스레드에 가까운 속도를 보이며, 항목들이 소수의 그룹을 공유하는 사이트에서는
  거의 영향이 없습니다. 권한을 전혀 읽지 않는 ``role.skip=true`` 는 이 비용을
  완전히 피합니다.
- 발견 처리는 사이트별로 순차적입니다: 한 사이트의 폴더 목록과 목록 조회는 하나의
  크롤링 대상이므로, 그 대상의 처리가 끝나 발견 결과가 큐에 들어갈 때까지
  스레드끼리 나눠 가질 작업이 없습니다.

**503 응답** 은 다른 오류와 마찬가지로 ``retry_limit`` 횟수까지 재시도되지만,
재시도마다 대기 시간이 늘어납니다: 2초, 4초, 8초로 30초를 상한으로 두 배씩
늘어나며, 각각 실제 값의 70~129%로 무작위화됩니다. 계속 503을 반환하는 크롤링
대상은 실제로 재시도가 이루어질 때마다 이 대기를 치르지만, 마지막 재시도 이후에는
치르지 않습니다.

**모든 응답** — 성공이든 실패든, 크롤링이 곧 버릴 예정인 목록의 한 페이지까지
포함해서 — 은 ``X-SharePointHealthScore`` 응답 헤더(0이 유휴, 10이 매우 바쁨)를
검사받습니다. 점수가 9 이상이면 크롤링은 다음 작업을 하기 전에 대기합니다: 점수
9는 약 2초, 점수 10은 약 4초 대기하며, 9를 넘는 매 점수마다 두 배씩 늘어납니다.
**이 대기는 상한 없이 크롤링 전체에 걸쳐 누적됩니다** — 지속적인 고부하 상태에서
헬스 스코어 9에 머무는 팜은 이 커넥터가 보내는 **요청 하나하나마다** 약 2초를
더하게 되며(모든 폴더·목록 조회의 모든 페이지 포함), 원래는 몇 시간이면 끝날
크롤링을 훨씬 더 오래 걸리게 만들 수 있습니다. 크롤링이 예상외로 자릿수 단위로
느려졌다면, 다른 원인을 의심하기 전에 먼저 해당 시간대의 팜 헬스 스코어를
확인하세요.

설정 예
=======

아래 예시는 모두 NTLM을 사용한다고 가정합니다. 대신 Kerberos나 OAuth를 사용하려면
`인증`_ 을 참조해 ``auth.ntlm.*`` 줄을 교체하세요.

목록 크롤
---------

파라미터:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.list_name=Tasks

스크립트:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

문서 라이브러리 크롤
--------------------

파라미터:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

스크립트:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

``/teams/`` 사이트 크롤링
-------------------------

``site.path`` 를 사용하면 ``/sites/`` 이외의 관리되는 경로 아래에 있는 사이트의
문서 라이브러리를 직접 지정할 수 있습니다.

파라미터:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/teams/eng
    site.doclib_path=/Shared Documents

스크립트:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

하위 사이트 재귀 크롤링
-----------------------

루트 사이트 모음에서 시작해 하위 사이트를 최대 3단계 깊이까지 따라갑니다.

파라미터:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/
    site.crawl_subsites=true
    site.max_depth=3

스크립트:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

제한 사항
=========

- **어떤 형태의 증분·차등 크롤링도 지원하지 않습니다.** 변경 토큰, 델타 쿼리, "마지막
  수정 이후"와 같은 필터링이 이 커넥터 어디에도 없으며, 실행할 때마다 설정된 모든
  목록·폴더·파일을 완전히 나열합니다. ``delete_old_docs`` 는 이번 전체 크롤링에서
  다시 발견되지 않은 문서를 이후에 삭제할지 여부만 제어하는 사후 정리 기능일 뿐,
  증분 가져오기가 아닙니다.
- **파일/폴더 이름 중의 ``%`` 와 ``#``** 은 기본(``2013`` 이외의) 코드 경로에서
  지원됩니다. 이 두 문자를 파일/폴더 이름에 사용할 수 있는 것은 SharePoint Server
  2019와 Subscription Edition뿐이며, 2016은 명시적으로 거부하고 2013도 거부합니다.
  기본 코드 경로는 디코딩된 경로를 받는 ``...ByServerRelativePath(decodedUrl=...)``
  계열 엔드포인트로 이런 파일에 접근하며, 색인에 등록하는 링크에서도 이 두 문자를
  이스케이프합니다. **``sp.version=2013`` 으로는 이런 파일에 접근할 수 없습니다.**
  예전의 ``...ByServerRelativeUrl(...)`` 계열 엔드포인트를 사용하는데, 이 엔드포인트는
  인자를 이미 인코딩된 URL로 해석하기 때문입니다. 이는 결함이 아니라 의도적인
  제한입니다. SharePoint 2013 팜 자체가 그런 이름을 보관할 수 없으므로, 문제가 되는
  것은 ``sp.version=2013`` 을 2019나 Subscription Edition 서버에 대해 사용하는
  경우뿐이며, 그 조합은 권장되지 않습니다. 자세한 내용은
  `Use of # and % characters in file and folder names
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2019>`__
  과 `File names - expanded support for special characters
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2016>`__
  을 참조하세요.
- **IIS Extended Protection의 ``tokenChecking=Require`` 는 지원할 수 없습니다.**
  Apache HttpClient는 4.5 계열과 5.x 계열 모두 Extended Protection의 ``Require``
  설정이 의존하는 채널 바인딩을 구현하지 않습니다. IIS는 이 설정의 기본값이
  ``None`` 이므로 대부분의 팜에는 영향이 없지만, ``Require`` 로 설정된 팜에 대한
  우회 방법은 없습니다.
- **데이터 설정 파라미터에 입력한 비밀번호는 평문으로 저장·표시됩니다.** 이는
  ``auth.ntlm.password`` 와 ``auth.kerberos.password`` 모두에 해당합니다: Fess에는
  데이터 스토어 핸들러 파라미터를 마스킹하는 기능이 없어, 데이터 설정 편집 화면은
  이를 일반 텍스트 영역으로 렌더링합니다. Kerberos를 사용할 수 있는 환경에서는
  ``auth.kerberos.password`` 보다 ``auth.kerberos.keytab`` 을 우선하고, 키탭
  파일에는 제한적인 권한을 설정하세요.
- **``sp.version=2013`` 과 OAuth의 조합은 한 번도 동작한 적이 없습니다.** SharePoint
  2013을 대상으로 하는 모든 API 호출은 XML/Atom 클라이언트를 경유하며, 그
  클라이언트의 어떤 코드 경로도 OAuth 토큰을 요청에 부여하지 않으므로, 둘 다
  설정하면 모든 요청이 미인증 상태로 전송됩니다. SharePoint 2013에는
  ``auth.ntlm.*`` 를 사용하세요.
- **``/sites/`` 및 ``site.path`` 로 설정한 하나의 관리되는 경로 이외는 자동으로
  발견되지 않습니다.** ``site.crawl_subsites`` 는 설정한 루트 사이트로부터의
  재귀만 수행하며, ``site.path`` 는 설정한 그 하나의 관리되는 경로에만 도달할
  뿐, 팜에 있는 모든 관리되는 경로를 아우르지는 않습니다.

문제 해결
=========

인증이 조용히 실패하는 경우
---------------------------

**증상**: 요청이 401(또는 유사한 오류)로 돌아오지만 로그에 명확한 원인이 나타나지
않음

**확인 사항**:

1. ``auth.kerberos.principal``, ``auth.ntlm.user``, ``auth.oauth.client_id`` 중
   2개 이상이 설정되어 있지 않은지 확인(2개 이상 설정하면 크롤링 시작 전에
   유효성 검사 오류로 잡이 실패함)
2. Kerberos를 사용하는 경우, ``jvm.crawler.options`` 에
   ``-Djava.security.krb5.conf=...`` 가 설정되어 있는지 확인. webapp 쪽에만
   영향을 주는 곳에 설정해도 효과가 없음. 변경 후에는 크롤링 잡을 다시 실행
   (webapp 재시작으로는 반영되지 않음)
3. Kerberos를 사용하는 경우, ``krb5.conf`` 의 ``[libdefaults]`` 에
   ``udp_preference_limit = 1`` 이 설정되어 있는지 확인. 설정하지 않으면 KDC가
   응답하지 않을 때 인증 1회당 약 90초(30초 UDP 재시도 3회) 동안 로그에 아무것도
   남기지 않은 채 멈출 수 있음
4. 프린시펄이 ``user@REALM`` 형식으로 작성되어 있는지 확인(렐름을 생략한
   ``user`` 는 공유된 ``krb5.conf`` 가 우연히 지정하고 있는 ``default_realm`` 을
   기준으로 해석됨)
5. OAuth를 사용하는 경우, ``client_secret``, ``tenant``, ``realm`` 이 비어 있지
   않은지 확인(``client_id`` 의 존재 여부만 검증되므로 나머지는 아무 말 없이 빈
   값일 수 있음)
6. IIS Extended Protection이 ``tokenChecking=Require`` 로 설정되어 있지 않은지
   확인(이 설정에는 우회 방법이 없음)
7. 오래 실행되는 크롤링의 경우, 도중부터 실패하기 시작했는지 확인(Kerberos 티켓은
   HTTP 클라이언트 생성 시 한 번만 획득되고 이후 갱신되지 않으므로, 티켓 유효
   기간보다 오래 걸리는 크롤링은 도중부터 실패하기 시작함)

크롤링이 느린 경우(503과 헬스 스코어)
-------------------------------------

**증상**: 크롤링이 예상보다 훨씬 오래 걸리거나 타임아웃됨

**확인 사항**:

1. 느려진 시간대의 SharePoint 팜 ``X-SharePointHealthScore`` 를 확인. 점수가 9
   이상이면 모든 요청 전에 대기가 추가되며(9에서 약 2초, 10에서 약 4초, 이후
   배증, 합계 상한 없음), 원래 몇 시간이면 끝날 크롤링이 훨씬 더 오래 걸리게
   될 수 있음
2. 503 응답이 반복되고 있지 않은지 확인. 503은 ``retry_limit`` 횟수까지
   재시도되며, 재시도마다 2초, 4초, 8초(상한 30초) 순으로 대기함
3. ``number_of_threads`` 를 지나치게 높이지 않았는지 확인. 스레드 수가 늘어나면
   SharePoint에 대한 요청 수도 거의 그만큼 늘어나므로 헬스 스코어가 더 나빠질
   수 있음. 온프레미스 팜에서는 단계적으로 올릴 것
4. ``site.crawl_subsites=true`` 인 경우, 전체 크롤링 시간이 발견된 하위 사이트
   수에 거의 비례해 늘어난다는 점에 유의. ``site.max_depth`` 로 범위를 좁히는
   것을 고려

색인되는 문서가 없음
--------------------

**증상**: 크롤링은 정상적으로 끝나지만 검색 결과가 0건

**확인 사항**:

1. 크롤러 로그에서 오류나 경고를 확인
   (``app/WEB-INF/env/crawler/resources/log4j2.xml`` 에서 ``org.codelibs.fess.ds``
   를 ``DEBUG`` 로 설정)
2. ``url``, ``site.name`` (또는 ``site.path``), ``site.list_name`` 에 오타가
   없는지 확인(``site.path`` 를 설정하면 ``site.name`` 은 필요 없다는 점에 유의)
3. 인증이 실제로 성공하고 있는지 확인(401이 발생하지 않는지) — 애초에 인증되지
   않는 요청 쪽이, ``role.skip`` 이나 ``default_permissions`` 설정 오류보다
   훨씬 흔한 원인임
4. ``include_pattern`` 이나 ``exclude_pattern`` 을 설정한 경우, 이들은 검색
   결과에 표시되는 URL이 아니라 서버 상대 경로(문서 라이브러리 파일이나 목록
   항목 첨부 파일의 경우) 또는 ``FileRef`` (목록 항목의 경우)에 대해 매칭된다는
   점에 유의. 전체 URL을 가정한 패턴이 되어 있지 않은지 확인
5. ``supported_mimetypes`` 나 ``max_content_length`` 설정으로 원하는 파일이
   제외되고 있지 않은지 확인
6. ``site.exclude_list`` 나 ``site.exclude_folder`` 가 의도치 않게 대상을
   제외하고 있지 않은지 확인

참고 정보
=========

- :doc:`ds-overview` - 데이터 스토어 커넥터 개요
- :doc:`ds-microsoft365` - Microsoft 365 커넥터(SharePoint Online용)
- :doc:`../../admin/dataconfig-guide` - 데이터 스토어 설정 가이드
- :doc:`../../admin/plugin-guide` - 플러그인 관리 가이드
