================================
Google Search Appliance兼容API
================================

.. warning::

   Google Search Appliance（GSA）兼容 API（ ``/gsa/`` ）已在 |Fess| 14.8 中删除，并且 |Fess| 15.9 本身以及提供旧 API 的插件（ ``fess-webapp-classic-api`` 和 ``fess-webapp-v1-api`` ）都没有实现 ``/gsa/`` ，因此设置 ``web.api.gsa`` 不会产生任何效果，对 ``/gsa/`` 的请求会返回 ``404`` 。请使用 :doc:`api-search` 中介绍的 ``/api/v2/search`` 进行搜索。
