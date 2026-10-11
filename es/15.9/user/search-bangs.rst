=========================================
Búsqueda con bangs (buscar en otro sitio)
=========================================

Un bang envía una búsqueda a otro sitio en lugar de buscar en |Fess|. Funciona como los bangs de DuckDuckGo: añada ``!`` y una palabra clave corta a la consulta, y |Fess| envía el resto de la consulta al sitio que representa esa palabra clave.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Consulta
     - Destino
   * - ``airplane !g``
     - Google, buscando ``airplane``
   * - ``!w Ohm's law``
     - Wikipedia, buscando ``Ohm's law``
   * - ``!g``
     - La página de inicio de Google
   * - ``airplane !unknown``
     - |Fess|, como una búsqueda normal (``!`` significa NOT, véase :doc:`search-not`)

Los bangs los proporciona el plugin ``fess-webapp-bangs``, que requiere |Fess| 15.9 o posterior. Instálelo desde [Sistema > Plugin] en la consola de administración o con ``bin/fess-setup install plugin fess-webapp-bangs`` (véase :doc:`../admin/plugin-guide`) y reinicie |Fess|.

Cómo se reconoce un bang
========================

- Un bang es ``!`` seguido de una palabra clave, escrito como una palabra independiente. La palabra clave no distingue mayúsculas de minúsculas.
- El bang se elimina de la consulta y el resto de la consulta se envía a la URL del bang.
- Si una consulta contiene varios bangs definidos, solo cuenta el primero.
- Una palabra clave que no está definida no es un bang. ``!unknown`` se busca como de costumbre y excluye la palabra ``unknown``.
- ``-g`` y ``NOT g`` siguen excluyendo la palabra ``g``. Solo ``!g`` es un bang.

La página de búsqueda y ``/api/v2/search`` siguen la redirección: la API devuelve ``redirect_url`` (véase :doc:`../api/api-search`) y el tema ``bootstrap`` incluido con |Fess| navega a esa URL. Otros temas necesitan el mismo tratamiento.

Los llamadores que no pueden redirigir, como el chat, MCP, las API JSON v1 y clásica y la búsqueda de la consola de administración, no envían la búsqueda a otro sitio. Eliminan el bang y buscan el resto de la consulta.

Definir bangs
=============

Los bangs se definen con la propiedad del sistema ``bangs.definitions``. Establézcala en ``app/WEB-INF/conf/system.properties`` o pásela como ``-Dfess.system.bangs.definitions=...``. Un cambio en ``system.properties`` se aplica sin reiniciar |Fess|.

El valor es una lista de entradas ``palabra_clave=URL`` separadas por espacios en blanco. En la URL, ``{query}`` se sustituye por el resto de la consulta codificado como URL:

::

    bangs.definitions=g=https://www.google.com/search?q={query} w=https://en.wikipedia.org/wiki/Special:Search?search={query}

- Una palabra clave no puede contener espacios en blanco, ``(``, ``)``, ``!``, ``"``, ``=`` ni ``:``.
- Solo se aceptan URL absolutas ``http`` o ``https``.
- Una entrada que no cumple estas reglas no se utiliza. Se escribe una advertencia en el registro de |Fess| y las demás entradas siguen vigentes.
- Si se define dos veces la misma palabra clave, se usa la primera definición.
- Un valor vacío desactiva todos los bangs.

Cuando ``bangs.definitions`` no está establecida, están disponibles los cinco bangs siguientes:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Palabra clave
     - Sitio
   * - ``g``
     - Google
   * - ``b``
     - Bing
   * - ``ddg``
     - DuckDuckGo
   * - ``w``
     - Wikipedia (inglés)
   * - ``gh``
     - GitHub

Al establecer ``bangs.definitions`` se sustituye esta lista. Para conservar los bangs predeterminados y añadir uno más, escriba todas las entradas que necesite.

Véase también
=============

- :doc:`search-not` - Búsqueda NOT
- :doc:`special-char` - Caracteres especiales y escape
- :doc:`../api/api-search` - API de búsqueda
