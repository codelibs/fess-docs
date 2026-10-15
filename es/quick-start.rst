==============
Guia de Configuracion Rapida
==============

Introduccion
============

Fess es un servidor de búsqueda de texto completo de código abierto que rastrea sitios web y servidores de archivos, permitiendo la búsqueda cruzada del contenido recopilado.

Esta guía está destinada a quienes desean probar Fess rápidamente, describiendo los pasos mínimos para ponerlo en marcha.

¿Qué metodo usar?
==================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * -
     - Docker (Recomendado)
     - Paquete ZIP
   * - Requisitos previos
     - Docker y Docker Compose
     - Java 21 (OpenSearch se instala con el comando ``fess-setup``)
   * - Facilidad de inicio
     - ◎ Solo unos pocos comandos
     - △ Instalar Java y ejecutar unos pocos comandos de configuración
   * - Ideal para
     - Quienes quieren probarlo primero
     - Quienes no pueden usar Docker en su entorno

Metodo 1: Docker (Recomendado)
================================

Tiempo estimado: **5–10 minutos en el primer inicio** (incluyendo la descarga de la imagen Docker)

Docker proporciona la forma más rápida y fiable de ejecutar Fess. Todas las dependencias
están incluidas, por lo que no es necesario instalar nada más.

**Paso 1: Descargar los archivos de configuracion**

.. code-block:: bash

    mkdir fess-docker && cd fess-docker
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose-opensearch3.yaml

**Paso 2: Iniciar los contenedores**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Paso 3: Acceder a Fess**

Espere un par de minutos para que los servicios se inicialicen, luego abra su navegador:

- **Interfaz de busqueda:** http://localhost:8080/
- **Panel de administracion:** http://localhost:8080/admin
- **Credenciales predeterminadas:** admin / admin

.. warning::

   **Aviso de seguridad:** Cambie la contrasena de administrador predeterminada inmediatamente despues de su primer inicio de sesion.

**Paso 4: Detener Fess**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

Para configuracion avanzada de Docker (ajustes personalizados, OpenSearch externo, Kubernetes),
consulte la :doc:`Guia de instalacion con Docker <15.9/install/install-docker>`.

----

Metodo 2: Paquete ZIP
======================

Tiempo estimado: **20–30 minutos en el primer inicio** (incluyendo la instalación de Java y la descarga de OpenSearch)

Si no desea usar Docker, puede ejecutar Fess directamente desde el paquete ZIP.
Fess no incluye un motor de búsqueda; el comando ``fess-setup`` incluido en el paquete ZIP
descarga OpenSearch e instala los plugins que Fess necesita.

.. note::

   Este metodo esta destinado a fines de evaluacion. Para implementaciones en produccion,
   recomendamos usar Docker o instalar con :doc:`paquetes RPM/DEB <setup>`.

Preparacion Previa
------------------

Instale Java 21 antes de comenzar. Se recomienda `Eclipse Temurin <https://adoptium.net/temurin>`__ para Java 21.
No es necesario instalar OpenSearch de antemano: el Paso 2 lo instala.

.. note::

   OpenSearch publica compilaciones oficiales solo para Linux y Windows. En macOS,
   ``fess-setup install opensearch`` termina con un error; utilice Docker (Método 1) o consulte
   :doc:`15.9/install/install-linux` para instalar OpenSearch con Homebrew.

Paso 1: Descargar y extraer
---------------------------

Descargue el paquete ZIP más reciente desde `GitHub Releases <https://github.com/codelibs/fess/releases>`__,
extráigalo e ingrese al directorio:

.. code-block:: bash

    unzip fess-x.y.z.zip
    cd fess-x.y.z

Paso 2: Instalar OpenSearch
---------------------------

Ejecute ``fess-setup`` como usuario normal, no como ``root``: OpenSearch se niega a iniciarse como ``root``.

.. code-block:: bash

    # Linux
    bin/fess-setup install opensearch

    # Windows
    bin\fess-setup.bat install opensearch

Esto descarga la versión de OpenSearch compatible con este Fess en ``opensearch/`` dentro del
directorio de Fess, instala los cuatro plugins que Fess necesita y agrega los ajustes que Fess requiere a su
``config/opensearch.yml``. ``bin/fess`` encuentra este OpenSearch por sí mismo, por lo que no es necesario
editar ningún archivo de configuración mientras OpenSearch se ejecute en el mismo host.

