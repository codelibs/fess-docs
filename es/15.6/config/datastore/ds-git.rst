==================================
Conector Git
==================================

Descripcion general
===================

El conector Git proporciona la funcionalidad para obtener archivos de repositorios Git
y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-git``.

Repositorios compatibles
========================

- GitHub (publico/privado)
- GitLab (publico/privado)
- Bitbucket (publico/privado)
- Repositorios Git locales
- Otros servicios de alojamiento Git

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Para repositorios privados, se requieren credenciales de autenticacion
3. Se necesita acceso de lectura al repositorio

Instalacion del plugin
----------------------

Instale desde la pantalla de administracion en "Sistema" -> "Plugins".

O consulte :doc:`../../admin/plugin-guide` para mas detalles.

Configuracion
=============

Configure desde la pantalla de administracion en "Crawler" -> "Data Store" -> "Crear nuevo".

Configuracion basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Ejemplo
   * - Nombre
     - Project Git Repository
   * - Handler
     - GitDataStore
   * - Habilitado
     - Activado

Configuracion de parametros
---------------------------

Ejemplo de repositorio publico:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Ejemplo de repositorio privado (con autenticacion):

::

    uri=https://username:personal_access_token@github.com/company/private-repo.git
    base_url=https://github.com/company/private-repo/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``uri``
     - Si
     - URI del repositorio Git (para clonar)
   * - ``base_url``
     - Si
     - URL base para visualizacion de archivos
   * - ``extractors``
     - No
     - Configuracion de extractores por tipo MIME
   * - ``prev_commit_id``
     - No
     - ID del commit anterior (para crawl diferencial)
   * - ``delete_old_docs``
     - No
     - Eliminar archivos borrados del indice (predeterminado: ``false``)

Configuracion de scripts
------------------------

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    cache=""
    digest=author.toExternalString()
    anchor=
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

Campos disponibles
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``url``
     - URL del archivo
   * - ``path``
     - Ruta del archivo en el repositorio
   * - ``name``
     - Nombre del archivo
   * - ``content``
     - Contenido de texto del archivo
   * - ``contentLength``
     - Longitud del contenido
   * - ``timestamp``
     - Fecha y hora de ultima modificacion
   * - ``mimetype``
     - Tipo MIME del archivo
   * - ``author``
     - Informacion del ultimo autor del commit

Autenticacion en repositorios Git
=================================

GitHub Personal Access Token
----------------------------

1. Generar Personal Access Token en GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Acceda a https://github.com/settings/tokens:

1. Haga clic en "Generate new token" -> "Generate new token (classic)"
2. Ingrese el nombre del token (ej: Fess Crawler)
3. Marque "repo" en los scopes
4. Haga clic en "Generate token"
5. Copie el token generado

2. Incluir credenciales en la URI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:YOUR_GITHUB_TOKEN@github.com/company/repo.git

GitLab Private Token
--------------------

1. Generar Access Token en GitLab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En GitLab User Settings -> Access Tokens:

1. Ingrese el nombre del token
2. Marque "read_repository" en los scopes
3. Haga clic en "Create personal access token"
4. Copie el token generado

2. Incluir credenciales en la URI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:YOUR_GITLAB_TOKEN@gitlab.com/company/repo.git

Autenticacion SSH
-----------------

Al usar claves SSH:

::

    uri=git@github.com:company/repo.git

.. note::
   Al usar autenticacion SSH, es necesario configurar las claves SSH del usuario que ejecuta |Fess|.

Configuracion de extractores
============================

Extractores por tipo MIME
-------------------------

Especifique extractores por tipo de archivo con el parametro ``extractors``:

::

    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,application/json:textExtractor,

Formato: ``<regex_tipo_MIME>:<nombre_extractor>,``

Extractores predeterminados
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``textExtractor`` - Para archivos de texto
- ``tikaExtractor`` - Para archivos binarios (PDF, Word, etc.)

Solo archivos de texto
~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=text/.*:textExtractor,

Todos los archivos
~~~~~~~~~~~~~~~~~~

::

    extractors=.*:tikaExtractor,

Solo tipos de archivo especificos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Solo Markdown, YAML, JSON
    extractors=text/markdown:textExtractor,text/yaml:textExtractor,application/json:textExtractor,

Crawl diferencial
=================

Crawl solo de cambios desde el ultimo commit
--------------------------------------------

Despues del primer crawl, configure ``prev_commit_id`` con el ID del commit anterior:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    prev_commit_id=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
    delete_old_docs=true

