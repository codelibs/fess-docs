===================================================
Conectar sistemas de negocio con la API de búsqueda
===================================================

Introducción
============

Mostrar documentos relacionados en la ficha de cliente del CRM, presentar primero preguntas frecuentes similares en la pantalla de registro de consultas o hacer que también se puedan buscar los informes que genera su propio sistema.
Este tipo de necesidades se cubren llamando a la API de búsqueda de Fess (``/api/v2``) desde el servidor del sistema de negocio.

En este artículo, con Fess 15.9, avanzaremos por los siguientes pasos.

- Llamar con curl a las API de búsqueda, etiquetas, sugerencias y palabras populares, y comprobar la forma de las respuestas
- Crear un token de acceso y controlar con los roles del token qué documentos se devuelven
- Escribir una función que llame a la API de búsqueda desde el lado del servidor del sistema de negocio
- Registrar con ``PUT /api/admin/documents/bulk`` datos que no se pueden rastrear
- Prepararse para errores y límites de tasa

Cómo incorporar un cuadro o una página de búsqueda en un sitio web existente (integración en el navegador, temas, Fess Site Search) se explica en :doc:`guide-03`.
Si todavía no ha iniciado Fess ni ha ejecutado un rastreo, complete primero :doc:`guide-02`.

La arquitectura de este artículo
================================

::

    [Navegador del usuario] --> [Servidor del sistema de negocio] --(con token)--> [Fess /api/v2]
                                       El token solo se guarda aquí

El navegador accede únicamente al sistema de negocio, y quien llama a Fess es el servidor del sistema de negocio.
Guarde el token de acceso, por ejemplo, en una variable de entorno del servidor y no lo entregue nunca al navegador.
Los motivos se explican en "Crear un token de acceso".

Visión general de la API
========================

Las API de búsqueda que ofrece el propio Fess 15.9 se encuentran bajo ``/api/v2``.
Las que usamos en este artículo son las siguientes.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Endpoint
     - Uso
   * - ``GET /api/v2/search``
     - Búsqueda de texto completo. Los resultados están en ``response.data``
   * - ``GET /api/v2/labels``
     - Lista de etiquetas que puede usar quien llama
   * - ``GET /api/v2/suggest-words``
     - Sugerencias para una palabra a medio escribir
   * - ``GET /api/v2/popular-words``
     - Palabras populares
   * - ``GET /api/v2/health``
     - Estado del motor de búsqueda (su uso en la monitorización se explica en :doc:`guide-10`)
   * - ``PUT /api/admin/documents/bulk``
     - Registro masivo de documentos (API de administración)

Todas las respuestas de ``/api/v2`` vienen envueltas en ``{"response": {...}}``, y si ``response.status`` es 0 la llamada ha tenido éxito.
Las claves JSON están en ``snake_case``.

.. note::

   El propio Fess 15.9 no ofrece ``/api/v1``.
   Para que sigan funcionando los clientes existentes que llaman a ``/api/v1``, necesita el plugin ``fess-webapp-v1-api`` (no se incluye en la imagen de Docker).
   Use ``/api/v2`` en cualquier integración nueva.

Primero, probar con curl
========================

Si la búsqueda anónima está permitida ("Requiere inicio de sesión" desactivado en [Sistema] > [General], que es el valor predeterminado), puede llamar a la API sin token.
Los términos de búsqueda que contienen espacios o caracteres no ASCII se codifican para URL y se envían con ``-G --data-urlencode``.
Usamos ``jq`` para que la salida sea más fácil de leer.

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=guía búsqueda" \
        --data-urlencode "num=3" \
      | jq '.response | {status, record_count, page_size, data: [.data[] | {doc_id, title, url_link, content_description}]}'

La respuesta tiene esta forma (de ``data`` solo se muestra el primer elemento; los valores dependen de su entorno).

