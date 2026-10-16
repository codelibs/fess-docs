======================
검색 결과 내보내기 API
======================

이 문서에서는 검색 결과를 CSV 또는 JSON 파일로 다운로드하는 |Fess| 의 v2 내보내기 API 에 대해 설명합니다. 공통 응답 엔벨로프·오류 모델에 대해서는 :doc:`api-overview` 를 참조하십시오.

베이스 URL은 ``http://<Server Name>/api/v2/`` 입니다 (로컬 환경 예: ``http://localhost:8080/api/v2`` ).

.. note::

   내보내기는 기본적으로 비활성화되어 있습니다. 사용하려면 ``fess_config.properties`` 에서 ``api.search.export=true`` 를 설정하십시오. 활성화하면 기본 제공 ``bootstrap`` 테마에서 검색 결과 건수 옆에 내보내기 메뉴(CSV / JSON)가 표시됩니다. ``/api/v2/ui/config`` 의 ``features.search_export`` 로 상태를 확인할 수 있습니다.

검색 결과 다운로드
==================

요청
----

==================  ====================================================
HTTP 메서드         GET
엔드포인트          ``/api/v2/documents/export``
==================  ====================================================

검색에 일치하는 문서를 파일 다운로드( ``Content-Disposition: attachment`` , 파일 이름은 ``search_results.csv`` 또는 ``search_results.json`` )로 반환합니다.

- ``/api/v2/search`` 와 같은 역할 필터가 적용됩니다. ``login.required=true`` 인 경우에도 ``/api/v2/search`` 와 마찬가지로 액세스 토큰을 사용할 수 있습니다.
- 출력하는 건수는 최대 ``api.search.export.max.size`` (기본값: ``1000`` )건입니다. 페이징 파라미터( ``start`` , ``num`` )는 사용하지 않습니다.
- 출력하는 필드는 ``api.search.export.fields`` (기본값: ``title,url_link,last_modified,content_length,filetype`` ) 중 API 응답에 포함할 수 있는 필드뿐입니다.
- 요청은 1분당 ``api.search.export.rate.limit.per.minute`` (기본값: ``10`` , ``0`` 은 무제한)회로 제한됩니다. 로그인한 사용자는 사용자별, 게스트는 클라이언트 IP 주소별로 셉니다. 초과하면 ``429`` 와 ``Retry-After`` 헤더가 반환됩니다.
- 내보내기는 검색 로그에 기록되지 않습니다.

요청 파라미터
-------------

``q`` , ``ex_q`` , ``fields.*`` , ``sort`` , ``lang`` 등 ``/api/v2/documents/all`` 과 같은 검색 조건 파라미터를 지정할 수 있습니다( :doc:`api-search` 참조). 이와 더불어 다음 파라미터가 있습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 파라미터

   * - ``format``
     - 파일 형식. ``csv`` (기본값) 또는 ``json`` . 그 밖의 값은 ``invalid_request`` (400)가 됩니다.

표: 요청 파라미터

응답
----

CSV 는 첫 행이 필드 이름의 머리글 행이며 ``csv.file.encoding`` 의 문자 코드로 출력됩니다(UTF-8 의 경우 BOM 이 붙습니다). ``=`` , ``+`` , ``-`` , ``@`` , 탭, 캐리지 리턴으로 시작하는 값에는 스프레드시트에서 수식으로 처리되지 않도록 앞에 ``'`` 가 붙습니다. 여러 값을 가진 필드는 공백으로 연결합니다.

::

    "title","url_link","last_modified","content_length","filetype"
    "Example","https://example.com/","2025-01-01T00:00:00.000Z","1234","html"

JSON 은 ``{"data":[{...},...]}`` 형식이며, 여러 값을 가진 필드는 배열 그대로입니다.

파일 출력이 시작되기 전에 실패하면 일반 오류 엔벨로프가 반환됩니다. 출력이 시작된 후에 실패하면 파일이 도중에 끝납니다(CSV 는 도중까지, JSON 은 해석할 수 없는 내용이 됩니다).

오류 응답
---------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 잘못된 쿼리, ``format`` 이 ``csv`` / ``json`` 이외, 또는 ``api.search.export=false`` 로 내보내기가 비활성화된 경우.
   * - 401 Unauthorized
     - 인증이 필요한 경우( ``login.required=true`` 에서 익명 호출자 등).
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 429 Too Many Requests
     - 1분당 요청 수 상한을 초과한 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

표: 오류 응답
