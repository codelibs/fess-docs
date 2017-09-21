============
Boost Search
============

Boost Search
============

|Fess| supports Boost search which prioritize specific search words.

Usage
-----

Boost search syntax is word^number, such as Apple^10.
The number is boost-weighted value, and higer value is prior.

To search document which contains more apples than oranges, 

::

    apples^100 oranges

Boost value specifies an integer greater than 1.
