==============
Flujo de Trabajo de Desarrollo
==============

Esta página explica el flujo de trabajo estándar en el desarrollo de |Fess|.
Puede aprender cómo proceder con el trabajo de desarrollo, como agregar funciones, corregir errores, pruebas y revisión de código.

.. contents:: Índice
   :local:
   :depth: 2

Flujo Básico de Desarrollo
==============

El desarrollo de |Fess| procede con el siguiente flujo:

.. code-block:: text

    1. Verificar/crear issue
       ↓
    2. Crear rama
       ↓
    3. Codificar
       ↓
    4. Ejecutar pruebas locales
       ↓
    5. Hacer commit
       ↓
    6. Hacer push
       ↓
    7. Crear pull request
       ↓
    8. Revisión de código
       ↓
    9. Responder a retroalimentación de revisión
       ↓
    10. Hacer merge

Cada paso se explica en detalle.

Paso 1: Verificar/Crear Issue
=========================

Antes de comenzar el desarrollo, verifique los issues de GitHub.

Verificar Issues Existentes
-----------------

1. Acceda a la `página de Issues de Fess <https://github.com/codelibs/fess/issues>`__
2. Busque un issue en el que desee trabajar
3. Comente en el issue para comunicar que comenzará el trabajo

.. tip::

   Para su primera contribución, se recomienda comenzar con issues etiquetados con ``good first issue``.

Crear Nuevo Issue
-----------------

Para nuevas funciones o correcciones de errores, cree un issue.

1. Haga clic en `New Issue <https://github.com/codelibs/fess/issues/new>`__
2. Seleccione plantilla de issue
3. Complete la información requerida:

   - **Título**: Descripción breve y clara
   - **Descripción**: Antecedentes detallados, comportamiento esperado, comportamiento actual
   - **Pasos de reproducción**: En caso de errores
   - **Información del entorno**: OS, versión de Java, versión de Fess, etc.

4. Haga clic en ``Submit new issue``

Plantilla de Issue
~~~~~~~~~~~~~~~~~~

**Reporte de Error:**

.. code-block:: markdown

    ## Descripción del Problema
    Descripción breve del error

    ## Pasos de Reproducción
    1. ...
    2. ...
    3. ...

    ## Comportamiento Esperado
    Cómo debería ser

    ## Comportamiento Actual
    Cómo es actualmente

    ## Entorno
    - OS:
    - Versión de Java:
    - Versión de Fess:

**Solicitud de Función:**

.. code-block:: markdown

    ## Descripción de la Función
    Descripción de la función a agregar

    ## Antecedentes y Motivación
    Por qué se necesita esta función

    ## Método de Implementación Propuesto
    Cómo implementarla (opcional)

Paso 2: Crear Rama
====================

Cree una rama de trabajo.

Convención de Nomenclatura de Ramas
--------------

Los nombres de ramas siguen el siguiente formato:

.. code-block:: text

    <type>/<issue-number>-<short-description>

**Tipos de type:**

- ``feature``: Agregar nueva función
- ``fix``: Corrección de error
- ``refactor``: Refactorización
- ``docs``: Actualización de documentación
- ``test``: Agregar/modificar pruebas

**Ejemplos:**

.. code-block:: bash

    # Agregar nueva función
    git checkout -b feature/123-add-search-filter

    # Corrección de error
    git checkout -b fix/456-fix-crawler-timeout

    # Actualización de documentación
    git checkout -b docs/789-update-api-docs

Procedimiento de Creación de Rama
----------------

1. Obtener la última rama main:

   .. code-block:: bash

       git checkout main
       git pull origin main

2. Crear nueva rama:

   .. code-block:: bash

       git checkout -b feature/123-add-search-filter

3. Verificar que se creó la rama:

   .. code-block:: bash

       git branch

Paso 3: Codificar
==================

Implemente la función o corrija el error.

Convenciones de Codificación
--------------

En |Fess|, seguimos las siguientes convenciones de codificación.

Estilo Básico
~~~~~~~~~~~~~~

- **Indentación**: 4 espacios
- **Longitud de línea**: Se recomienda 120 caracteres o menos
- **Codificación**: UTF-8
- **Código de nueva línea**: LF (estilo Unix)

Convenciones de Nomenclatura
~~~~~~

- **Nombres de clase**: PascalCase (ejemplo: ``SearchService``)
- **Nombres de método**: camelCase (ejemplo: ``executeSearch``)
- **Constantes**: UPPER_SNAKE_CASE (ejemplo: ``MAX_SEARCH_SIZE``)
- **Variables**: camelCase (ejemplo: ``searchResults``)

Comentarios
~~~~~~

- **Javadoc**: Obligatorio para clases y métodos públicos
- **Comentarios de implementación**: Agregar explicación en japonés o inglés para lógica compleja

**Ejemplo:**

