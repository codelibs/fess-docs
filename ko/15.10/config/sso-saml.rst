============================
SAML 인증을 통한 SSO 설정
============================

개요
====

|Fess| 에서는 SAML（Security Assertion Markup Language）2.0을 사용한 싱글 사인온（SSO）인증을 지원합니다.
SAML 인증을 사용하면 IdP（Identity Provider）에서 인증된 사용자 정보를 |Fess| 에 연동하고, 역할 기반 검색과 결합하여 사용자의 권한에 따른 검색 결과 구분이 가능해집니다.

.. note::
   SAML 인증 지원은 ``fess-sso-saml`` 플러그인에서 제공됩니다. 배포물에 포함되어 있지
   않으므로 관리 화면의 「시스템 > 플러그인」 페이지 또는
   ``bin/fess-setup install plugin fess-sso-saml`` 로 설치하십시오.
   이 플러그인은 SAML 라이브러리 `saml4j <https://github.com/codelibs/saml4j>`__ 로 SAML 메시지를 처리합니다.
   설치하기 전에는 ``sso.type=saml`` 설정만으로는 ``/sso/`` 요청이 로그인 페이지로
   리디렉션될 뿐입니다.

SAML 인증의 구조
----------------

SAML 인증에서는 |Fess| 가 SP（Service Provider）로 동작하여 외부 IdP와 연동하여 인증을 수행합니다.

1. 사용자가 |Fess| 의 SSO 엔드포인트（``/sso/``）에 접근
2. |Fess| 가 IdP에 인증 요청을 리다이렉트
3. 사용자가 IdP에서 인증 실행
4. IdP가 SAML 어서션을 |Fess| 에 전송
5. |Fess| 가 어서션을 검증하고 사용자를 로그인

.. note::
   지원되는 것은 위와 같이 |Fess| 측（``/sso/``）에서 시작하는 SP-Initiated 로그인뿐입니다.
   |Fess| 는 전송한 AuthnRequest의 ID와 SAML 응답을 대응시켜 검증하므로,
   IdP 포털（Okta 대시보드나 Microsoft Entra ID의 「내 앱」 등）에 배치한 타일에서 시작하는
   IdP-Initiated（미요청·unsolicited）SSO는 대응시킬 AuthnRequest가 없어 거부됩니다.
   IdP 측에 타일을 배치하는 경우에는 링크 대상을 |Fess| 의 ``/sso/`` 로 지정하십시오.

   참고로 15.7에서는 ``tomcat.sameSiteCookies=none`` 을 설정하면 IdP-Initiated 로그인이 결과적으로
   동작했습니다. |Fess| 가 대응시키지 못한 응답을 IdP로 되돌려 보내고, IdP가 즉시 SP-Initiated
   어서션을 반환했기 때문입니다. 15.8에서는 이 되돌려 보내기를 하지 않으므로 IdP-Initiated 로그인은
   동작하지 않습니다.

역할 기반 검색과의 연동에 대해서는 :doc:`security-role` 을 참조하십시오.

.. note::
   여러 노드를 실행하는 경우에는 노드 간에 HTTP 세션을 공유하는 환경 변수 ``FESS_SESSION_STORE=opensearch`` 를 설정하면, 한 노드에서 시작한 로그인을 다른 노드에서 완료할 수 있습니다. 활성화하기 전에 모든 노드의 플러그인을 15.10으로 업데이트하십시오. 15.9.0 플러그인은 로그인 상태를 공유하지 않으며, 다른 노드로 돌아온 사용자는 로그인하지 않은 상태로 남습니다. 세션을 공유하지 않는 경우에는 로드 밸런서가 세션마다 하나의 노드에 고정되도록 하십시오. 세션을 공유하는 경우에도 스티키 세션을 권장합니다(:doc:`session-store` 참조).

   ``FESS_SESSION_STORE=opensearch`` 를 설정한 경우 SSO 플러그인(``fess-sso-saml``, ``fess-sso-oidc``, ``fess-sso-entraid``)을 추가하거나 제거하면 저장된 세션의 형식 버전이 바뀝니다. 그러면 저장된 모든 세션이 무효가 되어 모든 사용자가 다시 로그인해야 합니다. 이 플러그인은 모든 노드에서 설치하거나 제거하십시오. 이 플러그인의 구성이 다른 노드와 다른 노드는 다른 노드가 저장한 세션을 읽을 수 없고, 다른 노드도 그 노드의 세션을 읽을 수 없습니다. 스토리지, 스크립트, SPNEGO 등 다른 플러그인은 형식을 바꾸지 않습니다.

