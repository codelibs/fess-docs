==================================
SSO와 접근 보호로 검색 기반 지키기
==================================

들어가며
========

사내 검색 기반에는 권한으로 보호된 문서가 모입니다.
사용자에게 Fess 전용 비밀번호를 나눠 주는 대신, 사내 ID 기반(IdP)으로 로그인하게 하고 그 그룹으로 검색 결과를 좁히고 싶다는 것이 많은 도입 현장의 요구 사항입니다.

이 글에서는 Fess 15.9에서 다음 설정을 하고, 동작하는 것을 확인하는 데까지 설명합니다.

- Entra ID·OpenID Connect·SAML·SPNEGO 중 하나로 싱글 사인온(SSO)한다
- "로그인 필요"로, 로그인하지 않은 사용자가 검색하지 못하게 한다
- TLS를 종단하는 리버스 프록시 뒤에서 Fess가 HTTPS를 올바르게 인식하게 한다
- 액세스 토큰과 감사 로그·검색 로그의 보존 기간을 점검한다

역할과 그룹을 어떻게 설계하고 크롤링 설정의 권한에 어떻게 적을지는 :doc:`guide-05`\ 에서 다룹니다.

SSO는 플러그인으로 제공된다
===========================

Fess 15.9에서는 SSO 인증 처리가 본체에서 4개의 플러그인으로 분리되었습니다.

.. list-table::
   :header-rows: 1
   :widths: 16 18 18 22 26

   * - 방식
     - 플러그인
     - "SSO Type"(``sso.type``)
     - 사용자 이름의 출처
     - 그룹·역할의 출처
   * - Microsoft Entra ID
     - ``fess-sso-entraid``
     - Entra ID(``entraid``)
     - 로그인한 계정의 사용자 이름(보통은 UPN)
     - Microsoft Graph로 가져온 그룹·역할
   * - OpenID Connect
     - ``fess-sso-oidc``
     - OpenID Connect(``oic``)
     - ID Token의 ``email`` 클레임
     - ID Token의 ``groups`` 클레임. 역할은 "기본 역할"뿐
   * - SAML 2.0
     - ``fess-sso-saml``
     - SAML(``saml``)
     - 어설션의 NameID
     - "그룹 속성 이름"(기본값 ``memberOf``)과 "역할 속성 이름"의 속성값
   * - SPNEGO(Kerberos)
     - ``fess-sso-spnego``
     - SPNEGO(``spnego``)
     - Kerberos 주체에서 ``@`` 앞부분
     - [일반]의 LDAP 설정으로 가져온 그룹

OpenID Connect만은 플러그인 이름(``oidc``)과 ``sso.type`` 값(``oic``)이 다릅니다.

어느 방식이든 절차는 같습니다.

1. 플러그인을 설치하고 Fess를 재시작한다
2. IdP 쪽에 Fess를 등록한다. 돌아올 주소(리다이렉트 URI·ACS URL)는 ``https://<Fess 호스트>/sso/``\ 입니다
3. 관리 화면의 [시스템] > [일반]에서 방식별 섹션에 IdP 정보를 입력하고, "SSO Type"을 선택한 뒤 갱신한다
4. 브라우저에서 ``https://<Fess 호스트>/sso/``\ 를 열고, IdP를 거쳐 로그인할 수 있는지 확인한다

플러그인 설치
-------------

Docker 이미지(``ghcr.io/codelibs/fess:15.9.0``)에는 4개의 SSO 플러그인이 들어 있습니다(``-slim``\ 이 붙은 이미지에는 들어 있지 않습니다).
ZIP·DEB·RPM 패키지에는 동봉되지 않으므로, [시스템] > [플러그인]의 [설치]에서 설치하거나 다음 명령으로 설치합니다.

::

    $ bin/fess-setup install plugin fess-sso-entraid

설치·삭제 후에는 Fess를 재시작합니다.
플러그인은 Fess와 같은 마이너 버전(15.9.x)을 사용하십시오.