.. code-block:: java

    /**
     * Ejecuta una búsqueda.
     *
     * @param query Consulta de búsqueda
     * @return Resultados de búsqueda
     */
    public SearchResponse executeSearch(String query) {
        // Normalización de consulta
        String normalizedQuery = normalizeQuery(query);

        // Ejecutar búsqueda
        return searchEngine.search(normalizedQuery);
    }

Manejo de null
~~~~~~~~~

- No devolver ``null`` siempre que sea posible
- Se recomienda usar ``Optional``
- Realizar verificación de ``null`` explícitamente

**Ejemplo:**

.. code-block:: java

    // Buen ejemplo
    public Optional<User> findUser(String id) {
        return userRepository.findById(id);
    }

    // Ejemplo a evitar
    public User findUser(String id) {
        return userRepository.findById(id);  // Posibilidad de null
    }

Manejo de Excepciones
~~~~~~

- Capturar y procesar excepciones apropiadamente
- Realizar salida de registro
- Proporcionar mensajes comprensibles para el usuario

**Ejemplo:**

.. code-block:: java

    try {
        // Procesamiento
    } catch (IOException e) {
        logger.error("Error de lectura de archivo", e);
        throw new FessSystemException("Error al leer archivo", e);
    }

Salida de Registro
~~~~~~

Use el nivel de registro apropiado:

- ``ERROR``: Cuando ocurre error
- ``WARN``: Situación que requiere advertencia
- ``INFO``: Información importante
- ``DEBUG``: Información de depuración
- ``TRACE``: Información de rastreo detallada

**Ejemplo:**

.. code-block:: java

    if (logger.isDebugEnabled()) {
        logger.debug("Consulta de búsqueda: {}", query);
    }

Pruebas Durante el Desarrollo
------------

Durante el desarrollo, pruebe de las siguientes maneras:

Ejecución Local
~~~~~~~~~~

Ejecute Fess en IDE o línea de comandos y verifique el funcionamiento:

.. code-block:: bash

    mvn compile exec:java

Ejecución de Depuración
~~~~~~~~~~

Use el depurador del IDE para rastrear el comportamiento del código.

Ejecución de Pruebas Unitarias
~~~~~~~~~~~~~~

Ejecute pruebas relacionadas con los cambios:

.. code-block:: bash

    # Ejecutar clase de prueba específica
    mvn test -Dtest=SearchServiceTest

    # Ejecutar todas las pruebas
    mvn test

Consulte :doc:`building` para más detalles.

Paso 4: Ejecutar Pruebas Locales
=========================

Asegúrese de ejecutar pruebas antes de hacer commit.

Ejecución de Pruebas Unitarias
--------------

.. code-block:: bash

    mvn test

Ejecución de Pruebas de Integración
--------------

.. code-block:: bash

    mvn verify

Verificación de Estilo de Código
--------------------

.. code-block:: bash

    mvn checkstyle:check

Ejecutar Todas las Verificaciones
-------------------

.. code-block:: bash

    mvn clean verify

Paso 5: Hacer Commit
==============

Haga commit de los cambios.

Convención de Mensajes de Commit
--------------------

Los mensajes de commit siguen el siguiente formato:

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**Tipos de type:**

- ``feat``: Nueva función
- ``fix``: Corrección de error
- ``docs``: Solo cambios en documentación
- ``style``: Cambios que no afectan el significado del código (formato, etc.)
- ``refactor``: Refactorización
- ``test``: Agregar/modificar pruebas
- ``chore``: Cambios en proceso de construcción o herramientas

**Ejemplo:**

.. code-block:: text

    feat: Agregar función de filtro de búsqueda

    Se permite a los usuarios filtrar resultados de búsqueda por tipo de archivo.

    Fixes #123

Procedimiento de Commit
----------

1. Preparar cambios:

   .. code-block:: bash

       git add .

2. Hacer commit:

   .. code-block:: bash

       git commit -m "feat: Agregar función de filtro de búsqueda"

3. Verificar historial de commits:

   .. code-block:: bash

       git log --oneline

Granularidad de Commits
------------

- Incluir un cambio lógico por commit
- Dividir cambios grandes en múltiples commits
- Los mensajes de commit deben ser claros y específicos

Paso 6: Hacer Push
==============

Haga push de la rama al repositorio remoto.

.. code-block:: bash

    git push origin feature/123-add-search-filter

Para el primer push:

.. code-block:: bash

    git push -u origin feature/123-add-search-filter

Paso 7: Crear Pull Request
=========================

Cree un pull request (PR) en GitHub.

Procedimiento de Creación de PR
-----------

1. Acceda al `repositorio de Fess <https://github.com/codelibs/fess>`__
2. Haga clic en la pestaña ``Pull requests``
3. Haga clic en ``New pull request``
4. Seleccione rama base (``main``) y rama de comparación (rama de trabajo)
5. Haga clic en ``Create pull request``
6. Complete el contenido del PR (siga la plantilla)
7. Haga clic en ``Create pull request``