전제 조건
=========

SAML 인증을 설정하기 전에 다음 전제 조건을 확인하십시오.

- |Fess| 15.10 이상이 설치되어 있을 것
- SAML 2.0 대응 IdP（Identity Provider）를 사용할 수 있을 것
- |Fess| 가 HTTPS로 접근 가능할 것（운영 환경에서는 필수）
- IdP 측에서 |Fess| 를 SP로 등록할 수 있는 권한이 있을 것

지원 IdP의 예:

- Microsoft Entra ID（Azure AD）
- Okta
- Google Workspace
- Keycloak
- OneLogin
- 기타 SAML 2.0 대응 IdP

기본 설정
=========

SSO 기능 활성화
---------------

SAML 인증을 활성화하려면 ``app/WEB-INF/conf/system.properties`` 에 다음 설정을 추가합니다.

::

    sso.type=saml

.. note::
   ``sso.type`` 및 기본적인 SAML 설정（IdP 정보, SP 정보, 사용자 속성 매핑）은 관리 화면의 「시스템 > 전체」 페이지에서도 설정·변경할 수 있습니다.
   관리 화면에서 변경한 설정은 ``system.properties`` 에 저장되며, 재시작 후에도 유지됩니다.
   단, 서명·암호화 등의 보안 설정이나 SP 인증서·비밀 키는 관리 화면에서 설정할 수 없으므로 ``system.properties`` 에 직접 기술하십시오.

.. note::
   ``saml.`` 로 시작하는 설정은 ``system.properties`` 에서만 읽어 들입니다.
   JVM 시스템 프로퍼티（``-Dsaml.security....`` 나 ``-Dfess.saml.security....``）로 지정해도 참조되지 않습니다.
   특히 ``saml.security.*`` 는 관리 화면에도 항목이 없으므로
   ``system.properties`` 에 직접 기술하는 것 외에는 설정할 방법이 없습니다.

세션 쿠키 설정
--------------

IdP는 어설션을 |Fess| 로 **크로스 사이트 POST** 로 반환합니다. ``SameSite=Lax`` 쿠키는 이러한 요청에 전송되지 않으므로, |Fess| 에 포함된 기본값 그대로는 SAML 로그인이 완료되지 않습니다.

``tomcat_config.properties`` 의 ``tomcat.sameSiteCookies`` 를 ``none`` 으로 변경하십시오. 이 파일은 ZIP 패키지에서는 ``lib/classes/`` , DEB/RPM 패키지에서는 ``/etc/fess/`` 에 있습니다.

::

    tomcat.sameSiteCookies = none

.. warning::
   브라우저는 ``Secure`` 속성이 함께 있는 쿠키에 대해서만 ``none`` 을 허용하므로 |Fess| 를 HTTPS로 제공해야 합니다. 일반 HTTP에서는 이 설정으로 인해 |Fess| 에 로그인할 수 없게 됩니다.

.. note::
   기본값 ``lax`` 는 콜백이 리디렉션(GET)으로 돌아오는 SSO 방식을 위한 것입니다. SAML의 HTTP-POST 바인딩은 여기에 해당하지 않으므로 SAML을 사용할 때만 변경이 필요합니다. 설정 변경 후에는 |Fess| 를 재시작해야 합니다.

SP（Service Provider）설정
--------------------------

|Fess| 를 SP로 설정하려면 SP Base URL을 지정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.sp.base.url``
     - SP의 베이스 URL
     - ``http://localhost:8080``

.. note::
   ``saml.sp.base.url`` 의 기본값은 ``http://localhost:8080`` 입니다.
   검증 환경 이외에서는 반드시 |Fess| 에 외부에서 접근할 때의 URL（운영 환경에서는 HTTPS）을 설정하십시오.

이 설정에 의해 다음 엔드포인트가 자동으로 구성됩니다.

- **Entity ID**: ``{saml.sp.base.url}/sso/metadata``
- **ACS URL**: ``{saml.sp.base.url}/sso/``
- **SLO URL**: ``{saml.sp.base.url}/sso/logout``

설정 예::

    saml.sp.base.url=https://fess.example.com

개별 URL 설정
~~~~~~~~~~~~~

