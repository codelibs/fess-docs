===============================
Configuración de Imágenes en Miniatura
===============================

Visualización de Imágenes en Miniatura
=======================================

|Fess| puede mostrar imágenes en miniatura en los resultados de búsqueda.
Las imágenes en miniatura se generan en base al tipo MIME de los resultados de búsqueda.
Si el tipo MIME es compatible, se generará una imagen en miniatura al mostrar los resultados de búsqueda.
El proceso de generación de imágenes en miniatura se puede configurar y agregar para cada tipo MIME.

Para habilitar la visualización de imágenes en miniatura, inicie sesión como administrador, active la visualización de miniaturas en la configuración general y guarde los cambios.

Imágenes en Miniatura de Archivos HTML
=======================================

Las imágenes en miniatura de HTML utilizan las imágenes especificadas o incluidas dentro del HTML.
Las imágenes en miniatura se buscan en el siguiente orden y se muestran si están especificadas.

- Valor del atributo content de la etiqueta meta con el atributo name establecido en thumbnail
- Valor del atributo content de la etiqueta meta con el atributo property establecido en og:image
- Imágenes de tamaño adecuado para miniaturas en las etiquetas img


Imágenes en Miniatura de Archivos MS Office
============================================

Las imágenes en miniatura de archivos MS Office se generan utilizando LibreOffice e ImageMagick.
Si están instalados los comandos unoconv y convert, se generarán las imágenes en miniatura.

Instalación de Paquetes
------------------------

Para sistemas operativos basados en Redhat, instale los siguientes paquetes para la creación de imágenes.

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

Script de Generación
---------------------

Al instalar mediante paquetes RPM/Deb, el script de generación de miniaturas para MS Office se instalará en /usr/share/fess/bin/generate-thumbnail.

Imágenes en Miniatura de Archivos PDF
======================================

Las imágenes en miniatura de PDF se generan utilizando ImageMagick.
Si está instalado el comando convert, se generarán las imágenes en miniatura.

Desactivación del Trabajo de Miniaturas
========================================

Para desactivar el trabajo de miniaturas, configure lo siguiente:

1. En la pantalla de administración, vaya a Sistema > General, desmarque "Visualización de miniaturas" y haga clic en el botón "Actualizar".
2. Establezca ``false`` en ``thumbnail.crawler.enabled`` en ``app/WEB-INF/classes/fess_config.properties`` o ``/etc/fess/fess_config.properties``.

::

    thumbnail.crawler.enabled=false

3. Reinicie el servicio de Fess.
