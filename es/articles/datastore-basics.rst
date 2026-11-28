=============================================
Fundamentos del rastreo de almacenes de datos
=============================================

Introducción
============

El contenido de Google Drive, Slack o una base de datos no se puede hacer buscable con el rastreo web ni con el rastreo de archivos.
Un archivo CSV rastreado como archivo también se convierte en un único documento, por lo que no se pueden buscar sus filas por separado.
Fess trata estas fuentes como "almacenes de datos" y las importa registro a registro mediante plugins (conectores de almacén de datos).

La pantalla de configuración de almacenes de datos tiene campos distintos de los de las pantallas de configuración web y de sistema de archivos.
Usted mismo debe indicar qué valores se convierten en la URL, el título, etc., y con los valores predeterminados los documentos se registran de forma que se pueden buscar sin iniciar sesión.
Incluso cuando el procesamiento falla, el trabajo puede mostrarse como "OK".

Este artículo explica, con base en Fess 15.9, los mecanismos comunes a todos los conectores.
Con un pequeño ejemplo que usa un archivo CSV, recorremos todo el proceso: instalación del plugin, configuración, ejecución y comprobación de los resultados.
Para la autenticación y los parámetros de cada conector, consulte los artículos y las referencias que se indican al final.

Diferencias con el rastreo web y de archivos
============================================

En el rastreo web y el rastreo de archivos, Fess sigue enlaces y carpetas y extrae automáticamente el título y el cuerpo de los documentos obtenidos.
En el rastreo de almacenes de datos, un conector lee registros de una API o de un archivo.
Qué valor del registro va a qué campo del índice se escribe en el "Script" de la configuración.

Fess no incluye ningún manejador de almacén de datos.
La lista desplegable "Nombre del manejador" de [Rastreador] > [Almacén de datos] solo muestra los manejadores que proporcionan los plugins ``fess-ds-*`` instalados.

Además, las configuraciones de almacén de datos se diferencian en lo siguiente (se explica en secciones posteriores):

- La pantalla de configuración no tiene el campo "Etiqueta"
- No se aplican las reglas de [Rastreador] > [Impulso de documento]

Instalar el plugin
==================

Aquí usamos como ejemplo el conector CSV ``fess-ds-csv``.
La versión del plugin debe coincidir con la versión menor de Fess que utilice (15.9.x para Fess 15.9).

Para instalarlo desde la consola de administración, haga clic en [Instalar] en [Sistema] > [Plugin].
En la pestaña [Remoto], seleccione ``fess-ds-csv`` en la lista desplegable y haga clic en [Instalar].
Para usar un archivo jar que tenga a mano, utilice la pestaña [Local].

En entornos instalados desde el paquete ZIP o con RPM / DEB, también puede instalarlo desde la línea de comandos.

.. code-block:: bash

    bin/fess-setup install plugin fess-ds-csv:15.9.0

En Docker, añada ``FESS_PLUGINS`` al ``environment`` de ``fess01`` en ``compose.yaml`` para que el plugin se instale al arrancar.
Para varios plugins, sepárelos con espacios (no con comas).

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-csv:15.9.0"

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

En Docker, un plugin instalado desde la consola de administración se guarda dentro del contenedor, por lo que desaparece al volver a crear el contenedor.
En Docker, ``FESS_PLUGINS`` es el método más fiable.
Si cambia una variable de entorno y ejecuta ``up -d``, el contenedor se vuelve a crear.
Para los ajustes que se pierden en ese momento, consulte :doc:`guide-02`.

Si instaló el plugin desde la consola de administración o con ``fess-setup``, reinicie Fess (``FESS_PLUGINS`` instala los plugins antes de que arranque Fess, por lo que no es necesario reiniciar).
Después del reinicio, el plugin está instalado si ``CsvDataStore`` aparece en "Nombre del manejador" en [Rastreador] > [Almacén de datos] > [Crear nuevo].

Los tres campos principales de la pantalla de configuración
===========================================================

