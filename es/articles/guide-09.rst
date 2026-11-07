=====================================================================
Parte 9: Infraestructura de búsqueda para organizaciones multilingües
=====================================================================

Introducción
=============

En las empresas que operan a nivel global o en organizaciones con empleados de diversas nacionalidades, los documentos internos se crean en múltiples idiomas.
Se necesita una infraestructura de búsqueda que pueda manejar adecuadamente documentos en idiomas mixtos, como actas de reuniones en japonés, especificaciones técnicas en inglés e informes de mercado en chino.

En este artículo, asumimos un entorno en el que coexisten documentos en japonés, inglés y chino, y construimos un entorno que permite buscar correctamente documentos en cada idioma.

Público objetivo
=================

- Administradores de organizaciones que manejan documentos multilingües
- Personas que desean mejorar la calidad de búsqueda en idiomas distintos al japonés
- Personas que desean aprender los fundamentos de los Analyzers de búsqueda de texto completo

Escenario
=========

Suponemos una empresa con oficinas en Japón, Estados Unidos y China.

- Oficina de Japón: Crea documentos en japonés (especificaciones, actas de reuniones, informes)
- Oficina de EE. UU.: Crea documentos en inglés (documentos técnicos, materiales de presentación)
- Oficina de China: Crea documentos en chino (investigación de mercado, información de socios comerciales)
- Común: Documentos de políticas globales escritos en inglés

El objetivo es crear un entorno en el que los empleados de cada oficina puedan buscar documentos independientemente del idioma.

Fundamentos de la búsqueda multilingüe
========================================

Procesamiento del lenguaje en la búsqueda de texto completo
-------------------------------------------------------------

Para que un motor de búsqueda de texto completo haga que los documentos sean buscables, necesita dividir el texto en "tokens" (unidades buscables).
Este proceso se denomina "tokenización".

El método de tokenización difiere significativamente según el idioma.

**Inglés**: Las palabras separadas por espacios se convierten directamente en tokens.
Además, se aplica el stemming (por ejemplo, running -> run) y la conversión a minúsculas.

**Japonés**: Dado que las palabras no están separadas por espacios, se utiliza un analizador morfológico (como Kuromoji) para dividir el texto en palabras.
Por ejemplo, una frase se divide así: "servidor de búsqueda de texto completo" -> "texto completo" "búsqueda" "servidor".

**Chino**: Al igual que el japonés, las palabras no están separadas por espacios, por lo que se requiere un tokenizador dedicado. Fess utiliza su propio tokenizador chino para el procesamiento.

Soporte multilingüe de Fess
-----------------------------

Fess utiliza OpenSearch como backend y puede aprovechar los Analyzers multilingües proporcionados por OpenSearch.
En la configuración predeterminada de Fess, el Analyzer japonés (Kuromoji) está habilitado, pero también se admiten otros idiomas.

Fess cuenta con configuraciones de índice que admiten más de 20 idiomas y dispone de una función que detecta automáticamente el idioma de un documento y aplica el Analyzer apropiado.

Configuración por idioma
==========================

Configuración para japonés
----------------------------

Los documentos en japonés se procesan con el Kuromoji Analyzer.
Dado que el japonés se procesa adecuadamente con la configuración predeterminada de Fess, no se requiere ninguna configuración adicional especial.

Sin embargo, la calidad de búsqueda se puede mejorar con las siguientes personalizaciones.

**Diccionario de usuario**

Registre términos específicos de la industria y terminología interna en el diccionario.
Esto se puede configurar seleccionando el diccionario Kuromoji en [Sistema] > [Diccionario] en la consola de administración.

Por ejemplo, esto es útil cuando se desea que un término compuesto sea tratado como un único token en lugar de dividirse en palabras separadas.

**Sinónimos**

Manejo de variaciones de escritura específicas del japonés.

::

    サーバー,サーバ
    データベース,DB,ディービー
    ユーザー,ユーザ,利用者

Configuración para inglés
---------------------------

Los documentos en inglés se procesan automáticamente con el Analyzer apropiado a través del índice multilingüe de Fess.

Las personalizaciones específicas del inglés incluyen las siguientes.

**Palabras vacías (Stop Words)**

Las palabras vacías comunes del inglés (the, a, an, is, are, etc.) se excluyen de forma predeterminada, pero también se pueden agregar palabras vacías específicas de la industria.

**Anulación de Stemmer**

