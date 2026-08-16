============================
SAML 인증을 통한 SSO 설정
============================

개요
====

|Fess| 에서는 SAML（Security Assertion Markup Language）2.0을 사용한 싱글 사인온（SSO）인증을 지원합니다.
SAML 인증을 사용하면 IdP（Identity Provider）에서 인증된 사용자 정보를 |Fess| 에 연동하고, 역할 기반 검색과 결합하여 사용자의 권한에 따른 검색 결과 구분이 가능해집니다.

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

전제 조건
=========

SAML 인증을 설정하기 전에 다음 전제 조건을 확인하십시오.

- |Fess| 15.8 이상이 설치되어 있을 것
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
   특히 ``saml.security.*`` , ``saml.strict`` , ``saml.debug`` 는 관리 화면에도 항목이 없으므로
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

IdP가 동일한 속성 이름을 여러 ``<Attribute>`` 요소로 나누어 보내면 |Fess| 는 해당 어서션을
거부하며 로그인 자체가 실패합니다.

Keycloak은 기본적으로 이러한 형태의 어서션을 보냅니다. 역할 매퍼와 그룹 매퍼는 ``single``
옵션을 활성화하지 않는 한 값마다 별도의 ``<Attribute>`` 요소를 출력하며, Keycloak 계정은
기본적으로 여러 개의 렐름 역할을 가지기 때문입니다.

대처 방법은 다음 중 하나입니다.

- IdP 측에서 속성을 하나의 요소로 합칩니다(Keycloak에서는 매퍼의 ``single`` 옵션을 활성화합니다)
- |Fess| 측에서 중복을 허용하고 값을 병합합니다

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.security.allow_duplicated_attribute_name``
     - 동일한 속성 이름이 여러 요소에 나타나는 것을 허용하고 값을 병합합니다
     - ``false``

설정 예::

    saml.security.allow_duplicated_attribute_name=true

보안 설정
=========

운영 환경에서는 다음 보안 설정을 활성화하는 것을 권장합니다.

.. note::
   권장되지 않는 설정이 남아 있으면 SAML 설정을 읽어 들일 때 ``Insecure SAML settings: ...``
   경고가 로그에 출력됩니다.

서명 설정
---------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.security.authnrequest_signed``
     - 인증 요청에 서명한다
     - ``false``
   * - ``saml.security.want_messages_signed``
     - 메시지의 서명을 요구한다
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - 어서션의 서명을 요구한다
     - ``false``
   * - ``saml.security.logoutrequest_signed``
     - 로그아웃 요청에 서명한다
     - ``false``
   * - ``saml.security.logoutresponse_signed``
     - 로그아웃 응답에 서명한다
     - ``false``
   * - ``saml.security.reject_deprecated_alg``
     - SHA-1 등 사용이 권장되지 않는 서명 알고리즘을 거부한다
     - ``false``

.. warning::
   기본값에서는 보안 기능이 비활성화되어 있습니다.
   운영 환경에서는 최소한 ``saml.security.want_assertions_signed=true`` 를 설정하도록 강력히 권장합니다.

.. note::
   ``saml.security.reject_deprecated_alg`` 가 ``false`` 인 동안에는 SHA-1（``rsa-sha1`` 및 ``dsa-sha1``）로
   서명된 어서션이나 메시지도 허용됩니다. 기본적으로 활성화되어 있지 않은 이유는, 활성화하면 아직 SHA-1로
   서명하는 IdP를 거부하게 되기 때문입니다.
   IdP가 SHA-256 이상으로 서명하는지 확인한 후 ``saml.security.reject_deprecated_alg=true`` 를 설정하십시오.

.. warning::
   싱글 로그아웃（``saml.idp.single_logout_service.url``）을 설정하는 경우에는
   ``saml.security.want_messages_signed=true`` 도 반드시 함께 설정하십시오.
   ``false`` 인 상태에서는 서명이 없는 LogoutRequest가 수락되므로, 조작된 URL로 인증된 사용자의
   세션을 종료시킬 수 있습니다.
   영향은 강제 로그아웃（서비스 거부）이며, 계정 탈취는 아닙니다.

암호화 설정
-----------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.security.want_assertions_encrypted``
     - 어서션의 암호화를 요구한다
     - ``false``
   * - ``saml.security.want_nameid_encrypted``
     - NameID의 암호화를 요구한다
     - ``false``

SP 인증서 및 비밀 키 설정
--------------------------

