=============================
Conector de SharePoint Server
=============================

Descripción general
===================

El conector de SharePoint Server obtiene los archivos de bibliotecas de documentos y los elementos
de lista de una implementación local (on-premises) de **SharePoint Server** (2013, 2016, 2019 o
Subscription Edition) a través de su API REST/OData (y, para 2013, de su API XML/Atom), y los
registra en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-sharepoint``.

.. note::

   Si necesita rastrear SharePoint Online (Microsoft 365), use :doc:`ds-microsoft365` en lugar de
   este conector. La compatibilidad OAuth de este conector se limita a la autenticación exclusiva de
   aplicación (application-only) de Azure ACS, y no tiene integración con la API de Microsoft Graph.

Versiones compatibles: SharePoint Server 2013 / 2016 / 2019 / Subscription Edition (SE)

Contenido compatible
====================

- Archivos de bibliotecas de documentos
- Elementos de lista
- Archivos adjuntos de elementos de lista

Requisitos previos
==================

1. Se requiere la instalación del plugin
2. La cuenta de rastreo necesita acceso de lectura a los sitios, las listas y las bibliotecas de
   documentos que se van a rastrear
3. Elija exactamente un método de autenticación (NTLM, Kerberos [SPNEGO] u OAuth [ACS]) y tenga
   preparadas sus credenciales correspondientes

Instalación del plugin
----------------------

Instálelo desde la pantalla de administración en "Sistema" -> "Plugin":

1. Descargue ``fess-ds-sharepoint-X.X.X.jar``
2. Colóquelo en ``$FESS_HOME/app/WEB-INF/lib`` (o en ``/usr/share/fess/app/WEB-INF/lib``)
3. Reinicie |Fess|

Consulte :doc:`../../admin/plugin-guide` para más información.

Configuración
=============

Configure este conector desde la pantalla de administración en "Rastreador" -> "Almacén de datos" ->
"Crear nuevo".

Configuración básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo
   * - Nombre
     - SharePoint
   * - Nombre del manejador
     - SharePointDataStore
   * - Habilitado
     - Activado

Configuración de parámetros
---------------------------

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

Lista de parámetros
~~~~~~~~~~~~~~~~~~~

**URL / Sitio**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``url``
     - Sí
     - URL base del servidor SharePoint, p. ej., ``http://sharepoint.example.com/``
   * - ``site.name``
     - Condicional
     - Nombre de la colección de sitios que se rastrea bajo ``/sites/<site.name>/``. No es necesario si se configura ``site.path``
   * - ``site.path``
     - No
     - Ruta administrada relativa al servidor del sitio (p. ej., ``/teams/eng``; use ``/`` para la colección de sitios raíz). Cuando se configura, se usa tal cual en lugar del prefijo fijo ``/sites/``, y ``site.name`` deja de ser necesario
   * - ``site.list_id``
     - No
     - Rastrea una única lista mediante su GUID (modo Crawl de lista)
   * - ``site.list_name``
     - No
     - Rastrea una única lista mediante su nombre visible (modo Crawl de lista)
   * - ``site.doclib_path``
     - No
     - Ruta de la biblioteca de documentos dentro del sitio (modo Crawl de biblioteca de documentos), p. ej., ``/Shared Documents``
   * - ``site.exclude_list``
     - No
     - Patrones regex (separados por comas) de nombres de tipo de entidad de lista que se excluirán. Solo se aplica a un rastreo de todo el sitio
   * - ``site.exclude_folder``
     - No
     - Patrones regex (separados por comas) de títulos de carpetas de nivel superior que se excluirán. Solo se aplica a un rastreo de todo el sitio
   * - ``site.crawl_subsites``
     - No
     - Recorre recursivamente los subsitios del sitio (predeterminado: ``false``). Consulte `Subsitios y rutas administradas`_
   * - ``site.max_depth``
     - No
     - Cuántos saltos de subsitio puede recorrer ``site.crawl_subsites`` (predeterminado: ``10``); la raíz tiene profundidad 0

**Autenticación**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``auth.ntlm.user``
     - No
     - Nombre de usuario NTLM. Al configurarlo se habilita NTLM (funciona el formato ``DOMAIN\user``)
   * - ``auth.ntlm.password``
     - No
     - Contraseña NTLM
   * - ``auth.ntlm.domain``
     - No
     - Dominio de Windows, enviado como campo NTLM independiente
   * - ``auth.ntlm.workstation``
     - No
     - Nombre de estación de trabajo enviado en la negociación NTLM
   * - ``auth.kerberos.principal``
     - No
     - Principal del cliente, escrito como ``user@REALM``. Al configurarlo se habilita Kerberos/SPNEGO
   * - ``auth.kerberos.keytab``
     - No
     - Ruta a un archivo keytab que contiene una clave para el principal. Es mutuamente excluyente con ``auth.kerberos.password``
   * - ``auth.kerberos.password``
     - No
     - La contraseña del principal, usada solo cuando no se configura un keytab
   * - ``auth.kerberos.strip_port``
     - No
     - Elimina el puerto del nombre principal de servicio (predeterminado: ``true``)
   * - ``auth.kerberos.use_canonical_hostname``
     - No
     - Resuelve el host de destino a su nombre canónico antes de construir el nombre principal de servicio (predeterminado: ``false``)
   * - ``auth.kerberos.krb5_conf``
     - No
     - Ruta a un ``krb5.conf``. Solo se aplica cuando ``java.security.krb5.conf`` aún no está configurado
   * - ``auth.kerberos.debug``
     - No
     - Habilita la salida de depuración de ``Krb5LoginModule`` (predeterminado: ``false``)
   * - ``auth.oauth.client_id``
     - No
     - ID de cliente OAuth de aplicación exclusiva de Azure ACS. Al configurarlo se habilita OAuth
   * - ``auth.oauth.client_secret``
     - No
     - Secreto de cliente OAuth
   * - ``auth.oauth.tenant``
     - No
     - Nombre del tenant, sin ``.sharepoint.com``
   * - ``auth.oauth.realm``
     - No
     - Realm/ID de directorio de Azure AD

