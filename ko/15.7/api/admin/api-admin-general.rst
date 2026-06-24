==========================
General API
==========================

개요
====

General API는 |Fess| 의 일반 설정（시스템 전반에 관한 설정）을 관리하기 위한 API입니다.
크롤링, 로그, 검색 결과 표시, 서제스트, 로그 보존 기간, 알림, 인증（LDAP / SSO）,
클라우드 스토리지 연동 등의 설정을 조회·업데이트할 수 있습니다. 이러한 설정은 관리
화면의 「일반」 설정（:doc:`../../admin/general-guide`）에 대응합니다.

기본 URL
=========

::

    /api/admin/general

이 API에 접근하려면 ``Radmin-api`` 권한을 가진 액세스 토큰이 필요합니다.
인증 방법의 자세한 내용은 :doc:`api-admin-overview` 를 참조하십시오.

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /
     - 일반 설정 조회
   * - PUT
     - /
     - 일반 설정 업데이트

일반 설정 조회
==============

요청
----------

::

    GET /api/admin/general

이 엔드포인트는 쿼리 파라미터를 받지 않습니다.

응답
----------

``response.setting`` 에 현재 일반 설정이 포함됩니다. 응답에는 업데이트 가능한 모든
설정 필드가 포함되지만, 아래 예시에서는 대표적인 필드만 발췌하여 보여줍니다.
켜기/끄기 설정은 ``"true"`` / ``"false"`` 문자열로, 보존 일수나 스레드 수 등은
숫자로 표현됩니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "incrementalCrawling": "true",
          "dayForCleanup": -1,
          "crawlingThreadCount": 5,
          "searchLog": "true",
          "userInfo": "true",
          "userFavorite": "false",
          "webApiJson": "true",
          "defaultLabelValue": "",
          "defaultSortValue": "",
          "appendQueryParameter": "false",
          "loginRequired": "false",
          "thumbnail": "true",
          "failureCountThreshold": -1,
          "popularWord": "true",
          "csvFileEncoding": "UTF-8",
          "purgeSearchLogDay": 30,
          "purgeJobLogDay": 30,
          "purgeUserInfoDay": 30,
          "purgeSuggestSearchLogDay": 30,
          "notificationTo": "",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "ldapProviderUrl": "ldap://localhost:389/",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapAdminSecurityPrincipal": "cn=admin,dc=example,dc=com",
          "ldapAdminSecurityCredentials": null,
          "storageAccessKey": "**********",
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   보안상의 이유로 비밀번호 및 시크릿 값은 응답에 그대로 포함되지 않습니다. LDAP
   관리자 비밀번호 ``ldapAdminSecurityCredentials`` 는 항상 ``null`` 로 반환됩니다.
   그 외의 시크릿 필드（``storageAccessKey``, ``storageSecretKey``, ``oicClientId``,
   ``oicClientSecret``, ``spnegoPreauthPassword``, ``entraidClientId``,
   ``entraidClientSecret``）는 설정된 경우 마스크 값 ``"**********"``, 미설정인 경우
   빈 문자열로 반환됩니다.

일반 설정 업데이트
==================

요청
----------

::

    PUT /api/admin/general
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

업데이트는 부분 업데이트（merge）로 처리됩니다. 서버는 현재 설정 값을 읽어들인 후,
요청에 포함된 ``null`` 이 아닌 필드만 덮어씁니다. 요청에 포함되지 않은 필드나
``null`` 인 필드는 기존 값이 유지됩니다.

.. important::

   요청 본문은 덮어쓰기 처리 전에 검증됩니다. 따라서 필수 필드
   （``dayForCleanup``, ``crawlingThreadCount``, ``failureCountThreshold``,
   ``csvFileEncoding``）는 변경 여부에 관계없이 **항상 요청에 포함해야 합니다**.
   그 중 하나라도 누락되면 검증 오류가 발생하여 ``status: 1`` 이 반환됩니다.
   일부 필드만 변경하려면, 먼저 ``GET`` 으로 현재 설정을 조회한 후 필수 필드의
   현재 값을 포함하여 ``PUT`` 하십시오.

