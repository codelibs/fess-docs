=============
Conector JSON
=============

Descripción general
===================

El conector JSON proporciona la funcionalidad para obtener datos de archivos JSON
del sistema de archivos local y registrarlos en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-json``.

Es compatible con los siguientes tres formatos, y de forma predeterminada el formato
se determina automáticamente a partir del contenido del archivo.

- Formato JSON Lines (un objeto JSON por línea)
- Un array de objetos JSON (ya sea con formato legible o compactado en una sola línea)
- Un único objeto JSON

Los registros se leen uno por uno, por lo que incluso con un array grande, el archivo
completo no se mantiene en memoria.

.. note::

   Este conector solo admite archivos JSON en el sistema de archivos local. No admite
   la obtención remota mediante HTTP u otros medios, y si se especifica el parámetro
   ``urls``, esto no se ignora, sino que provoca un error.

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Se requiere acceso a los archivos JSON
3. Es necesario comprender la estructura del JSON

Instalación del plugin
----------------------

Método 1: Instalar desde la pantalla de administración

1. Abrir "Sistema" -> "Plugins"
2. Subir el archivo JAR
3. Reiniciar |Fess|

Método 2: Colocar el archivo JAR directamente

::

    # Descargar desde el repositorio de CodeLibs
    wget https://maven.codelibs.org/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Colocar
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # o
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

.. note::

   A partir de la versión 15.8.0, los JAR se distribuyen en el
   `repositorio de CodeLibs <https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-json/>`_.
   Para la versión 15.7.0 y anteriores, se encuentran en
   `Maven Central <https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/>`_.

Configuración
=============

Configure desde la pantalla de administración en "Crawler" -> "Data Store" -> "Crear nuevo".

Configuración básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Ejemplo
   * - Nombre
     - Products JSON
   * - Nombre del handler
     - JsonDataStore
   * - Habilitado
     - Activado

Configuración de parámetros
---------------------------

Archivo local:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

Múltiples archivos:

::

    files=/var/data/data1.json,/var/data/data2.json
    file_encoding=UTF-8

Especificar un directorio:

::

    directories=/var/data/json_dir/
    file_encoding=UTF-8

Lista de parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Parámetro
     - Valor predeterminado
     - Descripción
   * - ``files``
     -
     - Ruta de los archivos JSON a procesar (se pueden especificar varias, separadas por comas). Se procesan en el orden especificado.
   * - ``directories``
     -
     - Ruta de los directorios que contienen archivos JSON (se pueden especificar varias, separadas por comas).
   * - ``recursive``
     - ``false``
     - Indica si se debe recorrer ``directories`` incluyendo sus subdirectorios.
   * - ``max_depth``
     - ``10``
     - Cuando ``recursive=true``, indica hasta cuántos niveles de profundidad se desciende en cada directorio. Si se especifica ``0``, el comportamiento es el mismo que ``recursive=false``.
   * - ``include_pattern``
     -
     - Expresión regular con la que debe coincidir completamente la ruta absoluta del archivo.
   * - ``exclude_pattern``
     -
     - Expresión regular con la que no debe coincidir la ruta absoluta del archivo.
   * - ``file_suffixes``
     - ``.json,.jsonl``
     - Extensiones de los archivos a procesar (se pueden especificar varias, separadas por comas). No distingue entre mayúsculas y minúsculas.
   * - ``file_encoding``
     - ``UTF-8``
     - Codificación de caracteres del archivo.
   * - ``format``
     - ``auto``
     - Formato del documento. Uno de ``auto``, ``jsonl`` o ``json``.
   * - ``root_path``
     -
     - JSON Pointer que indica la posición desde la que se leen los registros (ejemplo: ``/data/items``).

.. note::

   Los nombres de los parámetros se muestran en snake_case, pero también se pueden usar
   en camelCase de la misma manera (por ejemplo, ``fileEncoding`` en lugar de
   ``file_encoding``).

.. note::

   Especifique al menos uno de ``files`` o ``directories``. Si ambos están vacíos, se
   produce un error. No son excluyentes entre sí: si se especifican ambos, se procesan
   los dos. Aunque el mismo archivo sea alcanzable desde ambos, solo se lee una vez.

Orden de exploración de archivos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Los archivos especificados en ``files`` se procesan en el orden especificado.
- Los archivos encontrados bajo ``directories`` se procesan en orden de fecha de
  modificación, del más antiguo al más reciente.
- Los archivos especificados en ``files`` se procesan antes que los archivos bajo
  ``directories``.

El filtrado mediante ``file_suffixes`` también se aplica a los archivos especificados
directamente en ``files``. Los archivos cuya extensión no coincide se omiten, y el motivo
se registra en el log.

Las rutas inexistentes, los directorios especificados en ``files`` y los archivos
especificados en ``directories`` se registran como advertencias en el log, y el crawl
continúa.

