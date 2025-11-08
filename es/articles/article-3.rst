========================================================
Servidor de Búsqueda Basado en Elasticsearch con Fess ~ Edición de API
========================================================

Introducción
========

Este artículo presenta cómo utilizar la API proporcionada por Fess para realizar búsquedas y mostrar resultados en el lado del cliente (navegador). Al utilizar la API, es posible integrar Fess como servidor de búsqueda en sistemas web existentes modificando solo el HTML.

Este artículo utiliza Fess 15.3.0 para la explicación.
Para el método de construcción de Fess, consulte la `edición de introducción <https://fess.codelibs.org/ja/articles/article-1.html>`__.

Lectores Objetivo
========

-  Personas que desean agregar funcionalidad de búsqueda a sistemas web existentes

Entorno Necesario
==========

El contenido de este artículo ha sido verificado en el siguiente entorno.

-  Google Chrome 120 o posterior

JSON API
========

Fess puede responder a resultados de búsqueda en JSON además de la expresión de búsqueda HTML normal. Al utilizar la API, es fácil consultar solo los resultados de búsqueda desde sistemas existentes después de construir un servidor Fess.
Dado que los resultados de búsqueda se pueden manejar en un formato independiente del lenguaje de desarrollo, creo que es fácil integrar Fess en sistemas distintos de Java.

