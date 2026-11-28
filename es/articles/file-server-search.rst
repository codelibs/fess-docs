==============================================
Búsqueda open source en servidores de archivos
==============================================

Introducción
============

Cuando cada departamento va añadiendo sus propios servidores de archivos, llega un momento en que nadie sabe dónde está un documento concreto.
La búsqueda de Windows solo funciona dentro de una única carpeta compartida, por lo que no permite buscar en varios servidores a la vez.
La búsqueda de texto completo integrada en un NAS tampoco funciona entre distintos dispositivos.

Una forma de resolver este problema es instalar un servidor de búsqueda de texto completo dedicado a los servidores de archivos.
Esta página resume los puntos que conviene comprobar antes de adoptar Fess, un servidor de búsqueda de texto completo de código abierto, para buscar en servidores de archivos.
El contenido corresponde a Fess 15.9.

Público objetivo
================

- Quienes tienen dificultades para buscar en los servidores de archivos y NAS internos
- Quienes están considerando la búsqueda de texto completo y quieren saber si es posible con código abierto
- Quienes quieren introducir la búsqueda sin romper los permisos de acceso existentes

Fess se publica bajo la Apache License 2.0 y puede utilizarse sin costes de licencia.

Dónde pueden estar los archivos que se buscan
=============================================

El rastreo de archivos de Fess admite los siguientes protocolos.
En la consola de administración, vaya a [Rastreador] > [Sistema de archivos] e indique en "Rutas" la ubicación donde empieza el rastreo.

.. list-table:: Protocolos admitidos
   :header-rows: 1
   :widths: 12 33 55

   * - Protocolo
     - Formato de la ruta
     - Uso principal
   * - ``file``
     - ``file:/home/share/documents/``
     - Directorios del servidor donde se ejecuta Fess, incluidos los volúmenes NAS montados
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Recursos compartidos de Windows y NAS que comparten archivos mediante SMB
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - Conexiones que usan la implementación antigua de SMB1; alternativa de reserva para dispositivos antiguos a los que ``smb`` no consigue conectarse
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - Servidores FTP
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 y almacenamiento de objetos compatible con S3 (requiere el plugin ``fess-storage-s3``)
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage (requiere el plugin ``fess-storage-gcs``)

Los protocolos que gestiona el propio Fess se determinan con el ajuste ``crawler.file.protocols``, cuyo valor predeterminado en 15.9 es ``file,smb,smb1,ftp``.
En 15.9, ``s3`` y ``gcs`` se separaron del propio Fess y pasaron a ser plugins.
La imagen de Docker incluye ambos plugins; en un Fess instalado desde el ZIP o los paquetes RPM/DEB, instálelos desde [Sistema] > [Plugin] y reinicie Fess antes de usarlos.

Para buscar en recursos compartidos de Windows, use ``smb``.
Salvo que configure otra cosa en Fess, ``smb`` negocia con el servidor la versión de conexión dentro del rango de SMB1 a SMB 3.1.1.
``smb1`` se conecta mediante otra implementación (el antiguo jcifs) y no es una opción para instalaciones nuevas.

Conservar los permisos de acceso existentes
===========================================

Al introducir la búsqueda en los servidores de archivos, la mayor preocupación es que "aparezcan en los resultados documentos que no deberían verse".
Si las carpetas compartidas de recursos humanos o de contabilidad aparecen en los resultados de búsqueda de todos los empleados, el propio sistema de búsqueda deja de ser utilizable.

Fess resuelve esto incorporando a la búsqueda los permisos de acceso del servidor de archivos.
Sin embargo, una configuración de rastreo recién creada todavía no filtra los resultados según los permisos. Revise sin falta el mecanismo siguiente y la próxima sección, "Eliminar {role}guest de los permisos".

Cómo funciona
-------------

