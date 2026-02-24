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

역할 기반 검색과의 연동에 대해서는 :doc:`security-role` 을 참조하십시오.

전제 조건
=========

SAML 인증을 설정하기 전에 다음 전제 조건을 확인하십시오.

- |Fess| 15.5 이상이 설치되어 있을 것
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
     - （필수）

이 설정에 의해 다음 엔드포인트가 자동으로 구성됩니다.

- **Entity ID**: ``{base_url}/sso/metadata``
- **ACS URL**: ``{base_url}/sso/``
- **SLO URL**: ``{base_url}/sso/logout``

설정 예::

    saml.sp.base.url=https://fess.example.com

개별 URL 설정
~~~~~~~~~~~~~

Base URL을 사용하지 않고 개별로 URL을 지정할 수도 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.sp.entityid``
     - SP의 Entity ID
     - （개별 설정 시 필수）
   * - ``saml.sp.assertion_consumer_service.url``
     - Assertion Consumer Service URL
     - （개별 설정 시 필수）
   * - ``saml.sp.single_logout_service.url``
     - Single Logout Service URL
     - （선택 사항）

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

보안 설정
=========

운영 환경에서는 다음 보안 설정을 활성화하는 것을 권장합니다.

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

.. warning::
   기본값에서는 보안 기능이 비활성화되어 있습니다.
   운영 환경에서는 최소한 ``saml.security.want_assertions_signed=true`` 를 설정하도록 강력히 권장합니다.

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

기타 보안 설정
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 프로퍼티
     - 설명
     - 기본값
   * - ``saml.security.strict``
     - 엄격 모드（검증을 엄격하게 수행）
     - ``true``
   * - ``saml.security.signature_algorithm``
     - 서명 알고리즘
     - ``http://www.w3.org/2000/09/xmldsig#rsa-sha1``
   * - ``saml.sp.nameidformat``
     - NameID 형식
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

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

문제 해결
=========

자주 발생하는 문제와 해결 방법
------------------------------

인증 후 |Fess| 로 돌아올 수 없음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP 측의 ACS URL이 올바르게 설정되어 있는지 확인하십시오
- ``saml.sp.base.url`` 의 값이 IdP 측의 설정과 일치하는지 확인하십시오

서명 검증 오류
~~~~~~~~~~~~~~

- IdP의 인증서가 올바르게 설정되어 있는지 확인하십시오
- 인증서의 유효 기간이 만료되지 않았는지 확인하십시오
- 인증서는 Base64 인코딩된 내용만 줄 바꿈 없이 설정하십시오

사용자의 그룹·역할이 반영되지 않음
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP 측에서 속성（Attribute）이 올바르게 설정되어 있는지 확인하십시오
- ``saml.attribute.group.name`` 의 값이 IdP에서 전송되는 속성명과 일치하는지 확인하십시오
- SAML 어서션의 내용을 확인하려면 디버그 모드를 활성화하십시오

디버그 설정
-----------

문제를 조사할 때는 다음 설정으로 디버그 모드를 활성화할 수 있습니다.

::

    saml.security.debug=true

또한 |Fess| 의 로그 레벨을 조정하면 SAML 관련 상세 로그를 출력할 수 있습니다.

참고 정보
=========

- :doc:`security-role` - 역할 기반 검색 설정에 대하여