**Solo se puede configurar uno** de ``auth.kerberos.principal``, ``auth.ntlm.user`` y
``auth.oauth.client_id``. Consulte `Autenticación`_ más abajo.

**Lista**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``list.items.number_per_page``
     - No
     - Tamaño de página para ``GetListItems`` (predeterminado: ``100``)
   * - ``list.item.content.include_fields``
     - No
     - Nombres de campo separados por comas; si se configura, solo estos campos del elemento de lista se concatenan en ``content``
   * - ``list.item.content.exclude_fields``
     - No
     - Patrones de nombre de campo separados por comas (cada uno tratado como una expresión regular), excluidos de ``content`` además de un amplio conjunto integrado de campos estándar
   * - ``list.is_sub_page``
     - No
     - Trata los elementos de lista como subpáginas de SitePages/wiki, lo que afecta al mecanismo de reserva de paginación y al formato del enlace web (predeterminado: ``false``)

**HTTP**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``http.connection_timeout``
     - No
     - Tiempo de espera de conexión HTTP en ms; también se usa como tiempo de espera del grupo de conexiones (predeterminado: ``30000``)
   * - ``http.socket_timeout``
     - No
     - Tiempo de espera de socket HTTP (lectura) en ms (predeterminado: ``30000``)
   * - ``proxy_host``
     - No
     - Host del proxy HTTP
   * - ``proxy_port``
     - Condicional
     - Puerto del proxy HTTP; obligatorio si se configura ``proxy_host`` (predeterminado: ``-1`` = sin proxy)

**Filtrado y contenido**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``include_pattern``
     - No
     - Expresión regular que debe coincidir con el valor de un elemento para que se rastree. Consulte la nota bajo esta tabla para saber cuál es ese valor
   * - ``exclude_pattern``
     - No
     - Expresión regular que excluye del rastreo a un elemento que coincida
   * - ``supported_mimetypes``
     - No
     - Expresiones regulares separadas por comas; el tipo MIME de un archivo debe coincidir con al menos una de ellas (predeterminado: ``.*``)
   * - ``max_content_length``
     - No
     - Tamaño máximo de archivo en bytes; un archivo que supere el límite se omite, no falla (predeterminado: ``-1`` = sin límite)
   * - ``extractor_name``
     - No
     - Extractor de reserva usado solo para un tipo MIME que la fábrica de extractores no tiene asignado (predeterminado: ``tikaExtractor``)

**Comportamiento**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``sp.version``
     - No
     - Establézcalo en ``2013`` para cambiar a la familia de API XML/Atom, ``GetXxxByServerRelativeUrl``, de SharePoint 2013 (sin configurar ⇒ dialecto REST de SharePoint Online / 2016 en adelante)
   * - ``retry_limit``
     - No
     - Número máximo de reintentos por unidad de rastreo ante una excepción de servidor/cliente de SharePoint (predeterminado: ``2``)
   * - ``role.skip``
     - No
     - Omite por completo la obtención de permisos por elemento (predeterminado: ``false``). Consulte `Permisos`_
   * - ``ignore_error``
     - No
     - Registra en el log y omite un fallo de extracción de contenido de un archivo en lugar de hacer fallar el objetivo de rastreo (predeterminado: ``false``)
   * - ``default_permissions``
     - No
     - Cadenas de permisos separadas por comas que se combinan en la lista de roles de cada documento, además de lo que haya devuelto SharePoint
   * - ``delete_old_docs``
     - No
     - Indica si se eliminan los documentos que no se han actualizado en esta ejecución (predeterminado del núcleo: ``true``). Este plugin lo fuerza a ``false`` para la ejecución actual siempre que algún objetivo de rastreo haya fallado
   * - ``number_of_threads``
     - No
     - Cuántos objetivos de rastreo se procesan a la vez (predeterminado: ``1`` = sin grupo de hilos), con un límite de hasta el doble del número de procesadores. Consulte `Rastreo paralelo y carga`_
   * - ``script_type``
     - No
     - Motor de scripts para el Script de la configuración de datos (predeterminado: ``groovy``)
   * - ``readInterval``
     - No
     - Espera entre resultados de rastreo sucesivos, en ms (predeterminado: ``0``). Tenga en cuenta que se escribe en camelCase, a diferencia de todos los demás parámetros de esta lista