1. Durante el rastreo, Fess lee la ACL (lista de control de acceso) de cada archivo
2. Las cuentas y grupos a los que se permite leer el archivo, y las cuentas y grupos a los que se les deniega, se registran como "roles" del documento en el campo ``role``
3. Los valores escritos en "Permisos" de la configuración de rastreo se añaden al mismo campo ``role``
4. Al buscar, Fess los compara con los roles del usuario que ha iniciado sesión y devuelve solo los documentos para los que tiene permiso

En el campo ``role``, los usuarios se registran con ``1`` y los grupos con ``2`` delante del nombre (por ejemplo, ``1taro`` y ``2sales``).
A las entradas de denegación se les antepone además ``D`` (por ejemplo, ``D2contractors``).
Un valor escrito como ``{role}guest`` en "Permisos" se registra como ``Rguest``.
Las indicaciones ``(allow)`` y ``(deny)`` que se ven en la consola de administración son la notación para introducir valores en "Permisos", no valores que se registren.

La obtención de roles a partir de las ACL está habilitada de forma predeterminada.

.. list-table:: Ajustes para conservar los permisos (fess_config.properties)
   :header-rows: 1
   :widths: 38 14 48

   * - Ajuste
     - Predeterminado
     - Descripción
   * - ``smb.role.from.file``
     - ``true``
     - Obtiene roles de las ACL de los archivos rastreados con ``smb`` y ``smb1``
   * - ``file.role.from.file``
     - ``true``
     - Obtiene roles de los permisos de acceso de los archivos rastreados con ``file`` (consulte las notas más adelante)
   * - ``ftp.role.from.file``
     - ``true``
     - Obtiene roles del propietario y el grupo de los archivos rastreados con ``ftp``
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - Los tipos de SID que se adoptan como roles y el tipo con el que se registra cada uno. De forma predeterminada, los usuarios (1) y los grupos de dominio (2) se registran tal cual, los grupos locales (4) como grupos y los SID integrados, como Everyone (5), como usuarios

Eliminar {role}guest de los permisos
------------------------------------

Al crear una configuración nueva en [Rastreador] > [Sistema de archivos], "Permisos" ya contiene ``{role}guest``.
Si la guarda así, todos los documentos reciben ``Rguest`` junto con los roles obtenidos de la ACL.
Como a los usuarios que no han iniciado sesión se les asigna el rol ``guest``, **los archivos restringidos por ACL se muestran todos en las búsquedas sin iniciar sesión**.

Para que el filtrado por ACL surta efecto, elimine ``{role}guest`` de "Permisos" en la configuración de rastreo y guárdela.
Los documentos ya rastreados se vuelven a registrar con los nuevos permisos en el siguiente rastreo.

Por su parte, a los usuarios que han iniciado sesión no se les asigna el rol ``guest``.
Por eso, aunque ``{role}guest`` siga presente, los usuarios con sesión iniciada obtienen resultados conformes a las ACL.
Como se indica en "Comprobar el funcionamiento", compruébelo siempre también sin haber iniciado sesión.

Hacer coincidir los nombres del lado del inicio de sesión
---------------------------------------------------------

Para que este mecanismo funcione de principio a fin, los usuarios que buscan también deben tener los mismos roles.
En el documento consta "los miembros de este grupo pueden leerlo", así que la comparación no es posible si el usuario que busca no puede indicar a Fess a qué grupos pertenece.

Por ello, la búsqueda que respeta los permisos requiere la integración con Active Directory o LDAP.
La configuración consiste en usar para iniciar sesión en Fess el mismo directorio que utilizan los servidores de archivos para la autenticación.
LDAP se configura en [Sistema] > [General].
El procedimiento y el planteamiento de los roles se explican en :doc:`guide-05`.

Como la comparación se hace con cadenas de nombres, tenga en cuenta lo siguiente.

