========================================
Obtención Masiva de Resultados de Búsqueda
========================================

Descripción General
===================

En las búsquedas normales de |Fess|, solo se muestra un número limitado de resultados de búsqueda mediante la función de paginación.
Si desea obtener todos los resultados de búsqueda de una sola vez, utilice la función de Búsqueda Scroll (Scroll Search).

Esta función es útil cuando necesita procesar todos los resultados de búsqueda, como en exportaciones masivas de datos, copias de seguridad y análisis de grandes volúmenes de datos.

Casos de Uso
============

La búsqueda scroll es adecuada para los siguientes propósitos:

- Exportación completa de resultados de búsqueda
- Obtención de grandes volúmenes de datos para análisis
- Obtención de datos en procesos por lotes
- Sincronización de datos con sistemas externos
- Recopilación de datos para generación de informes

.. warning::
   La búsqueda scroll devuelve grandes volúmenes de datos, por lo que consume más recursos del servidor en comparación con las búsquedas normales. Habilítela solo cuando sea necesario.

Método de Configuración
=======================

Habilitación de la Búsqueda Scroll
----------------------------------

Por defecto, la búsqueda scroll está deshabilitada por motivos de seguridad y rendimiento.
Para habilitarla, modifique la siguiente configuración en ``fess_config.properties`` o ``/etc/fess/fess_config.properties``.

::

    api.search.scroll=true

.. note::
   Después de cambiar la configuración, es necesario reiniciar |Fess|.

Configuración de Campos de Respuesta
-------------------------------------

Puede personalizar los campos que se incluyen en la respuesta de los resultados de búsqueda.
Por defecto, solo se devuelven campos básicos, pero puede especificar campos adicionales.

::

    query.additional.scroll.response.fields=content,mimetype,filename,created,last_modified

Al especificar múltiples campos, enumérelos separados por comas.

Configuración del Tiempo de Espera del Scroll
----------------------------------------------

Puede configurar el período de validez del contexto de scroll.
El valor predeterminado es 1 minuto.

::

    api.search.scroll.timeout=1m

Unidades:
- ``s``: segundos
- ``m``: minutos
- ``h``: horas

Método de Uso
=============

Uso Básico
----------

Para acceder a la búsqueda scroll, utilice la siguiente URL.

::

    http://localhost:8080/json/scroll?q=palabra_clave_búsqueda

Los resultados de búsqueda se devuelven en formato NDJSON (Newline Delimited JSON).
Cada línea representa un documento en formato JSON.

**Ejemplo:**

::

    curl "http://localhost:8080/json/scroll?q=Fess"

Parámetros de Solicitud
-----------------------

En la búsqueda scroll, puede utilizar los siguientes parámetros.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nombre del Parámetro
     - Descripción
   * - ``q``
     - Consulta de búsqueda (obligatorio)
   * - ``size``
     - Número de registros a obtener en cada scroll (predeterminado: 100)
   * - ``scroll``
     - Tiempo de validez del contexto de scroll (predeterminado: 1m)
   * - ``fields.label``
     - Filtrado por etiqueta

Especificación de Consulta de Búsqueda
---------------------------------------

Puede especificar consultas de búsqueda de la misma manera que en las búsquedas normales.

**Ejemplo: Búsqueda por palabra clave**

::

    curl "http://localhost:8080/json/scroll?q=motor_búsqueda"

**Ejemplo: Búsqueda con campo especificado**

::

    curl "http://localhost:8080/json/scroll?q=title:Fess"

**Ejemplo: Obtención completa (sin condiciones de búsqueda)**

::

    curl "http://localhost:8080/json/scroll?q=*:*"

Especificación del Número de Registros a Obtener
-------------------------------------------------

Puede cambiar el número de registros a obtener en cada scroll.

::

    curl "http://localhost:8080/json/scroll?q=Fess&size=500"

.. note::
   Si el parámetro ``size`` es demasiado grande, aumentará el uso de memoria.
   Normalmente se recomienda configurarlo en el rango de 100 a 1000.

Filtrado por Etiqueta
---------------------

Puede obtener solo los documentos que pertenecen a una etiqueta específica.

::

    curl "http://localhost:8080/json/scroll?q=*:*&fields.label=public"

Cuando se Requiere Autenticación
---------------------------------

Si utiliza búsqueda basada en roles, necesita incluir información de autenticación.

::

    curl -u usuario:contraseña "http://localhost:8080/json/scroll?q=Fess"

O, utilizando un token de API:

::

    curl -H "Authorization: Bearer SU_TOKEN_API" \
         "http://localhost:8080/json/scroll?q=Fess"

Formato de Respuesta
====================

Formato NDJSON
--------------

La respuesta de la búsqueda scroll se devuelve en formato NDJSON (Newline Delimited JSON).
Cada línea representa un documento.

