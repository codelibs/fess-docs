============================================================
Parte 3: Integrar la búsqueda en un portal corporativo -- Escenario para agregar funcionalidad de búsqueda a un sitio web existente
============================================================

Introducción
============

En la entrega anterior, iniciamos Fess con Docker Compose y experimentamos la búsqueda.
Sin embargo, en la práctica empresarial, además de "usar la pantalla de búsqueda de Fess tal cual", existe una gran demanda de "agregar funcionalidad de búsqueda a un sitio corporativo o portal existente".

En este artículo, presentamos tres enfoques para integrar la funcionalidad de búsqueda de Fess en un sitio web existente, y explicamos las características y criterios de selección de cada uno.

Público objetivo
================

- Personas que desean agregar funcionalidad de búsqueda a un portal corporativo o sitio web
- Personas con conocimientos básicos de desarrollo front-end
- Haber completado los pasos de la Parte 2 y tener Fess en funcionamiento

Requisitos del entorno
======================

- El entorno de Fess construido en la Parte 2 (Docker Compose)
- Una página web de prueba (puede ser un archivo HTML local)

Tres enfoques de integración
=============================

Existen tres formas principales de integrar la funcionalidad de búsqueda de Fess en un sitio existente.

.. list-table:: Comparación de enfoques de integración
   :header-rows: 1
   :widths: 15 30 25 30

   * - Enfoque
     - Descripción
     - Esfuerzo de desarrollo
     - Caso adecuado
   * - FSS (Fess Site Search)
     - Solo insertar una etiqueta JavaScript
     - Mínimo (unas pocas líneas de código)
     - Cuando se desea agregar búsqueda de forma sencilla
   * - Integración por formulario de búsqueda
     - Navegar a Fess desde un formulario HTML
     - Bajo (solo modificar HTML)
     - Cuando se desea usar la pantalla de búsqueda de Fess tal cual
   * - Integración por API de búsqueda
     - Construir una interfaz personalizada con la API JSON
     - Medio a alto (desarrollo front-end)
     - Cuando se desea personalizar completamente el diseño y el comportamiento

A continuación, explicamos cada método con escenarios concretos.

Enfoque 1: Agregar fácilmente con FSS (Fess Site Search)
==========================================================

Escenario
---------

Existe un portal corporativo y se tiene permiso para editar el HTML, pero se desea evitar modificaciones importantes.
Se quiere permitir la búsqueda de documentos internos desde el portal con cambios mínimos.

Qué es FSS
-----------

Fess Site Search (FSS) es un mecanismo que permite agregar funcionalidad de búsqueda simplemente insertando una etiqueta JavaScript en una página web.
Dado que tanto el campo de búsqueda como la visualización de resultados se procesan completamente mediante JavaScript, apenas es necesario modificar la estructura de la página existente.

Pasos de implementación
-----------------------

1. Habilite el acceso a la API en la pantalla de administración de Fess.
   En la página [Sistema] > [General], active las respuestas JSON.

2. Inserte el siguiente código en la página donde desea agregar la funcionalidad de búsqueda.

.. code-block:: html

    <script>
      (function() {
        var fess = document.createElement('script');
        fess.type = 'text/javascript';
        fess.async = true;
        fess.src = 'http://localhost:8080/js/fess-ss.min.js';
        fess.charset = 'utf-8';
        fess.setAttribute('id', 'fess-ss');
        fess.setAttribute('fess-url', 'http://localhost:8080/api/v1/documents');
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(fess, s);
      })();
    </script>

    <fess:search></fess:search>

El campo de búsqueda y los resultados se muestran en el lugar donde se coloca la etiqueta ``<fess:search>``.

Personalización
----------------

La apariencia de FSS se puede personalizar con CSS.
Es posible adaptar FSS al diseño del sitio existente sobrescribiendo los estilos predeterminados proporcionados por Fess.

.. code-block:: css

    .fessWrapper {
      font-family: 'Noto Sans JP', sans-serif;
      max-width: 800px;
      margin: 0 auto;
    }
    .fessWrapper .searchButton {
      background-color: #1a73e8;
    }

Enfoque 2: Implementación sencilla mediante integración por formulario de búsqueda
====================================================================================

Escenario
---------

El portal corporativo ya cuenta con una barra de navegación en el encabezado.
Se desea agregar un campo de búsqueda allí y, al ejecutar la búsqueda, redirigir a la pantalla de resultados de Fess.
Se quiere lograr esto solo con HTML, sin usar JavaScript.

Pasos de implementación
-----------------------

Agregue un formulario HTML como el siguiente a la barra de navegación existente.

.. code-block:: html

    <form action="http://localhost:8080/search" method="get">
      <input type="text" name="q" placeholder="Buscar internamente..." />
      <button type="submit">Buscar</button>
    </form>

Con solo esto, al ejecutar la búsqueda se redirige a la pantalla de resultados de Fess.
Personalizando el diseño de la pantalla de búsqueda de Fess, se puede ofrecer una experiencia coherente.

Personalización de la pantalla de búsqueda de Fess
----------------------------------------------------

La pantalla de búsqueda de Fess está compuesta por archivos JSP y también se puede editar desde la pantalla de administración.

1. Seleccione [Sistema] > [Diseño de página] en la pantalla de administración
2. Personalice el encabezado, el pie de página, CSS, etc.

