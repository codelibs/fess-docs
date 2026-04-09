===========================================================================
Parte 9: Infraestructura de busqueda para organizaciones multilingues -- Construccion de un entorno para buscar correctamente documentos en japones, ingles y chino
===========================================================================

Introduccion
=============

En las empresas que operan a nivel global o en organizaciones con empleados de diversas nacionalidades, los documentos internos se crean en multiples idiomas.
Se necesita una infraestructura de busqueda que pueda manejar adecuadamente documentos en idiomas mixtos, como actas de reuniones en japones, especificaciones tecnicas en ingles e informes de mercado en chino.

En este articulo, asumimos un entorno en el que coexisten documentos en japones, ingles y chino, y construimos un entorno que permite buscar correctamente documentos en cada idioma.

Publico objetivo
=================

- Administradores de organizaciones que manejan documentos multilingues
- Personas que desean mejorar la calidad de busqueda en idiomas distintos al japones
- Personas que desean aprender los fundamentos de los Analyzers de busqueda de texto completo

Escenario
=========

Suponemos una empresa con oficinas en Japon, Estados Unidos y China.

- Oficina de Japon: Crea documentos en japones (especificaciones, actas de reuniones, informes)
- Oficina de EE. UU.: Crea documentos en ingles (documentos tecnicos, materiales de presentacion)
- Oficina de China: Crea documentos en chino (investigacion de mercado, informacion de socios comerciales)
- Comun: Documentos de politicas globales escritos en ingles

El objetivo es crear un entorno en el que los empleados de cada oficina puedan buscar documentos independientemente del idioma.

Fundamentos de la busqueda multilingue
========================================

Procesamiento del lenguaje en la busqueda de texto completo
-------------------------------------------------------------

Para que un motor de busqueda de texto completo haga que los documentos sean buscables, necesita dividir el texto en "tokens" (unidades buscables).
Este proceso se denomina "tokenizacion".

El metodo de tokenizacion difiere significativamente segun el idioma.

**Ingles**: Las palabras separadas por espacios se convierten directamente en tokens.
Ademas, se aplica el stemming (por ejemplo, running -> run) y la conversion a minusculas.

**Japones**: Dado que las palabras no estan separadas por espacios, se utiliza un analizador morfologico (como Kuromoji) para dividir el texto en palabras.
Por ejemplo, una frase se divide asi: "servidor de busqueda de texto completo" -> "texto completo" "busqueda" "servidor".

**Chino**: Al igual que el japones, las palabras no estan separadas por espacios, por lo que se requiere un tokenizador dedicado. Fess utiliza su propio tokenizador chino para el procesamiento.

Soporte multilingue de Fess
-----------------------------

Fess utiliza OpenSearch como backend y puede aprovechar los Analyzers multilingues proporcionados por OpenSearch.
En la configuracion predeterminada de Fess, el Analyzer japones (Kuromoji) esta habilitado, pero tambien se admiten otros idiomas.

Fess cuenta con configuraciones de indice que admiten mas de 20 idiomas y dispone de una funcion que detecta automaticamente el idioma de un documento y aplica el Analyzer apropiado.

Configuracion por idioma
==========================

Configuracion para japones
----------------------------

Los documentos en japones se procesan con el Kuromoji Analyzer.
Dado que el japones se procesa adecuadamente con la configuracion predeterminada de Fess, no se requiere ninguna configuracion adicional especial.

Sin embargo, la calidad de busqueda se puede mejorar con las siguientes personalizaciones.

**Diccionario de usuario**

Registre terminos especificos de la industria y terminologia interna en el diccionario.
Esto se puede configurar seleccionando el diccionario Kuromoji en [Sistema] > [Diccionario] en la consola de administracion.

Por ejemplo, esto es util cuando se desea que un termino compuesto sea tratado como un unico token en lugar de dividirse en palabras separadas.

**Sinonimos**

Manejo de variaciones de escritura especificas del japones.

::

    サーバー,サーバ
    データベース,DB,ディービー
    ユーザー,ユーザ,利用者

Configuracion para ingles
---------------------------

Los documentos en ingles se procesan automaticamente con el Analyzer apropiado a traves del indice multilingue de Fess.

Las personalizaciones especificas del ingles incluyen las siguientes.

**Palabras vacias (Stop Words)**

Las palabras vacias comunes del ingles (the, a, an, is, are, etc.) se excluyen de forma predeterminada, pero tambien se pueden agregar palabras vacias especificas de la industria.