.. code-block:: json

    {
      "status": 0,
      "record_count": 12,
      "page_size": 3,
      "data": [
        {
          "doc_id": "5d4c0e0e5a7b4b5c9d2f6a1b3c8e7f90",
          "title": "Guía de búsqueda",
          "url_link": "https://fess.codelibs.org/es/stable/user/index.html",
          "content_description": "La <strong>guía</strong> de <strong>búsqueda</strong> de Fess. ..."
        }
      ]
    }

``response`` contiene además ``page_count``, ``next_page``, ``exec_time``, ``query_id``, entre otros.
Cada elemento de ``data`` contiene solo los campos permitidos para las respuestas de la API, como ``title``, ``url``, ``url_link``, ``content_description``, ``last_modified``, ``filetype`` y ``score``.
El texto completo (``content``) y las etiquetas (``label``) no se devuelven de forma predeterminada.
Para devolver más campos, añádalos a ``query.additional.api.response.fields`` en ``fess_config.properties``.
``content_description`` es un extracto en el que los términos de búsqueda están rodeados por etiquetas ``<strong>``; al mostrarlo en pantalla, trátelo como HTML o elimine las etiquetas.

Los parámetros más usados son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parámetro
     - Significado
   * - ``q``
     - Términos de búsqueda. Admite la misma sintaxis que la página de búsqueda (AND, OR, exclusión, búsqueda por campo, etc.)
   * - ``num`` / ``start``
     - Número de resultados por página (10 de forma predeterminada; si supera el límite superior, se ajusta a ese límite) y posición inicial (empieza en 0)
   * - ``sort``
     - Orden. Ejemplo: ``last_modified.desc`` (los actualizados más recientemente primero)
   * - ``fields.label``
     - Filtra por valor de etiqueta. Puede indicarse varias veces

Para los demás parámetros (facetas, idioma, búsqueda geográfica, etc.), consulte `API de búsqueda <https://fess.codelibs.org/es/stable/api/api-search.html>`__.

Las etiquetas, las sugerencias y las palabras populares se llaman de la misma manera.

::

    $ curl -s "http://localhost:8080/api/v2/labels" | jq .response
    $ curl -s -G "http://localhost:8080/api/v2/suggest-words" --data-urlencode "q=fe" | jq .response
    $ curl -s "http://localhost:8080/api/v2/popular-words" | jq .response

Los resultados están, respectivamente, en ``response.labels[]`` (``label`` y ``value``), ``response.suggest_words[]`` (``text`` y ``types``) y ``response.popular_words`` (un array de cadenas).
Por qué las sugerencias y las palabras populares pueden llegar vacías se explica en "Usar etiquetas, sugerencias y palabras populares".

Crear un token de acceso
========================

Las llamadas desde el sistema de negocio usan un token de acceso.
Al token se le asignan "permisos", y los resultados de búsqueda se filtran según esos permisos.

Procedimiento
-------------

1. En la consola de administración, abra [Sistema] > [Token de acceso] y haga clic en [Crear nuevo].
2. En "Nombre", escriba un nombre que indique su uso (por ejemplo, ``crm-search``).
3. En "Permisos", escriba los roles de los documentos que este token puede mostrar, uno por línea. Los formatos son ``{role}nombre_rol``, ``{group}nombre_grupo`` y ``{user}nombre_usuario``.
4. Introduzca "Caduca" con el formato ``2027-03-31T23:59:59``. Si lo deja en blanco, el token no caduca.
5. Deje "Nombre del parámetro" en blanco.
6. Haga clic en [Crear]. De vuelta en la lista, haga clic en el nombre y anote el valor que aparece en "Token" en la pantalla de detalles (60 caracteres alfanuméricos).

Si configura "Nombre del parámetro", quien llama puede añadir permisos mediante ese parámetro de solicitud.
No lo use salvo que controle por completo a quienes llaman.

Cómo enviar el token
--------------------

Envíe el token en la cabecera ``Authorization``.
También se acepta ``Authorization: <token>`` sin ``Bearer``.

::

    $ export FESS_SEARCH_TOKEN=<token anotado>
    $ curl -s -G "http://localhost:8080/api/v2/search" \
        -H "Authorization: Bearer $FESS_SEARCH_TOKEN" \
        --data-urlencode "q=propuesta" | jq '.response.record_count'

