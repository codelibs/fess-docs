==============================
Google Search Appliance 호환 API
==============================

.. warning::

   Google Search Appliance(GSA) 호환 API ( ``/gsa/`` ) 는 |Fess| 14.8 에서 삭제되었습니다. |Fess| 15.9 본체에도, 이전 API 를 제공하는 플러그인 ( ``fess-webapp-classic-api`` , ``fess-webapp-v1-api`` ) 에도 ``/gsa/`` 를 제공하는 구현이 없으므로, ``web.api.gsa`` 를 설정해도 효과가 없으며 ``/gsa/`` 에 대한 요청은 ``404`` 가 됩니다. 검색에는 :doc:`api-search` 에서 설명하는 ``/api/v2/search`` 를 사용하십시오.
