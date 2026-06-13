==========================
General API
==========================

개요
====

General API는 |Fess| 의 일반 설정을 관리하기 위한 API입니다.
시스템 전반에 관련된 설정의 조회와 업데이트를 수행할 수 있습니다.

기본 URL
=========

::

    /api/admin/general

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

응답
----------

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
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   보안상의 이유로 LDAP 관리자 비밀번호인 ``ldapAdminSecurityCredentials``
   는 응답에서 항상 ``null`` 로 대체됩니다（소스:
   ``ApiAdminGeneralAction.java:71``）.

일반 설정 업데이트
==================

요청
----------

::

    PUT /api/admin/general
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

업데이트는 부분 업데이트(merge)로 처리됩니다. 요청에 포함되지 않은 필드는
기존 값이 유지되며, ``null`` 인 필드는 무시됩니다（소스:
``ApiAdminGeneralAction.java:84-90``）.

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

설정 항목은 매우 다양합니다. 대표적인 필드를 아래에 나타냅니다
（전체 필드는 ``EditForm.java`` 를 참조）. ``available`` 계열의 켜기/끄기 설정은
``"true"`` / ``"false"`` 문자열로 표현됩니다.

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
     - 크롤링된 문서를 보존하는 일수 (-1=클린업 비활성화)
   * - ``crawlingThreadCount``
     - 예
     - 크롤링에 사용하는 스레드 수
   * - ``failureCountThreshold``
     - 예
     - URL 크롤링을 중지하는 실패 횟수 임계값 (-1=비활성화)
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
     - 검색 로그를 보존하는 일수 (-1=비활성화)
   * - ``purgeJobLogDay``
     - 아니오
     - 잡 로그를 보존하는 일수 (-1=비활성화)
   * - ``purgeUserInfoDay``
     - 아니오
     - 사용자 정보를 보존하는 일수 (-1=비활성화)
   * - ``purgeSuggestSearchLogDay``
     - 아니오
     - 서제스트 검색 로그를 보존하는 일수 (0=비활성화)
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

LDAP 및 SSO(OpenID Connect, SAML, SPNEGO, Entra ID)에 관한 설정도
이 API로 관리합니다. 대표적인 필드를 아래에 나타냅니다
（전체 필드는 ``EditForm.java`` 를 참조）.

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

클라우드 스토리지(S3 / GCS) 연동 설정도 관리할 수 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 필드
     - 설명
   * - ``storageType``
     - 스토리지 타입 (``s3`` / ``gcs`` / ``auto``)
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

업데이트 성공 시 ``status`` 만 반환됩니다 (``id`` 나 ``created`` 는 포함되지 않습니다).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

사용 예
======

크롤링 설정 업데이트
------------------

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
------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

서제스트 설정 업데이트
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-systeminfo` - 시스템 정보 API
- :doc:`../../admin/general-guide` - 일반 설정 가이드