.. warning::

   El comando establece ``plugins.security.disabled: true``, por lo que OpenSearch acepta solicitudes sin
   autenticación. De forma predeterminada solo escucha en la dirección de loopback; no lo exponga a
   una red. Consulte :doc:`15.9/install/security` para la configuración de producción.

Para ver todos los comandos (instalación de Node.js y plugins, ``check``), consulte :doc:`15.9/install/fess-setup`.

Paso 3: Iniciar OpenSearch y Fess
---------------------------------

Inicie primero OpenSearch y después Fess:

.. code-block:: bash

    # Linux
    opensearch/opensearch-3.9.0/bin/opensearch -d
    bin/fess

.. code-block:: bat

    :: Windows (ejecute cada uno en su propio Símbolo del sistema)
    opensearch\opensearch-3.9.0\bin\opensearch.bat
    bin\fess.bat

Espere aproximadamente 30 segundos para que Fess se inicie, luego acceda a:

- http://localhost:8080/ (Busqueda)
- http://localhost:8080/admin (Administracion - usuario: admin/admin)

Para comprobar la instalación, ejecute ``bin/fess-setup check`` (``bin\fess-setup.bat check`` en Windows).
Informa de si OpenSearch es accesible y tiene los plugins que Fess necesita.

.. warning::

   Asegurese de cambiar la contrasena predeterminada.
   En entornos de produccion, se recomienda encarecidamente cambiar la contrasena inmediatamente despues del primer inicio de sesion.

Detencion de Fess (ZIP)
------------------------

Presione ``Ctrl+C`` en la terminal, o use ``kill`` para detener el proceso fess.
A continuación, detenga OpenSearch de la misma forma (``kill`` a su proceso, o ``Ctrl+C`` si se ejecuta en primer plano).

----

Configuracion de Rastreo y Busqueda
=====================================

**1. Crear una configuracion de rastreo web**

1. Inicie sesion en el Panel de administracion (http://localhost:8080/admin)
2. Navegue a **Crawler** > **Web** en el menu de la izquierda
3. Haga clic en **Crear nuevo** para crear una nueva configuracion
4. Complete los campos requeridos:

   - **Nombre:** Mi primer rastreo
   - **URL:** https://www.example.com/ (URL del sitio a rastrear)
   - **Maximo de accesos:** 10 (para pruebas iniciales, se recomienda un valor pequeño)
   - **Intervalo:** 10000 (milisegundos entre solicitudes; se recomienda el valor predeterminado ``10000`` ms)

5. Haga clic en **Crear** para guardar

.. warning::

   Establecer el Maximo de accesos demasiado alto puede sobrecargar el sitio objetivo.
   Siempre comience con un valor pequeño (alrededor de 10–100) para las pruebas.
   Al rastrear sitios que no administra, siga la configuracion de robots.txt.

**2. Ejecutar el rastreador**

1. Vaya a **Sistema** > **Programador**
2. Encuentre **Default Crawler** en la lista
3. Haga clic en **Iniciar ahora**
4. Monitoree el progreso en **Sistema** > **Informacion de rastreo**

Para ejecucion programada, seleccione **Default Crawler** y configure el horario.
Si la hora de inicio es 10:35 am, ingrese ``35 10 * * ?`` (formato: ``minuto hora dia mes dia_semana``).

**3. Buscar**

Una vez completado el rastreo (verifique WebIndexSize en la informacion de sesion):

Visite http://localhost:8080/ e ingrese un termino de busqueda para ver sus resultados.

----

Para saber mas
==============

- :doc:`Documentacion completa <documentation>` - Guia de referencia completa
- :doc:`Guia de instalacion <setup>` - Opciones de implementacion en produccion
- :doc:`Guia de administracion <15.9/admin/index>` - Configuracion y gestion
- :doc:`Referencia de API <15.9/api/index>` - Integre la busqueda en sus aplicaciones
- `Foro de discusion <https://discuss.codelibs.org/c/fessen/>`__ - Haga preguntas, comparta consejos
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - Reporte errores, solicite funciones
