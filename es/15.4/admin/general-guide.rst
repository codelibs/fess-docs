=======
General
=======

Descripción general
===================

En esta página de administración, puede gestionar la configuración de |Fess|.
Puede cambiar varias configuraciones de |Fess| sin necesidad de reiniciarlo.

|image0|

Contenido de la configuración
==============================

Sistema
-------

Respuesta JSON
::::::::::::::

Especifique si desea habilitar la API JSON.

Se requiere inicio de sesión
:::::::::::::::::::::::::::::

Especifique si desea hacer que el inicio de sesión sea obligatorio para la función de búsqueda.

Mostrar enlace de inicio de sesión
:::::::::::::::::::::::::::::::::::

Configure si desea mostrar el enlace a la página de inicio de sesión en la pantalla de búsqueda.

Contraer resultados duplicados
:::::::::::::::::::::::::::::::

Configure si desea habilitar la contracción de resultados duplicados.

Mostrar miniaturas
::::::::::::::::::

Configure si desea habilitar la visualización de miniaturas.

Valor de etiqueta predeterminado
:::::::::::::::::::::::::::::::::

Describa el valor de etiqueta que se agregará a las condiciones de búsqueda de forma predeterminada.
Si especifica por rol o grupo, añada "role:" o "group:" como en "role:admin=label1".

Valor de ordenamiento predeterminado
:::::::::::::::::::::::::::::::::::::

Describa el valor de ordenamiento que se agregará a las condiciones de búsqueda de forma predeterminada.
Si especifica por rol o grupo, añada "role:" o "group:" como en "role:admin=content_length.desc".

Host virtual
::::::::::::

Configure el host virtual.
Para más detalles, consulte :doc:`Host virtual en la guía de configuración <../config/virtual-host>`.

Respuesta de palabras populares
::::::::::::::::::::::::::::::::

Especifique si desea habilitar la API de palabras populares.

Codificación de archivos CSV
:::::::::::::::::::::::::::::

Especifique la codificación de los archivos CSV que se descargarán.

Agregar parámetros de búsqueda
:::::::::::::::::::::::::::::::

Habilite esto si desea pasar parámetros a la visualización de resultados de búsqueda.

Correo de notificación
::::::::::::::::::::::

Especifique las direcciones de correo electrónico que recibirán notificaciones al completarse el rastreo.
Se pueden especificar varias direcciones separadas por comas. Se requiere un servidor de correo para su uso.

Rastreador
----------

Verificar fecha de última actualización
::::::::::::::::::::::::::::::::::::::::

Habilite esto para realizar rastreo diferencial.

Configuración simultánea del rastreador
::::::::::::::::::::::::::::::::::::::::

Especifique el número de configuraciones de rastreo que se ejecutarán simultáneamente.

Eliminar documentos anteriores
:::::::::::::::::::::::::::::::

Especifique el número de días del período de validez después de la indexación.

Tipos de error excluidos
:::::::::::::::::::::::::

Las URL con fallas que excedan el umbral se excluyen del rastreo, pero los nombres de excepción especificados aquí seguirán siendo objeto de rastreo incluso si exceden el umbral de URL con fallas.

Umbral de número de fallas
:::::::::::::::::::::::::::

Si un documento objeto de rastreo se registra en las URL con fallas más veces que el número especificado aquí, se excluirá del próximo rastreo.

Registro
--------

Registro de búsqueda
::::::::::::::::::::

Especifique si desea habilitar el registro de búsquedas.

Registro de usuario
:::::::::::::::::::

Especifique si desea habilitar el registro de usuarios.

Registro de favoritos
:::::::::::::::::::::

Especifique si desea habilitar el registro de favoritos.

Eliminar registros de búsqueda anteriores
::::::::::::::::::::::::::::::::::::::::::

Elimina los registros de búsqueda anteriores al número de días especificado.

Eliminar registros de trabajo anteriores
:::::::::::::::::::::::::::::::::::::::::

Elimina los registros de trabajo anteriores al número de días especificado.

Eliminar registros de usuario anteriores
:::::::::::::::::::::::::::::::::::::::::

Elimina los registros de usuario anteriores al número de días especificado.

Nombres de bots para eliminar del registro
:::::::::::::::::::::::::::::::::::::::::::

Especifique los nombres de bots que se excluirán de los registros de búsqueda.