- Los nombres obtenidos de las ACL se registran como nombres de cuenta sin el nombre de dominio (``EXAMPLE\taro`` pasa a ser ``1taro``)
- Para los usuarios que inician sesión mediante LDAP, los nombres de grupo se toman de forma predeterminada del CN de ``memberOf``. Si el nombre de cuenta de un grupo en el servidor de archivos difiere de su CN, no coinciden
- Los grupos integrados, como Everyone, se registran como roles con ese nombre. Los usuarios que inician sesión mediante LDAP normalmente no tienen esos roles, de modo que las carpetas compartidas solo con grupos integrados pueden no mostrarse a nadie. Si es necesario, divida la configuración de rastreo y complete los roles en "Permisos"

Por el contrario, si solo se incluyen carpetas compartidas que todos los empleados pueden ver por igual, esta integración no es imprescindible.
Este es el punto que marca la diferencia al decidir el alcance de la implantación.

Notas por protocolo
-------------------

``smb`` / ``smb1``
   La cuenta de rastreo necesita permiso para leer no solo el contenido de los archivos, sino también sus permisos de acceso (información de seguridad).
   Los archivos cuyos permisos de acceso no se pueden leer no se indexan y se registran en [Información del sistema] > [URL de fallo].

``file``
   Si el sistema de archivos no proporciona ACL (como ocurre en los sistemas de archivos habituales de Linux), solo se registran dos roles: el usuario y el grupo propietarios.
   El permiso de lectura concedido a "otros" no se convierte en un rol.
   Si monta un NAS en el servidor de Fess y lo rastrea con ``file``, se registra el propietario visible en el punto de montaje, no las ACL del NAS.
   Los servidores de archivos en los que quiera filtrar por ACL, rastréelos directamente con ``smb`` sin montarlos.

``ftp``
   El propietario y el grupo que devuelve el servidor FTP se registran como roles.

Qué formatos de archivo se leen hasta su contenido
==================================================

Fess utiliza Apache Tika para extraer el texto del contenido de los archivos.
Como se puede buscar en el texto y no solo en el nombre del archivo, es posible encontrar incluso "documentos cuyo título no se recuerda".

Los principales formatos admitidos son los siguientes.

- MS Office (doc, xls, ppt, docx, xlsx, pptx, etc.)
- PDF
- Texto, HTML, XML
- Texto enriquecido (rtf)
- Código fuente (js, c, h, java, etc.)
- Archivos comprimidos (gz, tar, zip, etc.)

Para ver la lista completa, consulte `Archivos objetivo de búsqueda <https://fess.codelibs.org/es/supported-files.html>`__.

Los archivos que no contienen texto, como los PDF de imagen y los documentos escaneados, no permiten buscar en su contenido tal cual.
En Fess 15.9 se puede habilitar el OCR con Tesseract, que lee el texto de archivos de imagen, de imágenes incrustadas en documentos de Office y de PDF que no contienen texto.
El OCR está deshabilitado de forma predeterminada.
Instale ``tesseract`` en el host donde se ejecuta el rastreador y establezca ``crawler.document.ocr.enabled=true``.
Los PDF en los que solo algunas páginas son imágenes escaneadas no están cubiertos.
Para el procedimiento, consulte `Configuración de OCR <https://fess.codelibs.org/es/stable/config/crawler-ocr.html>`__.
Como el OCR alarga el tiempo de rastreo, se recomienda comprobar primero cuántos documentos escaneados hay en las carpetas objetivo.

Arquitectura y escala
=====================

Fess utiliza OpenSearch para almacenar el índice de búsqueda.
A pequeña escala, Fess y OpenSearch pueden funcionar juntos en el mismo servidor; cuando aumenten los archivos objetivo, puede separar OpenSearch en un clúster.

Al estimar la escala, la estimación será más precisa si, además del número de archivos, comprueba lo siguiente.

- El tamaño total de las carpetas objetivo y la proporción de archivos que contienen texto
- La frecuencia de actualización (a diario o unas pocas veces al mes). Influye en el diseño del intervalo de rastreo
- El tamaño de cada archivo