.. note::
   El commit ID debe ser el del ultimo crawl.
   Esto hara que solo se procesen los cambios desde ese commit.

Procesamiento de archivos eliminados
------------------------------------

Al configurar ``delete_old_docs=true``, los archivos eliminados del repositorio Git
tambien se eliminaran del indice.

Ejemplos de uso
===============

Repositorio publico de GitHub
-----------------------------

Parametros:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    delete_old_docs=false

Script:

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    last_modified=timestamp
    mimetype=mimetype

Repositorio privado de GitHub
-----------------------------

Parametros:

::

    uri=https://username:YOUR_GITHUB_TOKEN@github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    delete_old_docs=false

Script:

::

    url=url
    title=name
    content=content
    digest=author.toExternalString()
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

GitLab (self-hosted)
--------------------

Parametros:

::

    uri=https://username:glpat-abc123@gitlab.company.com/team/project.git
    base_url=https://gitlab.company.com/team/project/-/blob/main/
    extractors=text/.*:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Script:

::

    url=url
    host="gitlab.company.com"
    site="gitlab.company.com/team/project/" + path
    title=name
    content=content
    last_modified=timestamp

Solo documentos (archivos Markdown)
-----------------------------------

Parametros:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/markdown:textExtractor,text/plain:textExtractor,
    delete_old_docs=false

Script:

::

    if (mimetype.startsWith("text/")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
    }

Solo directorios especificos
----------------------------

Filtrado con script:

::

    if (path.startsWith("docs/") || path.startsWith("README")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
        mimetype=mimetype
    }

Solucion de problemas
=====================

Error de autenticacion
----------------------

**Sintoma**: ``Authentication failed`` o ``Not authorized``

**Verificaciones**:

1. Verificar que el Personal Access Token sea correcto
2. Confirmar que el token tenga los permisos apropiados (scope ``repo``)
3. Verificar que el formato de la URI sea correcto:

   ::

       # Correcto
       uri=https://username:token@github.com/company/repo.git

       # Incorrecto
       uri=https://github.com/company/repo.git?token=...

4. Verificar la fecha de expiracion del token

Repositorio no encontrado
-------------------------

**Sintoma**: ``Repository not found``

**Verificaciones**:

1. Verificar que la URL del repositorio sea correcta
2. Confirmar que el repositorio existe y no ha sido eliminado
3. Verificar que las credenciales sean correctas
4. Confirmar que tiene acceso al repositorio

No se pueden obtener archivos
-----------------------------

**Sintoma**: El crawl tiene exito pero hay 0 archivos

**Verificaciones**:

1. Verificar que la configuracion de ``extractors`` sea apropiada
2. Confirmar que existen archivos en el repositorio
3. Verificar que la configuracion del script sea correcta
4. Confirmar que existen archivos en la rama objetivo

Error de tipo MIME
------------------

**Sintoma**: Ciertos archivos no se procesan

**Solucion**:

Ajustar la configuracion de extractores:

::

    # Todos los archivos como objetivo
    extractors=.*:tikaExtractor,

    # Agregar tipos MIME especificos
    extractors=text/.*:textExtractor,application/json:textExtractor,application/xml:textExtractor,

Repositorio grande
------------------

**Sintoma**: El crawl toma mucho tiempo o hay memoria insuficiente

**Solucion**:

1. Limitar archivos objetivo con ``extractors``
2. Filtrar solo directorios especificos con script
3. Usar crawl diferencial (configurar ``prev_commit_id``)
4. Ajustar el intervalo de crawl

Especificacion de rama
----------------------

Para crawlear una rama diferente a la predeterminada:

::

    uri=https://github.com/company/repo.git#develop
    base_url=https://github.com/company/repo/blob/develop/

Especifique el nombre de la rama despues de ``#``.

Generacion de URL
=================

Patrones de configuracion de base_url
-------------------------------------

**GitHub**:

::

    base_url=https://github.com/user/repo/blob/master/

**GitLab**:

::

    base_url=https://gitlab.com/user/repo/-/blob/main/

**Bitbucket**:

::

    base_url=https://bitbucket.org/user/repo/src/master/

La URL se genera combinando ``base_url`` con la ruta del archivo.

Generacion de URL en script
---------------------------

::

    url=base_url + path
    title=name
    content=content

O con URL personalizada:

::

    url="https://github.com/mycompany/repo/blob/main/" + path
    title=name
    content=content

Informacion de referencia
=========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `GitHub Personal Access Tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
- `GitLab Personal Access Tokens <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_
