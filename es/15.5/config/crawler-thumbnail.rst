=======================================
Configuración de Imágenes en Miniatura
=======================================

Descripción General
===================

|Fess| puede mostrar imágenes en miniatura en los resultados de búsqueda.
Las imágenes en miniatura se generan en base al tipo MIME de los resultados de búsqueda.
Si el tipo MIME es compatible, se generará una imagen en miniatura al mostrar los resultados de búsqueda.
El proceso de generación de imágenes en miniatura se puede configurar y agregar para cada tipo MIME.

Para habilitar la visualización de imágenes en miniatura, inicie sesión como administrador, active la visualización de miniaturas en la configuración general y guarde los cambios.

Formatos de Archivo Soportados
==============================

Archivos de Imagen
------------------

.. list-table::
   :widths: 15.50 20
   :header-rows: 1

   * - Formato
     - Tipo MIME
     - Descripción
   * - JPEG
     - ``image/jpeg``
     - Fotos, etc.
   * - PNG
     - ``image/png``
     - Imágenes transparentes, etc.
   * - GIF
     - ``image/gif``
     - Incluyendo GIFs animados
   * - BMP
     - ``image/bmp``, ``image/x-windows-bmp``, ``image/x-ms-bmp``
     - Imágenes de mapa de bits
   * - TIFF
     - ``image/tiff``
     - Imágenes de alta calidad
   * - SVG
     - ``image/svg+xml``
     - Imágenes vectoriales
   * - Photoshop
     - ``image/vnd.adobe.photoshop``, ``image/photoshop``, ``application/x-photoshop``, ``application/photoshop``
     - Archivos PSD

Archivos de Documento
---------------------

.. list-table::
   :widths: 15 50 20
   :header-rows: 1

   * - Formato
     - Tipo MIME
     - Descripción
   * - PDF
     - ``application/pdf``
     - Documentos PDF
   * - Word
     - ``application/msword``, ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - Documentos Word
   * - Excel
     - ``application/vnd.ms-excel``, ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``
     - Hojas de cálculo Excel
   * - PowerPoint
     - ``application/vnd.ms-powerpoint``, ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
     - Presentaciones PowerPoint
   * - RTF
     - ``application/rtf``
     - Texto enriquecido
   * - PostScript
     - ``application/postscript``
     - Archivos PostScript

Contenido HTML
--------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - Formato
     - Tipo MIME
     - Descripción
   * - HTML
     - ``text/html``
     - Genera miniaturas a partir de imágenes incrustadas en páginas HTML

Herramientas Externas Requeridas
================================

La generación de miniaturas requiere las siguientes herramientas externas. Instálelas según los formatos de archivo que necesite soportar.

Herramientas Básicas (Requeridas)
---------------------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Herramienta
     - Propósito
     - Linux (apt)
     - Mac (Homebrew)
   * - ImageMagick
     - Conversión y redimensionamiento de imágenes
     - ``apt install imagemagick``
     - ``brew install imagemagick``

.. note::

   Se soportan tanto ImageMagick 6 (comando ``convert``) como ImageMagick 7 (comando ``magick``).

Soporte SVG
-----------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Herramienta
     - Propósito
     - Linux (apt)
     - Mac (Homebrew)
   * - rsvg-convert
     - Conversión SVG a PNG
     - ``apt install librsvg2-bin``
     - ``brew install librsvg``

Soporte PDF
-----------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Herramienta
     - Propósito
     - Linux (apt)
     - Mac (Homebrew)
   * - pdftoppm
     - Conversión PDF a PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

Soporte MS Office
-----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Herramienta
     - Propósito
     - Linux (apt)
     - Mac (Homebrew)
   * - unoconv
     - Conversión Office a PDF
     - ``apt install unoconv``
     - ``brew install unoconv``
   * - pdftoppm
     - Conversión PDF a PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

