==================
Diccionario de Mapeo
==================

Descripción general
===================

Puede mapear caracteres específicos (símbolos, códigos de caracteres, ancho completo/medio) a otros caracteres.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de mapeo que se muestra a continuación, seleccione [Sistema > Diccionario] en el menú izquierdo y luego haga clic en mapping.

|image0|

Para editar, haga clic en el nombre de la configuración.

Método de configuración
-----------------------

Para abrir la página de configuración de mapeo, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Origen de la conversión
:::::::::::::::::::::::

Ingrese los caracteres (símbolos, códigos de caracteres, ancho completo/medio) que serán objeto del mapeo.

Después de la conversión
:::::::::::::::::::::::::

Expanda los caracteres ingresados en el origen de la conversión con los caracteres después de la conversión.

Descarga
========

Puede descargar en el formato de diccionario de mapeo.

Carga
=====

Puede cargar en el formato de diccionario de mapeo.

Diccionarios de mapeo incluidos
===============================

El ``mapping.txt`` predeterminado se usa al analizar campos de búsqueda como ``title`` y
``content``. Unifica hiragana, kana pequeños y katakana de ancho medio en katakana de ancho completo,
de modo que りんご, リンゴ y ﾘﾝｺﾞ coinciden entre sí. En |Fess| 15.9 también unifica las siguientes
grafías:

- ゐ y ゑ (a イ y エ), kana pequeños como ゎ, ゕ, ゖ, ヮ, ヵ, ヶ y ㇰ-ㇿ, y ゝ y ゞ (a ヽ y ヾ)
- ヴ, ヴャ, ヴュ y ヴョ, el hiragana ゔ, ｳﾞ de ancho medio, y ウ o う seguidos de una marca de sonoridad
  combinable (U+3099); por ejemplo, ラヴ pasa a ラブ y レヴュー a レビユー

Además, ‐ ‑ ‒ – — ― ⁻ ₋ − y － escritos justo después de un kana se tratan como la marca de vocal
larga ー (``prolonged_sound_mark_filter``), por lo que サ―バ－ y サ−バ‐ coinciden con サーバー. El
guion ASCII (``-``) y los guiones después de kanji, letras o dígitos (東京－大阪, 2026−10−02) no se
modifican.

``ja/mapping.txt`` para japonés (los campos ``*_ja``) mantiene el hiragana y los kana pequeños tal
cual, porque el analizador morfológico los necesita, y solo unifica grafías como ヴ.

.. note::

   Estos ajustes se aplican a un índice de documentos recién creado. Un índice existente conserva
   sus ajustes de análisis y diccionarios hasta que se reindexa. Para aplicarlos a un índice
   existente, reindexe con "Restablecer diccionarios" activado en la página :doc:`maintenance-guide`.
   Restablecer los diccionarios sobrescribe las modificaciones de ``mapping.txt`` /
   ``ja/mapping.txt`` hechas en la pantalla de administración.

.. |image0| image:: ../../../resources/images/en/15.9/admin/mapping-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/mapping-2.png

