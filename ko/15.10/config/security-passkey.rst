============================
패스키(WebAuthn) 로그인 설정
============================

개요
====

|Fess| 에서는 로컬 사용자(관리 화면의 "사용자"에서 만든 사용자)가 비밀번호 대신 패스키(WebAuthn)로 로그인할 수 있습니다. 이 기능은 15.10에서 추가되었으며 기본적으로 꺼져 있습니다.

- 사용자는 비밀번호와 패스키 중 어느 쪽으로든 로그인할 수 있습니다. 둘 다 요구하는 다단계 인증이 아닙니다.
- 대상은 ``fess_user`` 인덱스의 로컬 사용자뿐입니다. LDAP 사용자나 SSO 사용자는 패스키를 등록할 수 없으며, 패스키 로그인은 LDAP에 문의하지 않습니다.
- |Fess| 는 패스키의 공개 키와 이름 등을 저장합니다. 개인 키는 사용자의 인증기(브라우저, OS, 보안 키 등)에 남으며 |Fess| 에 전달되지 않습니다.

설정
====

패스키 설정은 ``fess_config.properties`` (ZIP 패키지는 ``app/WEB-INF/classes/fess_config.properties`` , RPM/DEB은 ``/etc/fess/fess_config.properties`` )에 기술합니다. 관리 화면의 "시스템" → "일반"에는 이 설정 항목이 없으며 ``system.properties`` 에서도 설정할 수 없습니다. 변경을 적용하려면 |Fess| 를 재시작해야 합니다. Docker에서는 ``FESS_JAVA_OPTS`` 에 ``-Dfess.config.passkey.enabled=true`` 와 같이 전달할 수 있습니다( :doc:`../install/install-docker` 참조).

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - 키
     - 기본값
     - 설명
   * - ``passkey.enabled``
     - ``false``
     - 패스키 로그인을 활성화합니다. ``true`` 여도 아래의 ``passkey.rp.id`` 와 ``passkey.origins`` 에 사용 가능한 값이 없으면 기능은 꺼진 채로 유지됩니다.
   * - ``passkey.rp.id``
     - (빈 값)
     - 신뢰 당사자(Relying Party) ID: 패스키가 연결되는 도메인입니다(예: ``example.com`` ). 패스키는 이 호스트와 그 하위 도메인에서만 동작합니다.
   * - ``passkey.rp.name``
     - ``Fess``
     - 패스키를 만들 때 브라우저에 표시되는 신뢰 당사자 이름입니다.
   * - ``passkey.origins``
     - (빈 값)
     - 패스키 처리(ceremony)를 받아들이는 오리진(쉼표 구분)입니다(예: ``https://fess.example.com`` ). 각 항목은 호스트 이름이 있는 ``http`` 또는 ``https`` 오리진이어야 합니다.

기능을 켜는 예입니다.
::

    passkey.enabled=true
    passkey.rp.id=example.com
    passkey.rp.name=Fess
    passkey.origins=https://fess.example.com

- ``passkey.rp.id`` 는 모든 패스키가 연결되는 도메인입니다. 사용자가 패스키를 등록한 후에 변경하면 등록된 패스키를 모두 사용할 수 없게 되어 사용자가 새 ID로 다시 등록해야 하므로, 한 번만 신중하게 정하십시오. ``passkey.origins`` 의 각 오리진의 호스트는 ``passkey.rp.id`` 이거나 그 하위 도메인이어야 합니다.
- ``passkey.origins`` 에는 리버스 프록시 뒤의 주소가 아니라, 사용자가 브라우저에서 |Fess| 를 여는 오리진(스킴, 호스트, 포트)을 그대로 나열합니다. 그 외의 오리진에서의 처리는 거부됩니다.

기능이 꺼진 채로 유지되는 경우
------------------------------

``passkey.enabled=true`` 여도 다음 경우에는 **화면에 오류가 표시되지 않은 채** 패스키가 꺼진 채로 유지됩니다. 로그인 화면에 패스키 버튼이 표시되지 않고, ``/api/v2/auth/passkey`` 아래의 모든 API가 ``404`` 를 반환하며, ``/api/v2/ui/config`` 의 ``features.passkey_enabled`` 는 ``false`` 입니다. 이유는 ``fess.log`` 의 경고에 있으며, 경고는 시작 후 한 번만 출력됩니다.

- ``passkey.rp.id`` 또는 ``passkey.origins`` 가 비어 있음: ``passkey.enabled is true but passkey.rp.id or passkey.origins is empty, so passkeys are disabled.``
- ``passkey.origins`` 에 항목이 없음: ``passkey.enabled is true but passkey.origins holds no origin, so passkeys are disabled.``
- ``passkey.origins`` 에 ``http`` 나 ``https`` 오리진이 아닌 항목이 있음(호스트 이름이 없는 값, 다른 스킴 등): ``passkey.origins holds an entry that is not an http or https origin, so passkeys are disabled: entry=...``

``passkey.origins`` 가 사용 가능한 값이어도 사용자가 연 오리진이 그 안에 없으면 모든 등록과 로그인이 거부됩니다. 사용자 화면에는 이유가 표시되지 않으므로 ``fess.log`` 를 확인하십시오. ``A passkey response came from an origin that is not in passkey.origins: origin=...`` 가 거부된 오리진과 설정을 보여 줍니다(첫 번째만 출력됩니다). 그 오리진을 ``passkey.origins`` 에 추가하십시오.

사용 방법
=========

로그인
------

패스키가 켜져 있고 브라우저가 WebAuthn을 지원하면, 검색 화면의 로그인과 관리 화면의 로그인 페이지에 "패스키로 로그인" 버튼이 표시됩니다. 브라우저가 인증기를 요청하며, 사용자는 사용자 이름을 입력하지 않고 로그인합니다.

패스키 로그인은 비밀번호 로그인과 같은 IP 주소별 횟수 제한(``theme.api.login.*`` )을 사용합니다. 실패는 횟수에 집계되고 성공하면 횟수가 돌아옵니다( :doc:`rate-limiting` 참조). 화면은 실패한 이유를 알려 주지 않으며, 잘못된 비밀번호와 같은 메시지를 표시합니다.

패스키 등록과 삭제
------------------

로컬 사용자는 검색 화면의 사용자 메뉴에 있는 "비밀번호 변경"(``/profile`` )의 "패스키"에서 자신의 패스키를 등록하고 삭제합니다.

1. 패스키 이름(최대 64자)과 현재 비밀번호를 입력하고 "패스키 등록"을 누릅니다.
2. 브라우저의 안내에 따라 인증기에 패스키를 만듭니다.

- 등록할 때마다 현재 비밀번호가 필요합니다. 사용자 이름과 비밀번호를 디렉터리(LDAP)도 받아들이는 로컬 사용자는, 비밀번호 확인으로는 어느 계정을 확인했는지 알 수 없으므로 패스키를 등록할 수 없습니다.
- 사용자 한 명이 가질 수 있는 패스키는 최대 20개입니다.
- 패스키가 없고 등록도 할 수 없는 사용자(LDAP 또는 SSO 사용자, 또는 WebAuthn이 없는 브라우저)에게는 "패스키" 섹션이 표시되지 않습니다.
- 패스키를 삭제하면 분실한 인증기로 연 세션이 남지 않도록 해당 사용자의 **다른 로그인 세션이 종료됩니다**. 비밀번호 변경과 같은 방식으로 동작합니다(아래의 "비밀번호와의 관계" 참조). 삭제를 수행한 세션은 유지됩니다.

관리자 조작
-----------

관리 화면의 "사용자"에 있는 사용자 상세 페이지에는 그 사용자의 패스키(이름, 생성 시각, 마지막 사용 시각)가 나열됩니다. 관리자는 패스키를 등록할 수 없지만, 편집 권한이 있는 관리자는 사용자가 인증기를 분실한 경우 등에 "리셋"으로 패스키를 삭제할 수 있습니다. 그러면 사용자는 새 패스키를 등록할 수 있습니다. 리셋하면 해당 사용자의 로그인 세션도 종료됩니다(아래의 "비밀번호와의 관계" 참조).

``passkey.enabled`` 를 다시 ``false`` 로 해도, 패스키가 있는 사용자의 상세 페이지에는 계속 패스키가 나열되며 삭제할 수 있습니다. 기능을 꺼도 패스키 데이터는 삭제되지 않습니다.

비밀번호와의 관계
=================

- 패스키와 비밀번호는 별개의 자격 증명입니다. 사용자의 비밀번호를 변경하거나 관리자가 새 비밀번호를 설정해도 등록된 패스키는 삭제되지 않으며, 계속 로그인에 사용할 수 있습니다.
- 비밀번호가 변경되면 해당 사용자의 다른 로그인 세션이 종료됩니다( :doc:`../install/security` 참조). 패스키로 연 세션도 포함됩니다. 각 세션은 ``password.changed.check.interval`` 초(기본값 ``60`` )에 한 번 이하로 확인하므로 세션은 그 시간 이내에 종료됩니다.
- 패스키를 삭제하면 다른 세션이 같은 방식으로 종료됩니다(위 참조).

사용자 삭제와 이름 변경
=======================

패스키는 사용자 이름만으로 사용자에 연결됩니다. 같은 이름의 다른 사용자가 패스키를 물려받지 않도록 다음 경우에도 패스키가 삭제됩니다.

- 사용자를 삭제할 때.
- 사용자를 만들 때(그 이름으로 남아 있던 패스키가 삭제됩니다).
- 사용자 이름을 변경할 때(이전 이름과 새 이름 양쪽의 패스키가 삭제됩니다). 패스키는 이름 변경을 따라가지 않으므로 사용자가 다시 등록합니다. 다른 사용자가 이미 사용 중인 이름으로의 변경은 패스키가 삭제되기 전에 거부됩니다.

저장과 백업
===========

패스키는 ``fess_user.passkey`` 인덱스에 저장됩니다(접두사는 ``index.user.index`` 이며 기본값은 ``fess_user`` ). 이 인덱스는 패스키가 꺼져 있어도 |Fess| 가 시작할 때 만들어지며, 사용자를 삭제하거나 이름을 변경할 때와 사용자 상세 페이지에서 사용됩니다. |Fess| 가 인덱스를 만들 수 없는 환경이라면 업그레이드 전에 직접 만드십시오( :ref:`upgrade-1510-passkey` 참조).

이 인덱스는 ``fess_user`` 별칭에 포함되지 않으므로 관리 화면 "백업"의 ``fess_user.bulk`` 에는 패스키가 들어 있지 않습니다. 백업에서 복원한 후에는 사용자가 패스키를 다시 등록합니다.

요구 사항
=========

- **HTTPS**: 브라우저는 보안 컨텍스트(HTTPS 또는 ``localhost`` )에서만 WebAuthn을 허용합니다. |Fess| 는 ``passkey.origins`` 의 ``http`` 오리진도 받아들이지만, 운영 환경에서는 |Fess| 를 HTTPS로 제공하고 ``https://`` 오리진을 지정하십시오( :doc:`../install/security` 의 "HTTPS 활성화" 참조).
- **브라우저**: WebAuthn API(``PublicKeyCredential`` )를 제공하는 브라우저가 필요합니다. 제공하지 않는 브라우저에는 로그인 버튼도 등록 섹션도 표시되지 않습니다.
- **인증기**: 검색 가능한 자격 증명(discoverable credential)과 사용자 확인(PIN, 생체 인증 등)을 지원해야 합니다. |Fess| 는 둘 다 요구하고, 서명 알고리즘 ES256과 RS256을 지원하며, 증명(attestation)은 사용하지 않습니다.
- **여러 노드**: 패스키 처리의 챌린지는 HTTP 세션에 5분 동안 보관됩니다. 로드 밸런서 뒤에 여러 노드를 두는 경우에는 노드 간에 세션을 공유하거나(환경 변수 ``FESS_SESSION_STORE=opensearch`` ) 로드 밸런서가 세션마다 하나의 노드에 고정되도록 하십시오.

API
===

패스키 API는 ``/api/v2/auth/passkey`` 아래에 있습니다. 패스키가 꺼져 있는 동안에는 모두 ``404`` 를 반환합니다. 기능을 사용할 수 있는지는 ``/api/v2/ui/config`` 의 ``features.passkey_enabled`` 로 알 수 있습니다( :doc:`../api/api-uiconfig` 참조).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 엔드포인트
     - 설명
   * - ``POST /api/v2/auth/passkey/login/options``
     - 로그인 옵션(챌린지)을 가져옵니다.
   * - ``POST /api/v2/auth/passkey/login/verify``
     - 인증기의 응답을 검증하고 로그인합니다.
   * - ``GET /api/v2/auth/passkey``
     - 로그인한 사용자의 패스키를 나열하고, 사용자가 패스키를 등록할 수 있는지(``can_register`` )를 알려 줍니다.
   * - ``POST /api/v2/auth/passkey/register/options``
     - 현재 비밀번호(``current_password`` )를 확인하고 등록 옵션을 가져옵니다.
   * - ``POST /api/v2/auth/passkey/register/verify``
     - 이름(``label`` )과 인증기의 응답을 검증하고 패스키를 등록합니다.
   * - ``DELETE /api/v2/auth/passkey/{credentialId}``
     - 로그인한 사용자의 패스키를 삭제합니다.

``register`` 호출과 삭제에는 ``X-Fess-CSRF-Token`` 헤더가 필요합니다. 로그인 호출 두 개는 ``/api/v2/auth/login`` 과 마찬가지로 CSRF 토큰이 필요하지 않습니다.

문제 해결
=========

패스키 버튼이 표시되지 않음
---------------------------

- ``/api/v2/ui/config`` 의 ``features.passkey_enabled`` 를 확인하십시오. ``false`` 이면 ``fess.log`` 에서 경고를 찾아 설정이 사용 가능한 값인지 확인하십시오(위의 "기능이 꺼진 채로 유지되는 경우" 참조).
- 변경한 후 |Fess| 를 재시작했는지 확인하십시오.
- 브라우저가 WebAuthn을 지원하는지, 페이지가 HTTPS(또는 ``localhost`` )로 열려 있는지 확인하십시오.
- 번들된 테마가 아닌 테마를 사용하는 경우, 그 테마가 패스키 버튼을 지원해야 합니다.

등록 또는 로그인이 실패함
-------------------------

- ``fess.log`` 에 ``is not in passkey.origins`` 가 포함된 경고가 있으면, 브라우저에서 연 오리진을 ``passkey.origins`` 에 추가하십시오.
- ``passkey.rp.id`` 를 변경한 후에는 변경 전에 등록한 패스키를 사용할 수 없습니다. 이전 패스키를 삭제하고 다시 등록하십시오.
