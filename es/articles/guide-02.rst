=============================================
Parte 2: Experiencia de búsqueda en 5 minutos
=============================================

Introducción
============

En la entrega anterior, presentamos la necesidad de una plataforma de búsqueda en el ámbito empresarial y una visión general de Fess.
En este artículo, mostraremos el procedimiento más rápido para iniciar Fess y experimentar la búsqueda.

El objetivo es comprender rápidamente qué tipo de experiencia de búsqueda ofrece Fess.
Usando Docker Compose, levantaremos un entorno de Fess con tan solo unas pocas líneas de comandos, rastrearemos un sitio web y experimentaremos la búsqueda.

Lectores objetivo
=================

- Personas que prueban Fess por primera vez
- Personas que desean realizar rápidamente una PoC (prueba de concepto) para evaluar su implementación
- Personas con conocimientos básicos de operación de Docker

Requisitos del entorno
======================

- Un entorno donde Docker y Docker Compose estén disponibles
- Memoria de 4 GB o más (se recomiendan 8 GB o más)
- Conexión a internet

Preparación previa (en el caso de Linux / WSL2)
------------------------------------------------

OpenSearch, utilizado por Fess, requiere una gran cantidad de áreas de mapeo de memoria al iniciarse.
En entornos Linux o WSL2, aumente el valor de ``vm.max_map_count`` con el siguiente comando.

::

    $ sudo sysctl -w vm.max_map_count=262144

Esta configuración se restablece al reiniciar el sistema operativo. Para hacerla permanente, agréguela a ``/etc/sysctl.conf``.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

.. note::

   Si utiliza Docker Desktop en macOS, esta configuración no es necesaria.

Iniciar Fess
=============

Obtención del archivo Docker Compose
-------------------------------------

El archivo Docker Compose de Fess está publicado en el repositorio de GitHub.
Obténgalo con los siguientes comandos.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

En el directorio compose se encuentran varios archivos de configuración.
Primero, iniciemos con una configuración sencilla.

Inicio
------

Inicie Fess y OpenSearch con el siguiente comando.

::

    $ docker compose up -d

Durante el primer inicio, se descargan las imágenes de Docker, por lo que puede tardar varios minutos.
Puede verificar el estado del inicio con el siguiente comando.

::

    $ docker compose ps

Cuando todos los contenedores muestren el estado "running", el inicio se habrá completado.

Acceder a la pantalla de búsqueda
---------------------------------

Acceda a ``http://localhost:8080/`` desde el navegador.
Si se muestra la pantalla principal de búsqueda de Fess, el sistema se ha iniciado correctamente.

En este punto, el índice está vacío, por lo que las búsquedas no devolverán resultados.
En el siguiente paso, registraremos los objetivos de rastreo y habilitaremos la búsqueda.

Verificar la pantalla de administración
========================================

Inicio de sesión en la pantalla de administración
-------------------------------------------------

Acceda a ``http://localhost:8080/admin/`` e inicie sesión en la pantalla de administración.
Las credenciales predeterminadas son las siguientes.

- Nombre de usuario: ``admin``
- Contraseña: ``admin``

En el panel de control de la pantalla de administración, puede ver el estado general del sistema.

Estructura de la pantalla de administración
-------------------------------------------

En el menú lateral izquierdo de la pantalla de administración, se encuentran las principales funciones de administración de Fess.
Aquí solo revisaremos una descripción general.

**Rastreador**

Es la sección donde se registran los objetivos de búsqueda. Administra la configuración de rastreo para tres tipos: web, sistema de archivos y almacén de datos.

**Sistema**

Funciones de administración del sistema en general, como el programador, el diseño y los diccionarios. En los diccionarios se administran configuraciones relacionadas con la calidad de búsqueda, como sinónimos y palabras vacías (stop words).

**Información del sistema**

Proporciona registros de búsqueda, registros de trabajos, información de rastreo, copias de seguridad y otras funciones de registro y mantenimiento.

Rastrear un sitio web
======================

Registro del objetivo de rastreo
---------------------------------

Rastreemos un sitio web real para que sea posible realizar búsquedas.
Aquí utilizaremos el sitio oficial de Fess como objetivo.

1. En el menú izquierdo de la pantalla de administración, seleccione [Rastreador] > [Web]
2. Haga clic en [Crear nuevo]
3. Ingrese la siguiente información

   - URL: ``https://fess.codelibs.org/ja/``
   - URL objetivo de rastreo: ``https://fess.codelibs.org/ja/.*``
   - Número máximo de accesos: ``50``
   - Número de hilos: ``2``
   - Intervalo: ``10000``

4. Haga clic en [Crear] para guardar

