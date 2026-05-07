====================
Range-Specified Search
====================

When data that supports range specification, such as numeric values, is stored in a field, you can perform range-specified searches on that field.

Usage
-----

To perform a range-specified search, enter "field_name:[value TO value]" in the search form.

For example, to search for documents in the content_length field ranging from 1 kilobyte to 10 kilobytes, enter the following in the search form:

::

    content_length:[1000 TO 10000]

To perform a time range-specified search, enter "last_modified:[datetime1 TO datetime2]" (datetime1 < datetime2) in the search form.

Date and time are based on ISO 8601.

.. list-table::

   * - Date and time with fractional seconds
     - When based on current date and time
   * - YYYY-MM-DDThh:mm:sssZ (Example: 2012-12-02T10:45:235Z)
     - now (current date and time), y (year), M (month), w (week), d (day), h (hour), m (minute), s (second)

When based on now or a specific time, you can add symbols such as +, - (addition, subtraction) and / (rounding). However, when based on a specific time, you need to insert || between the time and the symbol.

/ is a symbol that rounds to the unit following /. now-1d/d represents the previous day at 00:00, which is 1 day subtracted from today at 00:00, regardless of what time it is executed today.

For example, to search for documents updated within the last 30 days from February 21, 2016 at 20:00 (current date and time) in the last_modified field, enter the following in the search form:

::

    last_modified:[now-30d TO now](=[2016-01-23T00:00:000Z+TO+2016-02-21T20:00:000Z(current date and time)])