플러그인 없이 "SSO Type"을 선택하면 ``/sso/``\ 는 로그인 화면으로 돌아갈 뿐이며, ``fess.log``\ 에 ``No SSO authenticator is registered as ...``\ 라는 WARN이 한 번 출력됩니다.

설정의 저장 위치
----------------

[일반]에서 입력한 값은 ``system.properties``\ 에 저장됩니다(ZIP 패키지는 ``app/WEB-INF/conf/``, DEB·RPM 패키지는 ``/etc/fess/``).
OpenID Connect·SAML·Entra ID 항목은 로그인 처리 때마다 읽히므로, 저장하면 재시작 없이 사용됩니다.
SPNEGO 항목은 프로세스 전체에서 공유되므로, 변경한 후 재시작이 필요합니다.

Docker의 ``fess01`` 컨테이너에는 볼륨이 없어서, ``docker compose down`` 후에 ``up``\ 하면 [일반]의 설정이 사라집니다.
컨테이너를 다시 만들기 전에 [시스템 정보] > [백업]에서 ``system.properties``\ 를 다운로드하고, 다시 만든 뒤에 같은 화면에서 업로드하여 되돌립니다.

Entra ID로 SSO하기
==================

Microsoft 365를 사용하는 조직에서는 ``fess-sso-entraid``\ 가 간편합니다.
그룹은 로그인 후에 Microsoft Graph에서 가져오므로, IdP 쪽에서 그룹 클레임을 설정할 필요가 없습니다.

Entra ID 쪽 설정
----------------

Azure Portal의 "앱 등록"에서 새로 등록하고, 다음과 같이 설정합니다.

- 지원되는 계정 유형: 이 조직 디렉터리의 계정만
- 리다이렉트 URI: 플랫폼 "Web"으로 ``https://fess.example.com/sso/``\ (끝의 ``/``\ 까지 일치시킵니다)
- "인증서 및 비밀"에서 클라이언트 비밀을 만들고 값을 적어 둔다(만든 직후에만 표시됩니다)
- "API 권한"에서 Microsoft Graph의 위임된 권한 ``User.Read``\ 와 ``GroupMember.Read.All``\ 을 추가하고, 관리자 동의를 부여한다

``GroupMember.Read.All``\ 이 없으면 중첩된 상위 그룹을 가져올 수 없으며, ``fess.log``\ 에 ``Not allowed to read the parent groups of ...``\ 라는 경고가 출력됩니다.

Fess 쪽 설정
------------

[시스템] > [일반]의 "Entra ID" 섹션에 입력합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 항목
     - 키
     - 값
   * - 테넌트 (ID 또는 도메인)
     - ``entraid.tenant``
     - 디렉터리(테넌트) ID 또는 ``yourcompany.onmicrosoft.com``
   * - 클라이언트 ID
     - ``entraid.client.id``
     - 애플리케이션(클라이언트) ID
   * - 클라이언트 암호
     - ``entraid.client.secret``
     - 만든 비밀의 값
   * - 회신 URL
     - ``entraid.reply.url``
     - ``https://fess.example.com/sso/``

마지막으로 "시스템" 섹션의 "SSO Type"에서 "Entra ID"를 선택하고 [갱신]을 누릅니다.

그룹과 문서의 권한을 일치시키기
-------------------------------

Entra ID에서 얻은 그룹과 역할은 그 ID(GUID)가 반드시 권한이 됩니다.
여기에 더해 "권한 필드"(``entraid.permission.fields``, 기본값 ``mail``)에 나열한 속성의 값도 권한이 됩니다.

보안 그룹은 메일이 활성화되어 있지 않으므로, 기본값 그대로면 GUID만 권한이 됩니다.
파일 서버의 ACL이 그룹 이름으로 작성되어 있는 경우에는 "권한 필드"를 ``mail,displayName``\ 으로 합니다.
다만 ``displayName``\ 은 고유하지 않으므로, Windows 기본 제공 그룹(``Administrators`` 등)과 같은 이름의 그룹이 있으면 그 문서에도 일치합니다.