Pasar el token como parámetro de consulta está desactivado, porque ``api.access.token.request.parameter`` está vacío de forma predeterminada.
Las URL quedan registradas en los registros de acceso, así que use la cabecera.

Los roles del token determinan los resultados
---------------------------------------------

En una solicitud con token, solo los permisos del token se usan como roles.
El rol de invitado (``{role}guest``), que reciben las llamadas anónimas sin token, no se añade mientras los permisos del token no estén vacíos.

Por otra parte, al crear una nueva configuración de rastreo, el campo de permisos contiene ``{role}guest``, por lo que los documentos públicos habituales llevan ``{role}guest``.
Por eso, con un token cuyo único permiso es ``{group}sales``, los documentos públicos desaparecen de los resultados de búsqueda.
Si quiere devolver tanto los documentos públicos como los destinados al departamento de ventas, ponga en los permisos del token estas dos líneas.

::

    {role}guest
    {group}sales

Una vez configurado, compare ``record_count`` para los mismos términos de búsqueda sin token y con token, y confirme que aumenta o disminuye como esperaba.
El diseño de los permisos del lado de los documentos se trata en :doc:`guide-05`.

Por qué no entregar el token al navegador
-----------------------------------------

- Cualquiera puede leer con las herramientas de desarrollo un token escrito en el JavaScript del navegador. Quien lo lea puede buscar todos los documentos visibles con los permisos del token sin pasar por el sistema de negocio.
- Un token no pertenece a cada usuario, sino que agrupa los permisos indicados al emitirlo. Si lo reparte a los navegadores, desaparecen las diferencias de permisos entre usuarios.
- Aunque "Requiere inicio de sesión" esté activado, ``/search``, ``/documents/all``, ``/documents/export``, ``/suggest-words``, ``/labels`` y ``/popular-words`` responden sin inicio de sesión si se presenta un token válido. Un token filtrado puede usarse en lugar de un inicio de sesión.

Si quiere que el alcance visible dependa del usuario del sistema de negocio, cree un token por alcance y elija en el servidor el adecuado para cada usuario.

Llamar a la API de búsqueda desde el servidor
=============================================

Este es un ejemplo de función en Python para el backend del sistema de negocio.
Usa solo la biblioteca estándar y devuelve los resultados de búsqueda reducidos a los elementos que necesita la pantalla.

.. code-block:: python

    import json
    import os
    import urllib.error
    import urllib.parse
    import urllib.request

    FESS_URL = os.environ.get("FESS_URL", "http://localhost:8080")
    FESS_SEARCH_TOKEN = os.environ["FESS_SEARCH_TOKEN"]


    class FessApiError(Exception):
        def __init__(self, http_status, code, retry_after=None):
            super().__init__(f"Fess API error: {http_status} {code}")
            self.http_status = http_status
            self.code = code
            self.retry_after = retry_after


    def search_documents(query, label=None, num=5):
        params = [("q", query), ("num", str(num))]
        if label:
            params.append(("fields.label", label))
        url = FESS_URL + "/api/v2/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + FESS_SEARCH_TOKEN})
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                body = json.load(res)
        except urllib.error.HTTPError as e:
            try:
                code = json.load(e)["response"]["error"]["code"]
            except (ValueError, KeyError, TypeError):
                code = "unknown"
            raise FessApiError(e.code, code, e.headers.get("Retry-After")) from e
        response = body["response"]
        return {
            "total": response["record_count"],
            "items": [
                {
                    "title": doc.get("title"),
                    "url": doc.get("url_link"),
                    "snippet": doc.get("content_description"),
                    "last_modified": doc.get("last_modified"),
                }
                for doc in response["data"]
            ],
        }

En la ficha de cliente del CRM, pase el nombre del cliente y una etiqueta, como en ``search_documents("Ejemplo S.A.", label="sales_docs")``, y muestre el valor devuelto tal cual en la pantalla.

