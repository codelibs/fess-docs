==========================
API de General
==========================

Vision General
==============

La API de General es para gestionar la configuracion general de |Fess|.
Puede obtener y actualizar configuraciones relacionadas con todo el sistema.

URL Base
========

::

    /api/admin/general

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /
     - Obtener configuracion general
   * - PUT
     - /
     - Actualizar configuracion general

Obtener Configuracion General
=============================

Solicitud
---------

::

    GET /api/admin/general

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "crawlerDocumentMaxSize": "10485760",
          "crawlerDocumentMaxSiteLength": "50",
          "crawlerDocumentMaxFetcherSize": "3",
          "crawlerDocumentCrawlerThreadCount": "10",
          "crawlerDocumentMaxDepth": "-1",
          "crawlerDocumentMaxAccessCount": "100",
          "indexerThreadDumpEnabled": "true",
          "indexerUnprocessedDocumentSize": "1000",
          "indexerClickCountEnabled": "true",
          "indexerFavoriteCountEnabled": "true",
          "indexerWebfsMaxContentLength": "10485760",
          "indexerWebfsContentEncoding": "UTF-8",
          "queryReplaceTermWithPrefixQuery": "false",
          "queryMaxSearchResultOffset": "100000",
          "queryMaxPageSize": "1000",
          "queryDefaultPageSize": "20",
          "queryAdditionalDefaultQuery": "",
          "queryGeoEnabled": "false",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "suggestBadWord": "true",
          "suggestPopularWordSeedLength": "1",
          "suggestPopularWordTags": "user",
          "suggestPopularWordFields": "tags",
          "suggestPopularWordExcludeWordFields": "",
          "ldapInitialContextFactory": "com.sun.jndi.ldap.LdapCtxFactory",
          "ldapSecurityAuthentication": "simple",
          "ldapProviderUrl": "ldap://localhost:389",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapBindDn": "",
          "ldapBindPassword": "",
          "notificationLogin": "true",
          "notificationSearchTop": "true"
        }
      }
    }

Actualizar Configuracion General
================================

Solicitud
---------

::

    PUT /api/admin/general
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "crawlerDocumentMaxSize": "20971520",
      "crawlerDocumentMaxSiteLength": "100",
      "crawlerDocumentCrawlerThreadCount": "20",
      "queryMaxPageSize": "500",
      "queryDefaultPageSize": "50",
      "suggestSearchLog": "true",
      "suggestDocuments": "true",
      "suggestBadWord": "true",
      "notificationLogin": "false",
      "notificationSearchTop": "false"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Descripcion
   * - ``crawlerDocumentMaxSize``
     - Tamano maximo de documento a rastrear (bytes)
   * - ``crawlerDocumentMaxSiteLength``
     - Longitud maxima del sitio a rastrear
   * - ``crawlerDocumentMaxFetcherSize``
     - Tamano maximo del fetcher
   * - ``crawlerDocumentCrawlerThreadCount``
     - Numero de hilos del rastreador
   * - ``crawlerDocumentMaxDepth``
     - Profundidad maxima de rastreo (-1=ilimitado)
   * - ``crawlerDocumentMaxAccessCount``
     - Numero maximo de accesos
   * - ``indexerThreadDumpEnabled``
     - Habilitar volcado de hilos
   * - ``indexerUnprocessedDocumentSize``
     - Numero de documentos no procesados
   * - ``indexerClickCountEnabled``
     - Habilitar conteo de clics
   * - ``indexerFavoriteCountEnabled``
     - Habilitar conteo de favoritos
   * - ``queryReplaceTermWithPrefixQuery``
     - Conversion a consulta de prefijo
   * - ``queryMaxSearchResultOffset``
     - Desplazamiento maximo de resultados de busqueda
   * - ``queryMaxPageSize``
     - Numero maximo de elementos por pagina
   * - ``queryDefaultPageSize``
     - Numero predeterminado de elementos por pagina
   * - ``queryAdditionalDefaultQuery``
     - Consulta predeterminada adicional
   * - ``suggestSearchLog``
     - Habilitar sugerencias desde registro de busqueda
   * - ``suggestDocuments``
     - Habilitar sugerencias desde documentos
   * - ``suggestBadWord``
     - Habilitar filtro de palabras prohibidas
   * - ``ldapProviderUrl``
     - URL de conexion LDAP
   * - ``ldapBaseDn``
     - DN base de LDAP
   * - ``notificationLogin``
     - Notificacion de inicio de sesion
   * - ``notificationSearchTop``
     - Notificacion de busqueda principal

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Ejemplos de Uso
===============

Actualizar Configuracion del Rastreador
---------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "crawlerDocumentMaxSize": "52428800",
           "crawlerDocumentCrawlerThreadCount": "15",
           "crawlerDocumentMaxAccessCount": "1000"
         }'

Actualizar Configuracion de Busqueda
------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "queryMaxPageSize": "1000",
           "queryDefaultPageSize": "50",
           "queryMaxSearchResultOffset": "50000"
         }'

Actualizar Configuracion de Sugerencias
---------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true",
           "suggestBadWord": "true"
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-systeminfo` - API de informacion del sistema
- :doc:`../../admin/general-guide` - Guia de configuracion general