Una configuración de almacén de datos gira en torno a tres campos: "Nombre del manejador", "Parámetro" y "Script".

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Campo
     - Contenido
   * - Nombre del manejador
     - El conector que se usa. Ejemplos: ``CsvDataStore``, ``SlackDataStore``
   * - Parámetro
     - Instrucciones para el conector. Un ``clave=valor`` por línea (archivos que leer, destino de conexión, credenciales, etc.)
   * - Script
     - La correspondencia con los campos del índice. Un ``nombre_de_campo=expresión`` por línea

``script_type`` en los parámetros
---------------------------------

En la pantalla de creación, el campo "Parámetro" ya contiene ``script_type=javascript``.
Esto indica que las expresiones del campo "Script" se evalúan como JavaScript.
Conserve esta línea y añada los parámetros del conector debajo.

Si elimina la línea ``script_type``, el script se evalúa como Groovy (el valor predeterminado, para que las configuraciones creadas antes de la 15.9 sigan funcionando).
Para evaluar con Groovy se necesita el plugin ``fess-script-groovy``.
Está incluido en la imagen Docker estándar, pero no en la imagen slim.
En un entorno sin el plugin, la evaluación de las líneas que contienen una expresión falla con el error ``groovy is not found`` y el registro no se indexa (una línea cuyo lado derecho es solo un nombre de elemento, como ``title=subject``, usa el valor tal cual sin pasar por un motor de scripts).
Por el contrario, con la imagen Docker estándar la configuración sigue funcionando con Groovy aunque elimine la línea, lo que hace que el problema pase desapercibido.
Cuando pegue en el campo "Parámetro" un ejemplo de la referencia de un conector, procure no eliminar la línea ``script_type=javascript``.

Cómo escribir el script
-----------------------

Cada línea del campo "Script" tiene a la izquierda el nombre de un campo del índice y a la derecha una expresión JavaScript.
Encierre las cadenas entre comillas dobles.
No ponga punto y coma al final de la línea.
Con punto y coma, el valor de la expresión pasa a ser ``null`` y el campo no se establece.
No aparece ningún error ni mensaje de registro, así que solo lo notará porque el campo está vacío (para más detalles, consulte la "Guía de scripting JavaScript" en las referencias del final).

Los nombres de elementos que puede usar en el lado derecho dependen del conector.

- Los conectores de CSV, JSON y bases de datos hacen referencia directamente a los nombres de columna y de campo (en CSV también se puede usar ``cell1``, ``cell2``, etc.)
- Muchos conectores de servicios en la nube pasan el objeto obtenido con un prefijo. Por ejemplo, Box, Google Drive y OneDrive usan ``file.*``; Slack, ``message.*``; Jira, ``issue.*``, y Salesforce, ``object.*``

