====================================================================
Creación de un servidor de búsqueda basado en Elasticsearch con Fess ~ Edición FSS
====================================================================

Introducción
============

En este artículo se presenta cómo integrar un servicio de búsqueda en un sitio web utilizando un servidor Fess previamente configurado.
Mediante el uso de las etiquetas y el archivo JavaScript proporcionados por Fess Site Search (FSS), es posible mostrar un cuadro de búsqueda y los resultados de búsqueda en un sitio web existente.


Público objetivo
================

- Personas que deseen agregar funcionalidad de búsqueda a un sitio web existente.

- Personas que deseen migrar desde Google Site Search o Google Custom Search.


Qué es Fess Site Search (FSS)
===============================

FSS es una funcionalidad que permite incorporar el servidor de búsqueda Fess en un sitio web existente. Se ofrece a través del `sitio de FSS <https://fss-generator.codelibs.org/>`__ del proyecto CodeLibs. Al igual que los servicios de búsqueda interna de sitios como Google Site Search (GSS), basta con insertar una etiqueta JavaScript en la página donde se desea utilizar el servicio de búsqueda, lo que facilita también la migración desde GSS.

Qué es FSS JS
===============

FSS JS es un archivo JavaScript que muestra los resultados de búsqueda de Fess. Al colocar este archivo JavaScript en un sitio web, es posible mostrar los resultados de búsqueda.
FSS JS se puede obtener generándolo con FSS JS Generator en "https://fss-generator.codelibs.org/".
FSS JS es compatible con Fess versión 11.3 o superior, por lo que al configurar Fess, asegúrese de instalar la versión 11.3 o posterior. Para obtener información sobre cómo configurar Fess, consulte la\ `edición de introducción <https://fess.codelibs.org/ja/articles/article-1.html>`__\ .


En FSS JS Generator se puede especificar la combinación de colores del formulario de búsqueda y la fuente del texto.
Al presionar el botón "Generate", se genera el archivo JavaScript con la configuración especificada.

|image0|

Si no hay problemas con la vista previa, presione el botón "Download JS" para descargar el archivo JavaScript.

|image1|

Integración en el sitio
========================

En este caso, consideraremos el ejemplo de incorporar una búsqueda interna en el sitio "`www.n2sm.net`", construido con HTML estático.

Los resultados de búsqueda se mostrarán en search.html dentro del mismo sitio, y el servidor Fess se configurará por separado en "nss833024.n2search.net".

El archivo JavaScript de FSS JS descargado se colocará en el sitio como /js/fess-ss.min.js.

La información anterior se resume de la siguiente manera.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Nombre
     - URL
   * - Sitio objetivo de búsqueda
     - https://www.n2sm.net/
   * - Página de resultados de búsqueda
     - https://www.n2sm.net/search.html
   * - FSS JS
     - https://www.n2sm.net/js/fess-ss.min.js
   * - Servidor Fess
     - https://nss833024.n2search.net/

Para insertar la etiqueta JavaScript, coloque las siguientes etiquetas en la ubicación de search.html donde desea mostrar los resultados de búsqueda.

..
  <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      // Establezca la URL de FSS JS en src
      fess.src = 'https://www.n2sm.net/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      // Establezca la URL de la API de búsqueda de Fess en fess-url
      fess.setAttribute('fess-url', 'https://nss833024.n2search.net/json');
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(fess, s);
    })();
  </script>
  <fess:search></fess:search>

Al acceder a search.html se mostrará el formulario de búsqueda.

Al ingresar un término de búsqueda, se pueden mostrar los resultados de búsqueda como se muestra a continuación.

|image2|

Para colocar un formulario de búsqueda en otras páginas y mostrar los resultados de búsqueda, coloque un formulario de búsqueda como el siguiente en cada página, configurándolo para que redirija a "`https://www.n2sm.net/search.html?q=término de búsqueda`".

..
  <form action="https://www.n2sm.net/search.html" method="get">
    <input type="text" name="q">
    <input type="submit" value="Buscar">
  </form>


Conclusión
==========

Se presentó cómo integrar los resultados de búsqueda de Fess en un sitio simplemente colocando una etiqueta JavaScript.
Gracias a FSS, la migración desde GSS también se puede realizar simplemente reemplazando las etiquetas JavaScript existentes.
FSS JS también ofrece otros métodos de visualización y formas de vincular los registros de búsqueda con Google Analytics. Para obtener más información sobre otras configuraciones, consulte el `[manual] de FSS <https://fss-generator.codelibs.org/ja/docs/manual>`__.

Referencias
============
- `Fess Site Search <https://fss-generator.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/ja/article/5/FSS-JS-Generator1.png
.. |image1| image:: ../../resources/images/ja/article/5/FSS-JS-Generator2.png
.. |image2| image:: ../../resources/images/ja/article/5/N2Search-review.png