Para conocer qué tipo de respuestas devuelve la API proporcionada por Fess, consulte `Respuesta JSON <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__.

Fess utiliza OpenSearch como motor de búsqueda interno.
OpenSearch también proporciona una API basada en JSON, pero la API de Fess es diferente.
Los beneficios de utilizar la API de Fess en lugar de la API de OpenSearch incluyen poder aprovechar diversas funciones específicas de Fess, como la gestión de registros de búsqueda y el control de permisos de visualización.
Si desea desarrollar desde cero un mecanismo de rastreo de documentos de manera independiente, sería mejor utilizar OpenSearch, pero si simplemente desea agregar funcionalidad de búsqueda fácilmente, puede reducir muchos costos de desarrollo utilizando Fess.

Construcción de un Sitio de Búsqueda Utilizando JSON API
==================================

Esta vez se explicará cómo construir un sitio utilizando la API de Fess.
Para la comunicación con el servidor Fess se utilizará la respuesta JSON.
El servidor Fess utilizado esta vez es el servidor Fess publicado como demostración por el proyecto Fess.
Si desea utilizar su propio servidor Fess, instale Fess 15.3.0 o una versión posterior.

JSON y CORS
-----------

Al acceder mediante JSON, es necesario prestar atención a la política Same-Origin.
Debido a esto, si el servidor que genera el HTML que se muestra en el navegador y el servidor Fess están en el mismo dominio, se puede utilizar JSON, pero si están en dominios diferentes, es necesario utilizar CORS (Cross-Origin Resource Sharing).
Esta vez procederemos con el caso en que el servidor donde está ubicado el HTML y el servidor Fess están en dominios diferentes.
Fess es compatible con CORS, y los valores de configuración se pueden establecer en app/WEB-INF/classes/fess_config.properties. Por defecto, se establece lo siguiente:

::

    api.cors.allow.origin=*
    api.cors.allow.methods=GET, POST, OPTIONS, DELETE, PUT
    api.cors.max.age=3600
    api.cors.allow.headers=Origin, Content-Type, Accept, Authorization, X-Requested-With
    api.cors.allow.credentials=true

Esta vez utilizaremos la configuración predeterminada, pero si cambia la configuración, reinicie Fess.


Archivos a Crear
----------------

Esta vez implementaremos el proceso de búsqueda utilizando JavaScript en HTML.
Como biblioteca de JavaScript utilizaremos jQuery.
Los archivos a crear son los siguientes:

-  Archivo HTML "index.html" que muestra el formulario de búsqueda y los resultados de búsqueda

- Archivo JS "fess.js" que se comunica con el servidor Fess

En este ejemplo de construcción, se implementan las siguientes funciones:

-  Envío de solicitudes de búsqueda mediante el botón de búsqueda

-  Lista de resultados de búsqueda

-  Procesamiento de paginación de resultados de búsqueda

Creación del Archivo HTML
------------------

Primero, crearemos el HTML que muestra el formulario de búsqueda y los resultados de búsqueda.
Esta vez, para facilitar la comprensión, la estructura de etiquetas es simple sin ajustar el diseño con CSS.
El archivo HTML a utilizar será el siguiente.

Contenido de index.html
::

    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Sitio de Búsqueda</title>
    </head>
    <body>
    <div id="header">
      <form id="searchForm">
        <input id="searchQuery" type="text" name="query" size="30"/>
        <input id="searchButton" type="submit" value="Buscar"/>
        <input id="searchStart" type="hidden" name="start" value="0"/>
        <input id="searchNum" type="hidden" name="num" value="20"/>
      </form>
    </div>
    <div id="subheader"></div>
    <div id="result"></div>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript" src="fess.js"></script>
    </body>
    </html>

Mirando debajo de la etiqueta body, primero en la parte de la etiqueta div con atributo id de header, se colocan el campo de entrada de búsqueda y el botón de búsqueda.
Además, en formularios ocultos se mantienen la posición de inicio de visualización (start) y el número de elementos a mostrar (num).
Los valores de start y num se actualizan con JavaScript después de enviar la solicitud de búsqueda.
Sin embargo, el número de elementos a mostrar es el número de elementos por página, y en este código de ejemplo, no hay función para cambiar el número de elementos a mostrar, por lo que el valor de num no se modifica.

En la parte de la etiqueta div de subheader se muestra información como el número de resultados que coincidieron con la búsqueda.
En la etiqueta div de result se muestran los resultados de búsqueda y los enlaces de paginación.

Finalmente, se carga el archivo JS de jQuery y el JavaScript "fess.js" creado esta vez.
Se puede guardar el archivo JS de jQuery en el mismo directorio que "index.html", pero esta vez lo configuramos para obtenerlo a través del CDN de Google.

Creación del Archivo JS
----------------

A continuación, crearemos el archivo JS "fess.js" que se comunica con el servidor Fess y muestra los resultados de búsqueda.
Cree "fess.js" con el siguiente contenido y colóquelo en el mismo directorio que "index.html".

Contenido de fess.js
::

    $(function(){
        // (1) URL de Fess
        var baseUrl = "http://SERVERNAME:8080/api/v1/documents?q=";
        // (2) Objeto jQuery del botón de búsqueda
        var $searchButton = $('#searchButton');

        // (3) Función de procesamiento de búsqueda
        var doSearch = function(event){
          // (4) Obtención de posición de inicio de visualización y número de elementos
          var start = parseInt($('#searchStart').val()),
              num = parseInt($('#searchNum').val());
          // Verificación de posición de inicio de visualización
          if(start < 0) {
            start = 0;
          }
          // Verificación de número de elementos
          if(num < 1 || num > 100) {
            num = 20;
          }
          // (5) Obtención de información de página a mostrar
          switch(event.data.navi) {
            case -1:
              // Caso de página anterior
              start -= num;
              break;
            case 1:
              // Caso de página siguiente
              start += num;
              break;
            default:
            case 0:
              start = 0;
              break;
          }
          // Recortar y almacenar el valor del campo de búsqueda
          var searchQuery = $.trim($('#searchQuery').val());
          // (6) Verificación de que el formulario de búsqueda no esté vacío
          if(searchQuery.length != 0) {
            var urlBuf = [];
            // (7) Deshabilitar el botón de búsqueda
            $searchButton.attr('disabled', true);
            // (8) Construcción de URL
            urlBuf.push(baseUrl, encodeURIComponent(searchQuery),
              '&start=', start, '&num=', num);
            // (9) Envío de solicitud de búsqueda
            $.ajax({
              url: urlBuf.join(""),
              dataType: 'json',
            }).done(function(data) {
              // Procesamiento de resultados de búsqueda
              var dataResponse = data.response;
              // (10) Verificación de estado
              if(dataResponse.status != 0) {
                alert("Ocurrió un problema durante la búsqueda. Consulte al administrador.");
                return;
              }

              var $subheader = $('#subheader'),
                  $result = $('#result'),
                  record_count = dataResponse.record_count,
                  offset = 0,
                  buf = [];
              if(record_count == 0) { // (11) Caso de que no haya resultados de búsqueda
                // Salida en área de subencabezado
                $subheader[0].innerHTML = "";
                // Salida en área de resultados
                buf.push("<b>", dataResponse.q, "</b> no se encontró información que coincida.");
                $result[0].innerHTML = buf.join("");
              } else { // (12) Caso de que la búsqueda tenga coincidencias
                var page_number = dataResponse.page_number,
                    startRange = dataResponse.start_record_number,
                    endRange = dataResponse.end_record_number,
                    i = 0,
                    max;
                offset = startRange - 1;
                // (13) Salida en subencabezado
                buf.push("Resultados de búsqueda de <b>", dataResponse.q, "</b> ",
                  startRange, " - ", endRange, " de ", record_count,
                  " elementos (", dataResponse.exec_time, " segundos)");
                $subheader[0].innerHTML = buf.join("");

                // Limpiar área de resultados de búsqueda
                $result.empty();

                // (14) Salida de resultados de búsqueda
                var $resultBody = $("<ol/>");
                var results = dataResponse.result;
                for(i = 0, max = results.length; i < max; i++) {
                  buf = [];
                  buf.push('<li><h3 class="title">', '<a href="',
                    results[i].url_link, '">', results[i].title,
                    '</a></h3><div class="body">', results[i].content_description,
                    '<br/><cite>', results[i].site, '</cite></div></li>');
                  $(buf.join("")).appendTo($resultBody);
                }
                $resultBody.appendTo($result);

                // (15) Salida de información de número de página
                buf = [];
                buf.push('<div id="pageInfo">Página ', page_number, '<br/>');
                if(dataResponse.prev_page) {
                  // Enlace a página anterior
                  buf.push('<a id="prevPageLink" href="#">&lt;&lt;Página anterior</a> ');
                }
                if(dataResponse.next_page) {
                  // Enlace a página siguiente
                  buf.push('<a id="nextPageLink" href="#">Página siguiente&gt;&gt;</a>');
                }
                buf.push('</div>');
                $(buf.join("")).appendTo($result);
              }
              // (16) Actualización de información de página
              $('#searchStart').val(offset);
              $('#searchNum').val(num);
              // (17) Mover visualización de página a la parte superior
              $(document).scrollTop(0);
            }).always(function() {
              // (18) Habilitar el botón de búsqueda
              $searchButton.attr('disabled', false);
            });
          }
          // (19) Devolver false para no hacer submit
          return false;
        };

        // (20) Procesamiento cuando se presiona la tecla Enter en el campo de entrada de búsqueda
        $('#searchForm').submit({navi:0}, doSearch);
        // (21) Procesamiento cuando se presiona el enlace de página anterior
        $('#result').on("click", "#prevPageLink", {navi:-1}, doSearch)
        // (22) Procesamiento cuando se presiona el enlace de página siguiente
          .on("click", "#nextPageLink", {navi:1}, doSearch);
      });

El procesamiento de "fess.js" se ejecuta después de que se construye el DOM del archivo HTML.
Primero, en 1 se especifica la URL del servidor Fess construido.

2 guarda el objeto jQuery del botón de búsqueda.
Como se utiliza el objeto jQuery del botón de búsqueda varias veces, se mantiene en una variable para reutilizarlo.

En 3 se define la función de procesamiento de búsqueda. El contenido de esta función se explicará en la siguiente sección.

20 registra el evento para cuando se envía el formulario de búsqueda.
El procesamiento registrado en 20 se ejecuta cuando se presiona el botón de búsqueda o cuando se presiona la tecla Enter en el campo de entrada de búsqueda.
Cuando ocurre el evento, se llama a la función de procesamiento de búsqueda doSearch.
El valor de navi se pasa al llamar a la función de procesamiento de búsqueda, y ese valor se utiliza para realizar el procesamiento de paginación.

21 y 22 registran los eventos para cuando se hacen clic en los enlaces agregados en el procesamiento de paginación.
Estos enlaces se agregan dinámicamente, por lo que es necesario registrar los eventos mediante delegate.
En estos eventos también se llama a la función de procesamiento de búsqueda de manera similar a 20.

Función de Procesamiento de Búsqueda doSearch
--------------------

Se explicará la función de procesamiento de búsqueda doSearch de 3.

En 4 se obtienen la posición de inicio de visualización y el número de elementos a mostrar.
Estos valores se guardan como valores ocultos en el formulario de búsqueda del área header.
Se asume que la posición de inicio de visualización es 0 o mayor, y el número de elementos es un valor entre 1 y 100, por lo que si se obtienen otros valores, se establece un valor predeterminado.

En 5 se determina el valor del parámetro navi pasado cuando doSearch fue registrado como evento, y se modifica la posición de inicio de visualización.
Aquí, -1 cambia al movimiento a la página anterior, 1 al movimiento a la página siguiente, y cualquier otro valor al movimiento a la primera página.

6 determina si se ejecutará la búsqueda si hay un valor ingresado en el campo de entrada de búsqueda, y si está vacío, termina el procesamiento sin hacer nada.

En 7 se deshabilita el botón de búsqueda durante la consulta al servidor Fess para prevenir el doble envío.

En 8 se construye la URL para enviar la solicitud Ajax.
Se combinan la URL de 1 con el término de búsqueda, la posición de inicio de visualización y el número de elementos.

En 9 se envía la solicitud Ajax.
Cuando la solicitud se devuelve normalmente, se ejecuta la función success.
El argumento de success recibe el objeto de resultados de búsqueda devuelto por el servidor Fess.

Primero, en 10 se verifica el contenido del estado de la respuesta.
Si la solicitud de búsqueda se procesó normalmente, se establece 0.
Para detalles sobre la respuesta JSON de Fess, consulte el `sitio de Fess <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__.

