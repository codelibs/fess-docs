================================
Google Search Appliance 互換 API
================================

.. warning::

   GSA 互換 API（ ``/gsa/`` ）は、 |Fess| 14.8 で削除されました。15.9 の |Fess| 本体にも、旧 API を提供するプラグイン（ ``fess-webapp-classic-api`` ・ ``fess-webapp-v1-api`` ）にも、 ``/gsa/`` を提供する実装はありません。 ``web.api.gsa`` を設定しても有効にならず、 ``/gsa/`` へのリクエストは ``404`` になります。検索には、 :doc:`api-search` の ``/api/v2/search`` を使用してください。