``format``
----------

``auto`` lee el inicio del documento y determina el formato a partir de su sintaxis.
Esto permite la detección correcta con cualquiera de los tres formatos, siempre que el
archivo esté escrito correctamente.

Especifique explícitamente ``format=jsonl`` cuando el archivo esté en formato JSON Lines
y exista la posibilidad de que las líneas cercanas al inicio estén dañadas (líneas de
banner, logs de progreso, registros cortados a mitad de una transferencia, etc.), ya que
la detección automática necesitaría omitir esas líneas para poder determinar el formato.

Esta configuración también determina el alcance del impacto de los registros no válidos.

- **Formato JSON Lines**: como cada línea se analiza de forma independiente, el costo de
  una línea no válida se limita a esa línea. El fallo se registra en las URL fallidas con
  la clave ``<ruta absoluta del archivo>@<número de línea>``, y el procesamiento continúa
  normalmente desde la línea siguiente.
- **El resto de formatos**: como se leen como un flujo de tokens, un único fallo puede
  afectar a los registros posteriores. Un documento cortado a mitad de un objeto no puede
  recuperarse, y si se producen fallos consecutivos un número determinado de veces, el
  procesamiento de ese archivo se interrumpe con una advertencia.

``root_path``
-------------

Si se especifica un JSON Pointer que apunta a un array anidado, sus elementos se
registran como registros.

::

    root_path=/data/items

.. code-block:: json

    { "meta": { "count": 2 }, "data": { "items": [ { "id": "1" }, { "id": "2" } ] } }

- Si apunta a un array, cada uno de sus elementos se convierte en un registro.
- Si apunta a un objeto, ese objeto se convierte en un único registro.
- Si no coincide con ninguna posición, no se produce un error, sino que el número de
  registros resultante es 0.
- Se pueden usar los caracteres de escape de JSON Pointer (``~1`` para ``/`` y ``~0``
  para ``~``).

``root_path`` tiene prioridad sobre ``format``. Esto se debe a que el documento al que se
llega mediante el JSON Pointer no se lee línea por línea; si se especifica junto con
``format=jsonl``, se registra en el log una advertencia al respecto.

.. warning::

   ``root_path`` debe comenzar con ``/``. Si se olvida el ``/`` inicial, como en
   ``data/items``, no puede interpretarse como un JSON Pointer y toda la configuración de
   Data Store termina en error. En este caso, la URL fallida se registra con el nombre de
   la configuración de Data Store, no con el nombre del parámetro, por lo que debe
   identificar el parámetro causante a partir del mensaje
   ``JSON Pointer expression must start with '/'`` en el log.

.. note::

   Si se lee, sin especificar ``root_path``, un documento con formato legible cuyos
   registros abarcan varias líneas (el llamado formato envoltorio, que incluye
   metainformación y un array), se intentará un análisis línea por línea, por lo que no
   se obtendrán los registros previstos y se registrarán fallos. Para este tipo de
   documentos, especifique ``root_path``.

Configuración de scripts
------------------------

Los valores de cada campo se construyen referenciando los valores de cada campo del
objeto JSON. Los campos de nivel superior del objeto JSON pueden referenciarse
directamente en el script como **variables sin prefijo** (no se usa ningún prefijo como
``data.``).

Objeto JSON simple:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description
    digest=description
    host="shop.example.com"
    site="shop.example.com"

Los objetos anidados pueden referenciarse como mapas, y los arrays anidados como listas:

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    first_tag=tags[0]

Campos disponibles
~~~~~~~~~~~~~~~~~~

- ``<nombre_de_campo>`` - Referencia directa por nombre a un campo de nivel superior del
  objeto JSON
- ``<padre>.<hijo>`` - Campo de un objeto anidado
- ``<array>[<índice>]`` - Elemento de un array

.. note::

   Si el valor de un campo es ``null``, ese campo no se registra en el documento.

.. note::

   En |Fess| 15.9, el motor de scripts integrado pasó a ser JavaScript. Groovy se ofrece
   como el plugin ``fess-script-groovy``. El motor a utilizar se especifica mediante el
   parámetro de Data Store ``script_type`` (por ejemplo, ``script_type=javascript``). Si
   se omite, se utiliza ``groovy``. Las referencias simples y la concatenación de cadenas
   como en los ejemplos anteriores funcionan igual en ambos motores, pero el resto de la
   sintaxis difiere según el motor.

Consideraciones
===============

Los parámetros cuyo nombre coincide con ``app.encrypt.property.pattern`` (por defecto,
los que terminan en ``password``, ``key``, ``token`` o ``secret``) se referencian desde
el script como ``null``. Esto evita que las credenciales escritas en los parámetros de
Data Store se copien a los campos del índice.

Si existe un campo con el mismo nombre en el registro, al igual que con los demás
parámetros, tiene prioridad el valor del registro.

