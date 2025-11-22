=======================
Impulso de Documento
=======================

Descripción general
===================

Aquí se explica la configuración relacionada con el impulso de documento.
Al configurar el impulso de documento, puede posicionar documentos en la parte superior de los resultados de búsqueda independientemente del término de búsqueda.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de impulso de documento que se muestra a continuación, haga clic en [Rastreador > Impulso de documento] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración de impulso de documento, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Condición
:::::::::

Especifique la condición de los documentos que desea posicionar en la parte superior.
Por ejemplo, si desea mostrar en la parte superior las URL que contienen https://www.n2sm.net/, describa url.matches("https://www.n2sm.net/.*").
Las condiciones se pueden describir en Groovy.

Expresión de valor de impulso
::::::::::::::::::::::::::::::

Especifique el valor de ponderación del documento.
Las expresiones se pueden describir en Groovy.

Orden de clasificación
:::::::::::::::::::::::

Configure el orden de clasificación del impulso de documento.

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación. Al presionar el botón de eliminar, se eliminará la configuración.


.. |image0| image:: ../../../resources/images/es/15.3/admin/boostdoc-1.png
.. |image1| image:: ../../../resources/images/es/15.3/admin/boostdoc-2.png
