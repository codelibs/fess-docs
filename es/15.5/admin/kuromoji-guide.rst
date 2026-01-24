=====================
Diccionario Kuromoji
=====================

Descripción general
===================

Puede registrar nombres de personas, nombres propios, términos especializados, etc. para el análisis morfológico.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de Kuromoji que se muestra a continuación, seleccione [Sistema > Diccionario] en el menú izquierdo y luego haga clic en kuromoji.

|image0|

Para editar, haga clic en el nombre de la configuración.

Método de configuración
-----------------------

Para abrir la página de configuración de Kuromoji, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Token
:::::

Ingrese la palabra a procesar en el análisis morfológico.

Segmentación
::::::::::::

Si una palabra está compuesta de una palabra compuesta, puede hacer que se encuentre incluso cuando se busca con la palabra segmentada.
Por ejemplo, al ingresar "全文検索エンジン" como "全文 検索 エンジン", puede permitir que se busque también con palabras segmentadas.

Lectura
:::::::

Ingrese la lectura de la palabra ingresada como token en katakana.
Si se realizó segmentación, ingrésela segmentada.
Por ejemplo, ingrese "ゼンブン ケンサク エンジン".

Parte del discurso
::::::::::::::::::

Ingrese la parte del discurso de la palabra ingresada.

Descarga
========

Puede descargar en el formato de diccionario de Kuromoji.

Carga
=====

Puede cargar en el formato de diccionario de Kuromoji.
El formato de diccionario de Kuromoji está separado por comas (,) como "token,token segmentado,lectura del token segmentado,parte del discurso".
Los tokens segmentados se separan con espacios.
Si no es necesario segmentar, el token y el token segmentado serán iguales.
Por ejemplo, sería como sigue:

::

    朝青龍,朝青龍,アサショウリュウ,カスタム名詞
    関西国際空港,関西 国際 空港,カンサイ コクサイ クウコウ,カスタム名詞


.. |image0| image:: ../../../resources/images/en/15.5/admin/kuromoji-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/kuromoji-2.png