Configuración de scripts
------------------------

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

Campos disponibles
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 20 32 32

   * - Clave
     - Elemento de lista (ItemCrawl)
     - Archivo de biblioteca de documentos (FolderCrawl->FileCrawl)
     - Archivo adjunto (ItemAttachmentsCrawl->FileCrawl)
   * - ``url``
     - Enlace web
     - URL del archivo
     - URL del archivo
   * - ``host``
     - Nombre de host
     - Nombre de host
     - Nombre de host
   * - ``site``
     - Ruta relativa al servidor (``FileRef``)
     - Ruta relativa al servidor
     - Ruta relativa al servidor
   * - ``title``
     - Campo ``Title``; si no, ``FileLeafRef``/nombre de archivo
     - El propio valor de lista ``Title`` del archivo de la biblioteca de documentos si existe; si no, el nombre de archivo
     - Nombre de archivo
   * - ``titleWithListName``
     - ``"[listName] title"``
     - ``"[listName] filename"`` (el nombre de lista siempre está vacío en un crawl de biblioteca de documentos, por lo que en la práctica es solo el nombre de archivo)
     - ``"[listName] filename"``
   * - ``listName``
     - Nombre visible de la lista, o ``""``
     - Siempre ``""``
     - Nombre real de la lista
   * - ``content``
     - Concatenación de valores de campo
     - Texto extraído
     - Texto extraído
   * - ``digest``
     - ``content`` abreviado
     - ``content`` abreviado
     - ``content`` abreviado
   * - ``content_length``
     - ``content.length()``
     - ``content.length()``
     - ``content.length()``
   * - ``last_modified``
     - Del listado
     - Del listado
     - Del listado
   * - ``created``
     - Del listado
     - Del listado
     - Del listado
   * - ``mimetype``
     - Siempre ``text/html``
     - Detectado
     - Detectado
   * - ``filetype``
     - Derivado de ``mimetype``
     - Derivado de ``mimetype``
     - Derivado de ``mimetype``
   * - ``role``
     - Lista de permisos, solo si no está vacía
     - Lista de permisos, solo si no está vacía
     - Lista de permisos, solo si no está vacía
   * - ``list_name``
     - Presente
     - **Ausente**
     - Presente
   * - ``list_id``
     - Presente
     - **Ausente**
     - Presente
   * - ``item_id``
     - Presente
     - **Ausente**
     - Presente

.. note::

   ``content_length`` es ``content.length()``, es decir, el número de caracteres (unidades de código
   UTF-16) del texto extraído o concatenado, no el tamaño en bytes del archivo. Esto difiere de
   ``file.size`` en los conectores de Box, Google Drive y Dropbox, que es el tamaño en bytes real
   obtenido de los propios metadatos de archivo de cada servicio. No compare el ``content_length``
   de este conector con esos valores.

**Claves dinámicas: ``val_*``**

Cada clave del ``FieldValuesAsText`` de un elemento de lista (el mapa de valores de campo en bruto
que SharePoint devuelve para ese elemento, incluidas las claves de metadatos OData como
``odata.metadata``) se expone con dos nombres: uno sin prefijo (solo si ese nombre no coincide ya
con alguna de las claves fijas anteriores) y otro, incondicionalmente, con el prefijo ``val_`` - por
ejemplo, un campo ``Status`` se convierte tanto en ``Status`` como en ``val_Status``.

Las claves ``val_*`` solo existen en la **ruta de crawl de elementos de lista (ItemCrawl)**. Un
archivo de biblioteca de documentos (FolderCrawl->FileCrawl) o un archivo adjunto de elemento de
lista (ItemAttachmentsCrawl->FileCrawl) nunca produce ninguna clave ``val_*``.

Autenticación
=============

Hay disponibles tres métodos de autenticación, y **solo se puede configurar uno**. Si se configura
más de uno de ``auth.kerberos.principal``, ``auth.ntlm.user`` y ``auth.oauth.client_id``, el trabajo
de configuración de datos falla con un error de validación antes de que se realice ninguna
solicitud. Esto es intencional: solo se registra una credencial en el cliente HTTP, y el ámbito bajo
el que se registra coincide tanto con un desafío ``Negotiate`` como con uno ``NTLM``, por lo que
configurar más de una produciría errores 401 que el log no explicaría en absoluto.

NTLM
----

::

    auth.ntlm.user={nombre de usuario de SharePoint}
    auth.ntlm.password={contraseña}
    auth.ntlm.domain={dominio de Windows. Opcional; sin configurar de forma predeterminada.}
    auth.ntlm.workstation={nombre de estación de trabajo enviado en la negociación NTLM. Opcional; sin configurar de forma predeterminada.}

``auth.ntlm.domain`` y ``auth.ntlm.workstation`` no están configurados de forma predeterminada, lo
que construye exactamente la misma credencial que este conector siempre ha construido. Escribir el
dominio dentro del nombre de usuario como ``DOMAIN\user`` sigue funcionando. Al configurar
``auth.ntlm.domain``, el dominio se envía en su lugar como un campo NTLM independiente, que es lo
que necesita un servidor que rechace la forma combinada.

