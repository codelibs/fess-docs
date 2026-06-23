==========================
API de SystemInfo
==========================

Vision General
==============

La API de SystemInfo es para obtener informacion del sistema de |Fess|.
Permite verificar las variables de entorno, las propiedades del sistema de Java, las propiedades de configuracion de |Fess| y la informacion para reportes de errores.

URL Base
========

::

    /api/admin/systeminfo

El acceso a esta API requiere un token de acceso con el permiso ``Radmin-api``.
Para mas detalles sobre la autenticacion, consulte :doc:`api-admin-overview`.

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
     - Obtener informacion del sistema

Obtener Informacion del Sistema
===============================

Solicitud
---------

::

    GET /api/admin/systeminfo

Este endpoint no acepta parametros de consulta.

Respuesta
---------

La respuesta incluye ``version``, que indica la version del producto, ``status``, que indica el resultado del procesamiento, y los siguientes cuatro grupos de propiedades. Cada grupo de propiedades es un arreglo de objetos que tienen ``label`` y ``value``.

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
     - Descripcion
   * - ``version``
     - Version del producto |Fess| (ejemplo: ``15.7.0``).
   * - ``status``
     - Codigo que indica el resultado del procesamiento. ``0`` significa finalizacion exitosa.
   * - ``envProps``
     - Lista de variables de entorno (arreglo de ``label`` / ``value``). Se devuelven los valores obtenidos mediante ``System.getenv()`` tal como estan.
   * - ``systemProps``
     - Lista de propiedades del sistema de Java (arreglo de ``label`` / ``value``). Se devuelven los valores obtenidos mediante ``System.getProperties()`` tal como estan.
   * - ``fessProps``
     - Lista de propiedades de configuracion de |Fess| (arreglo de ``label`` / ``value``). Incluye los valores de configuracion de ``fess_config.properties`` y las propiedades del sistema establecidas desde la pantalla de administracion. Los elementos sensibles son enmascarados (vease la nota a continuacion).
   * - ``bugReportProps``
     - Lista de informacion recopilada para reportes de errores (arreglo de ``label`` / ``value``). Incluye las principales propiedades del sistema relacionadas con el SO y el entorno de ejecucion de Java (``os.name``, ``os.version``, ``java.vm.version``, etc.) y los valores de propiedades del sistema de |Fess|.

.. note::

   En ``fessProps``, los siguientes valores de configuracion sensibles son enmascarados y se devuelven como ``XXXXXXXX``:
   ``http.proxy.password``, ``ldap.admin.security.credentials``, ``spnego.preauth.password``,
   ``app.cipher.key``, ``oic.client.id``, ``oic.client.secret``.

.. warning::

   ``envProps`` (variables de entorno) y ``systemProps`` (propiedades del sistema de Java) no son enmascarados:
   los valores configurados se devuelven tal como estan. Si las variables de entorno o las propiedades del sistema
   contienen informacion confidencial como credenciales, esos valores apareceran en la respuesta.

Ejemplos de Uso
===============

Obtener Informacion del Sistema
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraer una Propiedad del Sistema Especifica
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

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-stats` - API de estadisticas
- :doc:`api-admin-general` - API de configuracion general
- :doc:`../../admin/systeminfo-guide` - Guia de informacion del sistema
