==========================
Configuración de Analyzer
==========================

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

La configuración del Analyzer se registra creando el índice fess con app/WEB-INF/classes/fess_indices/fess.json cuando el índice fess no existe en el momento del inicio de |Fess|.
Para obtener información sobre cómo configurar el Analyzer, consulte la documentación del Analyzer de OpenSearch.

La configuración del Analyzer tiene un gran impacto en la búsqueda.
Si va a modificar el Analyzer, hágalo después de comprender el funcionamiento del Analyzer de Lucene, o consulte con el soporte comercial.