.. note::

   비밀번호·시크릿 필드（``ldapAdminSecurityCredentials``, ``storageAccessKey``,
   ``storageSecretKey``, ``oicClientId``, ``oicClientSecret``,
   ``spnegoPreauthPassword``, ``entraidClientId``, ``entraidClientSecret``）는
   빈 문자열이나 마스크 값（``**********``）을 전송한 경우 무시되며, 기존 값이
   유지됩니다. 이 필드들은 실제 값을 전송한 경우에만 업데이트됩니다.

.. code-block:: json

    {
      "incrementalCrawling": "true",
      "dayForCleanup": -1,
      "crawlingThreadCount": 10,
      "failureCountThreshold": 100,
      "csvFileEncoding": "UTF-8",
      "popularWord": "true"
    }

주요 필드
~~~~~~~~~~~~~~

설정 항목은 매우 다양합니다. 대표적인 필드를 아래에 나타냅니다（모든 필드는 관리
화면의 「일반」 설정에 대응합니다）. 켜기/끄기 설정은 ``"true"`` / ``"false"``
문자열로 지정합니다.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 필드
     - 필수
     - 설명
   * - ``incrementalCrawling``
     - 아니오
     - 증분 크롤링 활성화/비활성화
   * - ``dayForCleanup``
     - 예
     - 크롤링된 문서를 보존하는 일수 (-1=클린업 비활성화; 지정 범위: -1~1000)
   * - ``crawlingThreadCount``
     - 예
     - 크롤링에 사용하는 스레드 수 (지정 범위: 0~100)
   * - ``failureCountThreshold``
     - 예
     - URL 크롤링을 중지하는 실패 횟수 임계값 (-1=비활성화; 지정 범위: -1~10000)
   * - ``csvFileEncoding``
     - 예
     - CSV 내보내기 인코딩
   * - ``searchLog``
     - 아니오
     - 검색 쿼리 로그 활성화/비활성화
   * - ``userInfo``
     - 아니오
     - 사용자 정보 기록 활성화/비활성화
   * - ``userFavorite``
     - 아니오
     - 즐겨찾기 기능 활성화/비활성화
   * - ``webApiJson``
     - 아니오
     - JSON Web API 활성화/비활성화
   * - ``popularWord``
     - 아니오
     - 인기 워드 집계·표시 활성화/비활성화
   * - ``defaultLabelValue``
     - 아니오
     - 기본 라벨 값
   * - ``defaultSortValue``
     - 아니오
     - 기본 정렬 순서
   * - ``appendQueryParameter``
     - 아니오
     - 검색 결과 URL에 쿼리 파라미터 부여
   * - ``loginRequired``
     - 아니오
     - 검색에 로그인을 필수로 할지 여부
   * - ``thumbnail``
     - 아니오
     - 썸네일 생성 활성화/비활성화
   * - ``ignoreFailureType``
     - 아니오
     - 무시할 크롤링 실패 타입
   * - ``purgeSearchLogDay``
     - 아니오
     - 검색 로그를 보존하는 일수 (-1=비활성화; 지정 범위: -1~100000)
   * - ``purgeJobLogDay``
     - 아니오
     - 잡 로그를 보존하는 일수 (-1=비활성화; 지정 범위: -1~100000)
   * - ``purgeUserInfoDay``
     - 아니오
     - 사용자 정보를 보존하는 일수 (-1=비활성화; 지정 범위: -1~100000)
   * - ``purgeSuggestSearchLogDay``
     - 아니오
     - 서제스트 검색 로그를 보존하는 일수 (0=비활성화; 지정 범위: 0~100000)
   * - ``purgeByBots``
     - 아니오
     - 검색 로그를 폐기할 대상 봇 User-Agent
   * - ``notificationTo``
     - 아니오
     - 시스템 알림 발송처 이메일 주소
   * - ``notificationLogin``
     - 아니오
     - 로그인 페이지에 표시할 알림 메시지
   * - ``notificationSearchTop``
     - 아니오
     - 검색 톱 페이지에 표시할 알림 메시지
   * - ``notificationAdvanceSearch``
     - 아니오
     - 상세 검색 페이지에 표시할 알림 메시지
   * - ``suggestSearchLog``
     - 아니오
     - 검색 로그에서 서제스트 활성화/비활성화
   * - ``suggestDocuments``
     - 아니오
     - 문서에서 서제스트 활성화/비활성화
   * - ``logLevel``
     - 아니오
     - 시스템 로그의 로그 레벨
   * - ``logNotificationEnabled``
     - 아니오
     - ERROR/WARN 로그 알림 활성화/비활성화
   * - ``logNotificationLevel``
     - 아니오
     - 로그 알림 레벨
   * - ``slackWebhookUrls``
     - 아니오
     - 알림용 Slack Webhook URL
   * - ``googleChatWebhookUrls``
     - 아니오
     - 알림용 Google Chat Webhook URL

