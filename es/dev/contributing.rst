========================
Guía de Contribución
========================

¡Damos la bienvenida a las contribuciones al proyecto |Fess|!
Esta página explica cómo contribuir a |Fess|, las directrices de la comunidad,
el procedimiento para crear pull requests, etc.

.. contents:: Índice
   :local:
   :depth: 2

Introducción
======

|Fess| es un proyecto de código abierto que crece gracias a las contribuciones de la comunidad.
Cualquier persona puede contribuir, independientemente de su nivel de experiencia en programación.

Formas de Contribuir
========

Hay varias formas de contribuir a |Fess|.

Contribuciones de Código
----------

- Agregar nuevas funciones
- Corrección de errores
- Mejoras de rendimiento
- Refactorización
- Agregar pruebas

Contribuciones de Documentación
----------------

- Mejora de los manuales de usuario
- Agregar y actualizar documentación de API
- Crear tutoriales
- Traducciones

Reportar Issues
-----------

- Reportes de errores
- Solicitudes de funciones
- Preguntas y sugerencias

Actividades Comunitarias
--------------

- Discusiones en GitHub Discussions
- Responder preguntas en foros
- Escribir artículos de blog y tutoriales
- Presentaciones en eventos

Primera Contribución
==========

Si es la primera vez que contribuye a |Fess|, se recomiendan los siguientes pasos.

Paso 1: Comprender el Proyecto
---------------------------

1. Verificar información básica en el `Sitio Oficial de Fess <https://fess.codelibs.org/ja/>`__
2. Comprender la visión general del desarrollo en :doc:`getting-started`
3. Aprender la estructura del código en :doc:`architecture`

Paso 2: Buscar Issues
-------------------

Busque issues etiquetados con ``good first issue`` en la `página de Issues de GitHub <https://github.com/codelibs/fess/issues>`__.

Estos issues son tareas relativamente fáciles adecuadas para contribuidores principiantes.

Paso 3: Configurar el Entorno de Desarrollo
----------------------------

Configure el entorno de desarrollo siguiendo :doc:`setup`.

Paso 4: Crear una Rama y Trabajar
----------------------------

Cree una rama y comience a codificar siguiendo :doc:`workflow`.

Paso 5: Crear un Pull Request
--------------------------

Haga commit de los cambios y cree un pull request.

Convenciones de Codificación
==============

En |Fess|, seguimos las siguientes convenciones de codificación para mantener un código consistente.

Estilo de Codificación Java
----------------------

Estilo Básico
~~~~~~~~~~

- **Indentación**: 4 espacios
- **Código de nueva línea**: LF (estilo Unix)
- **Codificación**: UTF-8
- **Longitud de línea**: Se recomienda 120 caracteres o menos

Convenciones de Nomenclatura
~~~~~~

- **Paquetes**: Minúsculas, separadas por puntos (ejemplo: ``org.codelibs.fess``)
- **Clases**: PascalCase (ejemplo: ``SearchService``)
- **Interfaces**: PascalCase (ejemplo: ``Crawler``)
- **Métodos**: camelCase (ejemplo: ``executeSearch``)
- **Variables**: camelCase (ejemplo: ``searchResult``)
- **Constantes**: UPPER_SNAKE_CASE (ejemplo: ``MAX_SEARCH_SIZE``)

Comentarios
~~~~~~

**Javadoc:**

Escriba Javadoc para clases, métodos y campos públicos.

.. code-block:: java

    /**
     * Ejecuta una búsqueda.
     *
     * @param query Consulta de búsqueda
     * @return Resultados de búsqueda
     * @throws SearchException Si falla la búsqueda
     */
    public SearchResponse executeSearch(String query) throws SearchException {
        // Implementación
    }

**Comentarios de Implementación:**

Agregue comentarios en japonés o inglés para lógica compleja.

.. code-block:: java

    // Normalización de consultas (conversión de ancho completo a medio ancho)
    String normalizedQuery = QueryNormalizer.normalize(query);

Diseño de Clases y Métodos
~~~~~~~~~~~~~~~~~~~~

- **Principio de responsabilidad única**: Una clase debe tener solo una responsabilidad
- **Métodos pequeños**: Un método debe hacer solo una cosa
- **Nombres significativos**: Los nombres de clases y métodos deben tener intenciones claras

Manejo de Excepciones
~~~~~~

.. code-block:: java

    // Buen ejemplo: Manejo apropiado de excepciones
    try {
        executeSearch(query);
    } catch (IOException e) {
        logger.error("Se produjo un error durante la búsqueda", e);
        throw new SearchException("Error al ejecutar la búsqueda", e);
    }

    // Ejemplo a evitar: Bloque catch vacío
    try {
        executeSearch(query);
    } catch (IOException e) {
        // No hacer nada
    }

Manejo de null
~~~~~~~~~