Para sistemas operativos basados en Redhat, instale los siguientes paquetes:

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick poppler-utils

Soporte PostScript
------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Herramienta
     - Propósito
     - Linux (apt)
     - Mac (Homebrew)
   * - ps2pdf
     - Conversión PS a PDF
     - ``apt install ghostscript``
     - ``brew install ghostscript``
   * - pdftoppm
     - Conversión PDF a PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

Imágenes en Miniatura de Archivos HTML
======================================

Las imágenes en miniatura de HTML utilizan las imágenes especificadas o incluidas dentro del HTML.
Las imágenes en miniatura se buscan en el siguiente orden y se muestran si están especificadas:

1. Valor del atributo content de la etiqueta meta con el atributo name establecido en "thumbnail"
2. Valor del atributo content de la etiqueta meta con el atributo property establecido en "og:image"
3. Imágenes de tamaño adecuado para miniaturas en las etiquetas img

Configuración
=============

Archivo de Configuración
------------------------

El generador de miniaturas se configura en ``fess_thumbnail.xml``.

::

    src/main/resources/fess_thumbnail.xml

Principales Opciones de Configuración (fess_config.properties)
--------------------------------------------------------------

Las siguientes opciones pueden configurarse en ``app/WEB-INF/classes/fess_config.properties`` o ``/etc/fess/fess_config.properties``.

::

    # Ancho mínimo para imágenes en miniatura (píxeles)
    thumbnail.html.image.min.width=100

    # Altura mínima para imágenes en miniatura (píxeles)
    thumbnail.html.image.min.height=100

    # Relación de aspecto máxima (ancho:altura o altura:ancho)
    thumbnail.html.image.max.aspect.ratio=3.0

    # Ancho de miniatura generada
    thumbnail.html.image.thumbnail.width=100

    # Altura de miniatura generada
    thumbnail.html.image.thumbnail.height=100

    # Formato de salida
    thumbnail.html.image.format=png

    # XPath para extraer imágenes del HTML
    thumbnail.html.image.xpath=//IMG

    # Extensiones excluidas
    thumbnail.html.image.exclude.extensions=svg,html,css,js

    # Intervalo de generación de miniaturas (milisegundos)
    thumbnail.generator.interval=0

    # Tiempo de espera de ejecución de comando (milisegundos)
    thumbnail.command.timeout=30000

    # Tiempo de espera de destrucción de proceso (milisegundos)
    thumbnail.command.destroy.timeout=5000

Script generate-thumbnail
=========================

Descripción General
-------------------

``generate-thumbnail`` es un script de shell que realiza la generación real de miniaturas.
Al instalar mediante paquetes RPM/Deb, se instala en ``/usr/share/fess/bin/generate-thumbnail``.

Uso
---

::

    generate-thumbnail <type> <url> <output_file> [mimetype]

Argumentos
----------

.. list-table::
   :widths: 15.50 30
   :header-rows: 1

   * - Argumento
     - Descripción
     - Ejemplo
   * - ``type``
     - Tipo de archivo
     - ``image``, ``svg``, ``pdf``, ``msoffice``, ``ps``
   * - ``url``
     - URL del archivo de entrada
     - ``file:/path/to/file.jpg``
   * - ``output_file``
     - Ruta del archivo de salida
     - ``/var/lib/fess/thumbnails/_0/_1/abc.png``
   * - ``mimetype``
     - Tipo MIME (opcional)
     - ``image/gif``

Tipos Soportados
----------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - Tipo
     - Descripción
     - Herramientas Utilizadas
   * - ``image``
     - Archivos de imagen
     - ImageMagick (convert/magick)
   * - ``svg``
     - Archivos SVG
     - rsvg-convert
   * - ``pdf``
     - Archivos PDF
     - pdftoppm + ImageMagick
   * - ``msoffice``
     - Archivos MS Office
     - unoconv + pdftoppm + ImageMagick
   * - ``ps``
     - Archivos PostScript
     - ps2pdf + pdftoppm + ImageMagick