- El tiempo de espera es algo más largo que el tiempo límite de búsqueda de Fess (``query.timeout``, 10000 milisegundos de forma predeterminada).
- Consulte ``code`` y ``retry_after`` de ``FessApiError`` para decidir el mensaje que verá el usuario y los reintentos (consulte "Gestión de errores").
- ``content_description`` contiene etiquetas ``<strong>``; si su plantilla lo muestra como HTML, permita únicamente la etiqueta ``<strong>``.

Registrar datos de sistemas externos
====================================

Los datos que no se pueden rastrear (informes generados por el sistema de negocio, resúmenes de tickets, etc.) pueden registrarse directamente en el índice con ``PUT /api/admin/documents/bulk`` de la API de administración.

Usar un token aparte para la API de administración
--------------------------------------------------

La API de administración requiere un token cuyos permisos incluyan ``{role}admin-api`` (``api.admin.access.permissions=Radmin-api``).
Este permiso da acceso a todos los endpoints de la API de administración.
No existe un permiso limitado al registro de documentos.
Con este token también se pueden manipular las configuraciones de rastreo, los usuarios e incluso los propios tokens de acceso, así que guárdelo con el mismo cuidado que la contraseña del administrador.

Además, si busca con un token que solo tiene ``{role}admin-api``, su único rol es ``admin-api`` y casi no se devuelven documentos.
Use tokens distintos para buscar y para registrar.
En [Sistema] > [Token de acceso], cree otro token cuyos permisos sean solo la línea ``{role}admin-api`` (por ejemplo, con el nombre ``crm-indexer``) y anote su valor.

::

    $ export FESS_ADMIN_TOKEN=<token de la API de administración anotado>

Registrar
---------

``url`` y ``title`` son obligatorios.
``content`` es el texto del documento y ``label`` es un array de valores de etiqueta.

::

    $ curl -s -X PUT "http://localhost:8080/api/admin/documents/bulk" \
        -H "Authorization: Bearer $FESS_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "documents": [
            {
              "url": "https://crm.example.com/reports/2026-11",
              "title": "Informe mensual de ventas noviembre 2026",
              "content": "Las nuevas oportunidades comerciales de noviembre aumentaron respecto al mes anterior.",
              "label": ["sales_docs"]
            }
          ]
        }' | jq .response

Si tiene éxito, el resultado de cada documento se devuelve en ``items``.
Una creación devuelve ``CREATED`` y la actualización de un documento existente, ``OK``.

.. code-block:: json

    {
      "version": "15.9",
      "status": 0,
      "items": [
        { "result": "CREATED", "id": "9c1e47b2...e04b" }
      ]
    }

``id`` es un valor hash calculado a partir de ``url`` y otros datos (128 dígitos hexadecimales); en el ejemplo anterior se omite la parte central.
El registro está completo cuando una búsqueda de ``q=informe mensual de ventas`` con el token de búsqueda encuentra el documento.

Precauciones al registrar
-------------------------

- Si omite ``role``, se asigna el rol de invitado y cualquiera puede encontrar el documento. Para limitar quién lo ve, ponga en ``role`` un array de valores en formato interno. En el formato interno, ``{role}x`` pasa a ser ``Rx``, ``{group}x`` pasa a ser ``2x`` y ``{user}x`` pasa a ser ``1x`` (por ejemplo, ``"role": ["2sales"]``).
- El ID del documento se genera a partir de ``url`` y ``role`` (y del host virtual). Volver a enviar la misma ``url`` actualiza el documento, pero enviarla con otro ``role`` lo añade como un documento distinto y deja el antiguo en el índice.
- ``items[].id`` de la respuesta es el ID en el índice y es distinto del ``doc_id`` del documento. Para eliminar documentos de uno en uno con ``DELETE /api/admin/searchlist/doc/{id}``, pase el ``doc_id`` de los resultados de búsqueda. Para eliminar en bloque según una condición, use ``DELETE /api/admin/searchlist/query`` (`SearchList API <https://fess.codelibs.org/es/stable/api/admin/api-admin-searchlist.html>`__).
- Si solo fallan algunos documentos, ``status`` pasa a 9 y los elementos fallidos contienen ``message``. Si la propia solicitud no es válida, por ejemplo porque falta ``url`` o ``title`` o un valor tiene un tipo incorrecto, ``status`` pasa a 1 y no se registra nada.

