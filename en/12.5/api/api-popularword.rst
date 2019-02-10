==================
Popular Word API
==================

Popular Word API
====================

Popular Word API returns popular words as JSON format.
URL for Popular Word API is ``http://<Server Name>/json/?type=popularword``.
Enabling Popular Word Response at System > General page, this feature is available.


Request Parameter
--------------------

Available parameters are as below.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameter

   * - seed
     - Random seed to return popular words.


Response
----------

The response is as below.

::

    {
        "response":{
            "version":12.5,
            "status":0,
            "result":[
                 "\u65E5\u672C\u8A9E",
                 ".pdf",
                 "\u66F4\u65B0\u65E5",
                 "\u691C\u7D22\u7D50\u679C",
                 "google",
                 "pdf",
                 "excel",
                 "solr",
                 "fess",
                 "\u30D5\u30A1\u30A4\u30EB"
            ]
        }
    }

Descriptions for properties are as below.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Properties in Response

   * - response
     - Root element.
   * - version
     - API version.
   * - status
     - Response status. (0: successful, 1: search error, 2 or 3: invalid request parameter, 9: service unavailable, -1: invalid API type)
   * - result
     - Popular words.

