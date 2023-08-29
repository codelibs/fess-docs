=================
Popular Words API
=================

Get List of Popular Words
=========================

By sending a request to ``http://<Server Name>/api/v1/popular-words?seed=123`` to |Fess|, you can receive a list of popular words registered in |Fess| in JSON format. To use the Popular Words API, you need to enable the response of popular words in the general settings of the administration screen.

Request Parameters
------------------

The available request parameters are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameters

   * - seed
     - Seed to retrieve popular words (this value allows you to obtain words in different patterns).
   * - label
     - Filtered label name.
   * - field
     - Field name to generate popular words.


Response
--------

The response will be as follows:

::

    {
      "record_count": 9,
      "data": [
        "python"
      ]
    }

The elements in the response are described as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Response Information

   * - record_count
     - The number of registered popular words.
   * - data
     - Popular words.