Usar etiquetas, sugerencias y palabras populares
================================================

Crear categorías con etiquetas
------------------------------

Las etiquetas para filtrar con ``fields.label`` se crean en [Rastreador] > [Etiqueta].
"Valor" solo admite caracteres alfanuméricos y guiones bajos (no se pueden usar ``sales-docs`` ni caracteres no ASCII).
Un documento rastreado recibe la etiqueta cuando su URL coincide con las "Rutas incluidas" de la etiqueta (:doc:`guide-04`).
Para los documentos registrados en bloque, envíe ``label`` como en la sección anterior.

``/api/v2/labels`` devuelve solo las etiquetas que pueden usar los roles de quien llama.
Las etiquetas también tienen permisos, de modo que las que no coinciden con los permisos del token no aparecen en la lista.
Construya la lista de categorías del portal a partir de ``label`` (nombre visible) y ``value`` (el valor que se pasa a ``fields.label``) de esta respuesta.

Sugerencias
-----------

``/api/v2/suggest-words`` devuelve candidatos que empiezan por ``q``.
La cantidad se indica con ``num`` (10 de forma predeterminada) y los campos de destino se especifican repitiendo ``fn``.
Los candidatos provienen de las palabras de los documentos rastreados ("Sugerir por documentos" en [Sistema] > [General]), de los términos de búsqueda ("Sugerir por término de búsqueda" en la misma pantalla) y de las palabras de sugerencia registradas por el administrador.
Las palabras de los documentos no aparecen como candidatos hasta que se ejecuta el trabajo "Suggest Indexer" del programador (una vez al día de forma predeterminada).
Los candidatos también se filtran según los roles de quien llama.

Palabras populares
------------------

``/api/v2/popular-words`` devuelve, de entre los términos recopilados del registro de búsquedas, los que se han buscado con más frecuencia.
Si se devuelve un array vacío, compruebe los siguientes puntos.

- Si "Respuesta de palabras populares" en [Sistema] > [General] (``web.api.popularword``, activado de forma predeterminada) está desactivado, la llamada devuelve ``invalid_request`` (HTTP 400).
- "Sugerir por término de búsqueda" debe estar activado. Los términos de búsqueda solo se recopilan mientras este ajuste está activado.
- El mismo término debe haberse buscado 10 veces o más (``suggest.popular.word.query.freq=10``). Las búsquedas repetidas desde la misma sesión dentro de un minuto cuentan como una sola. Justo después de la instalación, lo normal es que esté vacío.
- Solo se cuentan las búsquedas realizadas únicamente con el rol de invitado (``suggest.search.log.permissions={user}guest,{role}guest``). No se cuentan las búsquedas con tokens que tienen, por ejemplo, ``{group}sales`` ni las de usuarios que han iniciado sesión.
- Las palabras populares también se filtran según los roles de quien llama. Los términos contabilizados solo llevan el rol de invitado, así que un token cuyos permisos no incluyen ``{role}guest`` siempre obtiene un resultado vacío.
- Los resultados se almacenan en caché, por lo que no cambian de inmediato aunque aumenten las búsquedas.

Si cambia ``seed``, se devuelve otra combinación de entre los candidatos.

Gestión de errores
==================

En caso de error, ``/api/v2`` devuelve un estado HTTP y ``response.error.code``.

::

    {"response": {"status": 1, "error": {"code": "invalid_request", "message": "..."}}}