Kerberos (SPNEGO)
-----------------

**Entorno admitido:** una única JVM de rastreo, un ``krb5.conf`` por instancia de Fess, un keytab o
una contraseña, sin delegación, sin channel binding, y mutuamente excluyente con NTLM y OAuth.
Cualquier configuración fuera de esto no es compatible.

::

    auth.kerberos.principal={principal del cliente, escrito como user@REALM. Al configurarlo se habilita Kerberos.}
    auth.kerberos.keytab={ruta a un keytab que contiene una clave para el principal. Mutuamente excluyente con auth.kerberos.password.}
    auth.kerberos.password={la contraseña del principal. Se usa solo cuando no hay un keytab configurado.}
    auth.kerberos.strip_port={true o false. Elimina el puerto del nombre principal de servicio. El valor predeterminado es true.}
    auth.kerberos.use_canonical_hostname={true o false. Resuelve el host de destino a su nombre canónico para el nombre principal de servicio. El valor predeterminado es false.}
    auth.kerberos.krb5_conf={ruta a un krb5.conf. Solo se aplica cuando java.security.krb5.conf aún no está configurado.}
    auth.kerberos.debug={true o false. Salida de depuración de Krb5LoginModule. El valor predeterminado es false.}

- **``krb5.conf`` se configura en ``jvm.crawler.options``**, como
  ``-Djava.security.krb5.conf=/ruta/a/krb5.conf``. El rastreo de almacenes de datos se ejecuta en el
  **proceso hijo** del rastreador, por lo que configurar esto en cualquier lugar que solo afecte a
  la aplicación web no tiene ningún efecto, y reiniciar la aplicación web no recoge el cambio: hay
  que volver a ejecutar el trabajo de rastreo. ``auth.kerberos.krb5_conf`` es una comodidad para
  cuando aún nada ha configurado la propiedad: **nunca sobrescribe un valor ya configurado**, ya que
  la propiedad es global a la JVM y una única JVM de rastreo ejecuta todas las configuraciones de
  datos de un trabajo de rastreo. Cuando se abstiene de sobrescribir, registra una advertencia en el
  log indicando ambas rutas.
- **Ponga ``udp_preference_limit = 1`` en la sección ``[libdefaults]`` de ``krb5.conf``.** Sin esto,
  el JDK intenta primero UDP, y cuando el KDC no responde (inalcanzable, un firewall que descarta
  UDP 88, o una respuesta mayor que el tamaño del datagrama), reintenta tres veces a treinta
  segundos cada una antes de recurrir a TCP. Un rastreo que parece bloqueado durante aproximadamente
  un minuto y medio por cada autenticación, sin nada en el log, suele deberse a esto.
- **Escriba siempre el principal como ``user@REALM``.** ``default_realm`` es global a la JVM, y
  varias granjas de SharePoint en distintos realms pueden tener que compartir un mismo
  ``krb5.conf``, de modo que un ``user`` sin realm se resuelve contra el realm que ese archivo
  indique en ese momento.
- **``auth.kerberos.use_canonical_hostname`` es ``false`` de forma predeterminada**, deliberadamente
  distinto del valor predeterminado propio de Apache HttpClient. Con esta opción activada, el host
  de destino pasa por una resolución DNS inversa antes de construir el nombre principal de servicio,
  lo que en mapeos de acceso alternativos o detrás de un balanceador de carga puede producir un
  nombre para el que no hay ningún SPN registrado, y el fallo resultante no dice nada sobre el DNS.
  Actívela solo si el SPN está realmente registrado con el nombre canónico.
- **IIS Extended Protection configurado como ``tokenChecking=Require`` no puede funcionar.** Ni
  Apache HttpClient 4.5 ni 5.x admiten channel binding. IIS establece esto en ``None`` de forma
  predeterminada, por lo que normalmente no se da el caso, y no hay ninguna solución alternativa
  cuando sí se da.
- **El ticket se obtiene una sola vez, al construirse el cliente HTTP del rastreo, y nunca se
  renueva.** Un rastreo que se ejecuta más tiempo que la vida útil del ticket empieza a fallar en la
  autenticación a mitad de camino.
- **``auth.kerberos.password`` se almacena y se muestra en texto sin cifrar**, exactamente igual que
  ``auth.ntlm.password``. Fess no cuenta con ningún mecanismo de enmascaramiento para los parámetros
  de los manejadores de almacén de datos; la pantalla de edición de la configuración de datos los
  muestra como un área de texto plano. Dé preferencia a ``auth.kerberos.keytab`` y asigne al archivo
  keytab permisos restrictivos.
- ``auth.kerberos.debug=true`` hace que ``Krb5LoginModule`` escriba en la salida estándar del
  proceso del rastreador, no en el log de Fess.

OAuth (ACS)
-----------

::

    auth.oauth.client_id={ID de cliente OAuth}
    auth.oauth.client_secret={secreto de cliente OAuth}
    auth.oauth.tenant={nombre del tenant, sin .sharepoint.com}
    auth.oauth.realm={realm/ID de directorio de Azure AD}

