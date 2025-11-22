==============
쿼리 요청
==============

개요
====

이 페이지에서는 JSON 파일의 쿼리 요청을 OpenSearch에 전송합니다.

|image0|

작업 방법
======

요청 전송
------------

관리자로 로그인 후 /admin/esreq/를 URL 경로로 입력하십시오.
OpenSearch에 전송하려는 쿼리 요청을 JSON 파일로 작성하여 "요청 파일"로 해당 JSON 파일을 선택하고 "전송" 버튼을 클릭하여 OpenSearch에 요청을 전송합니다.
응답은 파일로 다운로드됩니다.

설정 항목
------

요청 파일
::::::::::::::

쿼리 DSL을 기술한 JSON 파일을 지정합니다.
예를 들어, JSON 파일의 내용은 다음과 같습니다.

::

    POST /_search
    {
      "query": {
        "match_all": {}
      }
    }

.. |image0| image:: ../../../resources/images/en/15.3/admin/esreq-1.png
