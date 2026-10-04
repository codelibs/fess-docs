===================
Etiqueta de usuario
===================

Descripción general
===================

Aquí se explica la pantalla que gestiona las etiquetas de los usuarios.

Una etiqueta de usuario es una marca que un usuario que ha iniciado sesión asigna a documentos de los
resultados de búsqueda. Se gestionan por usuario: quien crea una etiqueta es su propietario, y dos
usuarios pueden usar el mismo nombre y tener aun así dos etiquetas distintas. Las etiquetas de usuario
no son :doc:`etiquetas <labeltype-guide>`, que los administradores definen mediante patrones de URL;
los usuarios las crean ellos mismos y las asignan a documentos concretos.

Las etiquetas de usuario están deshabilitadas de forma predeterminada. Para usarlas, configure
``user.tag.enabled=true`` en ``fess_config.properties``. Una vez habilitadas, el tema ``bootstrap``
incluido permite a los usuarios que han iniciado sesión asignar etiquetas a los resultados de búsqueda
y quitarlas, y filtrar con una faceta de etiquetas. En "Mis etiquetas" pueden renombrar, compartir y
eliminar sus propias etiquetas. Las etiquetas compartidas de otros usuarios se muestran con el
prefijo "Compartida:". Para la API de usuario y la configuración, consulte :doc:`../api/api-tag`.

En esta pantalla, los administradores pueden listar, crear, editar y eliminar las etiquetas de todos
los usuarios.

Método de gestión
=================

Método de visualización
-----------------------

Para abrir la página de lista de etiquetas de usuario, haga clic en [Rastreador > Etiqueta de usuario]
en el menú izquierdo. Para verla se necesita el rol ``admin-tagtype`` o ``admin-tagtype-view``, y para
crear, editar y eliminar, ``admin-tagtype``.

La lista muestra el nombre y el propietario de cada etiqueta, por orden de clasificación, nombre y
propietario. Puede buscar por nombre y por propietario; cada uno coincide con las etiquetas que
contienen el texto introducido.

Para editar una etiqueta, haga clic en su nombre.

Crear configuración
-------------------

Para abrir la página de creación de etiquetas, haga clic en el botón de nueva creación.

Parámetros de configuración
---------------------------

Nombre
::::::

Especifica el nombre de la etiqueta. El nombre se normaliza con NFKC, los espacios consecutivos se
reducen a uno y se recortan los extremos. El resultado debe tener entre 1 y
``user.tag.name.max.length`` (predeterminado: 50) caracteres y no puede contener caracteres de
control ni de formato.

Propietario
:::::::::::

Especifica el ID de usuario de inicio de sesión del usuario propietario de la etiqueta. El
propietario y el nombre juntos identifican una etiqueta, por lo que un propietario no puede tener dos
etiquetas con el mismo nombre, ni siquiera en hosts virtuales distintos.

Si cambia el propietario, el permiso de usuario del propietario anterior en Permisos se sustituye por
el del nuevo propietario.

Rutas
:::::

Especifica las URL de los documentos a los que se asigna la etiqueta, una por línea. Una URL debe ser
igual al campo ``url`` de un documento indexado; no se usan expresiones regulares. Una etiqueta puede
tener como máximo ``user.tag.max.paths`` (predeterminado: 10000) URL.

Permisos
::::::::

Especifica los usuarios, grupos y roles que pueden ver la etiqueta, igual que en las etiquetas:
{user}nombre de usuario para un usuario, {group}nombre de grupo para un grupo y {role}nombre de rol
para un rol. Si se deja vacío, solo el propietario puede ver la etiqueta.

El propietario siempre ve sus propias etiquetas, sean cuales sean los permisos. Un usuario que no ha
iniciado sesión nunca ve una etiqueta, sean cuales sean los permisos.

Host virtual
::::::::::::

Especifica el nombre de host del host virtual en el que se muestra la etiqueta. Una etiqueta creada
por un usuario recibe el host virtual por el que accedía el usuario. En una pantalla de búsqueda a la
que se accede mediante un host virtual, solo son visibles las etiquetas que tienen aquí ese nombre de
host virtual. Un acceso que no coincide con ningún host virtual ve las etiquetas sea cual sea el valor
de este campo. Para obtener más información, consulte
:doc:`Host virtual en la guía de configuración <../config/security-virtual-host>`.

