============
Diccionario
============

Descripción general
===================

Aquí se explica la configuración relacionada con los diccionarios.

Realice cambios en los diccionarios después de comprender las especificaciones de cada diccionario.
Si la modificación del diccionario falla, es posible que no se pueda acceder al índice.

Lista
=====

Para abrir la página de lista de diccionarios administrables que se muestra a continuación, haga clic en [Sistema > Diccionario] en el menú izquierdo.


|image0|


Kuromoji
========

Administra el diccionario para el análisis morfológico del japonés.
ja/kuromoji.txt es el archivo de diccionario para el análisis morfológico del japonés.

Sinónimos
=========

Administra el diccionario de sinónimos.
synonym.txt es el archivo de diccionario de sinónimos utilizado comúnmente en todos los idiomas.

Mapeo
=====

Administra el diccionario de sustitución de caracteres.
mapping.txt es el archivo de diccionario de sustitución de palabras común a todos los idiomas o para cada idioma.

Protwords
=========

Administra el diccionario de palabras protegidas.
protwords.txt se coloca para cada idioma y es un archivo de lista de palabras que se excluirán del stemming, etc.

Palabras vacías
===============

Administra el diccionario de palabras vacías.
stopwords.txt se coloca para cada idioma y es un archivo de lista de palabras que se excluirán al crear el índice.

Anulación de Stemmer
====================

Administra el diccionario de anulación de Stemmer.
stemmer_override.txt se coloca para cada idioma y es un archivo de diccionario de sustitución de palabras para anular el procesamiento de stemming.


.. |image0| image:: ../../../resources/images/en/15.4/admin/dict-1.png
            :height: 940px
