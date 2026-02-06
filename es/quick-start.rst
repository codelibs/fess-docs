==============
Guia de Configuracion Rapida
==============

Introduccion
========

Esta guia le ayudara a poner en marcha Fess lo mas rapido posible.
Elija el metodo que mejor se adapte a su entorno.

.. tip::

   **Forma mas rapida: Docker (Recomendado)**

   Si tiene Docker instalado, puede tener Fess funcionando en aproximadamente 3 minutos
   con solo unos pocos comandos, sin necesidad de otras dependencias.

----

Inicio rapido con Docker (recomendado)
======================================

Docker proporciona la forma mas rapida y fiable de ejecutar Fess. Todas las dependencias
estan incluidas, por lo que no es necesario instalar nada mas.

**Requisitos:**

- Docker 20.10 o posterior
- Docker Compose 2.0 o posterior

**Paso 1: Descargar los archivos de configuracion**

.. code-block:: bash

    mkdir fess-docker && cd fess-docker
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

**Paso 2: Iniciar los contenedores**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Paso 3: Verificar el acceso**

Espere un par de minutos para que los servicios se inicialicen, luego abra su navegador:

- **Interfaz de busqueda:** http://localhost:8080/
- **Panel de administracion:** http://localhost:8080/admin
- **Credenciales predeterminadas:** admin / admin

.. warning::

   **Aviso de seguridad:** Cambie la contrasena de administrador predeterminada inmediatamente despues de su primer inicio de sesion.

**Paso 4: Detener Fess:**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

Para configuracion avanzada de Docker (ajustes personalizados, OpenSearch externo, Kubernetes),
consulte la `Guia de instalacion con Docker <15.5/install/install-docker.html>`__.

----

Inicio con el paquete ZIP
=========================

.. note::

   Este metodo esta destinado a fines de evaluacion. Para implementaciones en produccion,
   recomendamos usar Docker o instalar con :doc:`paquetes RPM/DEB <setup>`.

Preparacion Previa
------------------

Se requiere **Java 21**. Se recomienda `Eclipse Temurin <https://adoptium.net/temurin>`__.

Verifique su instalacion de Java:

.. code-block:: bash

    java -version

Descarga e Instalacion
-----------------------

1. Descargue el paquete ZIP mas reciente desde `GitHub Releases <https://github.com/codelibs/fess/releases>`__

2. Extraiga e ingrese al directorio:

.. code-block:: bash

    unzip fess-15.5.0.zip
    cd fess-15.5.0

Inicio de Fess
--------------

.. code-block:: bash

    # Linux/Mac
    ./bin/fess

    # Windows
    bin\fess.bat

Espere aproximadamente 30 segundos para que Fess se inicie, luego acceda a:

- http://localhost:8080/ (Busqueda)
- http://localhost:8080/admin (Administracion - usuario: admin/admin)

.. warning::

   Asegurese de cambiar la contrasena predeterminada.
   En entornos de produccion, se recomienda encarecidamente cambiar la contrasena inmediatamente despues del primer inicio de sesion.

Detencion de Fess
-----------------

Presione ``Ctrl+C`` en la terminal, o use ``kill`` para detener el proceso fess.

----

Su primera busqueda: Tutorial rapido
=====================================

Ahora que Fess esta en ejecucion, configuremos su primer rastreo web.

Paso 1: Crear una configuracion de rastreo web
-----------------------------------------------

1. Inicie sesion en el Panel de administracion (http://localhost:8080/admin)
2. Navegue a **Crawler** > **Web** en el menu de la izquierda
3. Haga clic en **Crear nuevo** para crear una nueva configuracion
4. Complete los campos requeridos:

   - **Nombre:** Mi primer rastreo
   - **URL:** https://fess.codelibs.org/ (o cualquier sitio web que desee indexar)
   - **Maximo de accesos:** 100 (limita las paginas a rastrear)
   - **Intervalo:** 1000 (milisegundos entre solicitudes)

5. Haga clic en **Crear** para guardar

Paso 2: Ejecutar el rastreador
------------------------------

1. Vaya a **Sistema** > **Programador**
2. Encuentre **Default Crawler** en la lista
3. Haga clic en **Iniciar ahora**
4. Monitoree el progreso en **Sistema** > **Informacion de rastreo**

Paso 3: Buscar su contenido
----------------------------

Una vez completado el rastreo (verifique WebIndexSize en la informacion de sesion):

1. Visite http://localhost:8080/
2. Ingrese un termino de busqueda relacionado con las paginas rastreadas
3. Vea los resultados de busqueda.

----

Para saber mas
==================

**Listo para profundizar?**

- `Documentacion completa <documentation.html>`__ - Guia de referencia completa
- `Guia de instalacion <setup.html>`__ - Opciones de implementacion en produccion
- `Guia de administracion <15.5/admin/index.html>`__ - Configuracion y gestion
- `Referencia de API <15.5/api/index.html>`__ - Integre la busqueda en sus aplicaciones

**Necesita ayuda?**

- `Foro de discusion <https://discuss.codelibs.org/c/fessen/>`__ - Haga preguntas, comparta consejos
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - Reporte errores, solicite funciones
- `Soporte comercial <support-services.html>`__ - Asistencia profesional

**Explore mas funciones:**

- Rastreo de sistemas de archivos (archivos locales, recursos compartidos de red)
- Integracion con bases de datos
- Autenticacion LDAP/Active Directory
- Clasificacion personalizada de resultados de busqueda
- Soporte multiidioma