크롤링 설정의 권한에는 가져온 값을 그대로 ``{group}``\ 을 붙여 적습니다(예: ``{group}sales@example.com``).

.. warning::

   "기본 역할"(``entraid.default.roles``)은 테넌트의 모든 사용자에게 부여됩니다.
   여기에 ``admin``\ 을 넣으면 모든 사람이 관리 화면에 들어갈 수 있게 됩니다.

OpenID Connect·SAML·SPNEGO로 SSO하기
====================================

OpenID Connect
--------------

Keycloak이나 Okta 등의 OpenID Connect 공급자와는 ``fess-sso-oidc``\ 로 연동합니다.
공급자 쪽에서는 Fess를 웹 애플리케이션(클라이언트)으로 등록하고, 리다이렉트 URI를 ``https://fess.example.com/sso/``\ 로 합니다.

[일반]의 "OpenID Connect" 섹션에 입력하는 주요 항목은 다음과 같습니다.

- 권한 부여 서버 URL(``oic.auth.server.url``)과 토큰 서버 URL(``oic.token.server.url``): 공급자의 ``/.well-known/openid-configuration``\ 에 있는 값을 각각 입력합니다. 토큰 서버 URL은 ``https``\ 여야 합니다(``localhost``·``127.x.x.x``·``::1``\ 만 ``http`` 가능)
- 클라이언트 ID·클라이언트 암호
- 범위: ``openid email``. 사용자 이름은 ``email`` 클레임에서 가져오므로 ``email``\ 이 필요합니다
- 베이스 URL(``oic.base.url``): ``https://fess.example.com``. 리디렉션 URL을 비워 두면 ``{베이스 URL}/sso/``\ 가 됩니다

그룹은 ID Token의 ``groups`` 클레임 값이 그대로 권한이 됩니다.
Entra ID처럼 상위 그룹을 따라가지 않으므로, 중첩된 그룹이 필요하면 공급자 쪽에서 클레임에 포함합니다.
역할은 클레임에서 가져오지 않고, "기본 역할"의 값만 부여됩니다.

발급자(``iss``)를 검증하는 ``oic.issuer``\ 는 [일반]에 항목이 없으므로, ``system.properties``\ 에 직접 적습니다.

SAML
----

``fess-sso-saml``\ 에서는 Fess가 SP로 동작합니다.
IdP는 어설션을 크로스 사이트 POST로 돌려주므로, 기본값 ``tomcat.sameSiteCookies = lax`` 그대로는 로그인이 완료되지 않습니다.
``tomcat_config.properties``\ 에서 다음과 같이 바꾸고 Fess를 재시작합니다.

::

    tomcat.sameSiteCookies = none

``none``\ 은 HTTPS에서만 사용할 수 있습니다.
HTTP 그대로는 로그인할 수 없게 되므로, 먼저 뒤에서 설명하는 HTTPS 설정을 마칩니다.

[일반]의 "SAML" 섹션에 다음을 입력합니다.

- SP 베이스 URL(``saml.sp.base.url``): ``https://fess.example.com``. 여기서 SP의 Entity ID(``{SP 베이스 URL}/sso/metadata``)와 ACS URL(``{SP 베이스 URL}/sso/``)이 정해집니다
- IdP 엔터티 ID·IdP SSO URL·IdP X.509 인증서: IdP의 관리 화면에서 옮겨 적습니다. 인증서는 ``-----BEGIN CERTIFICATE-----`` 줄을 제외한 Base64를 한 줄로 넣습니다
- 그룹 속성 이름(기본값 ``memberOf``)·역할 속성 이름: IdP가 보내는 속성 이름에 맞춥니다

IdP의 메타데이터 URL을 읽어 들이는 기능은 없습니다.
반대로 Fess의 SP 메타데이터는 ``https://fess.example.com/sso/metadata``\ 에서 가져올 수 있으며, IdP에 읽어 들이게 할 수 있습니다.
사용자 이름은 NameID가 되며, NameID 형식은 기본적으로 이메일 주소 형식입니다.
로그인은 Fess의 ``/sso/``\ 에서 시작하는 SP-Initiated 방식만 지원하며, IdP 포털의 타일에서 시작하는 로그인은 거부됩니다.

