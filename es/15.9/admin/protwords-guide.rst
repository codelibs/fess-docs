========================
Diccionario de Protwords
========================

Descripción general
===================

Puede administrar palabras que se excluirán del procesamiento de stemming.
El procesamiento de stemming es básicamente un procesamiento basado en reglas, por lo que puede ocurrir una normalización no deseada.
Por ejemplo, la palabra Maine (nombre de un estado de EE. UU.) se normaliza a main.

Para que esta palabra se pueda buscar tal cual, registre ``maine`` (escriba las palabras en minúsculas; consulte "Parámetros de configuración").

La lista muestra un diccionario por idioma (``en/protwords.txt``, ``de/protwords.txt``, etc.). Elija y edite el diccionario que corresponda al idioma de la palabra. Consulte :doc:`dict-guide` para saber qué diccionario se aplica a qué campos.
Guardar un cambio no basta para que surta efecto en las búsquedas. Consulte :ref:`dict-apply-changes` para saber cómo aplicarlo.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de Protwords que se muestra a continuación, seleccione [Sistema > Diccionario] en el menú izquierdo y luego haga clic en protwords.

|image0|

Para editar, haga clic en el nombre de la configuración.

Método de configuración
-----------------------

Para abrir la página de configuración de Protwords, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Información de la palabra
::::::::::::::::::::::::::

Ingrese las palabras que se excluirán del procesamiento de stemming.

Ingrese las palabras en minúsculas. El análisis convierte la palabra a minúsculas antes de compararla con este diccionario, por lo que ingresar ``Maine`` no la protege. En el ejemplo de la descripción general, ingrese ``maine``.


Descarga
========

Puede descargar en el formato de diccionario de Protwords.

Carga
=====

Puede cargar en el formato de diccionario de Protwords.

.. warning::

   Al cargar un archivo, el contenido del diccionario se sustituye por el contenido del archivo cargado. Se eliminan las palabras que no estén en el archivo, incluidas las registradas desde la pantalla. Si es necesario, descargue primero el diccionario e incluya su contenido en el archivo que va a cargar.


.. |image0| image:: ../../../resources/images/en/15.9/admin/protwords-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/protwords-2.png