인증 관련 필드
~~~~~~~~~~~~~~~~~~

LDAP 및 SSO（OpenID Connect, SAML, SPNEGO, Entra ID）에 관한 설정도 이 API로
관리합니다. 대표적인 필드를 아래에 나타냅니다（모든 필드는 관리 화면의 「일반」
설정에 대응합니다）.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 필드
     - 설명
   * - ``ldapProviderUrl``
     - LDAP 연결 URL
   * - ``ldapBaseDn``
     - LDAP 베이스 DN
   * - ``ldapSecurityPrincipal``
     - LDAP 바인드용 시큐리티 프린시펄
   * - ``ldapAdminSecurityPrincipal``
     - LDAP 관리 작업용 시큐리티 프린시펄
   * - ``ldapAdminSecurityCredentials``
     - LDAP 관리자 비밀번호 (응답에서 ``null`` 로 대체)
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - 사용자/그룹 검색 필터
   * - ``ssoType``
     - SSO 타입 (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oicClientId`` / ``oicClientSecret`` / ``oicAuthServerUrl`` 외
     - OpenID Connect 설정
   * - ``samlIdpEntityid`` / ``samlSpEntityid`` 외
     - SAML 설정
   * - ``spnegoKrb5Conf`` / ``spnegoLoginConf`` 외
     - SPNEGO 설정
   * - ``entraidClientId`` / ``entraidTenant`` 외
     - Microsoft Entra ID 설정

스토리지 관련 필드
~~~~~~~~~~~~~~~~~~~~~~~~

클라우드 스토리지（S3 / GCS） 연동 설정도 관리할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 필드
     - 설명
   * - ``storageType``
     - 스토리지 타입 (``auto`` / ``s3`` / ``gcs``)
   * - ``storageEndpoint``
     - 스토리지 엔드포인트 URL
   * - ``storageAccessKey`` / ``storageSecretKey``
     - 인증용 액세스 키/시크릿 키
   * - ``storageBucket``
     - 버킷 이름
   * - ``storageRegion``
     - S3 리전
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - GCS 프로젝트 ID / 인증 정보 파일 경로

응답
----------

업데이트 성공 시 ``version`` 과 ``status`` 만 반환됩니다（``id`` 나 ``created`` 는
포함되지 않습니다）.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

검증 오류 등으로 업데이트에 실패한 경우, ``status`` 에 0 이외의 값（검증 오류는 ``1``）이
설정되고 ``message`` 에 오류 내용이 포함됩니다. ``status`` 값의 목록은
:doc:`api-admin-overview` 를 참조하십시오.

사용 예
=======

.. note::

   아래 예시에서는 필수 필드（``dayForCleanup``, ``crawlingThreadCount``,
   ``failureCountThreshold``, ``csvFileEncoding``）를 포함하고 있습니다. 이 필드들은
   변경 내용에 관계없이 항상 지정해야 하므로, 실제 운용 시에는 ``GET`` 으로 조회한
   현재 값을 지정하십시오.

크롤링 설정 업데이트
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incrementalCrawling": "true",
           "crawlingThreadCount": 10,
           "failureCountThreshold": 100,
           "dayForCleanup": -1,
           "csvFileEncoding": "UTF-8"
         }'

로그 보존 기간 업데이트
-----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

서제스트 설정 업데이트
----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-systeminfo` - 시스템 정보 API
- :doc:`../../admin/general-guide` - 일반 설정 가이드
