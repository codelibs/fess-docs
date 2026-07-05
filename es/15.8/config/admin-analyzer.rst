==============================
Configuración del Analyzer
==============================

Acerca del Analyzer
===================

Al crear un índice para búsqueda, es necesario dividir los documentos para registrarlos como índices.
En |Fess|, la función que descompone los documentos en palabras está registrada como Analyzer.
El Analyzer está compuesto por CharFilter, Tokenizer y TokenFilter.

Básicamente, los elementos más pequeños que las unidades divididas por el Analyzer no generarán resultados en una búsqueda.
Por ejemplo, consideremos la oración "東京都に住む" (vivir en Tokio).
Supongamos que esta oración fue dividida por el Analyzer en "東京都" (Tokio), "に" (en), "住む" (vivir).
En este caso, si se realiza una búsqueda con la palabra "東京都" (Tokio), se obtendrán resultados.
Sin embargo, si se realiza una búsqueda con la palabra "京都" (Kioto), no se obtendrán resultados.

|Fess| dispone de un Analyzer dedicado para cada idioma.
Según el sufijo del nombre de campo dentro del índice (por ejemplo, ``content_ja``, ``content_en``), el Analyzer específico del idioma que se aplica cambia automáticamente.

Archivos de definición del Analyzer
=====================================

El Analyzer no dispone de una pantalla de administración propia; los cambios se realizan editando directamente los archivos de configuración.
Los archivos relacionados se encuentran en ``app/WEB-INF/classes/fess_indices/``.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Archivo
     - Contenido
   * - ``fess_indices/fess.json``
     - Configuración del índice de documentos. Contiene las definiciones de CharFilter, Tokenizer, TokenFilter y Analyzer.
   * - ``fess_indices/fess/doc.json``
     - Mapeo del índice de documentos. Asigna el Analyzer que se aplica a cada patrón de nombre de campo, como ``*_ja`` o ``*_en``.
   * - ``fess_indices/fess/<idioma>/``
     - Archivos de diccionario por idioma (por ejemplo, ``ja/kuromoji.txt``, ``ko/nori.txt``, ``en/protwords.txt``, ``en/stemmer_override.txt``, ``stopwords.txt`` para cada idioma).
   * - ``fess_indices/fess/mapping.txt``, ``fess_indices/fess/synonym.txt``
     - Diccionario de mapeo de caracteres y diccionario de sinónimos compartidos por todos los idiomas.

La definición del propio Analyzer (combinación de Tokenizer y TokenFilter) se realiza en ``fess.json``, mientras que la asignación de qué Analyzer se aplica a cada campo se especifica en ``fess/doc.json``.

.. note::
   Cuando se utilizan servicios gestionados como Amazon OpenSearch Service, se usan con prioridad los archivos de configuración correspondientes al tipo de motor de búsqueda, como ``fess_indices/_aws/fess.json`` o ``fess_indices/_cloud/fess.json``.

Registro del Analyzer
=======================

La configuración del Analyzer se registra creando el índice a partir de los archivos de configuración indicados anteriormente, cuando el índice de búsqueda no existe en el momento del inicio de |Fess|.
El índice se crea con un nombre que incluye una marca de tiempo (por ejemplo, ``fess.20240101120000000``), y se le asignan los alias ``fess.search`` y ``fess.update``.

Los marcadores de posición como ``${fess.dictionary.path}`` en los archivos de configuración se sustituyen por los valores reales en el momento de la creación del índice.
La ubicación de los archivos de diccionario puede modificarse mediante la propiedad del sistema ``fess.dictionary.path``.

Si ya existe un índice, se reutiliza la configuración previamente definida.
Por ello, si se modifica la definición del Analyzer, es necesario recrear el índice para que los cambios surtan efecto.

Ajuste mediante diccionarios
==============================

Los diccionarios a los que hace referencia el Analyzer pueden editarse desde la pantalla de administración.

* :doc:`../admin/kuromoji-guide` - Diccionario de usuario para el análisis morfológico del japonés
* :doc:`../admin/synonym-guide` - Diccionario de sinónimos
* :doc:`../admin/mapping-guide` - Mapeo de caracteres
* :doc:`../admin/stopwords-guide` - Palabras vacías (stopwords)
* :doc:`../admin/protwords-guide` - Palabras protegidas
* :doc:`../admin/stemmeroverride-guide` - Sustitución de la derivación (stemming)

Para conocer cómo configurar el Analyzer, consulte la documentación del Analyzer de OpenSearch.

Consideraciones importantes
==============================

La configuración del Analyzer tiene un gran impacto en la búsqueda.
Si va a modificar el Analyzer, hágalo después de comprender el funcionamiento del Analyzer de Lucene, o consulte con el soporte comercial.