Anule el stemming de palabras específicas.
Esto se puede configurar seleccionando el diccionario de anulación de Stemmer en [Sistema] > [Diccionario] en la consola de administración.

Por ejemplo, esto se utiliza cuando los términos técnicos sufren transformaciones no deseadas.

Configuración para chino
--------------------------

Los documentos en chino utilizan el tokenizador chino propio de Fess.
En el índice multilingüe de Fess, tanto los textos en chino simplificado como en chino tradicional se tokenizan correctamente.

Las consideraciones específicas del chino incluyen las siguientes.

- Correspondencia entre caracteres chinos simplificados y tradicionales
- Soporte de búsqueda mediante entrada Pinyin
- Configuración de sinónimos específicos del chino

Experiencia de búsqueda en un entorno multilingüe
===================================================

Consideraciones de la UI de búsqueda
--------------------------------------

En un entorno multilingüe, la UI de búsqueda también debe adaptarse al idioma del usuario.

Fess dispone de una función que cambia automáticamente el idioma de la UI según la configuración de idioma del navegador.
La UI de la pantalla de búsqueda se ofrece en múltiples idiomas, incluidos japonés, inglés y chino.

Consideraciones sobre la búsqueda entre idiomas
-------------------------------------------------

También existe la necesidad de búsqueda entre idiomas, como "encontrar documentos en inglés usando palabras clave en japonés".
Actualmente, Fess por si solo no admite la búsqueda basada en traducción completamente automática, pero los siguientes métodos pueden abordar parcialmente esta necesidad.

**Configuración de sinónimos multilingües**

Registre traducciones entre japonés e inglés como sinónimos.

::

    会議,meeting,ミーティング
    報告書,report,レポート
    仕様書,specification,スペック

Esto permite que una búsqueda con la palabra japonesa para "reunión" también devuelva documentos en inglés que contengan "meeting".

**Filtrado de idioma con etiquetas**

Configure etiquetas para cada idioma de modo que los usuarios puedan seleccionar el ámbito de idioma de su búsqueda.

- ``lang-ja``: Documentos en japonés
- ``lang-en``: Documentos en inglés
- ``lang-zh``: Documentos en chino

Mejores prácticas de gestión de diccionarios
=============================================

En un entorno multilingüe, la gestión de diccionarios tiene un impacto significativo en la calidad de búsqueda.

Mantenimiento de diccionarios por idioma
------------------------------------------

.. list-table:: Puntos de mantenimiento de diccionarios
   :header-rows: 1
   :widths: 20 40 40

   * - Diccionario
     - Japonés
     - Inglés / Chino
   * - Sinónimos
     - Variaciones de escritura, abreviaturas, términos técnicos
     - Expansión de abreviaturas, sinónimos
   * - Palabras vacías
     - Palabras innecesarias específicas de la industria
     - Palabras innecesarias específicas del dominio
   * - Diccionario de usuario
     - Términos internos, nombres de productos
     - (Específico de Kuromoji)
   * - Protwords (Palabras protegidas)
     - Palabras que no deben someterse a stemming
     - Términos técnicos, nombres propios

Mantenimiento regular de diccionarios
--------------------------------------

Los diccionarios no son algo que se configura una vez y se olvida; necesitan revisarse regularmente.

- Agregar nuevos nombres de productos y proyectos
- Depurar términos que ya no se utilizan
- Agregar nuevos candidatos a sinónimos descubiertos en los registros de búsqueda

Combine esto con el ciclo de ajuste de calidad de búsqueda presentado en la Parte 8 para mantener los diccionarios de forma continua.

Resumen
=======

En este artículo, explicamos cómo construir una infraestructura de búsqueda en un entorno donde coexisten documentos en japonés, inglés y chino.

- Comprensión de los diferentes procesos de tokenización para cada idioma
- Índice multilingüe y configuración de Analyzers de Fess
- Personalización para japonés (Kuromoji), inglés y chino
- Soporte de búsqueda entre idiomas mediante sinónimos multilingües
- Mejores prácticas de gestión de diccionarios

El soporte multilingüe no es algo que se pueda completar con una única configuración; la mejora continua basada en los patrones de uso es importante.

En el próximo artículo, trataremos la operación estable de los sistemas de búsqueda.

Referencias
===========

- `Gestión de diccionarios de Fess <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__

- `OpenSearch Analyzer <https://opensearch.org/docs/latest/analyzers/>`__
