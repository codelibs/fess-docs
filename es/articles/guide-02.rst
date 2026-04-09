============================================================
Parte 2: Experiencia de busqueda en 5 minutos -- Primer contacto con Fess usando Docker Compose
============================================================

Introduccion
============

En la entrega anterior, presentamos la necesidad de una plataforma de busqueda en el ambito empresarial y una vision general de Fess.
En este articulo, mostraremos el procedimiento mas rapido para iniciar Fess y experimentar la busqueda.

El objetivo es comprender rapidamente que tipo de experiencia de busqueda ofrece Fess.
Usando Docker Compose, levantaremos un entorno de Fess con tan solo unas pocas lineas de comandos, rastrearemos un sitio web y experimentaremos la busqueda.

Lectores objetivo
=================

- Personas que prueban Fess por primera vez
- Personas que desean realizar rapidamente una PoC (prueba de concepto) para evaluar su implementacion
- Personas con conocimientos basicos de operacion de Docker

Requisitos del entorno
======================

- Un entorno donde Docker y Docker Compose esten disponibles
- Memoria de 4 GB o mas (se recomiendan 8 GB o mas)
- Conexion a internet

Preparacion previa (en el caso de Linux / WSL2)
------------------------------------------------

OpenSearch, utilizado por Fess, requiere una gran cantidad de areas de mapeo de memoria al iniciarse.
En entornos Linux o WSL2, aumente el valor de ``vm.max_map_count`` con el siguiente comando.

::

    $ sudo sysctl -w vm.max_map_count=262144

Esta configuracion se restablece al reiniciar el sistema operativo. Para hacerla permanente, agreguela a ``/etc/sysctl.conf``.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

.. note::

   Si utiliza Docker Desktop en macOS, esta configuracion no es necesaria.

Iniciar Fess
=============

Obtencion del archivo Docker Compose
-------------------------------------

El archivo Docker Compose de Fess esta publicado en el repositorio de GitHub.
Obtengalo con los siguientes comandos.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

En el directorio compose se encuentran varios archivos de configuracion.
Primero, iniciemos con una configuracion sencilla.

Inicio
------

Inicie Fess y OpenSearch con el siguiente comando.

::

    $ docker compose up -d

Durante el primer inicio, se descargan las imagenes de Docker, por lo que puede tardar varios minutos.
Puede verificar el estado del inicio con el siguiente comando.

::

    $ docker compose ps

Cuando todos los contenedores muestren el estado "running", el inicio se habra completado.

Acceder a la pantalla de busqueda
---------------------------------

Acceda a ``http://localhost:8080/`` desde el navegador.
Si se muestra la pantalla principal de busqueda de Fess, el sistema se ha iniciado correctamente.

En este punto, el indice esta vacio, por lo que las busquedas no devolveran resultados.
En el siguiente paso, registraremos los objetivos de rastreo y habilitaremos la busqueda.

Verificar la pantalla de administracion
========================================

Inicio de sesion en la pantalla de administracion
-------------------------------------------------

Acceda a ``http://localhost:8080/admin/`` e inicie sesion en la pantalla de administracion.
Las credenciales predeterminadas son las siguientes.

- Nombre de usuario: ``admin``
- Contrasena: ``admin``

En el panel de control de la pantalla de administracion, puede ver el estado general del sistema.

Estructura de la pantalla de administracion
-------------------------------------------

En el menu lateral izquierdo de la pantalla de administracion, se encuentran las principales funciones de administracion de Fess.
Aqui solo revisaremos una descripcion general.

**Rastreador**

Es la seccion donde se registran los objetivos de busqueda. Administra la configuracion de rastreo para tres tipos: web, sistema de archivos y almacen de datos.

**Sistema**

Funciones de administracion del sistema en general, como el programador, el diseno y los diccionarios. En los diccionarios se administran configuraciones relacionadas con la calidad de busqueda, como sinonimos y palabras vacias (stop words).

**Informacion del sistema**

Proporciona registros de busqueda, registros de trabajos, informacion de rastreo, copias de seguridad y otras funciones de registro y mantenimiento.

Rastrear un sitio web
======================

Registro del objetivo de rastreo
---------------------------------

Rastreemos un sitio web real para que sea posible realizar busquedas.
Aqui utilizaremos el sitio oficial de Fess como objetivo.

1. En el menu izquierdo de la pantalla de administracion, seleccione [Rastreador] > [Web]
2. Haga clic en [Crear nuevo]
3. Ingrese la siguiente informacion

   - URL: ``https://fess.codelibs.org/ja/``
   - URL objetivo de rastreo: ``https://fess.codelibs.org/ja/.*``
   - Numero maximo de accesos: ``50``
   - Numero de hilos: ``2``
   - Intervalo: ``10000``