Ejemplos
--------

::

    # Generar miniatura para archivo de imagen
    ./generate-thumbnail image file:/path/to/image.jpg /tmp/thumbnail.png image/jpeg

    # Generar miniatura para archivo SVG
    ./generate-thumbnail svg file:/path/to/image.svg /tmp/thumbnail.png

    # Generar miniatura para archivo PDF
    ./generate-thumbnail pdf file:/path/to/document.pdf /tmp/thumbnail.png

    # Archivo GIF (especificar tipo MIME para habilitar indicación de formato)
    ./generate-thumbnail image file:/path/to/image.gif /tmp/thumbnail.png image/gif

Ubicación de Almacenamiento de Miniaturas
=========================================

Ruta Predeterminada
-------------------

::

    ${FESS_VAR_PATH}/thumbnails/

o

::

    /var/lib/fess/thumbnails/

Estructura de Directorios
-------------------------

Las miniaturas se almacenan en una estructura de directorios basada en hash.

::

    thumbnails/
    ├── _0/
    │   ├── _1/
    │   │   ├── _2/
    │   │   │   └── _3/
    │   │   │       └── abcdef123456.png
    │   │   └── ...
    │   └── ...
    └── ...

Desactivación del Trabajo de Miniaturas
=======================================

Para desactivar el trabajo de miniaturas, configure lo siguiente:

1. En la pantalla de administración, vaya a Sistema > General, desmarque "Visualización de miniaturas" y haga clic en el botón "Actualizar".
2. Establezca ``thumbnail.crawler.enabled`` en ``false`` en ``app/WEB-INF/classes/fess_config.properties`` o ``/etc/fess/fess_config.properties``.

::

    thumbnail.crawler.enabled=false

3. Reinicie el servicio de Fess.

Solución de Problemas
=====================

Las Miniaturas No Se Generan
----------------------------

1. **Verificar herramientas externas**

::

    # Verificar ImageMagick
    which convert || which magick

    # Verificar rsvg-convert (para SVG)
    which rsvg-convert

    # Verificar pdftoppm (para PDF)
    which pdftoppm

2. **Verificar logs**

::

    ${FESS_LOG_PATH}/fess-thumbnail.log

3. **Ejecutar script manualmente**

::

    /usr/share/fess/bin/generate-thumbnail image file:/path/to/test.jpg /tmp/test_thumbnail.png image/jpeg

Errores con Archivos GIF/TIFF
-----------------------------

Al usar ImageMagick 6, especifique el tipo MIME para habilitar las indicaciones de formato. Esto se hace automáticamente si Fess está configurado correctamente.

Ejemplo de error::

    convert-im6.q16: corrupt image `/tmp/thumbnail_xxx' @ error/gif.c/DecodeImage/512

Soluciones:

- Actualizar a ImageMagick 7
- O verificar que el tipo MIME se está pasando correctamente

Las Miniaturas SVG No Se Generan
--------------------------------

1. Verificar si ``rsvg-convert`` está instalado

::

    which rsvg-convert

2. Probar conversión manualmente

::

    rsvg-convert -w 100 -h 100 --keep-aspect-ratio input.svg -o output.png

Errores de Permisos
-------------------

Verifique los permisos del directorio de almacenamiento de miniaturas.

::

    ls -la /var/lib/fess/thumbnails/

Corrija los permisos si es necesario.

::

    chown -R fess:fess /var/lib/fess/thumbnails/
    chmod -R 755 /var/lib/fess/thumbnails/

Soporte de Plataformas
======================

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Plataforma
     - Estado de Soporte
     - Notas
   * - Linux
     - Totalmente soportado
     - \-
   * - macOS
     - Totalmente soportado
     - Instalar herramientas externas via Homebrew
   * - Windows
     - No soportado
     - Debido a la dependencia del script bash