SP 측에서 인증 요청이나 로그아웃 메시지에 서명하는 경우（``saml.security.authnrequest_signed`` 등）,
또는 어서션이나 NameID의 암호화를 요구하는 경우（``saml.security.want_assertions_encrypted`` 등）는,
SP의 비밀 키와 X.509 인증서를 설정해야 합니다.

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
   * - ``saml.strict``
     - 엄격 모드（검증을 엄격하게 수행）
     - ``true``
   * - ``saml.security.want_xml_validation``
     - 메시지의 XML 스키마 검증을 수행한다
     - ``true``
   * - ``saml.security.signature_algorithm``
     - 서명 알고리즘
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``
   * - ``saml.security.requested_authncontext``
     - 요구하는 인증 컨텍스트
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.sp.nameidformat``
     - NameID 형식
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   |Fess| 는 내부적으로 SAML 라이브러리（java-saml）를 사용하며, ``saml.`` 로 시작하는 프로퍼티는
   라이브러리의 대응하는 설정（``onelogin.saml2.`` 프리픽스）에 매핑됩니다.
   이 때문에 여기서 소개한 것 외에도, 바인딩（``saml.sp.assertion_consumer_service.binding`` 등）,
   조직 정보（``saml.organization.*``）, 연락처 정보（``saml.contacts.*``）와 같은 상세 설정을
   ``system.properties`` 에 지정할 수 있습니다.

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
    saml.security.want_assertions_signed=true
    saml.security.want_messages_signed=true

    # IdP가 SHA-256 이상으로 서명하는지 확인한 후 활성화한다
    saml.security.reject_deprecated_alg=true

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

리버스 프록시 환경에서 Destination 검증에 실패함
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TLS를 종단하는 리버스 프록시나 로드 밸런서 뒤에 |Fess| 를 배치하면,
``saml.sp.base.url`` 을 올바르게 설정했더라도 어설션 검증에 실패할 수 있습니다.

어설션의 ``Destination`` 속성은 |Fess| 에 도달한 시점의 요청 URL과 비교됩니다.
TLS를 종단하는 프록시 뒤에서는 이 값이 IdP가 어설션을 보낸 외부 URL이 아니라 내부 ``http://`` URL입니다.
``saml.sp.base.url`` 은 이 비교에 사용되지 않으므로 이 설정만으로는 해결되지 않습니다.

``saml.debug=true`` 를 설정하면 로그에 다음과 같은 이유가 출력됩니다.

::

    The response was received at http://... instead of https://fess.example.com/sso/

이 경우 ``tomcat_config.properties`` 의 커넥터 설정을 외부에서 보이는 스킴과 포트에 맞추십시오.
다음 설정은 기본적으로 주석 처리되어 있습니다.

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

아울러 리버스 프록시가 원래의 ``Host`` 헤더를 그대로 |Fess| 로 전달하도록 설정하십시오.
요청 URL의 호스트명 부분은 ``Host`` 헤더로부터 조립됩니다.
``tomcat_config.properties`` 를 변경한 후에는 |Fess| 의 재시작이 필요합니다.

같은 검증이 싱글 로그아웃 메시지에도 적용되므로, SLO를 사용하는 경우에도 동일하게 설정하십시오.

서명 검증 오류
~~~~~~~~~~~~~~

- IdP의 인증서가 올바르게 설정되어 있는지 확인하십시오
- 인증서의 유효 기간이 만료되지 않았는지 확인하십시오
- 인증서는 Base64 인코딩된 내용만 줄 바꿈 없이 설정하십시오

속성 이름 중복으로 로그인할 수 없음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 로그에 ``The IdP repeated an attribute name in the SAML assertion`` 으로 시작하는 경고가
  출력된다면, IdP가 동일한 속성 이름을 여러 ``<Attribute>`` 요소로 나누어 보내고 있습니다
- 어서션 검증 자체는 성공했으므로 인증서나 시각 오차는 원인이 아닙니다
- IdP 측에서 속성을 하나로 합치거나 ``saml.security.allow_duplicated_attribute_name=true`` 를
  설정하세요

사용자의 그룹·역할이 반영되지 않음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP 측에서 속성（Attribute）이 올바르게 설정되어 있는지 확인하십시오
- ``saml.attribute.group.name`` 의 값이 IdP에서 전송되는 속성명과 일치하는지 확인하십시오
- Microsoft Entra ID에서는 소스 속성을 변경하지 않는 한 그룹 클레임의 값이 그룹의 ``ObjectId`` (GUID)이므로
  그룹 이름과 일치하지 않습니다
- 사용자가 150개를 초과하는 그룹에 소속된 경우 Microsoft Entra ID는 그룹 클레임 자체를 보내지 않으며
  (중첩 그룹도 이 상한에 포함됩니다), 이때 |Fess| 는 ``saml.default.groups`` 로 폴백합니다
- SAML 어서션의 내용을 확인하려면 디버그 모드를 활성화하십시오

디버그 설정
-----------

문제를 조사할 때는 다음 설정으로 디버그 모드를 활성화할 수 있습니다.

::

    saml.debug=true

``saml.debug=true`` 를 설정하면 SAML 인증에 실패했을 때의 상세한 이유가 로그에 출력됩니다.

또한 ``app/WEB-INF/classes/log4j2.xml`` 에 다음 로거를 추가하면 SAML 관련 상세 로그를 출력할 수 있습니다.

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

참고 정보
=========

- :doc:`security-role` - 역할 기반 검색 설정에 대하여
- :doc:`sso-oidc` - OpenID Connect에 의한 SSO 설정에 대하여
- :doc:`sso-entraid` - Microsoft Entra ID 전용 SSO 설정에 대하여
