================
Descripción de la API
================


API proporcionadas por |Fess|
==============================

Este documento describe las API proporcionadas por |Fess|.
Utilizando las API, puede usar |Fess| como servidor de búsqueda en sistemas web existentes y otros.

URL base
========

Los endpoints de la API de |Fess| se proporcionan con la siguiente URL base:

::

    http://<Server Name>/api/v1/

Por ejemplo, si se ejecuta en un entorno local, sería:

::

    http://localhost:8080/api/v1/

Autenticación
=============

En la versión actual, no se requiere autenticación para usar la API.
Sin embargo, es necesario habilitar la API en las diversas configuraciones de la consola de administración.

Método HTTP
===========

Todos los endpoints de la API se acceden mediante el método **GET**.

Formato de respuesta
====================

Todas las respuestas de la API se devuelven en **formato JSON** (excepto la API compatible con GSA).
El ``Content-Type`` de la respuesta es ``application/json``.

Manejo de errores
=================

Si una solicitud de API falla, se devuelve información de error junto con el código de estado HTTP apropiado.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Códigos de estado HTTP

   * - 200
     - La solicitud se procesó correctamente.
   * - 400
     - Los parámetros de la solicitud son incorrectos.
   * - 404
     - No se encontró el recurso solicitado.
   * - 500
     - Se produjo un error interno del servidor.

Tabla: Códigos de estado HTTP

Tipos de API
============

|Fess| proporciona las siguientes API:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - API para obtener resultados de búsqueda.
   * - popularword
     - API para obtener palabras populares.
   * - label
     - API para obtener la lista de etiquetas creadas.
   * - health
     - API para obtener el estado del servidor.
   * - suggest
     - API para obtener palabras sugeridas.

Tabla: Tipos de API