일반적으로 ``saml.sp.base.url`` 을 설정하면 각 엔드포인트 URL이 자동으로 구성되지만,
필요에 따라 다음 프로퍼티로 개별 URL을 명시적으로 지정하여 덮어쓸 수도 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.sp.entityid``
     - SP의 Entity ID
     - ``{saml.sp.base.url}/sso/metadata``
   * - ``saml.sp.assertion_consumer_service.url``
     - Assertion Consumer Service URL
     - ``{saml.sp.base.url}/sso/``
   * - ``saml.sp.single_logout_service.url``
     - Single Logout Service URL
     - ``{saml.sp.base.url}/sso/logout``

IdP（Identity Provider）설정
----------------------------

IdP에서 취득한 정보를 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.idp.entityid``
     - IdP의 Entity ID
     - （필수）
   * - ``saml.idp.single_sign_on_service.url``
     - IdP의 SSO 서비스 URL
     - （필수）
   * - ``saml.idp.x509cert``
     - IdP의 서명용 X.509 인증서（Base64 인코딩, 줄 바꿈 없음）
     - （필수）
   * - ``saml.idp.single_logout_service.url``
     - IdP의 SLO 서비스 URL
     - （선택 사항）
   * - ``saml.idp.x509certMulti.1``, ``.2``, ...
     - 추가 IdP 서명용 인증서（예: 키 롤오버 중）
     - （선택 사항）

.. note::
   IdP 인증서는 서명에 대한 유일한 신뢰 기점이며, 메시지에 포함된 인증서는 결코 신뢰하지 않습니다.
   IdP 및 SP 인증서는 2048비트 이상의 RSA 키여야 합니다.
   ``saml.idp.x509certMulti.N`` 을 설정한 경우에는 ``saml.idp.x509cert`` 를 생략할 수 있습니다.

.. note::
   ``saml.idp.x509cert`` 에는 인증서의 Base64 인코딩된 내용을 줄 바꿈 없이 1행으로 지정합니다.
   ``-----BEGIN CERTIFICATE-----`` 와 ``-----END CERTIFICATE-----`` 행은 포함하지 마십시오.

SP 메타데이터 취득
------------------

|Fess| 를 시작하면 ``/sso/metadata`` 엔드포인트에서 SP 메타데이터를 XML 형식으로 취득할 수 있습니다.

::

    https://fess.example.com/sso/metadata

이 메타데이터를 IdP에 임포트하거나, 메타데이터의 내용을 참고하여 IdP 측에서 SP를 수동으로 등록하십시오.

.. note::
   메타데이터를 취득하려면 먼저 기본적인 SAML 설정（``sso.type=saml`` 과 ``saml.sp.base.url``）을 완료하고 |Fess| 를 시작해 두어야 합니다.

IdP 측 설정
===========