**Ejemplo:**

::

    {"url":"http://example.com/page1","title":"Page 1","content":"..."}
    {"url":"http://example.com/page2","title":"Page 2","content":"..."}
    {"url":"http://example.com/page3","title":"Page 3","content":"..."}

Campos de Respuesta
-------------------

Principales campos incluidos por defecto:

- ``url``: URL del documento
- ``title``: Título
- ``content``: Contenido (extracto)
- ``score``: Puntuación de búsqueda
- ``boost``: Valor de boost
- ``created``: Fecha de creación
- ``last_modified``: Fecha de última modificación

Ejemplos de Procesamiento de Datos
===================================

Ejemplo de Procesamiento en Python
-----------------------------------

.. code-block:: python

    import requests
    import json

    # Ejecutar búsqueda scroll
    url = "http://localhost:8080/json/scroll"
    params = {
        "q": "Fess",
        "size": 100
    }

    response = requests.get(url, params=params, stream=True)

    # Procesar respuesta NDJSON línea por línea
    for line in response.iter_lines():
        if line:
            doc = json.loads(line)
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

Guardar en Archivo
------------------

Ejemplo de cómo guardar los resultados de búsqueda en un archivo:

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=*:*" > all_documents.ndjson

Conversión a CSV
----------------

Ejemplo de conversión a CSV utilizando el comando jq:

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=Fess" | \
        jq -r '[.url, .title, .score] | @csv' > results.csv

Análisis de Datos
-----------------

Ejemplo de análisis de datos obtenidos:

.. code-block:: python

    import json
    import pandas as pd
    from collections import Counter

    # Leer archivo NDJSON
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            documents.append(json.loads(line))

    # Convertir a DataFrame
    df = pd.DataFrame(documents)

    # Estadísticas básicas
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # Análisis de dominios de URL
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

Rendimiento y Mejores Prácticas
================================

Uso Eficiente
-------------

1. **Configuración Apropiada del Parámetro size**

   - Si es demasiado pequeño, aumenta la sobrecarga de comunicación
   - Si es demasiado grande, aumenta el uso de memoria
   - Recomendado: 100-1000

2. **Optimización de Condiciones de Búsqueda**

   - Especifique condiciones de búsqueda para obtener solo los documentos necesarios
   - Ejecute la obtención completa solo cuando sea realmente necesario

3. **Uso en Horarios de Baja Demanda**

   - Ejecute la obtención de grandes volúmenes de datos durante períodos de baja carga del sistema

4. **Uso en Procesos por Lotes**

   - Ejecute sincronizaciones de datos periódicas como trabajos por lotes

Optimización del Uso de Memoria
--------------------------------

Al procesar grandes volúmenes de datos, utilice procesamiento en streaming para reducir el uso de memoria.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/json/scroll"
    params = {"q": "*:*", "size": 100}

    # Procesar en streaming
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                doc = json.loads(line)
                # Procesar documento
                process_document(doc)

Consideraciones de Seguridad
=============================

Restricciones de Acceso
-----------------------

Dado que la búsqueda scroll devuelve grandes volúmenes de datos, configure restricciones de acceso apropiadas.

1. **Restricción por Dirección IP**

   Permitir acceso solo desde direcciones IP específicas

2. **Autenticación de API**

   Utilizar tokens de API o autenticación básica

3. **Restricción Basada en Roles**

   Permitir acceso solo a usuarios con roles específicos

Limitación de Tasa
------------------

Se recomienda configurar limitación de tasa en el proxy inverso para evitar accesos excesivos.

Solución de Problemas
=====================

La Búsqueda Scroll No Está Disponible
--------------------------------------

1. Verifique que ``api.search.scroll`` esté configurado como ``true``.
2. Verifique que haya reiniciado |Fess|.
3. Revise los registros de errores.

Se Produce un Error de Tiempo de Espera
----------------------------------------

1. Aumente el valor de ``api.search.scroll.timeout``.
2. Reduzca el parámetro ``size`` para distribuir el procesamiento.
3. Refine las condiciones de búsqueda para reducir la cantidad de datos obtenidos.

Error de Memoria Insuficiente
------------------------------

1. Reduzca el parámetro ``size``.
2. Aumente el tamaño de memoria heap de |Fess|.
3. Verifique el tamaño de memoria heap de OpenSearch.

La Respuesta Está Vacía
------------------------

1. Verifique que la consulta de búsqueda sea correcta.
2. Verifique que las etiquetas o condiciones de filtro especificadas sean correctas.
3. Verifique la configuración de permisos de búsqueda basada en roles.

Información de Referencia
==========================

- :doc:`search` - Detalles de la función de búsqueda
- :doc:`search-config` - Configuración relacionada con la búsqueda
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
