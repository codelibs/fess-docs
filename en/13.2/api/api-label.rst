==================
Label API
==================

Label API
============

Label API returns registered labels as JSON format.
URL for Label API is ``http://<Server Name>/json/?type=label``.


Request Parameter
--------------------

No request parameter exists.


Response
----------

The response is as below.

::

    {
        "response":{
            "version":13.2,
            "status":0,
            "record_count":3,
            "result":[
                {"label":"label1", "value":"label1"},
                {"label":"label2", "value":"label2"},
                {"label":"label3", "value":"label3"}
            ]
        }
    }

Descriptions for properties are as below.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Properties in Response

   * - response
     - Root element
   * - version
     - API Version.
   * - status
     - Response status. (0: successful, 1: search error, 2 or 3: invalid request parameter, 9: service unavailable, -1: invalid API type)
   * - record_count
     - The number of labels.
   * - result
     - Result element.
   * - label
     - Label name.
   * - value
     - Label value.

