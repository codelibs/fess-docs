==================================
Configuración de OCR
==================================

Descripción general
===================

|Fess| extrae texto de los documentos con Apache Tika.
El analizador OCR de Tesseract de Tika se incluye en |Fess|. Al activarlo, |Fess| reconoce el texto de las imágenes y de los PDF escaneados y lo hace buscable.

El OCR se ejecuta cuando se cumplen las dos condiciones siguientes:

- El comando ``tesseract`` está instalado en el host donde se ejecuta el proceso del rastreador de |Fess|
- El OCR está activado en |Fess|

El OCR está desactivado de forma predeterminada.
Si ``tesseract`` no está instalado, |Fess| omite el OCR. No se produce ningún error.

A qué se aplica el OCR
======================

Cuando el OCR está activado, se aplica a lo siguiente:

- Archivos de imagen (PNG, JPEG, TIFF, GIF, BMP, etc.)
- Imágenes incrustadas en documentos que procesa Tika (por ejemplo, archivos de Office)
- PDF cuya capa de texto está vacía (PDF escaneados)

Tratamiento de los PDF escaneados
---------------------------------

|Fess| normalmente extrae el texto de los PDF con PDFBox.
Cuando el OCR está activado y PDFBox no obtiene ningún texto de un PDF, |Fess| vuelve a extraer el PDF mediante Tika.
Tika convierte las páginas en imágenes y les aplica OCR.

.. note::
   Los PDF que ya contienen algo de texto no se procesan con OCR.
   Los PDF mixtos, en los que solo algunas páginas son imágenes escaneadas, no están cubiertos.

Instalación de Tesseract
========================

Instale Tesseract en el host donde se ejecuta |Fess|.
Para reconocer texto en japonés, también necesita los datos de entrenamiento en japonés (traineddata).

Debian / Ubuntu::

    $ sudo apt-get install tesseract-ocr tesseract-ocr-jpn

RHEL / Rocky Linux / AlmaLinux (active EPEL antes)::

    $ sudo dnf install tesseract tesseract-langpack-jpn

Para comprobar los idiomas instalados, ejecute::

    $ tesseract --list-langs

Activación del OCR
==================

Configure las siguientes propiedades en ``fess_config.properties``.

- Paquete ZIP: ``app/WEB-INF/classes/fess_config.properties``
- Paquete RPM/DEB: ``/etc/fess/fess_config.properties``

::

    # Activar el OCR (predeterminado: false)
    crawler.document.ocr.enabled=true

    # Idioma(s) de Tesseract, unidos con + (predeterminado: eng)
    crawler.document.ocr.language=jpn+eng

    # Tiempo de espera en segundos para una ejecución de Tesseract (predeterminado: 120)
    crawler.document.ocr.timeout=120

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Propiedad
     - Predeterminado
     - Descripción
   * - ``crawler.document.ocr.enabled``
     - ``false``
     - Establézcala en ``true`` para activar el OCR.
   * - ``crawler.document.ocr.language``
     - ``eng``
     - Idioma(s) de Tesseract. Los varios idiomas se unen con ``+`` (por ejemplo, ``jpn+eng``). Deben estar instalados los datos de entrenamiento (traineddata) correspondientes.
   * - ``crawler.document.ocr.timeout``
     - ``120``
     - Tiempo de espera de una ejecución de Tesseract (una imagen o una página de PDF), en segundos.

También puede establecerlas como propiedades del sistema de la JVM.
Por ejemplo, indíquelas en ``FESS_JAVA_OPTS``. Resulta práctico en entornos Docker.

::

    -Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng

.. note::
   Reinicie |Fess| después de cambiar esta configuración.

Uso del OCR con Docker
======================

Para usar el OCR en un entorno Docker, añada Tesseract a la imagen de |Fess|.
Construya una imagen con Tesseract usando ``compose/tesseract/Dockerfile`` de `docker-fess <https://github.com/codelibs/docker-fess>`__.

Ejemplo de ``compose/tesseract/Dockerfile``::

    FROM ghcr.io/codelibs/fess:15.9.0

    RUN apk add --no-cache tesseract-ocr tesseract-ocr-data-osd tesseract-ocr-data-eng tesseract-ocr-data-jpn

En ``compose/compose.yaml``, sustituya la línea ``image:`` por ``build: ./tesseract`` y active la línea ``FESS_JAVA_OPTS``.
Funciona igual que ``build: ./playwright``.