Nivel de registro
:::::::::::::::::

Especifique el nivel de registro para fess.log.

Sugerencias
-----------

Sugerir con términos de búsqueda
:::::::::::::::::::::::::::::::::

Especifique si desea generar candidatos de sugerencia a partir de los registros de búsqueda.

Sugerir con documentos
:::::::::::::::::::::::

Especifique si desea generar candidatos de sugerencia a partir de los documentos indexados.

Eliminar información de sugerencias anterior
:::::::::::::::::::::::::::::::::::::::::::::

Elimina los datos de sugerencias anteriores al número de días especificado.

LDAP
----

URL de LDAP
:::::::::::

Especifique la URL del servidor LDAP.

Base DN
:::::::

Especifique el nombre distinguido base para iniciar sesión en la pantalla de búsqueda.

Bind DN
:::::::

Especifique el Bind DN del administrador.

Contraseña
::::::::::

Especifique la contraseña del Bind DN.

User DN
:::::::

Especifique el nombre distinguido del usuario.

Filtro de cuenta
::::::::::::::::

Especifique el Common Name o uid del usuario.

Filtro de grupo
:::::::::::::::

Especifique las condiciones de filtro para los grupos que desea obtener.

Atributo memberOf
:::::::::::::::::

Especifique el nombre del atributo memberOf disponible en el servidor LDAP.
Para Active Directory, es memberOf.
Para otros servidores LDAP, puede ser isMemberOf.


Visualización de notificaciones
--------------------------------

Página de inicio de sesión
:::::::::::::::::::::::::::

Describa el mensaje que se mostrará en la pantalla de inicio de sesión.

Página principal de búsqueda
:::::::::::::::::::::::::::::

Describa el mensaje que se mostrará en la pantalla principal de búsqueda.

Almacenamiento
--------------

Después de configurar cada elemento, aparecerá un menú [Sistema > Almacenamiento] en el menú izquierdo.
Para la gestión de archivos, consulte :doc:`Almacenamiento <../admin/storage-guide>`.

Tipo
::::

Especifique el tipo de almacenamiento.
Cuando se selecciona "Automático", el tipo de almacenamiento se determina automáticamente a partir del punto de acceso.

- **Automático**: Detección automática desde el punto de acceso
- **S3**: Amazon S3
- **GCS**: Google Cloud Storage

Bucket
::::::

Especifique el nombre del bucket a gestionar.

Punto de acceso
:::::::::::::::

Especifique la URL del punto de acceso del servidor de almacenamiento.

- S3: Utiliza el punto de acceso predeterminado de AWS si está vacío
- GCS: Utiliza el punto de acceso predeterminado de Google Cloud si está vacío
- MinIO, etc.: La URL del punto de acceso del servidor MinIO

Clave de acceso
:::::::::::::::

Especifique la clave de acceso para S3 o almacenamiento compatible con S3.

Clave secreta
:::::::::::::

Especifique la clave secreta para S3 o almacenamiento compatible con S3.

Región
::::::

Especifique la región de S3 (ej.: ap-northeast-1).

ID de proyecto
::::::::::::::

Especifique el ID del proyecto de Google Cloud para GCS.

Ruta de credenciales
::::::::::::::::::::

Especifique la ruta al archivo JSON de credenciales de la cuenta de servicio para GCS.

Ejemplo
=======

Ejemplo de configuración LDAP
------------------------------

.. tabularcolumns:: |p{4cm}|p{4cm}|p{4cm}|
.. list-table:: Configuración de LDAP/Active Directory
   :header-rows: 1

   * - Nombre
     - Valor (LDAP)
     - Valor (Active Directory)
   * - URL de LDAP
     - ldap://SERVERNAME:389
     - ldap://SERVERNAME:389
   * - Base DN
     - cn=Directory Manager
     - dc=fess,dc=codelibs,dc=org
   * - Bind DN
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - manager@fess.codelibs.org
   * - User DN
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - %s@fess.codelibs.org
   * - Filtro de cuenta
     - cn=%s o uid=%s
     - (&(objectClass=user)(sAMAccountName=%s))
   * - Filtro de grupo
     -
     - (member:1.2.840.113556.1.4.1941:=%s)
   * - memberOf
     - isMemberOf
     - memberOf


.. |image0| image:: ../../../resources/images/en/15.4/admin/general-1.png
.. pdf            :height: 940 px
