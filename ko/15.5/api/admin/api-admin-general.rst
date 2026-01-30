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
============

요청
----------

::

    GET /api/admin/general

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "crawlerDocumentMaxSize": "10485760",
          "crawlerDocumentMaxSiteLength": "50",
          "crawlerDocumentMaxFetcherSize": "3",
          "crawlerDocumentCrawlerThreadCount": "10",
          "crawlerDocumentMaxDepth": "-1",
          "crawlerDocumentMaxAccessCount": "100",
          "indexerThreadDumpEnabled": "true",
          "indexerUnprocessedDocumentSize": "1000",
          "indexerClickCountEnabled": "true",
          "indexerFavoriteCountEnabled": "true",
          "indexerWebfsMaxContentLength": "10485760",
          "indexerWebfsContentEncoding": "UTF-8",
          "queryReplaceTermWithPrefixQuery": "false",
          "queryMaxSearchResultOffset": "100000",
          "queryMaxPageSize": "1000",
          "queryDefaultPageSize": "20",
          "queryAdditionalDefaultQuery": "",
          "queryGeoEnabled": "false",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "suggestBadWord": "true",
          "suggestPopularWordSeedLength": "1",
          "suggestPopularWordTags": "user",
          "suggestPopularWordFields": "tags",
          "suggestPopularWordExcludeWordFields": "",
          "ldapInitialContextFactory": "com.sun.jndi.ldap.LdapCtxFactory",
          "ldapSecurityAuthentication": "simple",
          "ldapProviderUrl": "ldap://localhost:389",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapBindDn": "",
          "ldapBindPassword": "",
          "notificationLogin": "true",
          "notificationSearchTop": "true"
        }
      }
    }

일반 설정 업데이트
============

요청
----------

::

    PUT /api/admin/general
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "crawlerDocumentMaxSize": "20971520",
      "crawlerDocumentMaxSiteLength": "100",
      "crawlerDocumentCrawlerThreadCount": "20",
      "queryMaxPageSize": "500",
      "queryDefaultPageSize": "50",
      "suggestSearchLog": "true",
      "suggestDocuments": "true",
      "suggestBadWord": "true",
      "notificationLogin": "false",
      "notificationSearchTop": "false"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 필드
     - 설명
   * - ``crawlerDocumentMaxSize``
     - 크롤링 대상 문서의 최대 크기 (바이트)
   * - ``crawlerDocumentMaxSiteLength``
     - 크롤링 대상 사이트의 최대 길이
   * - ``crawlerDocumentMaxFetcherSize``
     - 최대 페처 크기
   * - ``crawlerDocumentCrawlerThreadCount``
     - 크롤러 스레드 수
   * - ``crawlerDocumentMaxDepth``
     - 크롤링 최대 깊이 (-1=무제한)
   * - ``crawlerDocumentMaxAccessCount``
     - 최대 액세스 수
   * - ``indexerThreadDumpEnabled``
     - 스레드 덤프 활성화
   * - ``indexerUnprocessedDocumentSize``
     - 미처리 문서 수
   * - ``indexerClickCountEnabled``
     - 클릭 수 카운트 활성화
   * - ``indexerFavoriteCountEnabled``
     - 즐겨찾기 수 카운트 활성화
   * - ``queryReplaceTermWithPrefixQuery``
     - 전방일치 쿼리 변환
   * - ``queryMaxSearchResultOffset``
     - 검색 결과의 최대 오프셋
   * - ``queryMaxPageSize``
     - 페이지당 최대 건수
   * - ``queryDefaultPageSize``
     - 페이지당 기본 건수
   * - ``queryAdditionalDefaultQuery``
     - 추가 기본 쿼리
   * - ``suggestSearchLog``
     - 검색 로그에서 서제스트 활성화
   * - ``suggestDocuments``
     - 문서에서 서제스트 활성화
   * - ``suggestBadWord``
     - NG 워드 필터 활성화
   * - ``ldapProviderUrl``
     - LDAP 연결 URL
   * - ``ldapBaseDn``
     - LDAP 베이스 DN
   * - ``notificationLogin``
     - 로그인 알림
   * - ``notificationSearchTop``
     - 검색 톱 알림

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

사용 예
======

크롤러 설정 업데이트
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "crawlerDocumentMaxSize": "52428800",
           "crawlerDocumentCrawlerThreadCount": "15",
           "crawlerDocumentMaxAccessCount": "1000"
         }'

검색 설정 업데이트
--------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "queryMaxPageSize": "1000",
           "queryDefaultPageSize": "50",
           "queryMaxSearchResultOffset": "50000"
         }'

서제스트 설정 업데이트
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true",
           "suggestBadWord": "true"
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-systeminfo` - 시스템 정보 API
- :doc:`../../admin/general-guide` - 일반 설정 가이드