Configurar ``auth.oauth.client_id`` habilita un flujo de credenciales de cliente (exclusivo de
aplicación) frente al Windows Azure Access Control Service,
``https://accounts.accesscontrol.windows.net/{realm}/tokens/OAuth/2``. El token de acceso se obtiene
una sola vez, al construirse el cliente HTTP del rastreo, se aplica como encabezado
``Authorization`` de tipo ``Bearer`` en cada solicitud, y se renueva y reintenta una vez ante un
401. **Microsoft ha declarado obsoleto ACS y ha programado su retirada**; este conector registra una
advertencia al respecto en cada rastreo configurado con OAuth. Aquí no está implementado ningún
flujo de registro de aplicación de Entra ID (por certificado o por secreto de cliente); solo la
autenticación heredada de aplicación exclusiva de ACS.

Antes de activar OAuth solo se comprueba la presencia de ``auth.oauth.client_id``;
``client_secret``, ``tenant`` y ``realm`` se leen incondicionalmente y pueden quedar vacíos en
silencio si se omiten, lo que rompe la obtención del token sin ningún mensaje de validación
dedicado.

**``sp.version=2013`` y OAuth nunca han funcionado juntos.** Todas las llamadas a la API de
SharePoint 2013 que hace este conector pasan por el cliente XML/Atom, y ninguna ruta de código de
ese cliente adjunta un token OAuth a una solicitud, de modo que, con ambos configurados, cada
solicitud se envía sin autenticar. El rastreo registra una advertencia que indica exactamente esto y
menciona ``auth.ntlm.*`` como alternativa; no hace fallar el trabajo. Use ``auth.ntlm.*`` para
SharePoint 2013.

Permisos
========

``role.skip=true`` (predeterminado ``false``) omite por completo la obtención de permisos por
elemento: no se realiza ninguna llamada a ``GetListItemRole``, nunca se establece la clave ``role``
para el elemento, y el documento termina llevando únicamente el ajuste estático de Permission de la
configuración de datos y, si está configurado, ``default_permissions``; ningún permiso derivado de
SharePoint llega a él en absoluto.

Cuando se obtienen los roles, los propios usuarios, grupos de seguridad y grupos de SharePoint se
expanden y se asignan a roles de búsqueda de Fess:

- Una cuenta o grupo de **AD local (on-premises)** (nombre de inicio de sesión que contiene una
  barra invertida y no comienza con un prefijo de reclamación de Azure) se asigna mediante los
  ayudantes de rol estándar de usuario/grupo de AD.