Orden de clasificación
::::::::::::::::::::::

Especifica el orden de visualización de la etiqueta.

Eliminar configuración
----------------------

Haga clic en un nombre en la página de lista y luego en el botón de eliminar para que aparezca una
pantalla de confirmación. Al presionar el botón de eliminar, se elimina la etiqueta y su valor se
quita de los documentos.

Compartir
=========

Cuando un usuario comparte una etiqueta, los valores de ``role.search.guest.permissions``
(predeterminado: ``{role}guest``) se añaden a sus permisos. La visibilidad de una etiqueta se decide
añadiendo estos valores a los roles del usuario que ha iniciado sesión, por lo que una etiqueta
compartida es visible para todos los usuarios que han iniciado sesión, que también pueden filtrar por
ella. Dejar de compartirla quita solo estos valores.

En esta pantalla, un administrador también puede añadir grupos o roles a los permisos para mostrar
una etiqueta solo a algunos usuarios. Solo el propietario y los administradores pueden cambiar una
etiqueta; los demás usuarios solo pueden mostrar y filtrar por las etiquetas que ven.

Cómo llegan los cambios a los documentos
========================================

Un documento guarda sus etiquetas de usuario en el campo ``tag`` del índice, como
``base64url(nombre):base64url(propietario)``.

- Crear, editar y eliminar etiquetas, y que los usuarios las asignen a documentos o las quiten, se
  guarda de inmediato en las etiquetas (el índice ``fess_config.tag_type``). Los documentos se
  actualizan mediante una cola en memoria que el trabajo "Log Aggregator" (``log_aggregator``) aplica
  en bloque cada minuto, por lo que los resultados de búsqueda reflejan un cambio al cabo de hasta un
  minuto aproximadamente.
- Cambiar las rutas en esta pantalla actualiza los documentos de las URL añadidas y quitadas. Cambiar
  el nombre o el propietario sustituye el valor anterior en los documentos por el nuevo.
- Cuando un rastreo o un almacén de datos indexa documentos, su campo ``tag`` se establece a partir
  de las rutas de las etiquetas, por lo que las etiquetas se conservan al volver a rastrear.
- El trabajo "Tag Updater" (``tag_updater``) reconstruye el campo ``tag`` de todos los documentos a
  partir de las etiquetas. No tiene programación; ejecútelo desde el programador cuando sea necesario.

Notas para la operación
=======================

- **Ejecute Log Aggregator en todos los nodos.** Cada JVM tiene su propia cola, que solo procesa el
  Log Aggregator de ese nodo. Mantenga el destino del trabajo ``log_aggregator`` en el valor
  predeterminado ``all``; si se limita a algunos nodos, los cambios recibidos por los demás nodos
  nunca llegan a los documentos.
- **Ejecute Tag Updater en los siguientes casos.** La cola está en memoria, por lo que los cambios
  aún no aplicados se pierden cuando |Fess| se reinicia. Mientras ``user.tag.enabled=false``, los
  cambios de etiquetas no llegan a los documentos y volver a rastrear borra su campo ``tag``. Después
  de restaurar desde una copia de seguridad, también hay que reconstruir las etiquetas de los
  documentos. Y cuando la cola supera ``user.tag.queue.max.size`` (predeterminado: 10000), los
  cambios que sobran se descartan con un registro WARN. En todos estos casos, ejecutar
  ``tag_updater`` reconstruye las etiquetas de los documentos.
- **El propietario de una etiqueta es el ID de usuario de inicio de sesión.** Si un ID de usuario
  cambia, las etiquetas se quedan con el ID anterior. Con SAML, el NameID debe ser persistente. Con
  Entra ID el propietario es el UPN, y con LDAP es el nombre de usuario con las mayúsculas y
  minúsculas escritas al iniciar sesión. Eliminar un usuario no elimina sus etiquetas; elimine en
  esta pantalla las que ya no se necesiten.
- **También funciona con índices existentes.** Al iniciar, si el índice de documentos no tiene
  asignación para el campo ``tag``, se añade como ``keyword``. Los campos existentes no se modifican.
- Las etiquetas de usuario se guardan en el índice ``fess_config.tag_type``. Se incluyen en
  ``fess_config.bulk`` de una copia de seguridad, pero no en ``fess_basic_config.bulk``.
