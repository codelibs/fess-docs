======================
Range-Specified Search
======================

When a field stores data that supports range specification, such as numeric values or dates and times, you can perform a range-specified search on that field.

Usage
-----

To perform a range-specified search, enter "field_name:[value TO value]" in the search form. Use uppercase half-width ``TO`` to separate the range.

For example, to search for documents in the content_length field with a size ranging from 1 kilobyte to 10 kilobytes, enter the following in the search form:

::

    content_length:[1000 TO 10000]

Square brackets ``[ ]`` are inclusive of the range boundaries (greater than or equal to / less than or equal to), while curly braces ``{ }`` are exclusive of the range boundaries (greater than / less than). You can also combine the two. For example, ``content_length:{1000 TO 10000]`` represents documents greater than 1000 and less than or equal to 10000.

Setting one side to ``*`` represents an open range with only an upper or lower bound specified. ``content_length:[1000 TO *]`` represents 1000 or greater, and ``content_length:[* TO 10000]`` represents 10000 or less.

Range-specified search is available only for fields that are registered as search targets. By default, you can perform range-specified searches on fields such as content_length, last_modified, timestamp, click_count, and favorite_count.

Time Range Search
------------------

To perform a time (date and time) range-specified search, enter "last_modified:[datetime1 TO datetime2]" (datetime1 < datetime2) in the search form. Note that if datetime1 is later than datetime2, this does not result in an error; the search simply returns zero results.

Specify the date and time in ISO 8601 format. The format is ``YYYY-MM-DDThh:mm:ss.SSSZ``, and everything from the time onward can be omitted.

.. list-table::
   :header-rows: 1

   * - Specification
     - Example
   * - Date only
     - 2012-12-02
   * - Date and time (hours, minutes, seconds)
     - 2012-12-02T10:45:23Z
   * - Date and time (including milliseconds)
     - 2012-12-02T10:45:23.235Z

For specifying a date and time, you can use date/time arithmetic based on the current date and time. The available symbols are as follows.

.. list-table::
   :header-rows: 1

   * - Symbol
     - Meaning
   * - ``now``
     - Current date and time
   * - ``y`` / ``M`` / ``w`` / ``d`` / ``h`` / ``m`` / ``s``
     - Year / Month / Week / Day / Hour / Minute / Second
   * - ``+`` / ``-``
     - Addition / Subtraction
   * - ``/``
     - Rounding (rounds to the unit that follows ``/``)

When basing the value on now or a specific date and time, you can append symbols such as +, - (addition, subtraction) or / (rounding). However, when basing the value on a specific date and time instead of now, you need to insert ``||`` between the date/time and the symbol (example: ``2016-01-01||+1M/d``).

``/`` is a symbol that rounds to the unit following ``/``. ``now-1d/d`` represents 00:00 on the previous day, one day subtracted from today's 00:00, regardless of what time it is executed today.

Note that these date/time calculations are evaluated on the search engine (OpenSearch) side and are valid only for fields of a date/time type.

For example, to search for documents in the last_modified field that were updated within the 30 days up to the current date and time (assumed to be February 21, 2016, 20:00), enter the following in the search form:

::

    last_modified:[now-30d TO now]

If the current date and time is February 21, 2016, 20:00 (UTC), the above roughly corresponds to the range ``[2016-01-22T20:00:00Z TO 2016-02-21T20:00:00Z]``.