- No devolver ``null`` siempre que sea posible
- Se recomienda usar ``Optional``
- Indicar explícitamente la posibilidad de null con la anotación ``@Nullable``

.. code-block:: java

    // Buen ejemplo
    public Optional<User> findUser(String id) {
        return Optional.ofNullable(userMap.get(id));
    }

    // Ejemplo de uso
    findUser("123").ifPresent(user -> {
        // Procesamiento cuando el usuario existe
    });

Escritura de Pruebas
~~~~~~~~~~

- Escribir pruebas para todos los métodos públicos
- Los nombres de métodos de prueba comienzan con ``test``
- Usar el patrón Given-When-Then

.. code-block:: java

    @Test
    public void testSearch() {
        // Given: Condiciones previas de la prueba
        SearchService service = new SearchService();
        String query = "test";

        // When: Ejecución del objetivo de la prueba
        SearchResponse response = service.search(query);

        // Then: Verificación de resultados
        assertNotNull(response);
        assertEquals(10, response.getDocuments().size());
    }

Directrices de Revisión de Código
========================

Proceso de Revisión de Pull Requests
----------------------------

1. **Verificación automática**: CI ejecuta automáticamente construcción y pruebas
2. **Revisión de código**: Los mantenedores revisan el código
3. **Retroalimentación**: Solicitud de modificaciones si es necesario
4. **Aprobación**: Se aprueba la revisión
5. **Merge**: El mantenedor fusiona con la rama main

Puntos de Revisión
----------

En la revisión, se verifican los siguientes puntos:

**Funcionalidad**

- ¿Cumple con los requisitos?
- ¿Funciona como se esperaba?
- ¿Se consideran los casos extremos?

**Calidad del Código**

- ¿Sigue las convenciones de codificación?
- ¿Es código legible y mantenible?
- ¿Tiene una abstracción apropiada?

**Pruebas**

- ¿Se han escrito suficientes pruebas?
- ¿Pasan las pruebas?
- ¿Las pruebas realizan verificaciones significativas?

**Rendimiento**

- ¿Hay impacto en el rendimiento?
- ¿El uso de recursos es apropiado?

**Seguridad**

- ¿Hay problemas de seguridad?
- ¿La validación de entrada es apropiada?

**Documentación**

- ¿Se ha actualizado la documentación necesaria?
- ¿El Javadoc está escrito apropiadamente?

Respuesta a Comentarios de Revisión
--------------------

Responda a los comentarios de revisión de manera rápida y cortés.

**Cuando se requieren modificaciones:**

.. code-block:: text

    Gracias por su comentario. Lo he corregido.
    [Breve explicación de las modificaciones]

**Cuando se necesita discusión:**

.. code-block:: text

    Gracias por su opinión.
    Tengo la implementación actual por la razón ○○,
    ¿sería mejor una implementación △△?

Mejores Prácticas de Pull Requests
================================

Tamaño del PR
---------

- Intente hacer PRs pequeños y fáciles de revisar
- Incluir un cambio lógico por PR
- Dividir cambios grandes en múltiples PRs

Título del PR
-----------

Ponga un título claro y descriptivo:

.. code-block:: text

    feat: Agregar función de filtrado de resultados de búsqueda
    fix: Corregir problema de tiempo de espera del crawler
    docs: Actualizar documentación de API

Descripción del PR
-------

Incluya la siguiente información:

- **Contenido del cambio**: Qué se cambió
- **Razón**: Por qué este cambio es necesario
- **Método de prueba**: Cómo se probó
- **Capturas de pantalla**: En caso de cambios en la UI
- **Issue relacionado**: Número de issue (ejemplo: Closes #123)

.. code-block:: markdown

    ## Contenido del Cambio
    Se agregó la funcionalidad para filtrar resultados de búsqueda por tipo de archivo.

    ## Razón
    Debido a que se recibieron numerosas solicitudes de usuarios para
    "buscar solo tipos de archivos específicos".

    ## Método de Prueba
    1. Seleccionar filtro de tipo de archivo en la pantalla de búsqueda
    2. Ejecutar búsqueda
    3. Verificar que solo se muestran resultados del tipo de archivo seleccionado

    ## Issue Relacionado
    Closes #123

Mensajes de Commit
----------------

Escriba mensajes de commit claros y descriptivos:

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**Ejemplo:**

.. code-block:: text

    feat: Agregar función de filtro de búsqueda

    Se permite a los usuarios filtrar resultados de búsqueda por tipo de archivo.

    - Agregar UI de filtro
    - Implementar procesamiento de filtro en backend
    - Agregar pruebas

    Closes #123

Uso de Draft PR
--------------

Cree PRs en progreso como Draft PR,
y cambie a Ready for review cuando esté completo.

.. code-block:: text

    1. Seleccionar "Create draft pull request" al crear PR
    2. Hacer clic en "Ready for review" cuando el trabajo esté completo

Directrices Comunitarias
======================

Código de Conducta
------

En la comunidad de |Fess|, cumplimos con el siguiente código de conducta:

- **Ser respetuoso**: Respetar a todas las personas
- **Ser colaborativo**: Proporcionar retroalimentación constructiva
- **Ser abierto**: Dar la bienvenida a diferentes perspectivas y experiencias
- **Ser cortés**: Esforzarse por usar un lenguaje educado

Comunicación
----------------

**Dónde hacer preguntas:**

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: Preguntas y discusiones generales
- `Rastreador de Issues <https://github.com/codelibs/fess/issues>`__: Reportes de errores y solicitudes de funciones
- `Foro de Fess <https://discuss.codelibs.org/c/FessJA>`__: Foro en japonés

**Cómo hacer preguntas:**

- Hacer preguntas específicas
- Explicar lo que se ha intentado
- Incluir mensajes de error y registros
- Indicar información del entorno (OS, versión de Java, etc.)

**Cómo responder:**

- De manera cortés y amable
- Presentar soluciones concretas
- Proporcionar enlaces a materiales de referencia

Expresión de Gratitud
--------

Expresamos gratitud por las contribuciones.
Incluso pequeñas contribuciones son valiosas para el proyecto.

Preguntas Frecuentes
==========

P: ¿Pueden contribuir los principiantes?
---------------------------

R: ¡Sí, son bienvenidos! Se recomienda comenzar con issues etiquetados con ``good first issue``.
Las mejoras en la documentación también son contribuciones adecuadas para principiantes.

P: ¿Cuánto tiempo tarda en revisarse un pull request?
-------------------------------------------------

R: Generalmente, lo revisamos en unos días.
Sin embargo, puede variar según el horario de los mantenedores.

P: ¿Qué pasa si se rechaza un pull request?
-----------------------------------

R: Verifique la razón del rechazo y puede corregir y volver a enviar si es necesario.
Si tiene alguna pregunta, no dude en hacer preguntas.

P: ¿Qué pasa si se violan las convenciones de codificación?
---------------------------------------

R: Se señalará en la revisión, por lo que no hay problema si lo corrige.
Puede verificarlo de antemano ejecutando Checkstyle.

P: ¿Qué pasa si quiero agregar una función grande?
-------------------------------

R: Se recomienda crear primero un issue y discutir el contenido de la propuesta.
Al obtener un consenso previo, puede evitar trabajo innecesario.

P: ¿Puedo hacer preguntas en japonés?
-------------------------------

R: Sí, puede hacerlo en japonés o inglés.
Fess es un proyecto originado en Japón, por lo que también hay un buen soporte en japonés.

Guía por Tipo de Contribución
================

Mejora de Documentación
----------------

1. Bifurcar el repositorio de documentación:

   .. code-block:: bash

       git clone https://github.com/codelibs/fess-docs.git

2. Realizar cambios
3. Crear pull request

Reporte de Errores
------

1. Buscar issues existentes para verificar duplicados
2. Crear nuevo issue
3. Incluir la siguiente información:

   - Descripción del error
   - Pasos para reproducir
   - Comportamiento esperado
   - Comportamiento actual
   - Información del entorno

Solicitud de Función
------------

1. Crear issue
2. Explicar lo siguiente:

   - Descripción de la función
   - Antecedentes y motivación
   - Método de implementación propuesto (opcional)

Revisión de Código
------------

Revisar pull requests de otras personas también es una contribución:

1. Encontrar PR de interés
2. Revisar el código
3. Proporcionar retroalimentación constructiva

Licencia
========

|Fess| se publica bajo la Apache License 2.0.
El código contribuido también está sujeto a la misma licencia.

Al crear un pull request,
se considera que acepta que su contribución se publique bajo esta licencia.

Agradecimientos
====

¡Gracias por contribuir al proyecto |Fess|!
Su contribución hace que |Fess| sea un mejor software.

Próximos Pasos
==========

Cuando esté listo para contribuir:

1. Configure el entorno de desarrollo con :doc:`setup`
2. Verifique el flujo de desarrollo con :doc:`workflow`
3. Busque issues en `GitHub <https://github.com/codelibs/fess>`__

Materiales de Referencia
======

- `Flujo de GitHub <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `Cómo contribuir al código abierto <https://opensource.guide/ja/how-to-contribute/>`__
- `Cómo escribir buenos mensajes de commit <https://chris.beams.io/posts/git-commit/>`__

Recursos Comunitarios
==================

- **GitHub**: `codelibs/fess <https://github.com/codelibs/fess>`__
- **Discusiones**: `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- **Foro**: `Foro de Fess <https://discuss.codelibs.org/c/FessJA>`__
- **Twitter**: `@codelibs <https://twitter.com/codelibs>`__
- **Sitio Web**: `fess.codelibs.org <https://fess.codelibs.org/ja/>`__