IdP 측에서 |Fess| 를 SP로 등록할 때 다음 정보를 설정합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 설정 항목
     - 설정값
   * - ACS URL / Reply URL
     - ``https://<Fess의 호스트>/sso/``
   * - Entity ID / Audience URI
     - ``https://<Fess의 호스트>/sso/metadata``
   * - Name ID Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` （권장）

IdP에서 취득하는 정보
---------------------

IdP의 설정 화면 또는 메타데이터에서 다음 정보를 취득하여 |Fess| 의 설정에 사용합니다.

- **IdP Entity ID**: IdP를 식별하기 위한 URI
- **SSO URL（HTTP-Redirect）**: 싱글 사인온의 엔드포인트 URL
- **X.509 인증서**: SAML 어서션의 서명 검증에 사용하는 공개 키 인증서

.. note::
   |Fess| 는 모든 어서션에 대해 다음을 검사합니다. URL은 수신한 요청이 아니라 ``saml.sp.base.url`` （또는 개별 URL 프로퍼티）에서 도출됩니다.

   - 어서션에 SP의 Entity ID를 지정하는 ``AudienceRestriction`` 이 있을 것
   - 서명된 Response의 ``Destination`` 과 SubjectConfirmation의 ``Recipient`` 가 Assertion Consumer Service URL일 것

사용자 속성 매핑
================

SAML 어서션에서 취득한 사용자 속성을 |Fess| 의 그룹이나 역할에 매핑할 수 있습니다.

그룹 속성 설정
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.attribute.group.name``
     - 그룹 정보를 포함하는 속성명
     - ``memberOf``
   * - ``saml.default.groups``
     - 기본 그룹（쉼표로 구분）
     - （없음）

설정 예::

    saml.attribute.group.name=groups
    saml.default.groups=user

.. note::
   |Fess| 는 어서션의 그룹 값을 그대로 사용하며, 디렉토리 조회나 중첩 그룹(상위 그룹)의 확장은
   수행하지 않습니다. 상위 그룹이 포함되는지 여부는 IdP 측의 클레임 설정에 따라서만 결정됩니다.
   Microsoft Graph API로 상위 그룹을 해결하는 :doc:`sso-entraid` 의 동작과는 다릅니다.

역할 속성 설정
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.attribute.role.name``
     - 역할 정보를 포함하는 속성명
     - （없음）
   * - ``saml.default.roles``
     - 기본 역할（쉼표로 구분）
     - （없음）

설정 예::

    saml.attribute.role.name=roles
    saml.default.roles=viewer

.. note::
   IdP에서 속성을 취득할 수 없는 경우 기본값이 사용됩니다.
   역할 기반 검색을 사용하는 경우 적절한 그룹 또는 역할을 설정하십시오.

.. warning::
   ``saml.attribute.role.name`` 을 설정하면 IdP가 보낸 속성 값이 그대로 |Fess| 의 역할이 됩니다.
   ``fess_config.properties`` 의 ``authentication.admin.roles`` 기본값은 ``admin`` 이므로,
   IdP가 역할 속성에 ``admin`` 을 포함해 보낸 사용자는 |Fess| 의 관리자 권한을 갖게 됩니다.
   IdP 측에서 역할 속성 값을 제어할 수 있는 범위를 확인하고, 필요하다면
   ``authentication.admin.roles`` 를 다른 이름으로 변경하십시오.

속성 이름이 중복되는 IdP
------------------------

IdP가 동일한 속성 이름을 여러 ``<Attribute>`` 요소로 나누어 보내면 |Fess| 는 그 값들을
병합합니다.

Keycloak은 기본적으로 이러한 형태의 어서션을 보냅니다. 역할 매퍼와 그룹 매퍼는 ``single``
옵션을 활성화하지 않는 한 값마다 별도의 ``<Attribute>`` 요소를 출력하며, Keycloak 계정은
기본적으로 여러 개의 렐름 역할을 가지기 때문입니다. 이를 위해 |Fess| 에서 설정할 것은 없습니다.

보안 설정
=========

다음 보안 설정은 ``system.properties`` 에서 읽어 들입니다.

.. note::
   기본값을 약화시키는 설정（싱글 로그아웃을 설정한 상태에서의 ``saml.security.want_logout_signed=false``,
   ``saml.security.allow_deprecated_alg=true`` 또는 ``saml.security.allow_rsa_1_5=true``）이 남아 있으면
   SAML 설정을 읽어 들일 때 ``Insecure SAML settings: ...`` 경고가 로그에 출력됩니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.session.end_with_idp``
     - IdP의 세션이 끝나면 |Fess| 의 로그인도 종료한다. Assertion의 ``SessionNotOnOrAfter`` 에 ``saml.security.clock_drift`` 를 더한 시각에 종료됩니다. ``false`` 로 비활성화한다
     - ``true``

.. note::
   IdP가 ``SessionNotOnOrAfter`` 를 보내지 않는 경우 이 설정은 동작하지 않습니다. IdP가 세션의 상한을 짧게 두는 경우（Keycloak의 기본값은 10시간）, 이전보다 일찍 로그아웃될 수 있습니다. IdP에서 로그아웃해도 |Fess| 의 로그인은 이 시각까지 유지됩니다.

서명 설정
---------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.security.authnrequest_signed``
     - 인증 요청에 서명한다（``saml.sp.privatekey`` 필요）
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Response의 서명을 요구한다
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Assertion의 서명을 요구한다
     - ``false``
   * - ``saml.security.want_logout_signed``
     - IdP가 보내는 로그아웃 메시지의 서명을 요구한다
     - ``true``
   * - ``saml.security.allow_deprecated_alg``
     - SHA-1 서명을 허용한다
     - ``false``
   * - ``saml.security.signature_algorithm``
     - 송신하는 서명의 알고리즘: ``rsa-sha256``, ``rsa-sha384`` 또는 ``rsa-sha512`` 의 URI
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``

.. note::
   이 설정들과 관계없이 Response 또는 Assertion 중 하나는 반드시 서명되어 있어야 합니다.
   IdP가 서명하는 요소에 대해 서명을 요구하려면 ``saml.security.want_messages_signed`` 또는 ``saml.security.want_assertions_signed`` 를 사용하십시오.
   서명은 서명 대상 요소를 해당 요소 자신의 ID로 참조해야 하며, ``rsa-sha256``, ``rsa-sha384`` 또는 ``rsa-sha512`` （또는 ECDSA 변형）를 사용해야 합니다.
   ``saml.security.allow_deprecated_alg=true`` 가 아니면 SHA-1 서명은 거부되므로, IdP가 SHA-256 이상으로 서명하는지 확인하십시오.

.. note::
   싱글 로그아웃（``saml.idp.single_logout_service.url``）을 설정한 경우, IdP가 보내는 LogoutRequest와
   LogoutResponse는 ``saml.idp.x509cert`` 의 키로 서명되어 있어야 합니다
   （``saml.security.want_logout_signed=true`` 가 기본값입니다）.
   서명할 수 없는 IdP에 대해서만 ``saml.security.want_logout_signed=false`` 를 설정하십시오.
   싱글 로그아웃 서비스（``/sso/logout``）는 리디렉션 바인딩（GET）과 POST 바인딩을 받아들입니다.
   IdP 측에도 ``/sso/logout`` URL을 POST 바인딩용으로 등록하십시오. IdP가 Assertion Consumer Service로
   POST하는 LogoutResponse는 인식되지 않습니다.

암호화 설정
-----------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.security.want_assertions_encrypted``
     - 어서션의 암호화를 요구한다（``saml.sp.privatekey`` 필요）
     - ``false``
   * - ``saml.security.allow_rsa_1_5``
     - RSA 1.5 키 전송을 허용한다（``saml.sp.privatekey`` 필요）. 설정하지 않으면 OAEP만 허용됩니다
     - ``false``

.. note::
   IdP가 RSA 1.5로만 암호화할 수 있는 경우가 아니면 ``saml.security.allow_rsa_1_5`` 를 ``false`` 로 두십시오.

SP 인증서 및 비밀 키 설정
--------------------------

SP 측에서 인증 요청이나 로그아웃 메시지에 서명하는 경우（``saml.security.authnrequest_signed`` 등）,
또는 어서션이나 NameID의 암호화를 요구하는 경우（``saml.security.want_assertions_encrypted`` 등）는,
SP의 비밀 키（PKCS#8）와 X.509 인증서를 설정해야 합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.sp.x509cert``
     - SP의 X.509 인증서（Base64 인코딩, 줄 바꿈 없음）
     - （빈 문자열）
   * - ``saml.sp.privatekey``
     - SP의 비밀 키（Base64 인코딩, 줄 바꿈 없음）
     - （빈 문자열）

.. note::
   ``saml.sp.x509cert`` 와 ``saml.sp.privatekey`` 에는 ``saml.idp.x509cert`` 와 마찬가지로,
   Base64 인코딩된 내용을 줄 바꿈 없이 1행으로 지정합니다（``-----BEGIN ...-----`` 와 ``-----END ...-----`` 행은 포함하지 않습니다）.
   서명·암호화를 활성화하는 경우 SP 인증서를 IdP 측에도 등록하십시오. SP 인증서는 ``/sso/metadata`` 의 SP 메타데이터에 포함되어 공개됩니다.

기타 보안 설정
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.security.requested_authncontext``
     - 요구하는 인증 컨텍스트（빈 값이면 요구하지 않음）
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.security.requested_authncontextcomparison``
     - 요구하는 인증 컨텍스트의 비교 방식（``exact``, ``minimum``, ``maximum`` 또는 ``better``）
     - ``exact``
   * - ``saml.security.clock_drift``
     - 유효 기간을 확인할 때 허용하는 시계 오차（초, 0~600）
     - ``120``
   * - ``saml.security.max_message_size``
     - 허용하는 디코딩 후 메시지의 최대 크기（바이트, 1024~16777216）
     - ``1048576``
   * - ``saml.sp.nameidformat``
     - NameID 형식
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   어서션의 Audience, Recipient, Destination, Issuer 및 유효 기간은 항상 검사되며,
   응답은 |Fess| 가 시작한 로그인에 대한 것이어야 합니다.
   Audience가 없거나 Audience에 SP의 Entity ID가 지정되어 있지 않은 어서션은 거부됩니다.
   검증은 항상 엄격합니다: ``saml.strict=false`` 는 거부됩니다.

더 이상 사용되지 않는 프로퍼티
------------------------------

다음 프로퍼티는 무시됩니다. 해당 프로퍼티를 명시하는 경고가 로그에 한 번 출력됩니다.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 프로퍼티
     - 현재 동작
   * - ``saml.security.reject_deprecated_alg``
     - SHA-1 서명은 기본적으로 거부됩니다. ``saml.security.allow_deprecated_alg=true`` 로 허용합니다
   * - ``saml.security.allowed_key_transport_algorithms``
     - 기본적으로 OAEP만 허용됩니다. ``saml.security.allow_rsa_1_5=true`` 로 RSA 1.5도 허용합니다
   * - ``saml.security.allow_duplicated_attribute_name``
     - 중복된 속성은 항상 병합됩니다
   * - ``saml.security.reject_missing_audience``
     - Audience가 없는 어서션은 항상 거부됩니다
   * - ``saml.idp.certfingerprint``, ``saml.idp.certfingerprint_algorithm``
     - ``saml.idp.x509cert`` 를 설정하십시오. 핑거프린트는 신뢰 기점이 아닙니다
   * - ``saml.security.sign_metadata``, ``saml.security.want_nameid_encrypted``, ``saml.security.want_xml_validation``, ``saml.security.logoutrequest_signed``, ``saml.security.logoutresponse_signed``, ``saml.security.digest_algorithm``, ``saml.keystore.*``, ``saml.contacts.*``, ``saml.organization.*``, ``saml.compress.*``, ``saml.parsing.*``, ``saml.unique_id_prefix``, the ``*.binding`` and ``*.response.url`` properties
     - 더 이상 사용되지 않습니다

라이브러리가 알지 못하는 그 밖의 ``saml.`` 프로퍼티가 있으면 해당 프로퍼티명을 명시하는 메시지와 함께
SAML 로그인이 중단되므로, 잘못 입력한 보안 설정을 놓치는 일이 없습니다. ``saml.debug`` 는 허용되지만 아무 효과가 없습니다.

AuthnRequest 유효 기간
======================

|Fess| 는 ``/sso/`` 에 접근할 때마다 AuthnRequest를 1건 IdP로 전송하고, 그 ID를 세션에 기록합니다.
IdP에서 반환된 SAML 응답은 기록된 ID와 대응시켜 검증됩니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.request.id.ttl``
     - 응답이 없는 AuthnRequest의 ID를 보관하는 기간（초）
     - ``3600``

기록된 ID는 이 기간이 지나면 폐기됩니다.
IdP 로그인 화면을 열어둔 채로 방치하는 등의 이유로 유효 기간이 지나면 반환된 어서션을 대응시킬 수 없어 그 자리에서 한 번만 로그인에 실패합니다.

설정 예
=======

최소 구성（검증 환경용）
------------------------

다음은 검증 환경에서 동작을 확인하기 위한 최소한의 설정 예입니다.

::

    # SSO 활성화
    sso.type=saml

    # SP 설정
    saml.sp.base.url=https://fess.example.com

    # IdP 설정（IdP의 관리 화면에서 취득한 값을 설정）
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...（Base64 인코딩된 인증서）

    # 기본 그룹
    saml.default.groups=user

권장 구성（운영 환경용）
------------------------

다음은 운영 환경에서 사용하기 위한 권장 설정 예입니다.

::

    # SSO 활성화
    sso.type=saml

    # SP 설정
    saml.sp.base.url=https://fess.example.com

    # IdP 설정
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.single_logout_service.url=https://idp.example.com/saml/logout
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...（Base64 인코딩된 인증서）

    # 사용자 속성 매핑
    saml.attribute.group.name=groups
    saml.attribute.role.name=roles
    saml.default.groups=user

    # 보안 설정（운영 환경에서는 활성화 권장）
    # IdP가 서명하는 요소에 대해 서명을 요구한다
    # （Response의 경우 saml.security.want_messages_signed=true）
    saml.security.want_assertions_signed=true

문제 해결
=========

자주 발생하는 문제와 해결 방법
------------------------------

인증 후 |Fess| 로 돌아올 수 없음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP 측의 ACS URL이 올바르게 설정되어 있는지 확인하십시오
- ``saml.sp.base.url`` 의 값이 IdP 측의 설정과 일치하는지 확인하십시오
- SAML 어설션은 IdP에서 교차 사이트 POST로 전송됩니다. ``tomcat_config.properties`` 의
  ``tomcat.sameSiteCookies`` 가 ``lax`` (기본값)인 경우 브라우저가 세션 쿠키를 함께 보내지 않으므로
  그 자리에서 한 번만 로그인에 실패합니다. 이 경우
  ``tomcat.sameSiteCookies = none`` 을 설정하십시오 (``SameSite=None`` 은 HTTPS가 필요합니다)
- IdP에서 로그인에 시간이 오래 걸리면 어설션이 돌아온 시점에 AuthnRequest의 ID가 남아 있지 않으므로
  그 자리에서 한 번만 로그인에 실패합니다. 이 경우에는 로그인을 다시 시작하십시오
- |Fess| 는 ``app/WEB-INF/web.xml`` 에 ``session-timeout`` 을 지정하지 않으므로 서블릿 컨테이너의
  기본값인 30분이 적용됩니다. 이는 ``saml.request.id.ttl`` 의 3600초보다 짧아 세션이 먼저 폐기됩니다.
  따라서 ``saml.request.id.ttl`` 만 늘려도 사용자가 IdP에서 로그인을 마칠 수 있는 시간은 늘어나지
  않으므로, 세션 타임아웃도 함께 늘리십시오

Destination 또는 Recipient 검증에 실패함
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

서명된 Response의 ``Destination`` 과 SubjectConfirmation의 ``Recipient`` 는 |Fess| 의
Assertion Consumer Service URL이어야 합니다. 이 URL은 |Fess| 에 도달한 요청이 아니라
``saml.sp.base.url`` （또는 ``saml.sp.assertion_consumer_service.url``）에서 도출되므로,
TLS를 종단하는 리버스 프록시는 이 비교에 영향을 주지 않습니다.

- ``saml.sp.base.url`` 을 스킴과 포트를 포함한 외부에서 보이는 URL로 설정하십시오
- IdP 측에도 같은 ACS URL（``{saml.sp.base.url}/sso/``）을 등록하십시오
- ``saml.sp.entityid`` 를 덮어쓴 경우 IdP는 그 값을 Audience로 사용해야 합니다

서명 검증 오류
~~~~~~~~~~~~~~

- IdP의 인증서가 올바르게 설정되어 있는지 확인하십시오
- 인증서의 유효 기간이 만료되지 않았는지 확인하십시오
- 인증서는 Base64 인코딩된 내용만 줄 바꿈 없이 설정하십시오
- IdP 인증서는 2048비트 이상의 RSA 키여야 합니다
- Response 또는 Assertion 중 하나는 서명되어 있어야 하며, 서명은 SHA-256 이상을 사용해야 합니다
  （SHA-1은 ``saml.security.allow_deprecated_alg=true`` 인 경우에만 허용됩니다）
- 응답이 거부된 이유는 ``Authentication failed: <reason> - <detail>`` 형식으로 로그에 출력됩니다

사용자의 그룹·역할이 반영되지 않음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP 측에서 속성（Attribute）이 올바르게 설정되어 있는지 확인하십시오
- ``saml.attribute.group.name`` 의 값이 IdP에서 전송되는 속성명과 일치하는지 확인하십시오
- Microsoft Entra ID에서는 소스 속성을 변경하지 않는 한 그룹 클레임의 값이 그룹의 ``ObjectId`` (GUID)이므로
  그룹 이름과 일치하지 않습니다
- 사용자가 150개를 초과하는 그룹에 소속된 경우 Microsoft Entra ID는 그룹 클레임 자체를 보내지 않으며
  (중첩 그룹도 이 상한에 포함됩니다), 이때 |Fess| 는 ``saml.default.groups`` 로 폴백합니다
- 속성명을 IdP가 실제로 보내는 어서션의 속성명과 비교하십시오

로그 설정
---------

SAML 인증에 실패하면 그 이유는 항상 경고로 로그에 출력됩니다.
``saml.debug`` 프로퍼티는 아무 효과가 없습니다.

SAML 관련 상세 로그를 출력하려면 ``app/WEB-INF/classes/log4j2.xml`` 에 다음 로거를 추가하십시오.

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

참고 정보
=========

- :doc:`security-role` - 역할 기반 검색 설정에 대하여
- :doc:`sso-oidc` - OpenID Connect에 의한 SSO 설정에 대하여
- :doc:`sso-entraid` - Microsoft Entra ID 전용 SSO 설정에 대하여