.. note::

   La coincidencia se determina mediante una comparación exacta y sensible a mayúsculas
   y minúsculas sobre el nombre del parámetro. ``access_token`` está incluido, pero su
   variante en camelCase, ``accessToken``, no lo está. Si escribe credenciales en los
   parámetros, hágalo en snake_case.

Errores en los parámetros
=========================

Si se especifica un valor no válido para ``format``, ``include_pattern``,
``exclude_pattern`` o ``urls``, el crawl finaliza antes de leer ningún archivo, y se
registra una URL fallida que incluye el nombre del parámetro (por ejemplo,
``JsonDataStore:format``).

Si se especifica un valor no numérico para ``max_depth``, esto se registra en el log y se
utiliza el valor predeterminado.

.. note::

   El crawl de Data Store finaliza como un trabajo exitoso incluso si no se obtiene
   ningún objetivo. Si el número de elementos obtenidos difiere de lo esperado, verifique
   el número de documentos en el índice, las URL fallidas y el archivo
   ``fess-crawler.log``.

Ejemplos de uso
===============

Catálogo de productos
---------------------

Parámetros:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

Script:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description
    digest=category
    host="shop.example.com"
    site="shop.example.com"

Archivo con una respuesta de API guardada
-----------------------------------------

Parámetros:

::

    files=/var/data/response.json
    root_path=/data/items

Script:

::

    url="https://example.com/item/" + id
    title=title
    content=body
    host="example.com"
    site="example.com"

Procesar un directorio de forma recursiva
-----------------------------------------

Parámetros:

::

    directories=/var/data/exports
    recursive=true
    max_depth=3
    include_pattern=.*\.jsonl
    file_encoding=UTF-8

Solución de problemas
=====================

Archivo no encontrado
---------------------

**Síntoma**: en el log aparece ``... does not exist.``, ``... is not a file.`` o
``... is skipped because its suffix is not one of ...``

**Verificaciones**:

1. Verificar que la ruta del archivo sea correcta
2. Confirmar que el archivo existe
3. Verificar que la extensión del archivo coincide con ``file_suffixes`` (por defecto,
   ``.json`` o ``.jsonl``)
4. Verificar que el usuario que ejecuta |Fess| tiene permisos de lectura

Error de análisis de JSON
-------------------------

**Síntoma**: en el log aparece ``Failed to parse ...`` o ``Failed to read ...``, o se
registra una URL fallida

**Verificaciones**:

1. Verificar que el archivo sea JSON válido

   ::

       # Para el formato JSON Lines, verificar que cada línea sea un objeto JSON válido
       cat data.jsonl | jq -c .

       # Para arrays u objetos únicos
       jq . data.json

2. Verificar que la codificación de caracteres sea correcta
3. Verificar que el archivo no esté cortado a mitad
4. Verificar que no contenga comentarios (el estándar JSON no admite comentarios)

No se obtienen datos
--------------------

**Síntoma**: el crawl tiene éxito pero el conteo es 0

**Verificaciones**:

1. Si especifica ``root_path``, verificar que ese JSON Pointer coincide con la
   estructura del documento (si no coincide, no se produce un error, sino que el
   resultado es 0 registros)
2. Verificar que ``include_pattern``, ``exclude_pattern`` o ``file_suffixes`` no estén
   excluyendo todos los objetivos. En ese caso, en el log aparece
   ``No sources to process``
3. Verificar que la configuración del script sea correcta (comprobar que las referencias
   a campos no llevan el prefijo ``data.``)
4. Verificar que los nombres de los campos sean correctos (incluyendo mayúsculas y
   minúsculas)
5. Verificar que ``url`` se construye correctamente. Si ``url`` está vacío, cada registro
   se cuenta como un fallo

Caracteres ilegibles
--------------------

**Síntoma**: los caracteres del documento registrado están corruptos

Si se especifica en ``file_encoding`` una codificación que existe pero es incorrecta, no
se produce un error y el documento se registra con los caracteres corruptos. Verifique la
codificación real del archivo. Si se especifica el nombre de una codificación que no
existe, se registra una URL fallida por cada archivo.

Archivo JSON grande
-------------------

**Síntoma**: memoria insuficiente o timeout

Los registros se leen uno por uno, por lo que el tamaño total del archivo no afecta
directamente al uso de memoria. Sin embargo, pueden surgir problemas cuando un registro
individual es extremadamente grande o cuando la carga del registro en el índice es alta.

**Solución**:

1. Dividir el archivo JSON en varios
2. Aumentar el tamaño del heap de |Fess|

Información de referencia
=========================

- :doc:`ds-overview` - Descripción general de conectores de Data Store
- :doc:`ds-csv` - Conector CSV
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de Data Store
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `JSON Pointer (RFC 6901) <https://datatracker.ietf.org/doc/html/rfc6901>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
