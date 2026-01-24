======
API 개요
======


|Fess| 에서 제공하는 API
==================

본 문서에서는 |Fess| 가 제공하는 API에 대해 설명합니다.
API를 활용하면 기존 웹 시스템 등에서도 |Fess| 를 검색 서버로 사용할 수 있습니다.

기본 URL
======

|Fess| 의 API 엔드포인트는 다음 기본 URL로 제공됩니다.

::

    http://<Server Name>/api/v1/

예를 들어, 로컬 환경에서 실행 중인 경우 다음과 같습니다.

::

    http://localhost:8080/api/v1/

인증
==

현재 버전에서는 API 사용에 인증이 필요하지 않습니다.
단, 관리 화면의 각종 설정에서 API를 활성화해야 합니다.

HTTP 메서드
========

모든 API 엔드포인트는 **GET** 메서드로 액세스합니다.

응답 형식
=====

모든 API 응답은 **JSON 형식** 으로 반환됩니다(GSA 호환 API 제외).
응답의 ``Content-Type`` 은 ``application/json`` 입니다.

오류 처리
=====

API 요청이 실패한 경우 적절한 HTTP 상태 코드와 함께 오류 정보가 반환됩니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: HTTP 상태 코드

   * - 200
     - 요청이 정상적으로 처리되었습니다.
   * - 400
     - 요청 매개변수가 올바르지 않습니다.
   * - 404
     - 요청된 리소스를 찾을 수 없습니다.
   * - 500
     - 서버 내부에서 오류가 발생했습니다.

표: HTTP 상태 코드

API 유형
======

|Fess| 는 다음 API를 제공합니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - 검색 결과를 조회하는 API.
   * - popularword
     - 인기 검색어를 조회하는 API.
   * - label
     - 생성된 레이블 목록을 조회하는 API.
   * - health
     - 서버 상태를 조회하는 API.
   * - suggest
     - 자동완성 검색어를 조회하는 API.

표: API 유형