Si la solicitud de búsqueda se procesó normalmente pero no hubo coincidencias en los resultados de búsqueda, dentro de la declaración condicional de 11 se vacía el contenido del área subheader y se muestra un mensaje en el área result indicando que no hubo coincidencias en los resultados de búsqueda.

Si hay coincidencias en los resultados de búsqueda, dentro de la declaración condicional de 12 se procesa el resultado de búsqueda.
En 13 se establece un mensaje con el número de elementos mostrados y el tiempo de ejecución en el área subheader.
14 agrega los resultados de búsqueda al área result.
Los resultados de búsqueda se almacenan como un array en data.response.result.
Se puede obtener el valor del campo del documento de resultado de búsqueda accediendo mediante results[i].〜.

En 15 se agrega al área result el número de página que se está mostrando actualmente y los enlaces a la página anterior y siguiente.
En 16 se guardan en el hidden del formulario de búsqueda la posición de inicio de visualización y el número de elementos actuales.
La posición de inicio de visualización y el número de elementos se volverán a utilizar en la siguiente solicitud de búsqueda.

A continuación, en 17 se cambia la posición de visualización de la página.
Cuando se hace clic en el enlace a la página siguiente, la página en sí no se actualiza, por lo que se mueve al inicio de la página mediante scrollTop.