Con esto, se ha completado la configuración para rastrear un máximo de 50 páginas del sitio oficial de Fess (páginas en japonés) con un intervalo de 10 segundos.

Ejecución del rastreo
----------------------

Solo guardar la configuración no inicia el rastreo.
Para iniciar el rastreo, ejecute el trabajo desde el programador.

1. Seleccione [Sistema] > [Programador]
2. Seleccione "Default Crawler"
3. Haga clic en [Iniciar ahora]

El rastreo comenzará.
Puede verificar el progreso desde [Información del sistema] > [Información de rastreo].
Para aproximadamente 50 páginas, el rastreo se completará en unos pocos minutos.

Experimentar la búsqueda
=========================

Realizar una búsqueda
---------------------

Después de completar el rastreo, vuelva a la pantalla de búsqueda ``http://localhost:8080/`` y realice una búsqueda.

Por ejemplo, si ingresa "インストール" (instalación) y busca, se mostrarán como resultados de búsqueda las páginas del sitio de Fess relacionadas con la instalación.

Elementos de la pantalla de resultados de búsqueda
---------------------------------------------------

En la pantalla de resultados de búsqueda se muestran los siguientes elementos.

**Lista de resultados de búsqueda**

Cada resultado muestra el título, la URL y un extracto del texto (snippet).
Las partes que coinciden con las palabras clave de búsqueda se muestran resaltadas.

**Número de resultados y tiempo de respuesta**

En la parte superior de los resultados de búsqueda se muestran el número de coincidencias y el tiempo que tardó la búsqueda.

**Paginación**

Cuando los resultados abarcan múltiples páginas, se muestra una navegación para pasar entre páginas.

Funciones de búsqueda avanzadas
-------------------------------

Fess cuenta con diversas funciones de búsqueda además de la búsqueda simple por palabras clave.

**Búsqueda AND/OR**

Al separar múltiples palabras clave con espacios, se realiza una búsqueda AND.
Usando ``OR``, también es posible realizar una búsqueda OR.

::

    インストール Docker       # Busqueda AND (contiene ambos)
    インストール OR Docker    # Busqueda OR (contiene alguno de los dos)

**Búsqueda por frase**

Al encerrar el texto entre comillas dobles, se buscan documentos que coincidan en ese orden de palabras.

::

    "全文検索サーバー"

**Búsqueda con exclusión**

Para buscar resultados que no contengan una palabra clave específica, utilice el signo menos.

::

    インストール -Windows    # Resultados que no contienen "Windows"

Detención y reanudación del entorno
====================================

Detención
---------

Una vez finalizada la experiencia de búsqueda, detenga el entorno con el siguiente comando.

::

    $ docker compose down

El entorno se detiene conservando los datos (índice), por lo que al reiniciar podrá continuar en el mismo estado.

Limpieza completa, incluyendo los datos
----------------------------------------

Si desea eliminar también los volúmenes, ejecute el siguiente comando.

::

    $ docker compose down -v

En este caso, los índices creados durante el rastreo también se eliminarán.

Lo que revela la experiencia de búsqueda
=========================================

Con la experiencia realizada hasta aquí, hemos verificado el funcionamiento básico de Fess.
Al considerar su uso en el entorno laboral real, pueden surgir algunas preguntas.

- "¿Se pueden incluir los servidores de archivos internos como objetivo de búsqueda?" -> Se aborda en la **Parte 4**
- "¿Se puede integrar un cuadro de búsqueda en el sitio interno existente?" -> Se aborda en la **Parte 3**
- "¿Se puede controlar la información visible por departamento?" -> Se aborda en la **Parte 5**
- "Quiero buscar también en Slack y Confluence" -> Se aborda en la **Parte 6**
- "Quiero que una IA responda preguntas" -> Se aborda en la **Parte 19**

Fess puede manejar todos estos escenarios.
A lo largo de esta serie, presentaremos de forma progresiva cómo lograr cada uno de ellos.

Resumen
=======

En este artículo, iniciamos Fess con Docker Compose y experimentamos desde el rastreo de un sitio web hasta la búsqueda.

- Inicio de Fess + OpenSearch con un solo comando mediante Docker Compose
- Registro de objetivos de rastreo desde la pantalla de administración y ejecución mediante el programador
- Experiencia de búsqueda por palabras clave, búsqueda AND/OR y búsqueda por frase en la pantalla de búsqueda
- Detención y reanudación del entorno de forma sencilla

En la próxima entrega, presentaremos cómo integrar la función de búsqueda de Fess en sitios web o portales existentes.

Referencias
===========

- `Fess <https://fess.codelibs.org/ja/>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__

- `Guía de instalación de Fess <https://fess.codelibs.org/ja/15.5/install/index.html>`__