El sistema que se integra debe decidir de antemano cómo tratar los siguientes casos.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - HTTP
     - ``error.code``
     - Causa y acción
   * - 400
     - ``invalid_request``
     - ``num`` es 0 o menor, hay un error de sintaxis en los términos de búsqueda, ``q`` supera ``api.param.max.length`` (1000 caracteres de forma predeterminada), etc. No reintente; revise la entrada
   * - 401
     - ``auth_required``
     - Token no registrado o caducado, o falta de token con "Requiere inicio de sesión" activado. Un token no válido no vuelve al acceso anónimo, sino que produce un 401. Vuelva a crear el token
   * - 503
     - ``service_unavailable``
     - El motor de búsqueda no pudo con la carga y rechazó la búsqueda. Se incluye ``Retry-After: 5``, así que puede reintentar tras esperar 5 segundos
   * - 500
     - ``internal_error``
     - Error interno de Fess. Revise ``fess.log`` en [Información del sistema] > [Archivo de registro]

En cuanto a los límites de tasa, los endpoints de inicio de sesión, cambio de contraseña, chat y exportación tienen cada uno su propio límite; si se supera, se devuelven 429 ``rate_limited`` y ``Retry-After``.
El límite de solicitudes para todo el servidor (``rate.limit.enabled``) está desactivado de forma predeterminada.
Si lo activa, el cuerpo de la respuesta 429 al superarlo es ``{"error":"rate_limit_exceeded", ...}``, no la forma ``response`` mostrada arriba.
Cuando llame desde el servidor del sistema de negocio, tenga en cuenta que todas las búsquedas llegan desde la misma dirección IP.
Para más detalles, consulte `Configuración de límite de tasa <https://fess.codelibs.org/es/stable/config/rate-limiting.html>`__.

La API de administración (``/api/admin/*``) usa una forma de error diferente.
Si no hay token o el token no tiene ``{role}admin-api``, la respuesta es HTTP 401 con ``response.status`` igual a 3, y el motivo figura en ``response.message``.

Llamar directamente desde el navegador (CORS)
=============================================

CORS no afecta a las llamadas entre servidores.
Solo cuando el JavaScript del navegador llama directamente a Fess en otro origen se aplican ``api.cors.allow.origin`` (``*`` de forma predeterminada), ``api.cors.allow.methods``, ``api.cors.allow.headers`` (incluye ``Authorization`` de forma predeterminada), ``api.cors.allow.credentials`` (``true`` de forma predeterminada) y ``api.cors.max.age`` (``3600`` segundos de forma predeterminada) de ``fess_config.properties``.

Cuando ``api.cors.allow.origin`` es ``*``, no se permiten solicitudes con credenciales como cookies.
Para que el navegador busque con los permisos del usuario que ha iniciado sesión, enumere los orígenes, como ``https://portal.example.com`` (separados por comas).
En Docker también puede indicar ``-Dfess.config.api.cors.allow.origin=https://portal.example.com`` en ``FESS_JAVA_OPTS``.
Reinicie Fess después del cambio.
Para la integración en el navegador, consulte :doc:`guide-03`.

Artículos recomendados
======================

- Para incorporar un cuadro o una página de búsqueda en un sitio existente: :doc:`guide-03`
- Para diseñar qué documentos ve cada token o usuario: :doc:`guide-05`
- Para usar la API en comprobaciones de estado y monitorización: :doc:`guide-10`
- Para gestionar la configuración como código con la API de administración y fessctl: :doc:`guide-16`
- Para proteger la plataforma de búsqueda, incluida la operación de SSO y tokens de acceso: :doc:`guide-15`

Referencias
===========

- `Descripción general de la API <https://fess.codelibs.org/es/stable/api/api-overview.html>`__
- `API de búsqueda <https://fess.codelibs.org/es/stable/api/api-search.html>`__
- `API de etiquetas <https://fess.codelibs.org/es/stable/api/api-label.html>`__
- `API de sugerencias <https://fess.codelibs.org/es/stable/api/api-suggest.html>`__
- `API de palabras populares <https://fess.codelibs.org/es/stable/api/api-popularword.html>`__
- `API de Documents <https://fess.codelibs.org/es/stable/api/admin/api-admin-documents.html>`__
- `Visión General de Admin API <https://fess.codelibs.org/es/stable/api/admin/api-admin-overview.html>`__
- `Token de Acceso <https://fess.codelibs.org/es/stable/admin/accesstoken-guide.html>`__
