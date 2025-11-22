================================
Google Search Appliance 호환 API
================================

|Fess| 는 검색 결과를 Google Search Appliance(GSA) 호환 XML 포맷으로 반환하는 API도 제공합니다.
XML 포맷에 대한 자세한 내용은 \ `GSA 공식 문서 <https://www.google.com/support/enterprise/static/gsa/docs/admin/74/gsa_doc_set/xml_reference/results_format.html>`__\ 를 참조하십시오.

설정
====

system.properties에 ``web.api.gsa=true`` 를 추가하여 Google Search Appliance 호환 API를 활성화하십시오.

요청
========

|Fess| 에
``http://localhost:8080/gsa/?q=검색어``
와 같은 요청을 전송하여 검색 결과를 GSA 호환 XML 형식으로 받을 수 있습니다.
요청 매개변수로 지정할 수 있는 값은 \ `JSON 응답의 검색 API <api-search.html>`__\ 와 동일합니다.
