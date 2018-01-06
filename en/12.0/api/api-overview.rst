==================
Overview
==================


Provided API in |Fess|
==================

This document describes API provided by |Fess|.
Using |Fess| API, you can construct a search system with your existing web applications.

API Type
==================

.. TODO: favorite, favorites

|Fess| provides several search APIs.
Using ``type`` request parameter, API is specified, such as ``http://<Server Name>/json/?type=popularword``.
Available ``type`` is as below.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: API Type

   * - search
     - Search results are returned. ``search`` is a default type.
   * - popularword
     - Poplular words are returned.
   * - label
     - Registered labels are returned.
   * - ping
     - |Fess| server state is returned.