::

    services:
      fess01:
        # image: ghcr.io/codelibs/fess:15.9.0
        build: ./tesseract
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng"

Después del cambio, reconstruya la imagen e inicie los contenedores::

    $ docker compose up -d --build

.. note::
   Si usa una imagen base que no es Alpine, como ``-noble`` o ``-al2023``, añada Tesseract con el gestor de paquetes de esa distribución en lugar de ``apk``.

Consulte :doc:`../install/install-docker` para más detalles.

Configuración por configuración de rastreo
==========================================

Si especifica ``config.tika.tesseract.config`` en los "Parámetros de configuración" de una configuración de rastreo, puede sobrescribir los ajustes de OCR solo para esa configuración de rastreo.

::

    config.tika.tesseract.config=tesseract.properties

``tesseract.properties`` es el nombre de un recurso del classpath, no una ruta del sistema de archivos.
Coloque el archivo en el directorio de configuración de |Fess|, que está en el classpath del rastreador.

- Paquete ZIP: ``app/WEB-INF/classes/``
- Paquete RPM/DEB: ``/etc/fess/``

En ``tesseract.properties``, escriba propiedades de ``TesseractOCRConfig`` de Tika.
Solo se aplican de forma fiable las claves simples, como ``language`` y ``timeoutSeconds``.

::

    language=jpn
    timeoutSeconds=300

Para esa configuración de rastreo, esto tiene prioridad sobre los ajustes globales descritos arriba.

Notas operativas
================

- El OCR consume mucha CPU y ralentiza considerablemente el rastreo. Considere reducir el número de hilos del rastreador o activar el OCR solo en las configuraciones de rastreo que lo necesiten.
- En las configuraciones de rastreo web nuevas, el patrón de URL excluidas predeterminado excluye las URL de imágenes (jpg, png, gif, etc.). Para rastrear imágenes de un sitio web, elimínelas de "URL excluidas del rastreo". El rastreo de archivos incluye las imágenes.
- También se aplican los límites de tamaño del rastreador. Para el límite de tamaño de indexación por tipo de archivo (predeterminado: 10 MB), consulte :doc:`crawler-basic`.
- La precisión del OCR depende de la calidad del escaneo. En general, la escritura a mano no se reconoce bien.
- Los archivos indexados antes de activar el OCR no se procesan con OCR por sí solos. Con el rastreo incremental activado ("Comprobar fecha de última modificación" en :doc:`../admin/general-guide`), un archivo cuya fecha de modificación no ha cambiado no se vuelve a obtener al rastrear de nuevo. Para aplicar el OCR a esos archivos, desactive "Comprobar fecha de última modificación" durante un rastreo, o elimine los documentos del índice y vuelva a rastrear.

Notas de actualización
======================

Hasta la versión 15.8, el ``tika.xml`` incluido excluía ``org.apache.tika.parser.ocr.TesseractOCRParser``.
Desde la versión 15.9, el ``tika.xml`` incluido ya no excluye este analizador.

Si conservó un ``tika.xml`` personalizado, elimine la siguiente línea:

::

    <parser-exclude class="org.apache.tika.parser.ocr.TesseractOCRParser"/>

Si esta línea permanece, el OCR sigue desactivado aunque establezca ``crawler.document.ocr.enabled=true``.

La ubicación de ``tika.xml`` es la siguiente:

- Paquete ZIP: ``app/WEB-INF/conf/tika.xml``
- Paquete RPM/DEB: ``/etc/fess/tika.xml``

Verificación del OCR
====================

1. Cree una configuración de rastreo de archivos para una carpeta que contenga una imagen escaneada (una imagen con texto).
2. Ejecute el rastreo.
3. Busque una palabra que aparezca en la imagen y compruebe que la imagen aparece en los resultados de búsqueda.

Si la imagen no aparece, compruebe lo siguiente:

- ``tesseract --list-langs`` muestra el idioma que usa
- ``crawler.document.ocr.enabled`` es ``true``
- ``tika.xml`` ya no excluye ``TesseractOCRParser``
- El ``fess-crawler.log`` del rastreo muestra ``OCR is enabled`` (la advertencia ``Tesseract OCR is not available`` indica que |Fess| no puede usar Tesseract)