En 18 se habilita el botón de búsqueda después de completar el procesamiento de búsqueda.
Se configura para que se llame en complete para que se ejecute ya sea que la solicitud tenga éxito o falle.

En 19 se devuelve false para que después de llamar a la función de procesamiento de búsqueda, el formulario o el enlace no se envíen.
Esto evita que ocurra una transición de página.

Ejecución
----

Acceda a "index.html" con un navegador.
Se mostrará el formulario de búsqueda como se muestra a continuación.

Formulario de búsqueda
|image1|

Ingrese un término de búsqueda apropiado y presione el botón de búsqueda, y se mostrarán los resultados de búsqueda.
El número predeterminado de elementos a mostrar es 20, pero si el número de resultados coincidentes es grande, se mostrará un enlace a la página siguiente debajo de la lista de resultados de búsqueda.

Resultados de búsqueda
|image2|

Resumen
======

Hemos construido un sitio de búsqueda de cliente basado en jQuery utilizando la JSON API de Fess.
Al utilizar la JSON API, no solo es posible construir aplicaciones basadas en navegador, sino también sistemas que utilizan Fess llamándolo desde otras aplicaciones.

Cabe señalar que aunque el código de ejemplo de este artículo muestra el formato de endpoint de API tradicional, en Fess 15.3 se recomienda el uso del endpoint ``/api/v1/documents``.
Para obtener detalles, consulte las `especificaciones de API <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__.

Material de Referencia
========

-  `Fess <https://fess.codelibs.org/ja/>`__

-  `jQuery <http://jquery.com/>`__

.. |image0| image:: ../../resources/images/ja/article/4/sameorigin.png
.. |image1| image:: ../../resources/images/ja/article/4/searchform.png
.. |image2| image:: ../../resources/images/ja/article/4/searchresult.png