De forma predeterminada, el tamaño de los archivos que se pueden indexar tiene un límite.
Los valores predeterminados de ``app/WEB-INF/classes/crawler/contentlength.xml`` son 2,5 MB para HTML y 10 MB para todo lo demás; los archivos que los superan no se indexan y se registran en [URL de fallo].
Aparte de esto, si escribe algo como ``client.maxContentLength=10485760`` en "Parámetro de configuración" de la configuración de rastreo, se limita el tamaño de los propios archivos que se obtienen (sin límite de forma predeterminada).
En carpetas con muchos documentos grandes, decida antes de la implantación si va a revisar estos límites.
Para saber cómo configurarlos, consulte la sección sobre la configuración del tamaño de archivo en `Configuración del rastreador <https://fess.codelibs.org/es/stable/config/crawler-basic.html>`__.

También hay que prestar atención al intervalo de rastreo.
Fess elimina del índice los documentos que no se han actualizado mediante un rastreo durante un determinado número de días.
Ese número de días es "Eliminar documentos anteriores" en [Sistema] > [General], y su valor predeterminado es 3 días.
El trabajo predeterminado "Default Crawler" se ejecuta a diario, por lo que no hay problema; pero si lo reduce, por ejemplo, a una vez por semana, haga que este número de días sea mayor que el intervalo de ejecución.

Criterios para elegir una herramienta de búsqueda para servidores de archivos
=============================================================================

Al comparar herramientas de búsqueda para servidores de archivos, la elección resulta más sencilla si, antes de comparar nombres de productos, comprueba si cumplen los puntos siguientes.

.. list-table:: Puntos que comprobar al elegir una herramienta de búsqueda
   :header-rows: 1
   :widths: 30 70

   * - Punto que comprobar
     - En el caso de Fess
   * - ¿Puede buscar en varios servidores y NAS a la vez?
     - Registrando varias configuraciones de rastreo, puede buscar en todos ellos desde un único cuadro de búsqueda
   * - ¿Puede buscar en el contenido de los archivos?
     - Apache Tika extrae el texto de los documentos de Office y los PDF y lo hace buscable. Los documentos escaneados pasan a ser buscables al habilitar el OCR
   * - ¿Puede conservar los permisos de acceso existentes?
     - Obtiene roles de las ACL de los archivos rastreados mediante SMB y filtra los resultados de búsqueda en consecuencia. Se necesita la integración con Active Directory o LDAP y revisar "Permisos" en la configuración de rastreo
   * - ¿Tiene costes de licencia?
     - Se publica bajo la Apache License 2.0 y no tiene costes de licencia
   * - ¿Se puede probar en local?
     - Puede iniciarlo con Docker Compose y probar la búsqueda en su propio equipo

Pasos de la implantación
========================

1. **Ponerlo en marcha** — Inicie Fess siguiendo la `Guía de configuración rápida <https://fess.codelibs.org/es/quick-start.html>`__ o :doc:`guide-02`
2. **Crear una configuración de rastreo** — En [Rastreador] > [Sistema de archivos], registre un nombre y las rutas. Si va a filtrar por ACL, elimine ``{role}guest`` de "Permisos" antes de guardar
3. **Configurar las credenciales** — Registre la cuenta para acceder a las carpetas compartidas en [Rastreador] > [Autenticación de archivos] y seleccione la configuración del paso 2 en "Configuración de rastreo de archivos"
4. **Comprobar los permisos de la cuenta de rastreo** — En el servidor de archivos, compruebe que la cuenta puede leer tanto el contenido como los permisos de acceso de las carpetas objetivo
5. **Integrar el inicio de sesión** — Configure LDAP (Active Directory) en [Sistema] > [General]
6. **Ejecutar el rastreo y comprobar** — En [Sistema] > [Programador], abra "Default Crawler", haga clic en [Iniciar ahora] y compruebe el resultado como se indica a continuación en "Comprobar el funcionamiento"

