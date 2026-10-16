====================================
Diccionario de Anulación de Stemmer
====================================

Descripción general
===================

Puede anular la raíz (stem) de palabras concretas con una raíz que usted especifique. Utilícelo para palabras cuyo resultado de stemming no sea el deseado.
Por ejemplo, si establece la raíz de ``mice`` como ``mous``, ``mice`` y ``mouse`` se buscan como la misma palabra (el stemmer de inglés convierte ``mouse`` en ``mous``).

Sustituir caracteres como símbolos, códigos de caracteres o caracteres de ancho completo/medio por otros caracteres no es función de este diccionario. Para ello utilice el diccionario de sustitución de caracteres (:doc:`mapping-guide`).

La lista muestra un diccionario por idioma (``en/stemmer_override.txt``, etc.). Elija y edite el diccionario que corresponda al idioma de la palabra. Consulte :doc:`dict-guide` para saber qué diccionario se aplica a qué campos.
Guardar un cambio no basta para que surta efecto en las búsquedas. Consulte :ref:`dict-apply-changes` para saber cómo aplicarlo.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de anulación de Stemmer que se muestra a continuación, seleccione [Sistema > Diccionario] en el menú izquierdo y luego haga clic en stemmeroverride.

|image0|

Para editar, haga clic en el nombre de la configuración.

Método de configuración
-----------------------

Para abrir la página de configuración de anulación de Stemmer, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Origen de la conversión
:::::::::::::::::::::::

Ingrese la palabra cuya raíz desea anular. El análisis convierte la palabra a minúsculas antes de compararla con este diccionario, por lo que debe ingresarla en minúsculas.

Después de la conversión
:::::::::::::::::::::::::

Ingrese la palabra que se usará como raíz de la palabra ingresada en el origen de la conversión.
La palabra de destino se indexa tal cual, sin aplicar stemming. Como los términos de búsqueda sí pasan por el stemming, para obtener los mismos resultados que con la palabra original ingrese el resultado de pasar la palabra normal por el stemmer (``mous`` para ``mouse``).
Por ejemplo, ingrese ``mice`` como origen y ``mous`` como destino.

Descarga
========

Puede descargar en el formato de diccionario de anulación de Stemmer.

Carga
=====

Puede cargar en el formato de diccionario de anulación de Stemmer.

.. warning::

   Al cargar un archivo, el contenido del diccionario se sustituye por el contenido del archivo cargado. Se elimina todo lo que no esté en el archivo, incluidas las entradas registradas desde la pantalla. Si es necesario, descargue primero el diccionario e incluya su contenido en el archivo que va a cargar.


.. |image0| image:: ../../../resources/images/en/15.10/admin/stemmeroverride-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/stemmeroverride-2.png