Plantilla de PR
---------------

.. code-block:: markdown

    ## Contenido del Cambio
    Qué se cambió en este PR

    ## Issue Relacionado
    Closes #123

    ## Tipo de Cambio
    - [ ] Nueva función
    - [ ] Corrección de error
    - [ ] Refactorización
    - [ ] Actualización de documentación
    - [ ] Otro

    ## Método de Prueba
    Cómo se probó este cambio

    ## Lista de Verificación
    - [ ] El código funciona
    - [ ] Se agregaron pruebas
    - [ ] Se actualizó la documentación
    - [ ] Sigue las convenciones de codificación

Descripción del PR
-------

La descripción del PR debe incluir:

- **Propósito del cambio**: Por qué es necesario este cambio
- **Contenido del cambio**: Qué se cambió
- **Método de prueba**: Cómo se probó
- **Capturas de pantalla**: En caso de cambios en UI

Paso 8: Revisión de Código
====================

Los mantenedores revisan el código.

Puntos de Revisión
------------

En la revisión, se verifican los siguientes puntos:

- Calidad del código
- Cumplimiento de convenciones de codificación
- Suficiencia de pruebas
- Impacto en el rendimiento
- Problemas de seguridad
- Actualización de documentación

Ejemplos de Comentarios de Revisión
------------------

**Aprobación:**

.. code-block:: text

    LGTM (Looks Good To Me)

**Solicitud de modificación:**

.. code-block:: text

    ¿No se necesita verificación de null aquí?

**Sugerencia:**

.. code-block:: text

    Podría ser mejor mover este procesamiento a una clase Helper.

Paso 9: Responder a Retroalimentación de Revisión
===================================

Responda a los comentarios de revisión.

Procedimiento de Respuesta a Retroalimentación
----------------------

1. Leer comentarios de revisión
2. Realizar modificaciones necesarias
3. Hacer commit de cambios:

   .. code-block:: bash

       git add .
       git commit -m "fix: Responder a comentarios de revisión"

4. Hacer push:

   .. code-block:: bash

       git push origin feature/123-add-search-filter

5. Responder al comentario en página de PR

Respuesta a Comentarios
--------------

Siempre responda a los comentarios de revisión:

.. code-block:: text

    Lo he corregido. Por favor, verifique.

O:

.. code-block:: text

    Gracias por su comentario.
    Tengo la implementación actual por la razón ○○, ¿qué le parece?

Paso 10: Hacer Merge
=============

Cuando se aprueba la revisión, el mantenedor hace merge del PR.

Acciones Después del Merge
------------

1. Actualizar rama main local:

   .. code-block:: bash

       git checkout main
       git pull origin main

2. Eliminar rama de trabajo:

   .. code-block:: bash

       git branch -d feature/123-add-search-filter

3. Eliminar rama remota (si no se elimina automáticamente en GitHub):

   .. code-block:: bash

       git push origin --delete feature/123-add-search-filter

Escenarios Comunes de Desarrollo
==================

Agregar Función
------

1. Crear issue (o verificar issue existente)
2. Crear rama: ``feature/xxx-description``
3. Implementar función
4. Agregar pruebas
5. Actualizar documentación
6. Crear PR

Corrección de Error
------

1. Verificar issue de reporte de error
2. Crear rama: ``fix/xxx-description``
3. Agregar prueba que reproduce el error
4. Corregir el error
5. Verificar que las pruebas pasen
6. Crear PR

Refactorización
--------------

1. Crear issue (explicar razón de refactorización)
2. Crear rama: ``refactor/xxx-description``
3. Ejecutar refactorización
4. Verificar que las pruebas existentes pasen
5. Crear PR

Actualización de Documentación
--------------

1. Crear rama: ``docs/xxx-description``
2. Actualizar documentación
3. Crear PR

Consejos de Desarrollo
==========

Desarrollo Eficiente
----------

- **Commits pequeños**: Hacer commit frecuentemente
- **Retroalimentación temprana**: Usar Draft PR
- **Automatización de pruebas**: Usar CI/CD
- **Revisión de código**: Revisar también el código de otros

Resolución de Problemas
--------

Cuando tenga dificultades, use lo siguiente:

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- `Foro de Fess <https://discuss.codelibs.org/c/FessJA>`__
- Comentarios de issues en GitHub

Próximos Pasos
==========

Una vez que comprenda el flujo de trabajo, consulte también los siguientes documentos:

- :doc:`building` - Detalles de construcción y pruebas
- :doc:`contributing` - Directrices de contribución
- :doc:`architecture` - Comprensión del código base

Materiales de Referencia
======

- `Flujo de GitHub <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `Directrices de mensajes de commit <https://chris.beams.io/posts/git-commit/>`__
- `Mejores prácticas de revisión de código <https://google.github.io/eng-practices/review/>`__