**Anulacion de Stemmer**

Anule el stemming de palabras especificas.
Esto se puede configurar seleccionando el diccionario de anulacion de Stemmer en [Sistema] > [Diccionario] en la consola de administracion.

Por ejemplo, esto se utiliza cuando los terminos tecnicos sufren transformaciones no deseadas.

Configuracion para chino
--------------------------

Los documentos en chino utilizan el tokenizador chino propio de Fess.
En el indice multilingue de Fess, tanto los textos en chino simplificado como en chino tradicional se tokenizan correctamente.

Las consideraciones especificas del chino incluyen las siguientes.

- Correspondencia entre caracteres chinos simplificados y tradicionales
- Soporte de busqueda mediante entrada Pinyin
- Configuracion de sinonimos especificos del chino

Experiencia de busqueda en un entorno multilingue
===================================================

Consideraciones de la UI de busqueda
--------------------------------------

En un entorno multilingue, la UI de busqueda tambien debe adaptarse al idioma del usuario.

Fess dispone de una funcion que cambia automaticamente el idioma de la UI segun la configuracion de idioma del navegador.
La UI de la pantalla de busqueda se ofrece en multiples idiomas, incluidos japones, ingles y chino.

Consideraciones sobre la busqueda entre idiomas
-------------------------------------------------

Tambien existe la necesidad de busqueda entre idiomas, como "encontrar documentos en ingles usando palabras clave en japones".
Actualmente, Fess por si solo no admite la busqueda basada en traduccion completamente automatica, pero los siguientes metodos pueden abordar parcialmente esta necesidad.

**Configuracion de sinonimos multilingues**

Registre traducciones entre japones e ingles como sinonimos.

::

    会議,meeting,ミーティング
    報告書,report,レポート
    仕様書,specification,スペック

Esto permite que una busqueda con la palabra japonesa para "reunion" tambien devuelva documentos en ingles que contengan "meeting".

**Filtrado de idioma con etiquetas**

Configure etiquetas para cada idioma de modo que los usuarios puedan seleccionar el ambito de idioma de su busqueda.

- ``lang-ja``: Documentos en japones
- ``lang-en``: Documentos en ingles
- ``lang-zh``: Documentos en chino

Mejores practicas de gestion de diccionarios
=============================================

En un entorno multilingue, la gestion de diccionarios tiene un impacto significativo en la calidad de busqueda.

Mantenimiento de diccionarios por idioma
------------------------------------------

.. list-table:: Puntos de mantenimiento de diccionarios
   :header-rows: 1
   :widths: 20 40 40

   * - Diccionario
     - Japones
     - Ingles / Chino
   * - Sinonimos
     - Variaciones de escritura, abreviaturas, terminos tecnicos
     - Expansion de abreviaturas, sinonimos
   * - Palabras vacias
     - Palabras innecesarias especificas de la industria
     - Palabras innecesarias especificas del dominio
   * - Diccionario de usuario
     - Terminos internos, nombres de productos
     - (Especifico de Kuromoji)
   * - Protwords (Palabras protegidas)
     - Palabras que no deben someterse a stemming
     - Terminos tecnicos, nombres propios

Mantenimiento regular de diccionarios
--------------------------------------

Los diccionarios no son algo que se configura una vez y se olvida; necesitan revisarse regularmente.

- Agregar nuevos nombres de productos y proyectos
- Depurar terminos que ya no se utilizan
- Agregar nuevos candidatos a sinonimos descubiertos en los registros de busqueda

Combine esto con el ciclo de ajuste de calidad de busqueda presentado en la Parte 8 para mantener los diccionarios de forma continua.

Resumen
=======

En este articulo, explicamos como construir una infraestructura de busqueda en un entorno donde coexisten documentos en japones, ingles y chino.

- Comprension de los diferentes procesos de tokenizacion para cada idioma
- Indice multilingue y configuracion de Analyzers de Fess
- Personalizacion para japones (Kuromoji), ingles y chino
- Soporte de busqueda entre idiomas mediante sinonimos multilingues
- Mejores practicas de gestion de diccionarios

El soporte multilingue no es algo que se pueda completar con una unica configuracion; la mejora continua basada en los patrones de uso es importante.

En el proximo articulo, trataremos la operacion estable de los sistemas de busqueda.

Referencias
===========

- `Gestion de diccionarios de Fess <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__

- `OpenSearch Analyzer <https://opensearch.org/docs/latest/analyzers/>`__