운영 환경에서는 ``system.properties``\ 에 ``saml.security.want_assertions_signed=true``\ 를 추가하여 어설션의 서명을 필수로 합니다.
서명이나 암호화 설정은 [일반]에 항목이 없고 JVM 시스템 프로퍼티로도 지정할 수 없으므로, 파일에 직접 적습니다.

.. warning::

   "역할 속성 이름"을 설정하면 IdP가 보낸 값이 그대로 Fess의 역할이 됩니다.
   관리자 역할은 ``authentication.admin.roles=admin``\ 이므로, IdP가 ``admin``\ 을 보낸 사용자는 관리자가 됩니다.

SPNEGO(Windows 통합 인증)
-------------------------

도메인에 가입한 Windows에서 비밀번호를 입력하지 않고 로그인하게 하려면 ``fess-sso-spnego``\ 를 사용합니다.
AD에 SPN 등록(``setspn -S HTTP/<Fess 호스트명> <서비스 계정>``), ``app/WEB-INF/classes/``\ 에 ``krb5.conf``\ 와 ``auth_login.conf`` 작성, 브라우저의 인트라넷 설정이 필요합니다.
그룹은 [일반]의 "LDAP" 섹션 설정으로 AD에서 가져옵니다.
절차는 `Windows 통합 인증을 통한 SSO 설정 <https://fess.codelibs.org/ko/stable/config/sso-spnego.html>`__\ 에 따라 진행하고, [일반]의 SPNEGO 항목을 바꾸면 재시작합니다.

SSO가 동작하는지 확인하기
=========================

먼저 로그아웃한 상태에서 ``https://fess.example.com/sso/``\ 를 열고, IdP의 로그인 화면으로 이동하는지 확인합니다.

로그인했으면 같은 브라우저에서 ``https://fess.example.com/api/v2/auth/me``\ 를 엽니다.

::

    {"response":{"status":0,"authenticated":true,"user":{"user_id":"taro@example.com", ...
      "groups":[...],"permissions":[...],"admin":false,"permission_state":"RESOLVED"}}}

``groups``\ 에 기대하는 그룹이 들어 있는지, ``admin``\ 이 의도한 대로인지 확인합니다.
Entra ID에서는 그룹을 로그인 후에 가져오므로, 직후에는 ``permission_state``\ 가 ``PENDING``\ 이 되고, 가져오기가 끝나면 ``RESOLVED``\ 로 바뀝니다.

감사 로그 ``audit.log``\ 에도 ``LOGIN`` 줄이 사용자 이름과 권한과 함께 기록됩니다.

로그인에 실패하면 로그인 화면으로 돌아가고 "SSO 로그인 프로세스에 실패했습니다."라고 표시됩니다.
원인은 ``fess.log``\ 의 WARN(``Failed to process SSO login`` 등)에 나옵니다.

SSO 설정을 잘못해도 ``/login/``\ 에서 로컬 ``admin`` 사용자로 로그인하여 고칠 수 있습니다.

.. note::

   로그인한 사용자에게는 ``{role}guest``\ 가 부여되지 않습니다.
   기본값인 ``{role}guest``\ 만 가진 크롤링 설정의 문서는 SSO로 로그인한 사용자의 검색 결과에서 사라집니다.
   권한을 구성하는 방법은 :doc:`guide-05`\ 를 참조하십시오.

로그인하지 않은 사용자가 검색하지 못하게 하기
=============================================

[시스템] > [일반]의 "로그인 필요"를 활성화하면, 로그인하지 않은 사용자는 검색할 수 없게 됩니다.

- SSO를 사용할 수 있는 상태(플러그인이 있고 "SSO Type"이 선택되어 있음)라면, 동봉된 ``bootstrap`` 테마의 검색 화면을 연 사용자는 자동으로 ``/sso/``\ 로 보내지고, IdP에서 로그인한 후 원래 검색으로 돌아옵니다
- SSO가 없는 경우에는 검색 화면에 로그인 대화 상자가 표시됩니다
- ``/api/v2/``\ 의 검색 API도 익명으로는 사용할 수 없게 되며, 액세스 토큰을 붙인 호출만 통과합니다

