==========
Etiquetas
==========

Descripción general
===================


Aquí se explica la configuración relacionada con las etiquetas.
Las etiquetas pueden clasificar los documentos que se muestran en los resultados de búsqueda.
La configuración de etiquetas especifica con expresiones regulares las rutas a las que se agregarán etiquetas.
Si registra etiquetas, se mostrará un cuadro desplegable de etiquetas en las opciones de búsqueda.

Esta configuración de etiquetas se aplica a la configuración de rastreo web o del sistema de archivos.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de etiquetas que se muestra a continuación, haga clic en [Rastreador > Etiqueta] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración de etiquetas, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Nombre
::::::

Especifique el nombre que se mostrará en el cuadro desplegable de selección de etiquetas durante la búsqueda.

Valor
:::::

Especifique el identificador al clasificar documentos.
Especifíquelo en caracteres alfanuméricos.

Rutas objetivo
::::::::::::::

Configure con expresiones regulares las rutas a las que se agregarán etiquetas.
Puede especificar múltiples rutas describiéndolas en múltiples líneas.
Se configurará la etiqueta en los documentos que coincidan con las rutas especificadas aquí.

Rutas excluidas
:::::::::::::::

Configure con expresiones regulares las rutas que desea excluir del objetivo entre las rutas objetivo de rastreo.
Puede especificar múltiples rutas describiéndolas en múltiples líneas.

Permisos
::::::::

Especifique el permiso para esta configuración.
La forma de especificar permisos es, por ejemplo, para mostrar resultados de búsqueda a usuarios que pertenecen al grupo developer, especifique {group}developer.
La especificación por usuario es {user}nombre_usuario, la especificación por rol es {role}nombre_rol, y la especificación por grupo es {group}nombre_grupo.

Host virtual
::::::::::::

Especifique el nombre de host del host virtual.
Para más detalles, consulte :doc:`Host virtual en la guía de configuración <../config/security-virtual-host>`.

En una pantalla de búsqueda a la que se accede mediante un host virtual solo se muestran las etiquetas cuyo campo especifica el nombre de ese host virtual.
Las etiquetas con este campo vacío no se muestran cuando se accede mediante un host virtual.
En los accesos que no coinciden con ningún host virtual se muestran todas las etiquetas, independientemente de este campo.

Cada etiqueta admite un solo host virtual.
Para mostrar la misma etiqueta en varios hosts virtuales, cree una etiqueta con el mismo nombre y valor para cada host virtual e indique en el campo de host virtual de cada una el nombre de ese host virtual.
Como el valor es el mismo, cualquiera de las etiquetas filtra los mismos documentos.

Orden de clasificación
::::::::::::::::::::::

Especifique el orden de clasificación de las etiquetas.

Tipo
::::

Indique "Etiqueta" o "Etiqueta de usuario". Una etiqueta normal es "Etiqueta". "Etiqueta de usuario"
es una etiqueta que los usuarios añaden desde la pantalla de búsqueda (consulte "Etiquetas de
usuario" más abajo). Una etiqueta existente sin tipo se trata como "Etiqueta".


Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.

Etiquetas de usuario
--------------------

Con ``user.tag.enabled=true`` (predeterminado: ``false``) en ``fess_config.properties``, los
usuarios que han iniciado sesión pueden etiquetar los resultados de búsqueda. En el tema incluido
``bootstrap``, las etiquetas se muestran en los resultados, los usuarios pueden añadir etiquetas y
quitar las suyas, y una faceta "Etiquetas" acota los resultados. Para la API, consulte
:doc:`../api/api-tag`.

Una etiqueta de usuario se guarda como una etiqueta del tipo "Etiqueta de usuario": el nombre es el
nombre de la etiqueta, el valor es el SHA-256 del nombre, las rutas incluidas son las URL etiquetadas
(una por línea, coincidencia exacta) y los permisos deciden quién puede verla. El usuario que añade
una etiqueta se agrega a sus permisos.

- Una etiqueta solo es visible cuando los permisos de su etiqueta coinciden con quien llama. Los
  administradores pueden editarla en esta página para compartirla con un rol o un grupo, o
  eliminarla.
- Las etiquetas con el mismo nombre se combinan en una sola, por lo que los usuarios que añadieron una
  etiqueta con el mismo nombre ven dónde están las etiquetas de los demás.
- Las etiquetas de usuario no se incluyen en la API de lista de etiquetas (``/api/v2/labels``) ni en
  las opciones de etiqueta de la pantalla de búsqueda.
- Cuentan para el límite de etiquetas (``page.labeltype.max.fetch.size``, predeterminado: 1000). Al
  alcanzarlo, no se pueden crear nuevas.
- Después de que un administrador cambie o elimine una etiqueta de usuario en esta página, los
  documentos indexados conservan los valores anteriores hasta que se vuelven a rastrear o se ejecuta
  el trabajo "Label Updater".
- Un documento puede tener hasta ``user.tag.max.document.tags`` (predeterminado: 100) etiquetas de
  usuario, y un nombre puede tener hasta ``user.tag.name.max.length`` (predeterminado: 50)
  caracteres.

.. |image0| image:: ../../../resources/images/en/15.9/admin/labeltype-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/labeltype-2.png