- Una cuenta de **Azure AD (Entra ID)** (nombre de inicio de sesión que comienza con
  ``i:0#.f|membership|``) se asigna **dos veces**: una por el valor completo de la reclamación de
  Azure y otra por la parte de cuenta de AD anterior al ``@`` de esa reclamación, de modo que se
  añaden tanto un rol de estilo Entra ID como uno de estilo AD para el mismo usuario. Un grupo de
  seguridad marcado como de Azure (mediante uno de varios prefijos de estilo reclamación, incluido
  el grupo especial «todos» ``spo-grid-all-users``) se asigna de la misma manera, en ambas formas.
- Un **grupo de SharePoint** tiene su propia membresía (usuarios, grupos de seguridad, grupos
  anidados) expandida de forma recursiva, con una protección de grupos visitados para detener la
  recursión infinita entre grupos que se contienen mutuamente.

``default_permissions`` (separado por comas) se combina **después** de todo lo anterior, y se aplica
incluso cuando SharePoint no devolvió ningún rol para el elemento, el caso que producen tanto
``role.skip=true`` como «SharePoint no devolvió nada». La lista final de roles es la unión, sin
duplicados, del ajuste estático de Permission de la configuración de datos, los roles derivados de
SharePoint (salvo que se omitan) y ``default_permissions``.

Subsitios y rutas administradas
===============================

Configurar ``site.path`` hace que se use tal cual la ruta administrada relativa al servidor
indicada, en lugar del prefijo fijo ``/sites/``, y ``site.name`` deja de ser necesario.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Escenario
     - Configuración
   * - Colección de sitios raíz
     - ``site.path=/``
   * - El sitio ``/teams/eng``
     - ``site.path=/teams/eng``
   * - La forma clásica ``/sites/mysite/``
     - ``site.name=mysite`` (deje ``site.path`` sin configurar)

Configurar ``site.crawl_subsites`` (predeterminado ``false``) hace que un rastreo de sitio completo
(aquel en el que no se configura ni ``site.list_name`` ni ``site.doclib_path``) recorra
recursivamente los subsitios del sitio, descubiertos mediante ``_api/web/webinfos``. Dejarlo sin
configurar mantiene el rastreo emitiendo exactamente las mismas solicitudes de siempre, incluyendo
no solicitar nunca ``webinfos``.

Los documentos de un subsitio terminan en la misma configuración de datos que los del sitio raíz,
bajo sus propias rutas relativas al servidor; no hay nada en el índice que marque un documento como
procedente de un subsitio en lugar de la raíz.

``site.max_depth`` (predeterminado ``10``) limita cuántos saltos de subsitio por debajo del sitio
raíz se rastrean una vez que ``site.crawl_subsites=true``. El propio sitio raíz tiene profundidad 0,
de modo que ``site.max_depth=1`` rastrea los hijos directos de la raíz y nada más. Configurarlo por
debajo de ``1`` mientras ``site.crawl_subsites=true`` desactiva de nuevo la función (no se rastrea
ningún subsitio en absoluto) y se registra como advertencia al iniciarse el rastreo.

Activar el rastreo de subsitios **multiplica el tiempo total del rastreo** aproximadamente por el
número de subsitios descubiertos (limitado por ``site.max_depth``): cada uno recibe su propio
listado completo de carpetas, su propio listado de listas y, si no ha alcanzado el límite de
profundidad, su propia llamada a ``webinfos``, todo ello además de todo lo que ya hace el rastreo
del sitio raíz.

``number_of_threads`` y ``readInterval``, descritos en `Rastreo paralelo y carga`_, se aplican a un
rastreo recursivo de subsitios de la misma manera que se aplican a cualquier otro rastreo.

Rastreo paralelo y carga
========================

``number_of_threads`` (predeterminado ``1``) indica cuántos objetivos de rastreo se procesan a la
vez. Con el valor predeterminado, el rastreo se ejecuta exactamente como siempre: cada objetivo se
rastrea en el hilo de rastreo y **no se crea ningún grupo de hilos**.

El valor está **limitado al doble del número de procesadores** de la máquina que ejecuta Fess, de
modo que una configuración de datos no puede pedir más concurrencia de la que el host puede ofrecer.
Un valor inferior a ``1``, o uno vacío o no interpretable, recurre a ``1`` en lugar de respetarse o
hacer fallar el trabajo. Un valor que se haya limitado, o uno inferior a ``1``, se registra con el
valor solicitado y el valor real; uno no interpretable registra una advertencia. Un valor vacío no
registra nada, porque un campo vacío significa simplemente que el parámetro no se configuró.

El grupo de conexiones HTTP se dimensiona en consecuencia. Apache HttpClient permite de forma
predeterminada solo 2 conexiones por ruta, y todo el rastreo constituye una única ruta: sin aumentar
este límite, cada hilo a partir del segundo pasaría el rastreo esperando una conexión en lugar de
hacer solicitudes.

**``readInterval`` sigue marcando el ritmo de entrega de documentos, uno por intervalo, sea cual sea
su valor.** Los hilos hacen que el rastreo descubra y obtenga contenido más rápido; no hacen que los
documentos lleguen al indexador más rápido. Esto es intencional: dividir el intervalo configurado
por el operador entre el número de hilos multiplicaría exactamente la carga que ese intervalo
pretendía limitar. Un trabajador que termina un documento mientras los anteriores aún se están
entregando simplemente espera.

Lo que aumentar ``number_of_threads`` **sí** multiplica es la tasa de solicitudes contra SharePoint.
La espera exponencial ante 503 y la espera por ``X-SharePointHealthScore`` que se describen más
abajo se aplican por objetivo de rastreo, en el hilo que lo rastrea, de modo que ``n`` hilos hacen
hasta ``n`` veces las solicitudes que haría un rastreo de un solo hilo, incluso durante un período
en el que la granja esté señalando que está ocupada. En una granja local (on-premises), aumente este
valor gradualmente.

Hay dos factores que ponen un techo a lo que más hilos realmente aportan:

- **La primera vez que se lee la membresía de cada grupo de SharePoint, se lee con un solo hilo a la
  vez.** Los permisos se resuelven a través de una caché compartida por todo el rastreo, protegida
  por un único bloqueo que se mantiene durante toda la consulta de los miembros de un grupo. Ese
  bloqueo impide que un hilo entregue a otro un grupo cuyos miembros aún se están leyendo, lo que
  indexaría los elementos que ese grupo protege sin ninguno de sus permisos. Una vez que un grupo
  está en la caché, cada referencia posterior a él es una consulta económica, por lo que se trata de
  un **coste de caché fría**: el rastreo de un sitio con muchos grupos distintos pasa sus primeros
  minutos más cerca de un único hilo que de ``n`` hilos, mientras que uno cuyos elementos comparten
  un puñado de grupos apenas lo nota. ``role.skip=true``, que no lee ningún permiso, evita este
  coste por completo.
- El descubrimiento es secuencial por sitio: el listado de carpetas y de listas de un sitio
  constituye un único objetivo de rastreo, por lo que los hilos no tienen nada que repartirse hasta
  que ese objetivo termina y encola lo que ha encontrado.

**Una respuesta 503** se reintenta igual que cualquier otro error, hasta ``retry_limit`` veces, pero
con una espera creciente antes de cada reintento: 2 segundos, luego 4, luego 8, duplicándose hasta
un límite de 30 segundos, cada uno aleatorizado entre el 70 % y el 129 % de ese valor. Un objetivo
de rastreo que sigue devolviendo 503 paga esta espera antes de cada reintento que realmente llega a
hacer, pero no después del último.

**Cada respuesta** (exitosa o no, incluida una página de un listado que el rastreo está a punto de
descartar) se inspecciona en busca del encabezado de respuesta ``X-SharePointHealthScore`` (0
inactivo a 10 muy ocupado). Una puntuación de 9 o superior hace que el rastreo espere antes de hacer
cualquier otra cosa: la puntuación 9 espera unos 2 segundos, la 10 unos 4 segundos, y así
sucesivamente, duplicándose por cada punto por encima de 9. **Esto se va acumulando a lo largo de
todo el rastreo, sin ningún límite agregado**: una granja que se mantiene en una puntuación de
estado de 9 bajo carga sostenida añade aproximadamente 2 segundos a *cada solicitud* que hace este
conector, incluida cada página de cada listado de carpetas y de listas, lo que puede convertir un
rastreo que de otro modo tardaría horas en uno que tarda sustancialmente más. Si un rastreo se
ralentiza inesperadamente en un orden de magnitud, compruebe la puntuación de estado de la granja
durante esa ventana antes de suponer que el problema es otro.

Ejemplos de configuración
=========================

Todos estos ejemplos asumen NTLM. Para usar Kerberos u OAuth en su lugar, consulte `Autenticación`_
y sustituya las líneas ``auth.ntlm.*``.

Crawl de lista
--------------

Parámetros:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.list_name=Tasks

Script:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Crawl de biblioteca de documentos
---------------------------------

Parámetros:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

Script:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Crawl de un sitio ``/teams/``
-----------------------------

``site.path`` permite apuntar directamente a una biblioteca de documentos de un sitio bajo una ruta
administrada distinta de ``/sites/``.

Parámetros:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/teams/eng
    site.doclib_path=/Shared Documents

Script:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Crawl recursivo de subsitios
----------------------------

Comienza en la colección de sitios raíz y sigue los subsitios hasta 3 niveles de profundidad.

Parámetros:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/
    site.crawl_subsites=true
    site.max_depth=3

Script:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

Limitaciones
============

- **No hay ningún tipo de crawl incremental ni de delta.** En este conector no existe en ningún
  sitio un token de cambio, una consulta de delta ni un filtrado de tipo «modificado desde la última
  vez»: cada ejecución hace un listado completo de todas las listas, carpetas y archivos que está
  configurada para alcanzar. ``delete_old_docs`` solo controla si los documentos que el rastreo
  completo actual no volvió a ver se eliminan después; eso es una limpieza posterior, no una
  obtención incremental.
- **Los caracteres ``%`` y ``#`` en nombres de archivo/carpeta** se admiten en la ruta de código
  predeterminada (distinta de ``2013``). Solo SharePoint Server 2019 y Subscription Edition
  aceptan esos dos caracteres en un nombre; 2016 los sigue rechazando explícitamente, y 2013
  también. La ruta predeterminada llega a esos archivos mediante los puntos finales
  ``...ByServerRelativePath(decodedUrl=...)``, que reciben la ruta ya decodificada, y el rastreo
  escapa ambos caracteres en el enlace con el que indexa el archivo. **Con ``sp.version=2013`` no
  es posible llegar a esos archivos**, porque usa los puntos finales más antiguos
  ``...ByServerRelativeUrl(...)``, que interpretan su argumento como una URL ya codificada. Es una
  limitación deliberada y no una carencia: una granja de SharePoint 2013 no puede contener un
  nombre así. Solo importa si se apunta ``sp.version=2013`` a un servidor 2019 o Subscription
  Edition, que no es una configuración que deba usarse. Consulte
  `Use of # and % characters in file and folder names
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2019>`__
  y `File names - expanded support for special characters
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2016>`__.
- **IIS Extended Protection con ``tokenChecking=Require`` no se puede admitir.** Ni Apache
  HttpClient 4.5 ni 5.x implementan channel binding, del que depende Extended Protection en
  ``Require``. IIS establece este ajuste en ``None`` de forma predeterminada, por lo que la mayoría
  de las granjas no se ven afectadas, y no hay ninguna solución alternativa para una granja en la
  que esté configurado como ``Require``.
- **Las contraseñas en los parámetros de configuración de datos se almacenan y se muestran en texto
  sin cifrar.** Esto se aplica tanto a ``auth.ntlm.password`` como a ``auth.kerberos.password``:
  Fess no cuenta con ningún mecanismo de enmascaramiento para los parámetros de los manejadores de
  almacén de datos, y la pantalla de edición de la configuración de datos los muestra en un área de
  texto plano. Dé preferencia a ``auth.kerberos.keytab`` frente a ``auth.kerberos.password`` cuando
  Kerberos esté disponible, y asigne al archivo keytab permisos restrictivos.
- **``sp.version=2013`` y OAuth nunca han funcionado juntos.** Todas las llamadas a la API de
  SharePoint 2013 pasan por el cliente XML/Atom, y ninguna ruta de código de ese cliente adjunta un
  token OAuth a una solicitud, de modo que, con ambos configurados, cada solicitud se envía sin
  autenticar. Use ``auth.ntlm.*`` para SharePoint 2013.
- **Las rutas administradas distintas de ``/sites/`` y de la establecida mediante ``site.path``
  siguen sin descubrirse por sí solas.** ``site.crawl_subsites`` recorre recursivamente solo desde
  el sitio raíz que configure, y ``site.path`` alcanza exactamente la única ruta administrada que
  establezca, no todas las rutas administradas de la granja.

Solución de problemas
=====================

La autenticación falla en silencio
----------------------------------

**Síntoma**: las solicitudes devuelven 401 (o algo similar) sin nada claro en el log que lo explique

**Puntos a verificar**:

1. Compruebe si hay configurado más de uno de ``auth.kerberos.principal``, ``auth.ntlm.user`` y
   ``auth.oauth.client_id``; dos o más hacen fallar el trabajo con un error de validación antes de
   que empiece el rastreo
2. Para Kerberos, confirme que ``-Djava.security.krb5.conf=...`` está configurado en
   ``jvm.crawler.options``. Configurarlo en cualquier lugar que solo afecte a la aplicación web no
   tiene ningún efecto. Después de cambiarlo, vuelva a ejecutar el trabajo de rastreo; reiniciar la
   aplicación web no lo recoge
3. Para Kerberos, confirme que ``udp_preference_limit = 1`` está configurado en la sección
   ``[libdefaults]`` de ``krb5.conf``. Sin esto, un KDC que no responda puede hacer que cada
   autenticación se bloquee durante unos 90 segundos (tres reintentos UDP de 30 segundos) sin nada
   en el log
4. Confirme que el principal está escrito como ``user@REALM``; un ``user`` sin realm se resuelve
   contra el ``default_realm`` que en ese momento indique el ``krb5.conf`` compartido
5. Para OAuth, confirme que ``client_secret``, ``tenant`` y ``realm`` no están vacíos; solo se
   valida la presencia de ``client_id``, por lo que los demás pueden quedar vacíos en silencio
6. Confirme que IIS Extended Protection no está configurado como ``tokenChecking=Require``; no hay
   ninguna solución alternativa para ese ajuste
7. Para un rastreo de larga duración, compruebe si empezó a fallar solo a mitad de camino; el ticket
   de Kerberos se obtiene una sola vez al construirse el cliente HTTP y nunca se renueva, por lo que
   un rastreo que dura más que el ticket empieza a fallar a mitad de camino

El rastreo es lento (503 y la puntuación de estado)
---------------------------------------------------

**Síntoma**: el rastreo tarda mucho más de lo esperado, o se agota el tiempo de espera

**Puntos a verificar**:

1. Compruebe el ``X-SharePointHealthScore`` de la granja de SharePoint durante la ventana de
   lentitud. Una puntuación de 9 o superior añade una espera antes de cada solicitud (unos 2
   segundos en 9, unos 4 en 10, duplicándose a partir de ahí, sin límite agregado), lo que puede
   convertir un rastreo que debería tardar horas en uno que tarda mucho más
2. Compruebe si hay respuestas 503 repetidas. Un 503 se reintenta hasta ``retry_limit`` veces,
   esperando 2, luego 4 y luego 8 segundos (con un límite de 30) antes de cada reintento
3. Compruebe si ``number_of_threads`` se ha aumentado demasiado. Más hilos suponen, de forma
   aproximadamente proporcional, más solicitudes contra SharePoint, lo que puede elevar la
   puntuación de estado. Auméntelo gradualmente en una granja local (on-premises)
4. Si ``site.crawl_subsites=true``, recuerde que el tiempo total de rastreo crece aproximadamente
   con el número de subsitios descubiertos; considere reducir el alcance con ``site.max_depth``

No se indexa nada
-----------------

**Síntoma**: el rastreo finaliza con normalidad, pero la búsqueda devuelve cero resultados

**Puntos a verificar**:

1. Compruebe el log del rastreador en busca de errores o advertencias (establezca
   ``org.codelibs.fess.ds`` en ``DEBUG`` en ``app/WEB-INF/env/crawler/resources/log4j2.xml``)
2. Compruebe si hay errores tipográficos en ``url``, ``site.name`` (o ``site.path``) y
   ``site.list_name``; recuerde que ``site.name`` no es necesario una vez que se configura
   ``site.path``
3. Confirme que la autenticación realmente se está realizando con éxito (sin 401); una solicitud que
   nunca llega a autenticarse es una causa mucho más habitual que un ``role.skip`` o
   ``default_permissions`` mal configurados
4. Si se configura ``include_pattern`` o ``exclude_pattern``, recuerde que estos comparan con una
   ruta relativa al servidor (para un archivo de biblioteca de documentos o un archivo adjunto de
   elemento de lista) o con ``FileRef`` (para un elemento de lista), no con la URL que se muestra en
   los resultados de búsqueda. Compruebe si el patrón está escrito para una URL completa
5. Compruebe si ``supported_mimetypes`` o ``max_content_length`` está excluyendo los archivos que
   espera ver
6. Compruebe si ``site.exclude_list`` o ``site.exclude_folder`` está excluyendo el objetivo de forma
   no intencionada

Información de referencia
=========================

- :doc:`ds-overview` - Descripción general de conectores de almacén de datos
- :doc:`ds-microsoft365` - Conector de Microsoft 365 (para SharePoint Online)
- :doc:`../../admin/dataconfig-guide` - Guía de configuración del almacén de datos
- :doc:`../../admin/plugin-guide` - Guía de gestión de plugins