"로그인 필요"를 활성화하지 않은 경우에도, SSO를 사용할 수 있는 상태에서 "로그인 링크 표시"가 활성화되어 있으면 검색 화면의 로그인 링크가 가리키는 곳이 ``/sso/``\ 가 됩니다.

HTTPS로 공개하기
================

리버스 프록시에서 TLS 종단하기
------------------------------

Nginx 등에서 TLS를 종단하고 Fess에는 HTTP로 전달하는 구성에서는, Fess가 받는 요청이 ``http://``\ 로 보입니다.
이대로라면 SAML의 어설션 검증(``Destination`` 대조)이 실패하고, SPNEGO의 Basic 인증 폴백도 제시되지 않습니다.

``tomcat_config.properties``\ 에서 외부에서 보이는 스킴과 포트를 Fess에 알려 줍니다.
이 파일은 ZIP 패키지에서는 ``lib/classes/``, DEB·RPM 패키지와 Docker 이미지에서는 ``/etc/fess/``\ 에 있습니다.

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

프록시 쪽에서는 ``Host`` 헤더를 원래대로 Fess에 전달합니다(Nginx라면 ``proxy_set_header Host $host;``).
Fess는 요청 URL의 호스트 이름을 ``Host`` 헤더로부터 구성하기 때문입니다.

아울러 ``fess_config.properties``\ 의 ``session.cookie.secure=true``\ 로 세션 쿠키에 ``Secure`` 속성을 붙입니다.
기본값(빈 값)에서는 Tomcat의 판단에 맡기지만, 프록시에서 TLS를 종단하는 운영 환경에서는 ``true``\ 를 명시합니다.
SAML에서 ``tomcat.sameSiteCookies = none``\ 을 사용하는 경우에도 ``SameSite=None`` 쿠키에는 ``Secure`` 속성이 필요합니다.

두 파일 모두 변경 후 Fess 재시작이 필요합니다.

Fess에서 직접 TLS 받기
----------------------

프록시를 두지 않는 경우에는 ``tomcat_config.properties``\ 에 ``tomcat.SSLEnabled=true``, ``tomcat.certificateKeystoreFile``, ``tomcat.certificateKeystorePassword``, ``tomcat.certificateKeyAlias`` 등을 설정합니다.
설정 예는 `보안 설정 <https://fess.codelibs.org/ko/stable/install/security.html>`__\ 을 참조하십시오.

OpenSearch 포트 닫기
--------------------