Compruebe los nombres de elementos disponibles en la descripción del script de la referencia de cada conector (``https://fess.codelibs.org/es/stable/config/datastore/ds-<nombre>.html``).
Si hace referencia a un nombre no definido, por ejemplo ``url`` en lugar de ``file.url``, la evaluación de la expresión falla y el registro no se indexa.

Ejemplo: hacer buscable un archivo CSV
======================================

En este ejemplo, unas preguntas frecuentes (FAQ) internas se mantienen en un archivo CSV y las hacemos buscables.
Guarde el siguiente contenido en UTF-8 como ``faq.csv``.

.. code-block:: text

    faq_id,question,answer
    1,¿Cuál es la fecha límite para los gastos?,Presente sus gastos antes de fin de mes.
    2,¿Cómo me conecto a los sistemas internos desde fuera?,Conéctese mediante el cliente VPN.
    3,¿Qué hago si pierdo la tarjeta de acceso?,Contacte con el departamento de Administración para solicitar una nueva.

Un archivo CSV guardado con Excel a menudo no está en UTF-8, sino en una codificación heredada de Windows: por ejemplo, windows-1252 con Excel en español o MS932 con Excel en japonés.
En ese caso, indique la codificación en los parámetros que se muestran más adelante, por ejemplo ``file_encoding=windows-1252`` o ``file_encoding=MS932``.
Coloque el archivo en una ruta que el rastreador de Fess pueda leer.
El rastreador se ejecuta en el mismo servidor que Fess, así que en un entorno ZIP o RPM / DEB, colóquelo en un directorio que pueda leer el usuario que ejecuta Fess.
Si solo quiere probarlo con Docker, lo más sencillo es copiarlo dentro del contenedor (desaparece al volver a crear el contenedor).

.. code-block:: bash

    docker cp faq.csv fess01:/tmp/faq.csv

En [Rastreador] > [Almacén de datos], haga clic en [Crear nuevo] e introduzca lo siguiente.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Valor
   * - Nombre
     - FAQ interna
   * - Nombre del manejador
     - ``CsvDataStore``
   * - Parámetro
     - Véase más abajo
   * - Script
     - Véase más abajo
   * - Permisos
     - Dejar ``{role}guest`` (las FAQ se pueden buscar sin iniciar sesión)

Parámetro:

.. code-block:: properties

    script_type=javascript
    files=/tmp/faq.csv
    file_encoding=UTF-8
    has_header_line=true

Script:

.. code-block:: javascript

    url="https://intranet.example.com/faq/" + faq_id
    title=question
    content=question + " " + answer
    digest=answer
    label="faq"

Con ``has_header_line=true``, los nombres de columna de la primera línea (``faq_id``, ``question``, ``answer``) se pueden usar en el script.
En ``url``, indique la URL de una página que pueda mostrar el registro; es la que se abre al hacer clic en el enlace de los resultados de búsqueda.
La URL de este ejemplo es ficticia.
Sustitúyala por la URL de su página de FAQ real.

Después de guardar con [Crear], cree y ejecute un trabajo como se describe en la sección "Programación" más abajo y compruebe el resultado como se describe en la sección "Comprobar los resultados".
Si todo funciona, al buscar "VPN" en la página de búsqueda sin haber iniciado sesión (o en una ventana privada del navegador) se encuentra la segunda entrada de las FAQ.
Los documentos con ``{role}guest`` se muestran a los usuarios que no han iniciado sesión y a los usuarios que tienen el rol ``guest`` (incluido el usuario inicial ``admin``). No se muestran si ha iniciado sesión con cualquier otro usuario.

Para mostrar la etiqueta ``faq`` en los filtros de la página de búsqueda, cree en [Rastreador] > [Etiqueta] una etiqueta cuyo "Valor" sea ``faq`` (consulte la siguiente sección, "Etiquetas").

Campos del índice
=================

Los campos que se suelen establecer en el script son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Campo
     - Descripción
   * - ``url``
     - Obligatorio. Destino del enlace en los resultados de búsqueda. Debe ser único para cada registro
   * - ``title``
     - Título en los resultados de búsqueda. Se puede buscar
   * - ``content``
     - Cuerpo. Se puede buscar
   * - ``digest``
     - Resumen que se muestra en los resultados de búsqueda
   * - ``label``
     - Valor de la etiqueta (se explica más adelante)
   * - ``role``
     - Roles que pueden ver el documento. Se usa cuando el conector proporciona ACL (se explica más adelante)

Además, ``config_id``, ``boost``, ``role``, ``virtual_host``, ``mimetype`` y otros campos se establecen automáticamente (``boost``, ``role`` y ``virtual_host`` son los valores de "Valor de impulso", "Permisos" y "Hosts virtuales" de la pantalla de configuración).
Si el script especifica el mismo campo, el valor del script lo sobrescribe.

Tenga en cuenta lo siguiente sobre ``url``.

- Un registro cuya expresión da ``null`` no se indexa. El conector CSV no registra esas filas como URL de fallo; solo escribe en ``fess-crawler.log`` una línea WARN con el número de filas
- El ID de documento se genera a partir de la URL, los roles y el host virtual. Los registros cuyo ``url`` es una cadena vacía, o los que tienen el mismo ``url``, obtienen el mismo ID de documento si también coinciden los roles y el host virtual; se sobrescriben entre sí y solo queda el último

Permisos
========

En la pantalla de creación, "Permisos" ya contiene ``{role}guest``.
Este valor se convierte en el rol de todos los documentos registrados desde ese almacén de datos.
El rol de invitado se asigna a los usuarios que no han iniciado sesión, así que, tal cual, los documentos se pueden buscar sin iniciar sesión.
Para datos que pueden ser públicos, como unas FAQ internas, puede dejarlo así.

Para datos cuyos lectores quiera restringir, controle el acceso de una de las siguientes formas.

- Cambie el campo "Permisos" por los grupos o roles que deben ver los datos (por ejemplo, ``{group}sales``). Todos los documentos del almacén de datos reciben los mismos permisos
- Si el conector genera roles a partir de la configuración de uso compartido (ACL) del servicio de origen, asígnelos en el script, por ejemplo ``role=file.roles``. El nombre del elemento depende del conector (``message.roles`` en Slack), y algunos conectores necesitan parámetros adicionales para obtener las ACL (como ``permission_sync=true`` en Slack). Consulte la referencia de cada conector

Si usa ACL, elimine ``{role}guest`` del campo "Permisos".
Conectores como Box, Slack y Microsoft 365 (OneDrive) también incluyen el valor del campo "Permisos" en ``file.roles`` / ``message.roles``.
Por eso, si deja ``{role}guest``, los documentos siguen pudiéndose buscar sin iniciar sesión aunque haya configurado las ACL.

Por el contrario, si deja vacío el campo "Permisos" y tampoco establece ``role`` en el script, los documentos no reciben ningún rol.
Esos documentos no se muestran a nadie en la página de búsqueda.

Los roles se escriben al registrar los documentos.
Si cambia los permisos o el script, los documentos existentes no se actualizan hasta que se vuelvan a rastrear.
El diseño de roles y grupos se explica en :doc:`guide-05`.

Etiquetas
=========

La pantalla de configuración de almacenes de datos no tiene el campo "Etiqueta" que sí tienen las pantallas de configuración web y de sistema de archivos.
Para asignar etiquetas, use una de las siguientes opciones.

- Escriba en el script, por ejemplo, ``label="faq"``. La etiqueta se asigna a todos los documentos de ese almacén de datos
- En [Rastreador] > [Etiqueta], escriba en "Rutas incluidas" una expresión regular que coincida con las URL de los documentos. Al registrar, la URL se compara con esta expresión regular y la etiqueta se asigna a los documentos que coinciden

"Rutas incluidas" se evalúa como coincidencia con la URL completa, así que para una coincidencia por prefijo añada ``.*`` al final (por ejemplo, ``https://intranet\.example\.com/faq/.*``).

Nota: una etiqueta asignada en el script se pierde si al menos una etiqueta de [Rastreador] > [Etiqueta] coincide con la URL del documento; solo quedan las etiquetas que coinciden.
Las etiquetas creadas para el rastreo web (por ejemplo, ``https://intranet\.example\.com/.*``) y las que solo definen "Rutas excluidas" también se tienen en cuenta.
Si asigna etiquetas en el script, compruebe que ninguna etiqueta coincida con las URL de los documentos.

Indique el "Valor" de una etiqueta solo con caracteres alfanuméricos y guiones bajos (no se admiten guiones ni caracteres no ASCII, como los del japonés).
Para que la etiqueta aparezca entre las opciones de etiqueta de la página de búsqueda, registre una etiqueta con el mismo valor en [Rastreador] > [Etiqueta], aunque la asigne en el script.
En ese caso, "Rutas incluidas" puede quedar vacío.

Valor de impulso
================

El "Valor de impulso" de la pantalla de configuración de almacenes de datos (predeterminado ``1.0``) se aplica a todos los documentos registrados desde ese almacén de datos.
El valor de impulso se multiplica por la puntuación en el momento de la búsqueda.
Para que los documentos de una fuente de datos concreta aparezcan más arriba, cambie este valor de impulso.

Las reglas de [Rastreador] > [Impulso de documento] solo se aplican a los documentos registrados mediante el rastreo web y el rastreo de archivos.
No se aplican a los documentos de los almacenes de datos.

Programación
============

El trabajo predeterminado "Default Crawler" se ejecuta todos los días a las 0:00 y rastrea todas las configuraciones web, de sistema de archivos y de almacén de datos habilitadas.
Para ejecutar cada almacén de datos con una frecuencia distinta, cree un trabajo para cada configuración.

1. En la lista de [Rastreador] > [Almacén de datos], haga clic en el nombre de la configuración para abrir la pantalla de detalles
2. Haga clic en [Crear nuevo trabajo]. Se abre la pantalla de creación del programador con "Nombre" (``Data Crawler - FAQ interna``) y un script que rastrea solo esta configuración ya rellenados
3. Introduzca la hora de ejecución en "Programación" en formato cron (minuto hora día mes día-de-la-semana) y haga clic en [Crear]. Ejemplo: ``0 2 * * *`` (todos los días a las 2:00)

Un trabajo con la "Programación" vacía no se ejecuta periódicamente; solo se ejecuta manualmente.
Para probarlo de inmediato, abra el trabajo creado en [Sistema] > [Programador] y haga clic en [Iniciar ahora].

Aunque cree un trabajo para una configuración, "Default Crawler" sigue rastreando también esa configuración.
Para evitar que se ejecute dos veces, deshabilite el "Estado" de esa configuración de almacén de datos.
"Default Crawler" solo procesa las configuraciones habilitadas, pero un trabajo que especifica un ID de configuración también rastrea las deshabilitadas.
Si crea un trabajo propio para cada configuración, también puede dejar vacía la "Programación" de "Default Crawler" (consulte :doc:`guide-04`).

Caducidad de los documentos
===========================

Los documentos registrados desde un almacén de datos tienen una fecha de caducidad.
Es la hora de inicio de ese rastreo más el número de días de "Eliminar documentos anteriores" en [Sistema] > [General] (``3`` días de forma predeterminada).
El trabajo "Doc Purger", que se ejecuta cada minuto, elimina del índice los documentos caducados.
Cuando el mismo documento se vuelve a registrar en el siguiente rastreo, su caducidad se amplía.

Por ello, los documentos desaparecen de los resultados de búsqueda en los dos casos siguientes.

- El intervalo entre ejecuciones del trabajo es más largo que el número de días de "Eliminar documentos anteriores"
- En un rastreo incremental que solo lee los elementos modificados (como ``incremental=true`` en Git o Google Drive), los documentos sin cambios no se vuelven a registrar

Para cambiar la caducidad por configuración, indique ``time_to_live`` en minutos en los parámetros (por ejemplo, ``time_to_live=11520`` para 8 días).
Los elementos eliminados de los datos de origen tampoco desaparecen de los resultados de búsqueda hasta que vence este plazo.
Si el plazo es demasiado largo, las eliminaciones tardan mucho en reflejarse.

Comprobar los resultados
========================

En el rastreo de almacenes de datos, un estado de trabajo "OK" no significa necesariamente que todo haya ido bien.
Aunque se produzca una excepción en el conector, Fess la registra por configuración o por registro y continúa el procesamiento.
Por eso el estado del registro de trabajos es "OK", y el "Estado del rastreador" de [Información del sistema] > [Información de rastreo] tampoco cambia.
Compruebe lo siguiente en orden.

1. En [Información del sistema] > [Registro de trabajo], confirme que el trabajo ha terminado. La línea ``Data Config Id:`` del "Resultado" muestra el ID de la configuración en cuestión
2. En [Información del sistema] > [Información de rastreo], compruebe el "Tamaño del índice (Almacén de datos)" de la sesión. Es el número de documentos registrados en esa sesión (en "Default Crawler", el total de todos los almacenes de datos)
3. En [Información del sistema] > [URL de fallo], compruebe que no se haya registrado ningún error
4. Descargue ``fess-crawler.log`` desde [Información del sistema] > [Archivo de registro] y revise las líneas ERROR y WARN (está en ``/var/log/fess/`` en Docker y RPM / DEB, y en ``logs/`` en el paquete ZIP)
5. En [Información del sistema] > [Búsqueda], busque por ejemplo ``label:faq`` y compruebe el número de resultados

El lugar donde quedan las pistas depende de cómo falle el rastreo.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Situación
     - URL de fallo
     - fess-crawler.log
   * - No se encuentra el manejador (por ejemplo, si se eliminó el plugin después de crear la configuración)
     - Sin registro
     - ``DataStore(...) is not found.``
   * - Falla toda la configuración (un error de autenticación que impide continuar al conector, falta un parámetro obligatorio, etc.)
     - Una entrada. La columna URL contiene ``D<ID de configuración>:<nombre de configuración>``
     - ``Failed to process a data crawling: <nombre de configuración>``
   * - Falla un registro (un error de evaluación del script, etc.)
     - Una por registro. En CSV, ``<ruta del archivo>:<número de línea>``
     - Líneas WARN

Con el conector CSV, tampoco se produce un error si no se encuentra el archivo indicado en ``files`` o si su extensión no es ``.csv`` / ``.tsv``.
El conector emite los mensajes WARN ``is not found.`` y ``No CSV file.`` y termina con 0 documentos.

[Información del sistema] > [Búsqueda] muestra todos los documentos sin filtrar por permisos, por lo que resulta adecuado para comprobar el número de documentos.
En cambio, no sirve para comprobar si los permisos son los previstos.
Compruebe los permisos en la página de búsqueda normal, con la sesión iniciada como el usuario en cuestión (o sin iniciar sesión, para los documentos con ``{role}guest``) (:doc:`guide-05`).

Si no sabe qué nombres de elementos pasa un conector, algunos conectores escriben en el registro los valores obtenidos cuando se establece el nivel de registro del rastreador en DEBUG (el conector CSV muestra los valores de cada fila).
Para saber cómo configurarlo, consulte "Configuración de Depuración" en `Descripción General de los Conectores de Almacén de Datos <https://fess.codelibs.org/es/stable/config/datastore/ds-overview.html>`__.

Artículos y referencias por conector
====================================

La configuración de cada conector se explica en los siguientes artículos.

- :doc:`guide-06` - Git, Confluence, Jira, Slack
- :doc:`guide-07` - Google Drive, SharePoint Online / OneDrive, Box
- :doc:`guide-12` - Bases de datos, CSV, Salesforce

Referencias:

- `Descripción General de los Conectores de Almacén de Datos <https://fess.codelibs.org/es/stable/config/datastore/ds-overview.html>`__ (lista de todos los conectores y nombres de los plugins)
- `Conector CSV <https://fess.codelibs.org/es/stable/config/datastore/ds-csv.html>`__ / `Conector JSON <https://fess.codelibs.org/es/stable/config/datastore/ds-json.html>`__ / `Conector de Base de Datos <https://fess.codelibs.org/es/stable/config/datastore/ds-database.html>`__
- `Google Drive <https://fess.codelibs.org/es/stable/config/datastore/ds-gsuite.html>`__ / `Microsoft 365 <https://fess.codelibs.org/es/stable/config/datastore/ds-microsoft365.html>`__ / `Box <https://fess.codelibs.org/es/stable/config/datastore/ds-box.html>`__
- `Atlassian <https://fess.codelibs.org/es/stable/config/datastore/ds-atlassian.html>`__ / `Slack <https://fess.codelibs.org/es/stable/config/datastore/ds-slack.html>`__ / `Git <https://fess.codelibs.org/es/stable/config/datastore/ds-git.html>`__ / `Salesforce <https://fess.codelibs.org/es/stable/config/datastore/ds-salesforce.html>`__
- `Rastreo de Almacén de Datos (consola de administración) <https://fess.codelibs.org/es/stable/admin/dataconfig-guide.html>`__ / `Programador de Tareas <https://fess.codelibs.org/es/stable/admin/scheduler-guide.html>`__ / `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__ / `Etiquetas <https://fess.codelibs.org/es/stable/admin/labeltype-guide.html>`__ / `Guía de scripting JavaScript <https://fess.codelibs.org/es/stable/config/scripting-javascript.html>`__
