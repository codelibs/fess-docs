==============
Guía de Configuración Rápida
==============

Introducción
========

Esta explicación está destinada a personas que desean probar Fess rápidamente.
Describe los pasos mínimos necesarios para utilizar Fess.

Este procedimiento es un método de inicio para pruebas, por lo que para procedimientos de construcción orientados a la operación, consulte el :doc:`procedimiento de instalación <setup>` utilizando Docker.
(Fess iniciado con este procedimiento está destinado a verificación de operación simple y no se recomienda su uso en este entorno para producción)

Preparación Previa
========

Antes de iniciar Fess, instale Java 21.
Se recomienda `Eclipse Temurin <https://adoptium.net/temurin>`__ para Java 21.

Descarga
============

Descargue el paquete ZIP más reciente de Fess desde el `sitio de lanzamientos de GitHub <https://github.com/codelibs/fess/releases>`__.

Instalación
============

Extraiga el archivo fess-x.y.z.zip descargado.

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

Inicio de Fess
===========

Ejecute el script fess para iniciar Fess.
(En Windows, ejecute fess.bat)

::

    $ ./bin/fess

Acceso a la interfaz de administración
==================

Acceda a \http://localhost:8080/admin.
El nombre de usuario/contraseña de la cuenta de administrador predeterminada es admin/admin.

.. warning::

   Asegúrese de cambiar la contraseña predeterminada.
   En entornos de producción, se recomienda encarecidamente cambiar la contraseña inmediatamente después del primer inicio de sesión.

Creación de configuración de rastreo
================

Después de iniciar sesión, haga clic en "Crawler" > "Web" en el menú de la izquierda.
Haga clic en el botón "Crear nuevo" para crear información de configuración de rastreo web.

Ingrese la siguiente información:

- **Nombre**: Nombre de la configuración de rastreo (ejemplo: Sitio web de la empresa)
- **URL**: URL del objetivo de rastreo (ejemplo: https://www.example.com/)
- **Máximo de accesos**: Límite superior del número de páginas a rastrear
- **Intervalo**: Intervalo de rastreo (milisegundos)

Ejecución del rastreo
============

Haga clic en "Sistema" > "Programador" en el menú de la izquierda.
Puede iniciar el rastreo inmediatamente haciendo clic en el botón "Iniciar ahora" del trabajo "Default Crawler".

Para ejecutarlo según una programación, seleccione "Default Crawler" y configure la programación.
Si la hora de inicio es 10:35 am, use 35 10 \* \* ? (formato: "minuto hora día mes día_semana año").
Después de actualizar, el rastreo comenzará después de esa hora.

Puede verificar si ha comenzado en "Información de rastreo".
Después de completar el rastreo, se mostrará la información de WebIndexSize en la información de sesión.

Búsqueda
====

Después de completar el rastreo, acceda a \http://localhost:8080/ y busque para ver los resultados de búsqueda.

Detención de Fess
===========

Detenga el proceso fess con Ctrl-C o el comando kill.

Para saber más
==================

Consulte la siguiente documentación:

* `Lista de documentación <documentation>`__
* `[Serie] Introducción al servidor de búsqueda de texto completo OSS Fess <https://news.mynavi.jp/techplus/series/_ossfess/>`__
* `Información para desarrolladores <development>`__
* `Foro de discusión <https://discuss.codelibs.org/c/fessja/>`__