docker-fess의 ``compose-opensearch3.yaml``\ 은 보안 플러그인이 비활성화된 OpenSearch를 호스트의 포트 9200으로 공개합니다.
Fess는 컨테이너 간 네트워크(``http://search01:9200``)로 접속하므로, 공유 서버에서는 ``search01``\ 의 ``ports``\ 를 빼도 됩니다.

액세스 토큰 관리하기
====================

업무 시스템에서 API를 호출하기 위한 토큰은 [시스템] > [액세스 토큰]에서 만듭니다.
API 호출 방법은 :doc:`guide-11`\ 에서 다루므로, 여기서는 안전하게 운영하기 위한 사항만 듭니다.

- 검색용 토큰에는 그 시스템에 보여 줘도 되는 문서의 권한(예: ``{group}sales``)만 붙입니다
- ``{role}admin-api``\ 를 붙인 토큰은 문서 등록뿐 아니라 Admin API의 모든 엔드포인트를 사용할 수 있습니다. "등록만"과 같은 좁은 권한은 없습니다
- "만료"를 설정하고, 기한이 되면 다시 만듭니다. 필요 없어진 토큰은 삭제합니다
- 토큰은 서버 쪽에 두고, 브라우저에서 동작하는 JavaScript에는 넣지 않습니다
- "파라미터 이름"은 비워 둡니다. 설정하면 URL 파라미터로 권한을 추가할 수 있게 됩니다
- 토큰을 발급할 수 있는 ``admin-accesstoken`` 역할과 값을 표시할 수 있는 ``admin-accesstoken-view`` 역할은 관리자와 동등하게 취급합니다

로그 보존 기간 정하기
=====================

로그 파일의 위치와 모니터링은 :doc:`guide-10`\ 에서 다룹니다.
여기서는 보안상 확인에 사용하는 기록과 그 보존 기간을 정리합니다.

감사 로그(``audit.log``)에는 로그인(``LOGIN``), 로그인 실패(``LOGIN_FAILURE``), 로그아웃(``LOGOUT``), 관리 화면과 Admin API에 대한 접근(``ACCESS``), 권한 부족으로 인한 거부(``ACCESS_DENIED``) 등이 한 줄씩 기록됩니다.
파일은 ZIP 패키지에서는 ``logs/``, DEB·RPM 패키지와 Docker 이미지에서는 ``/var/log/fess/``\ 에 출력되며, [시스템 정보] > [로그 파일]에서도 다운로드할 수 있습니다.
기본 형식은 LTSV이며, Docker 이미지에서는 ECS 형식의 JSON입니다.
로테이트된 파일은 360일이 지나면 삭제됩니다(``log4j2.xml``\ 의 ``backup.audit.max.age``).

누가 무엇을 검색했는지는 OpenSearch에 저장되는 검색 로그로, [시스템 정보] > [검색 로그]에서 확인할 수 있습니다.
[일반]의 "이전 검색 로그 삭제"의 기본값은 ``-1``\ 로, 검색 로그를 삭제하지 않고 계속 보관합니다.
이 일수는 클릭 로그, 즐겨찾기 로그, 채팅 로그에도 적용됩니다.
사내 규정으로 보존 기간이 정해져 있다면 그 일수를 입력하십시오.

여러 대로 운영하는 경우
=======================

Fess 15.9의 로그인 세션은 각 Fess 프로세스의 메모리에 있습니다.
SSO 도중에 사용하는 값(OpenID Connect의 ``state``\ 나 SAML의 AuthnRequest ID)도 세션에 들어가므로, 로드 밸런서 뒤에 여러 대를 두는 경우에는 같은 사용자를 같은 Fess로 보내는 스티키 세션을 활성화합니다.
여러 대 구성 자체는 :doc:`guide-14`\ 를 참조하십시오.

참고로, 세션을 OpenSearch에 저장하여 여러 대에서 공유하는 기능과 로컬 사용자의 패스키 로그인은 15.10 이후의 기능입니다.

다음에 읽을 글
==============

- 역할과 그룹의 설계, 크롤링 설정의 권한 작성법: :doc:`guide-05`
- 액세스 토큰을 사용한 API 연동: :doc:`guide-11`
- 로그의 위치, 모니터링, 백업: :doc:`guide-10`
- 여러 대 구성으로 확장: :doc:`guide-14`
- 파일 서버의 ACL을 검색 결과에 반영하기: :doc:`file-server-search`

참고 자료
=========

- `Microsoft Entra ID를 이용한 SSO 설정 <https://fess.codelibs.org/ko/stable/config/sso-entraid.html>`__
- `OpenID Connect를 통한 SSO 설정 <https://fess.codelibs.org/ko/stable/config/sso-oidc.html>`__
- `SAML 인증을 통한 SSO 설정 <https://fess.codelibs.org/ko/stable/config/sso-saml.html>`__
- `Windows 통합 인증을 통한 SSO 설정 <https://fess.codelibs.org/ko/stable/config/sso-spnego.html>`__
- `일반 <https://fess.codelibs.org/ko/stable/admin/general-guide.html>`__
- `액세스 토큰 <https://fess.codelibs.org/ko/stable/admin/accesstoken-guide.html>`__
- `보안 설정 <https://fess.codelibs.org/ko/stable/install/security.html>`__
- `로그 설정 <https://fess.codelibs.org/ko/stable/config/admin-logging.html>`__