4. Haga clic en [Crear] para guardar

Con esto, se ha completado la configuracion para rastrear un maximo de 50 paginas del sitio oficial de Fess (paginas en japones) con un intervalo de 10 segundos.

Ejecucion del rastreo
----------------------

Solo guardar la configuracion no inicia el rastreo.
Para iniciar el rastreo, ejecute el trabajo desde el programador.

1. Seleccione [Sistema] > [Programador]
2. Seleccione "Default Crawler"
3. Haga clic en [Iniciar ahora]

El rastreo comenzara.
Puede verificar el progreso desde [Informacion del sistema] > [Informacion de rastreo].
Para aproximadamente 50 paginas, el rastreo se completara en unos pocos minutos.

Experimentar la busqueda
=========================

Realizar una busqueda
---------------------

Despues de completar el rastreo, vuelva a la pantalla de busqueda ``http://localhost:8080/`` y realice una busqueda.

Por ejemplo, si ingresa "インストール" (instalacion) y busca, se mostraran como resultados de busqueda las paginas del sitio de Fess relacionadas con la instalacion.

Elementos de la pantalla de resultados de busqueda
---------------------------------------------------

En la pantalla de resultados de busqueda se muestran los siguientes elementos.

**Lista de resultados de busqueda**

Cada resultado muestra el titulo, la URL y un extracto del texto (snippet).
Las partes que coinciden con las palabras clave de busqueda se muestran resaltadas.

**Numero de resultados y tiempo de respuesta**

En la parte superior de los resultados de busqueda se muestran el numero de coincidencias y el tiempo que tardo la busqueda.

**Paginacion**

Cuando los resultados abarcan multiples paginas, se muestra una navegacion para pasar entre paginas.

Funciones de busqueda avanzadas
-------------------------------

Fess cuenta con diversas funciones de busqueda ademas de la busqueda simple por palabras clave.

**Busqueda AND/OR**

Al separar multiples palabras clave con espacios, se realiza una busqueda AND.
Usando ``OR``, tambien es posible realizar una busqueda OR.

::

    インストール Docker       # Busqueda AND (contiene ambos)
    インストール OR Docker    # Busqueda OR (contiene alguno de los dos)

**Busqueda por frase**

Al encerrar el texto entre comillas dobles, se buscan documentos que coincidan en ese orden de palabras.

::

    "全文検索サーバー"

**Busqueda con exclusion**

Para buscar resultados que no contengan una palabra clave especifica, utilice el signo menos.

::

    インストール -Windows    # Resultados que no contienen "Windows"

Detencion y reanudacion del entorno
====================================

Detencion
---------

Una vez finalizada la experiencia de busqueda, detenga el entorno con el siguiente comando.

::

    $ docker compose down

El entorno se detiene conservando los datos (indice), por lo que al reiniciar podra continuar en el mismo estado.

Limpieza completa, incluyendo los datos
----------------------------------------

Si desea eliminar tambien los volumenes, ejecute el siguiente comando.

::

    $ docker compose down -v

En este caso, los indices creados durante el rastreo tambien se eliminaran.

Lo que revela la experiencia de busqueda
=========================================

Con la experiencia realizada hasta aqui, hemos verificado el funcionamiento basico de Fess.
Al considerar su uso en el entorno laboral real, pueden surgir algunas preguntas.

- "Se pueden incluir los servidores de archivos internos como objetivo de busqueda?" -> Se aborda en la **Parte 4**
- "Se puede integrar un cuadro de busqueda en el sitio interno existente?" -> Se aborda en la **Parte 3**
- "Se puede controlar la informacion visible por departamento?" -> Se aborda en la **Parte 5**
- "Quiero buscar tambien en Slack y Confluence" -> Se aborda en la **Parte 6**
- "Quiero que una IA responda preguntas" -> Se aborda en la **Parte 19**

Fess puede manejar todos estos escenarios.
A lo largo de esta serie, presentaremos de forma progresiva como lograr cada uno de ellos.

Resumen
=======

En este articulo, iniciamos Fess con Docker Compose y experimentamos desde el rastreo de un sitio web hasta la busqueda.

- Inicio de Fess + OpenSearch con un solo comando mediante Docker Compose
- Registro de objetivos de rastreo desde la pantalla de administracion y ejecucion mediante el programador
- Experiencia de busqueda por palabras clave, busqueda AND/OR y busqueda por frase en la pantalla de busqueda
- Detencion y reanudacion del entorno de forma sencilla

En la proxima entrega, presentaremos como integrar la funcion de busqueda de Fess en sitios web o portales existentes.

Referencias
===========

- `Fess <https://fess.codelibs.org/ja/>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__

- `Guia de instalacion de Fess <https://fess.codelibs.org/ja/15.5/install/index.html>`__