Por ejemplo, al unificar el logotipo y la paleta de colores con el portal corporativo, se puede ofrecer una experiencia de búsqueda sin discontinuidades para los usuarios.

Uso del mapeo de rutas
-----------------------

Es posible transformar las URL que aparecen en los resultados de búsqueda a URL más accesibles para los usuarios.
Por ejemplo, aunque la URL al momento del rastreo sea ``http://internal-server:8888/docs/``, se puede mostrar en los resultados de búsqueda como ``https://portal.example.com/docs/``.

Esto se configura desde [Rastreador] > [Mapeo de rutas] en la pantalla de administración.

Enfoque 3: Personalización completa con la API de búsqueda
============================================================

Escenario
---------

Se desea integrar la funcionalidad de búsqueda dentro de una aplicación empresarial interna.
Se quiere tener control total sobre el diseño y la forma de mostrar los resultados.
Se cuenta con recursos de desarrollo front-end.

Conceptos básicos de la API de búsqueda
-----------------------------------------

Fess proporciona una API de búsqueda basada en JSON.

::

    GET http://localhost:8080/api/v1/documents?q=検索キーワード

La respuesta tiene el siguiente formato JSON.

.. code-block:: json

    {
      "record_count": 10,
      "page_count": 5,
      "data": [
        {
          "title": "ドキュメントタイトル",
          "url": "https://example.com/doc.html",
          "content_description": "...検索キーワードを含む本文の抜粋..."
        }
      ]
    }

Ejemplo de implementación en JavaScript
-----------------------------------------

A continuación se muestra un ejemplo básico de implementación utilizando la API de búsqueda.

.. code-block:: javascript

    async function searchFess(query) {
      const url = new URL('http://localhost:8080/api/v1/documents');
      url.searchParams.set('q', query);
      const response = await fetch(url);
      const data = await response.json();

      const results = data.data;
      const container = document.getElementById('search-results');
      container.textContent = '';

      results.forEach(item => {
        const div = document.createElement('div');
        const heading = document.createElement('h3');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        heading.appendChild(link);
        const desc = document.createElement('p');
        desc.textContent = item.content_description;
        div.appendChild(heading);
        div.appendChild(desc);
        container.appendChild(div);
      });
    }

Parámetros adicionales de la API
----------------------------------

La API de búsqueda permite personalizar el comportamiento de la búsqueda con diversos parámetros.

.. list-table:: Principales parámetros de la API
   :header-rows: 1
   :widths: 20 50 30

   * - Parámetro
     - Descripción
     - Ejemplo
   * - ``q``
     - Palabra clave de búsqueda
     - ``q=Fess``
   * - ``num``
     - Número de resultados por página
     - ``num=20``
   * - ``start``
     - Posición de inicio de los resultados
     - ``start=20``
   * - ``fields.label``
     - Filtrado por etiqueta
     - ``fields.label=intranet``
   * - ``sort``
     - Orden de clasificación
     - ``sort=last_modified.desc``

Utilizando la API, es posible realizar un control detallado del filtrado, la clasificación y la paginación de los resultados de búsqueda.

Cómo elegir el enfoque adecuado
=================================

Los tres enfoques se eligen según la situación.

**Cuándo elegir FSS**

- Los recursos de desarrollo son limitados
- Se desea agregar búsqueda con cambios mínimos en la página existente
- Una apariencia estándar de la funcionalidad de búsqueda es suficiente

**Cuándo elegir la integración por formulario de búsqueda**

- El diseño de la pantalla de búsqueda de Fess es suficiente
- No se desea usar JavaScript
- Solo se necesita agregar un campo de búsqueda en el encabezado o la barra lateral

**Cuándo elegir la API de búsqueda**

- Se desea personalizar completamente la visualización de los resultados de búsqueda
- Se quiere integrar en una SPA (Single Page Application)
- Se desea aplicar lógica propia (filtrado, resaltado, etc.) a los resultados de búsqueda
- Se cuenta con recursos de desarrollo front-end

También es posible combinarlos
-------------------------------

Estos enfoques no son mutuamente excluyentes.
Por ejemplo, es válido agregar fácilmente la funcionalidad de búsqueda con FSS en la página principal y, en una página de búsqueda dedicada, ofrecer una interfaz personalizada mediante la API.

Resumen
=======

En este artículo, presentamos tres enfoques para integrar la funcionalidad de búsqueda de Fess en un sitio web existente.

- **FSS**: Agregar funcionalidad de búsqueda con solo insertar una etiqueta JavaScript
- **Integración por formulario de búsqueda**: Navegar a la pantalla de búsqueda de Fess desde un formulario HTML
- **API de búsqueda**: Construir una experiencia de búsqueda completamente personalizada con la API JSON

Con cualquiera de los enfoques, se puede aprovechar la calidad de búsqueda proporcionada por el backend de Fess.
Elija el método óptimo según sus requisitos y recursos de desarrollo disponibles.

En la próxima entrega, abordaremos el escenario de búsqueda unificada en múltiples fuentes de datos, como servidores de archivos y almacenamiento en la nube.

Referencias
============

- `Fess Site Search <https://github.com/codelibs/fess-site-search>`__

- `API de búsqueda de Fess <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__
