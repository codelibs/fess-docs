============
Diccionario
============

Descripción general
===================

Aquí se explica la configuración relacionada con los diccionarios.

Realice cambios en los diccionarios después de comprender las especificaciones de cada diccionario.
Si la modificación del diccionario falla, es posible que no se pueda acceder al índice.

Lista
=====

Para abrir la página de lista de diccionarios administrables que se muestra a continuación, haga clic en [Sistema > Diccionario] en el menú izquierdo.


|image0|


Alcance de cada diccionario y cuándo surte efecto
=================================================

Cada diccionario se aplica a campos distintos y surte efecto en un momento
distinto. Si ha editado un diccionario y los resultados de búsqueda no cambian,
consulte primero esta tabla.

.. list-table::
   :header-rows: 1
   :widths: 22 26 28 24

   * - Diccionario
     - Archivo
     - Campos a los que se aplica
     - Cuándo surte efecto
   * - Kuromoji
     - ``ja/kuromoji.txt``
     - Solo los campos ``_ja``, como ``content_ja``
     - Al indexar (es necesario volver a rastrear)
   * - Sinónimos
     - ``synonym.txt``
     - ``content`` y ``title``
     - Al buscar (no es necesario volver a rastrear)
   * - Mapeo (común a todos los idiomas)
     - ``mapping.txt``
     - ``content`` y ``title``
     - Al indexar (es necesario volver a rastrear)
   * - Mapeo (por idioma)
     - ``ja/mapping.txt``
     - Solo los campos ``_ja``, como ``content_ja``
     - Al indexar (es necesario volver a rastrear)
   * - Protwords
     - ``en/protwords.txt``
     - ``content`` y ``title``
     - Al indexar y al buscar
   * - Palabras vacías
     - ``en/stopwords.txt``
     - ``content`` y ``title``
     - Al indexar y al buscar
   * - Sobrescritura de stemmer
     - ``en/stemmer_override.txt``
     - ``content`` y ``title``
     - Al indexar y al buscar

.. note::

   Un analizador se construye cuando se abre el índice, de modo que actualizar
   un archivo de diccionario no surte efecto **hasta que el índice se cierra y
   se vuelve a abrir**. Además, un diccionario que se aplica al indexar no se
   aplica de forma retroactiva a los documentos ya indexados: esos documentos
   deben rastrearse de nuevo.
   Consulte :ref:`dict-apply-changes` para saber cómo aplicar un cambio.

.. warning::

   El diccionario de sustitución de caracteres que se aplica a ``content``, el
   campo con el que se responde la mayoría de las búsquedas, es el
   ``mapping.txt`` de la **raíz**, no ``ja/mapping.txt``. Comparten el nombre
   Mapeo, pero son archivos distintos.

.. _dict-apply-changes:

Aplicar los cambios de diccionario
----------------------------------

Guardar un diccionario no cambia los resultados de búsqueda, por mucho que espere. El plugin
configsync de OpenSearch escribe los diccionarios guardados en sus archivos aproximadamente una vez
por minuto, pero un analizador lee sus diccionarios solo cuando se abre el índice, de modo que un
índice que ya está abierto sigue usando los anteriores. Después de editar diccionarios, recargue el
índice de documentos:

1. Abra [Información del sistema > Mantenimiento] en el menú izquierdo.
2. Haga clic en [Recargar] en «Recargar índice de documentos».

El botón escribe primero los diccionarios guardados en sus archivos y después cierra y vuelve a
abrir el índice al que apunta el alias ``fess.update``, por lo que no es necesario esperar a la
escritura periódica. Un diccionario que se aplica al buscar, como un sinónimo, surte efecto en
cuanto el índice vuelve a estar abierto. Para un diccionario que se aplica al indexar, rastree
además de nuevo los documentos afectados.

.. warning::

   Mientras el índice está cerrado, y hasta que sus fragmentos se vuelven a asignar después de
   abrirlo, no se puede buscar en el índice: las búsquedas fallan o no devuelven resultados.
   Cuanto mayor es el índice, más tarda, así que recárguelo en un momento de poca actividad.

Para hacer lo mismo desde un script sin la pantalla de administración, envíe las mismas operaciones
a OpenSearch::

    curl -X POST "localhost:9200/_configsync/flush"
    curl -X POST "localhost:9200/fess.update/_close"
    curl -X POST "localhost:9200/fess.update/_open"

``_configsync/flush`` escribe de inmediato los diccionarios guardados en sus archivos. Sin esta
llamada, espere al menos un minuto después de guardar antes de cerrar el índice.

El diccionario de usuario de Kuromoji y los resultados de búsqueda
-------------------------------------------------------------------

El campo ``content`` se analiza con el tokenizador estándar y ``cjk_bigram``,
por lo que no depende de cómo Kuromoji segmente una palabra. Registrar una
palabra compuesta japonesa en el diccionario de usuario de Kuromoji y volver a
rastrear no cambia, por tanto, lo que devuelve una búsqueda contra ``content``.
El registro se refleja en ``content_ja``, que se añade a la consulta según el
idioma de la petición.

Kuromoji
========

Administra el diccionario para el análisis morfológico del japonés.
ja/kuromoji.txt es el archivo de diccionario para el análisis morfológico del japonés.

Sinónimos
=========

Administra el diccionario de sinónimos.
synonym.txt es el archivo de diccionario de sinónimos utilizado comúnmente en todos los idiomas.

Mapeo
=====

Administra el diccionario de sustitución de caracteres.
mapping.txt es el archivo de diccionario de sustitución de palabras común a todos los idiomas o para cada idioma.

Protwords
=========

Administra el diccionario de palabras protegidas.
protwords.txt se coloca para cada idioma y es un archivo de lista de palabras que se excluirán del stemming, etc.

Palabras vacías
===============

Administra el diccionario de palabras vacías.
stopwords.txt se coloca para cada idioma y es un archivo de lista de palabras que se excluirán al crear el índice.

Anulación de Stemmer
====================

Administra el diccionario de anulación de Stemmer.
stemmer_override.txt se coloca para cada idioma y es un archivo de diccionario de sustitución de palabras para anular el procesamiento de stemming.


.. |image0| image:: ../../../resources/images/en/15.9/admin/dict-1.png
            :height: 940px
