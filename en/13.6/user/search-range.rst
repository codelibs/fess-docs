============
Range Search
============

Range Search
============

|Fess| supports Range search that specify values between the lower and upper bound by date type or numeric type.

Usage
-----

The syntax of Range search is "fieldname:[lower TO upper]"

For example, type to search document contentLength field against 1 k to
10 k bytes is shown below the search form.

To search documents of which size is from 10 bytes to 100 bytes, the query is below.

::

    content_length:[10 TO 100]

Date range search is also supported. 
The syntax is "last_modified:[fromdate TO todate].
The date format supports ISO 8601 or Date Math syntax.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - ISO8601
     - YYYY-MM-DDThh:mm:ss.sssZ(ex. 2013.68-02T10:45:23.5Z)
   * - Date Math
     - now, y(Year), M(Month), d(Day), h(hour), m(minute)

For example, if you look for documents updated from 30 days prior to now(2/21/2012), it's as below.

::

    last_modified:[now/d-30d TO now]

or

::

    last_modified:[2012-11-23T00:00:00Z TO 2012-12-21T20:00:00Z]