Si necesita filtrar por departamento, configure también etiquetas en [Rastreador] > [Etiqueta].

Los pasos concretos para buscar en varios servidores de archivos y sitios web internos desde un único cuadro de búsqueda se tratan en :doc:`guide-04`, y el diseño del filtrado de resultados con roles y grupos, en :doc:`guide-05`.

Comprobar el funcionamiento
===========================

Cuando termine el rastreo, compruebe lo siguiente en este orden.
El usuario integrado ``admin`` también tiene el rol ``guest``, así que no lo use para comprobar el filtrado.

1. Abra [Información del sistema] > [URL de fallo] y compruebe que no haya archivos que no se pudieran incorporar por errores de acceso o por exceder el tamaño
2. En [Información del sistema] > [Búsqueda], busque un archivo de una carpeta restringida. En esta pantalla no se filtra por roles, por lo que se muestran todos los documentos
3. Haga clic en [Actualizar] en el resultado para abrir la pantalla de edición y compruebe el campo ``role``. Asegúrese de que contiene valores procedentes de la ACL, como ``1taro`` o ``2sales``, y de que no contiene ``Rguest``
4. Sin haber iniciado sesión, busque el mismo archivo en la página de búsqueda y compruebe que no se muestra
5. Inicie sesión con un usuario que pertenezca a un grupo que puede leer la carpeta, busque y compruebe que se muestra
6. Inicie sesión con un usuario que no pertenezca a ese grupo, busque y compruebe que no se muestra

Si en el paso 3 los nombres del campo ``role`` no coinciden con los del lado de LDAP, revise cada punto de "Hacer coincidir los nombres del lado del inicio de sesión".

Resumen
=======

- Fess es un servidor de búsqueda de código abierto que permite la búsqueda de texto completo en servidores de archivos (SMB, FTP, local). S3 y GCS se admiten mediante plugins
- En los archivos rastreados mediante SMB, los permisos de acceso registrados en las ACL se usan para filtrar los resultados de búsqueda. La lectura de las ACL está habilitada de forma predeterminada
- Si no elimina ``{role}guest`` de "Permisos" en la configuración de rastreo, los usuarios que no han iniciado sesión verán todos los documentos
- La búsqueda que respeta los permisos requiere la integración con Active Directory o LDAP y que los nombres coincidan en ambos lados
- Apache Tika permite buscar en el contenido de los documentos de Office y los PDF, y al habilitar el OCR también en los documentos escaneados
- Puede empezar con poco y ampliar el sistema convirtiendo OpenSearch en un clúster a medida que crezcan los objetivos

Artículos recomendados
======================

- Pasos para buscar a la vez en varios servidores de archivos y sitios web internos: :doc:`guide-04`
- Diseño del filtrado de resultados con roles y grupos: :doc:`guide-05`
- Probar Fess en local con Docker: :doc:`guide-02`

Referencias
===========

- `Rastreo de sistema de archivos (búsqueda en servidores de archivos) <https://fess.codelibs.org/es/stable/admin/fileconfig-guide.html>`__
- `Autenticación de archivos <https://fess.codelibs.org/es/stable/admin/fileauth-guide.html>`__
- `Configuración del rastreador: rastreo web, de servidores de archivos y de bases de datos <https://fess.codelibs.org/es/stable/config/crawler-basic.html>`__
- `Configuración de OCR <https://fess.codelibs.org/es/stable/config/crawler-ocr.html>`__
- `Configuración de búsqueda basada en roles <https://fess.codelibs.org/es/stable/config/security-role.html>`__
- `Guía de integración LDAP <https://fess.codelibs.org/es/stable/config/ldap-integration.html>`__
- `URL de fallo <https://fess.codelibs.org/es/stable/admin/failureurl-guide.html>`__
- `Archivos objetivo de búsqueda <https://fess.codelibs.org/es/supported-files.html>`__
- `Guía de configuración rápida <https://fess.codelibs.org/es/quick-start.html>`__
