==========================
API de SystemInfo
==========================

Visión General
==============

La API de SystemInfo es para obtener información del sistema de |Fess|.
Permite verificar las variables de entorno, las propiedades del sistema de Java, las propiedades de configuración de |Fess| y la información para reportes de errores.

URL Base
========

::

    /api/admin/systeminfo

El acceso a esta API requiere un token de acceso con el permiso ``Radmin-api``.
Para más detalles sobre la autenticación, consulte :doc:`api-admin-overview`.

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /
     - Obtener información del sistema

Obtener Información del Sistema
===============================

Solicitud
---------

::

    GET /api/admin/systeminfo

Este endpoint no acepta parámetros de consulta.

Respuesta
---------

La respuesta incluye ``version``, que indica la versión del producto, ``status``, que indica el resultado del procesamiento, y los siguientes cuatro grupos de propiedades. Cada grupo de propiedades es un arreglo de objetos que tienen ``label`` y ``value``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"label": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"label": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"label": "java.version", "value": "21.0.1"},
          {"label": "java.vendor", "value": "Oracle Corporation"},
          {"label": "os.name", "value": "Linux"},
          {"label": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"label": "crawler.document.max.site.length", "value": "100"},
          {"label": "indexer.thread.dump.enabled", "value": "true"},
          {"label": "app.cipher.key", "value": "XXXXXXXX"}
        ],
        "bugReportProps": [
          {"label": "os.name", "value": "Linux"},
          {"label": "java.vm.version", "value": "21.0.1+12"}
        ]
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``version``
     - Versión del producto |Fess| (ejemplo: ``15.7.0``).
   * - ``status``
     - Código que indica el resultado del procesamiento. ``0`` significa finalización exitosa.
   * - ``envProps``
     - Lista de variables de entorno (arreglo de ``label`` / ``value``). Se devuelven los valores obtenidos mediante ``System.getenv()`` tal como están.
   * - ``systemProps``
     - Lista de propiedades del sistema de Java (arreglo de ``label`` / ``value``). Se devuelven los valores obtenidos mediante ``System.getProperties()`` tal como están.
   * - ``fessProps``
     - Lista de propiedades de configuración de |Fess| (arreglo de ``label`` / ``value``). Incluye los valores de configuración de ``fess_config.properties`` y las propiedades del sistema establecidas desde la pantalla de administración. Los elementos sensibles son enmascarados (véase la nota a continuación).
   * - ``bugReportProps``
     - Lista de información recopilada para reportes de errores (arreglo de ``label`` / ``value``). Incluye las principales propiedades del sistema relacionadas con el SO y el entorno de ejecución de Java (``os.name``, ``os.version``, ``java.vm.version``, etc.) y los valores de propiedades del sistema de |Fess|.

.. note::

   En ``fessProps``, los siguientes valores de configuración sensibles son enmascarados y se devuelven como ``XXXXXXXX``:
   ``http.proxy.password``, ``ldap.admin.security.credentials``, ``spnego.preauth.password``,
   ``app.cipher.key``, ``oic.client.id``, ``oic.client.secret``.

.. warning::

   ``envProps`` (variables de entorno) y ``systemProps`` (propiedades del sistema de Java) no son enmascarados:
   los valores configurados se devuelven tal como están. Si las variables de entorno o las propiedades del sistema
   contienen información confidencial como credenciales, esos valores aparecerán en la respuesta.

Ejemplos de Uso
===============

Obtener Información del Sistema
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraer una Propiedad del Sistema Específica
--------------------------------------------

.. code-block:: bash

    # Extraer solo el valor de java.version
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.systemProps[] | select(.label == "java.version") | .value'

Mostrar la Lista de Variables de Entorno
----------------------------------------

.. code-block:: bash

    # Mostrar las variables de entorno en formato label=value
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.label)=\(.value)"'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-stats` - API de estadísticas
- :doc:`api-admin-general` - API de configuración general
- :doc:`../../admin/systeminfo-guide` - Guía de información del sistema
