================================================
Mejorar la calidad de búsqueda con los registros
================================================

Introducción
============

Cuando los usuarios empiezan a utilizar la búsqueda, surgen comentarios como «no aparece el documento que busco» o «el documento que quiero está enterrado al final de la lista».
Qué ocurre con cada término de búsqueda se puede ver en los registros de búsqueda y de clics que guarda Fess.

En Fess 15.9, la pantalla [Información del sistema] > [Registro de búsqueda] de la consola de administración incluye un informe de análisis que agrega indicadores como la tasa de cero resultados y las posiciones de clic.
En este artículo se explica cómo encontrar en esta pantalla los términos de búsqueda problemáticos, decidir si corregirlos con sinónimos, coincidencia de clave, impulso de documento, consultas relacionadas o palabras vacías, aplicar la corrección y comprobar su efecto en la misma pantalla.

La agregación propia de los registros de búsqueda con OpenSearch Dashboards se trata en :doc:`guide-22`, y el análisis de documentos que mezclan japonés, inglés y chino, en :doc:`guide-09`.

Qué mirar en la pantalla de registro de búsqueda
================================================

Abra [Información del sistema] > [Registro de búsqueda] en el menú de la izquierda y se mostrará la pestaña [Resumen].
Para verla se necesita el rol ``admin-searchlog`` o ``admin-searchlog-view``.

En la parte superior de cada pestaña, elija el período («Hoy», «Ayer», «Últimos 7 días», «Últimos 28 días», «Últimos 90 días», «Personalizado») y el tipo de acceso, y haga clic en [Aplicar].
Si activa «Comparar con el período anterior», se muestran al lado los valores del período anterior con el mismo número de días.
Utilícelo para comparar el antes y el después de una mejora.

Los indicadores que dan pistas para mejorar, y las medidas eficaces para cada uno, son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 24 22 30 24

   * - Indicador
     - Dónde se muestra
     - Qué indica
     - Medidas principales
   * - Tasa de cero resultados, consultas sin resultados
     - Pestañas [Resumen] y [Consultas]
     - La proporción de búsquedas que no obtuvieron ningún resultado y sus términos de búsqueda
     - Sinónimos, consultas relacionadas, añadir documentos
   * - Consultas sin clics
     - Pestaña [Consultas]
     - Términos de búsqueda que obtuvieron resultados, pero cuyos resultados nunca se pulsaron
     - Coincidencia de clave, impulso de documento
   * - Posición media de clic
     - Pestaña [Consultas] (por término), pestaña [Clics] (global)
     - En qué posición estaban los resultados pulsados (el primer resultado es 1)
     - Coincidencia de clave, impulso de documento
   * - Distribución de posiciones de clic, tasa de páginas siguientes vistas
     - Pestaña [Clics]
     - Si los clics se concentran en las posiciones 1-10, 11-20 o de la 21 en adelante, y la proporción de búsquedas en las que se vio la página 2 o posteriores
     - Coincidencia de clave, impulso de documento
   * - Consultas más frecuentes, URL con más clics
     - Pestaña [Resumen], pestaña [Clics]
     - Los términos más buscados y los documentos que realmente se abren
     - Revisar los resultados empezando por los términos de arriba

Como base de estos datos, tenga en cuenta lo siguiente.

- El registro se activa con «Registro de búsqueda» y «Registro de usuario» en [Sistema] > [General] (ambos están activados de forma predeterminada). Si «Registro de usuario» está desactivado, no se cuenta el número de usuarios.
- Un clic se registra cuando «Registro de búsqueda» está activado y un enlace de los resultados de búsqueda se abre a través de ``/go/``. La página de búsqueda del tema estándar (bootstrap) genera sus enlaces de esta forma.
- Los indicadores de clics por término y las consultas sin clics solo cuentan los clics a partir de 15.9, la versión desde la que los clics se registran junto con el término de búsqueda.
- Si hay un número de días indicado en «Eliminar registros de búsqueda anteriores» de [General], los registros más antiguos no se pueden usar para comparar (el valor predeterminado ``-1`` no elimina nada).
- Los registros se escriben por lotes, por lo que una búsqueda puede tardar un poco en aparecer en la pantalla.

Distinguir las causas de las consultas sin resultados
=====================================================

Al hacer clic en una consulta sin resultados en la pestaña [Resumen] o [Consultas], la pestaña [Registros] muestra los registros de búsqueda de ese término filtrados con «Número de resultados» = «Solo sin resultados».
Después de comprobar cuándo y con qué tipo de acceso se buscó, busque realmente el término en la página de búsqueda y clasifique la causa en uno de los tres casos siguientes.

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Situación
     - Medida
     - Operación necesaria para aplicarla
   * - Los documentos existen, pero usan otras palabras (p. ej., los usuarios buscan «laptop» y los documentos dicen «portátil»)
     - Sinónimos
     - Recargar el índice de documentos
   * - Se quiere guiar hacia la denominación oficial (abreviaturas, nombres antiguos, errores de escritura)
     - Consultas relacionadas
     - Ninguna (se aplica al guardar)
   * - No hay documentos correspondientes en el índice
     - Añadir destinos de rastreo (:doc:`guide-04`)
     - Ejecutar un rastreo

La coincidencia de clave y el impulso de documento no sirven para las consultas sin resultados.
Ambos suben la posición de los documentos que coinciden con el término de búsqueda, y ninguno añade a los resultados documentos que no coinciden con él.

Ejemplo práctico: resolver la consulta sin resultados «laptop» con un sinónimo
==============================================================================

Supongamos que «laptop» aparece una y otra vez entre las consultas sin resultados de la pestaña [Consultas], mientras que las normas internas usan la palabra «portátil».
A partir de esta situación, recorreremos todo el proceso, desde la corrección hasta la comprobación.

1. Confirmar la causa
---------------------

Busque «portátil» en la página de búsqueda y compruebe que se encuentran los documentos que los usuarios presumiblemente buscaban.
Si no se encuentran, el problema no está en las palabras: los documentos no están en el índice.
En ese caso, revise los destinos de rastreo en lugar de añadir un sinónimo.

2. Registrar el sinónimo
------------------------

1. Abra [Sistema] > [Diccionario] y, en la lista, haga clic en la fila cuyo «Tipo» es ``synonym`` (la que tiene un nombre que termina en ``synonym.txt``).
2. Haga clic en [Crear nuevo].
3. Introduzca las dos líneas siguientes tanto en «Fuente» como en «Destino» y haga clic en [Crear].

::

    laptop
    portátil

Si pone las mismas palabras en «Fuente» y en «Destino», el diccionario las guarda en una sola línea, ``laptop,portátil``, y al buscar cualquiera de las dos palabras también se encuentran los documentos que contienen la otra.
Si solo quiere ampliar las búsquedas de «laptop», ponga en «Fuente» únicamente la línea «laptop» y en «Destino» las dos líneas anteriores (queda ``laptop=>laptop,portátil``).
Tenga en cuenta que, si «Destino» no incluye la palabra original, ya no se busca la propia palabra original.

Escriba una palabra por línea en los campos de entrada.
No se pueden registrar palabras que contengan una coma (,) o ``=>``.
La referencia del diccionario de sinónimos indica las siguientes reglas de registro.

- Registrar el hiragana como katakana, el katakana pequeño como katakana de tamaño normal y los caracteres alfanuméricos de ancho completo como caracteres de ancho medio
- De forma predeterminada, el texto japonés y el resto del texto CJK se indexan en bigramas divididos cada dos caracteres, por lo que no se deben registrar palabras de un solo carácter
- No registrar la misma palabra más de una vez

Los sinónimos se aplican a los campos ``content`` y ``title`` y expanden las palabras en el momento de la búsqueda.
No es necesario volver a indexar.

3. Aplicar el cambio del diccionario
------------------------------------

Guardar el diccionario no basta para que cambien los resultados de búsqueda.
El índice abierto sigue funcionando con el diccionario antiguo.

1. Abra [Información del sistema] > [Mantenimiento].
2. En «Recargar índice de documentos», haga clic en [Recargar].

Este botón escribe en archivos los diccionarios guardados y, a continuación, cierra el índice de documentos y lo vuelve a abrir.

.. warning::

   Mientras el índice está cerrado, y después de abrirlo hasta que se asignan sus fragmentos (shards), no se puede buscar: las búsquedas devuelven errores o 0 resultados.
   Cuanto mayor es el índice, más tarda, así que ejecútelo en un horario de poco uso.

4. Comprobar el efecto
----------------------

Primero, busque «laptop» en la página de búsqueda y compruebe que se encuentran documentos que contienen «portátil».

A continuación, en la pestaña [Registros] de [Información del sistema] > [Registro de búsqueda], filtre introduciendo «laptop» en «Consulta de búsqueda» y eligiendo «Uno o más resultados» en «Número de resultados».
Si las búsquedas realizadas por los usuarios después del cambio se registran con resultados, la corrección funciona.

Al cabo de unos días, en la pestaña [Resumen], ponga el período en «Personalizado», fije como fecha de inicio el día siguiente al cambio y active «Comparar con el período anterior».
Los períodos se dividen por días (fechas en la zona horaria del servidor), por lo que, si incluye el día del cambio, también se cuentan los cero resultados anteriores al cambio.
Compruebe que la tasa de cero resultados es menor que en el período anterior y que «laptop» ha desaparecido de la lista de consultas sin resultados.
Si deja el período en, por ejemplo, «Últimos 7 días», las búsquedas sin resultados anteriores al cambio siguen dentro del período, por lo que el término no desaparece de la lista de inmediato.

El contenido del diccionario se puede guardar como archivo con [Descargar] en la pantalla de lista.
Si lo guarda antes y después de un cambio, podrá usarlo para revertirlo.

Subir el documento deseado a las primeras posiciones: coincidencia de clave
===========================================================================

Los términos con una posición media de clic alta en la pestaña [Consultas], o los que figuran como consultas sin clics, pueden ser casos en los que el documento correcto se encuentra, pero queda enterrado en posiciones bajas.
Las URL con más clics de la pestaña [Clics] muestran qué documentos acaban abriendo los usuarios.
La coincidencia de clave sirve para subir ese documento a las primeras posiciones para un término de búsqueda concreto.

En [Rastreador] > [Coincidencia de clave], haga clic en [Crear nuevo], introduzca lo siguiente y haga clic en [Crear].

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Campo
     - Ejemplo
     - Descripción
   * - Término de búsqueda
     - ``reembolso``
     - Se aplica cuando una palabra de las palabras clave de búsqueda coincide con este valor (sin distinguir mayúsculas y minúsculas). Indique una sola palabra
   * - Consulta
     - ``url:"https://portal.example.com/manual/expense.html"``
     - Consulta de búsqueda que selecciona los documentos que se suben
   * - Tamaño
     - ``10`` (valor predeterminado)
     - Número máximo de documentos que coinciden con la consulta y que se toman como objetivo
   * - Valor de impulso
     - ``100`` (valor predeterminado)
     - Peso por el que se multiplica la puntuación de los documentos objetivo

Encierre siempre la URL de la consulta entre ``"``.
Si no la encierra, como en ``url:https://...``, el análisis de la consulta falla en el ``:`` de la URL, y la coincidencia de clave no se carga y no hace nada (solo se escribe un WARN en ``fess.log``).
El campo ``url`` es de coincidencia exacta, por lo que el valor debe ser idéntico, carácter por carácter, a la URL indexada.
Antes de registrarla, ejecute la misma consulta en la página de búsqueda y compruebe que encuentra exactamente el documento deseado.

No hace falta recargar como con los diccionarios.
Al guardar, se inicia en segundo plano la recarga de las coincidencias de clave, y el cambio se produce cuando se han leído todas.
La carga espera un segundo entre cada entrada, así que, con muchas entradas, tarda en surtir efecto.

Compruebe el resultado en la pantalla de detalles de la coincidencia de clave registrada, abierta desde la lista.
Si en el campo «URL» se muestra la URL del documento objetivo, está activa.
Justo después de guardar, es posible que la recarga no haya terminado y el campo esté vacío.
Si sigue vacío después de esperar un poco y volver a abrir la pantalla de detalles, la consulta no coincide con ningún documento.
Los documentos que coinciden con la consulta se vuelven a calcular al guardar y cada vez que termina un trabajo de rastreo.
Por eso, un documento que aún no se ha rastreado pasa a ser objetivo después del siguiente rastreo.

Tenga en cuenta también que solo se toman como objetivo los documentos que coinciden con el término de búsqueda.
Si al buscar «reembolso» no se encuentra en absoluto el documento objetivo, registrar una coincidencia de clave no hará que aparezca en los resultados.

Subir un sitio o un grupo de documentos: impulso de documento
=============================================================

Para subir un grupo concreto de documentos, como el sitio de los manuales oficiales, independientemente del término de búsqueda, utilice [Rastreador] > [Impulso de documento].

Haga clic en [Crear nuevo] e introduzca lo siguiente.

- Condición: ``url.startsWith("https://portal.example.com/manual/")``
- Expresión de impulso: ``10``
- Tipo de Script: ``javascript`` (ya rellenado al crear una regla nueva)
- Orden de clasificación: ``0``

La condición y la expresión de impulso se evalúan como expresiones de script, y cada campo del documento se puede usar como variable.
En los documentos para los que la condición devuelve ``true``, el valor de la expresión de impulso se guarda en el campo ``boost``.
Es el mismo campo que «Valor de impulso» de las configuraciones de rastreo web y de sistema de archivos (1.0 de forma predeterminada); en los documentos que coinciden con una regla se usa el valor de la regla.
Si un documento coincide con varias reglas, se usa la regla con el orden de clasificación más bajo.
En JavaScript, no ponga punto y coma al final de la expresión.
Si lo pone, el valor pasa a ser ``null`` y la regla no tiene efecto.

El impulso de documento surte efecto de forma distinta a la coincidencia de clave y a los sinónimos.

- Las reglas se evalúan cuando los documentos se registran en el índice mediante el rastreo web y el rastreo de archivos. No se aplican a los documentos de rastreos de almacenes de datos.
- Añadir o modificar una regla no cambia los valores de los documentos ya indexados.
- Si «Comprobar fecha de última modificación» de [General] está activado (valor predeterminado), los documentos cuyo contenido no ha cambiado no se vuelven a registrar al rastrear de nuevo. Para aplicar la regla a los documentos existentes, elimine los documentos afectados en [Información del sistema] > [Búsqueda] y vuelva a rastrear.

Una vez aplicada, busque con palabras que coincidan con ese grupo de documentos para comprobar que su posición ha subido y, pasado un tiempo, compare la posición media de clic de la pestaña [Consultas] con el período anterior.

Sugerir otra formulación: consultas relacionadas
================================================

Para recomendar una búsqueda con otra palabra sin ampliar el término de búsqueda del usuario, utilice las consultas relacionadas.
En [Rastreador] > [Consulta relacionada], haga clic en [Crear nuevo], introduzca la palabra de los usuarios en «Término de búsqueda» (p. ej., ``VPN``) y las palabras recomendadas en «Consultas», una por línea (p. ej., ``acceso remoto``, ``conexión externa``).

Con el tema estándar (bootstrap), cuando el término de búsqueda coincide, se muestran botones encima de los resultados bajo «Búsquedas relacionadas:».
También se muestran en la página de resultados vacía, por lo que sirven para guiar a los usuarios desde las consultas sin resultados.
El término se compara con toda la cadena de búsqueda introducida (sin distinguir mayúsculas y minúsculas).
Surte efecto al guardar, sin necesidad de recargar.

Con [Generar a partir de los registros de búsqueda] en la pantalla de lista, se pueden crear automáticamente consultas relacionadas a partir de pares de palabras que el mismo usuario volvió a buscar en un intervalo corto.
Para ello deben estar activados tanto «Registro de búsqueda» como «Registro de usuario» en [General].
Los términos que ya tienen una consulta relacionada no se modifican.
Para las condiciones de generación y los ajustes que permiten adaptarlas, consulte `Consulta Relacionada <https://fess.codelibs.org/es/stable/admin/relatedquery-guide.html>`__.

Antes de usar palabras vacías
=============================

Si una palabra que aparece en todos los documentos (por ejemplo, una palabra en inglés del pie de todas las páginas) se mezcla en los términos de búsqueda y amplía demasiado los resultados, puede eliminarla del análisis con palabras vacías.
Sin embargo, cada archivo de diccionario de palabras vacías solo se aplica a determinados campos.

- ``en/stopwords.txt`` se usa en el análisis de ``content``, ``title`` y los campos que terminan en ``_en``.
- ``ja/stopwords.txt`` solo se usa en los campos que terminan en ``_ja``, como ``content_ja`` y ``title_ja``, de los documentos detectados como japoneses. De forma predeterminada está vacío.

Tomemos como ejemplo un texto japonés: las partículas como «の» y «は» se eliminan mediante el filtro de categorías gramaticales en los campos ``_ja``, pero no en ``content`` y ``title``.
En ``content`` y ``title``, el texto japonés se divide en unidades de dos caracteres y el hiragana se convierte en katakana antes de la comparación («VPNとは» se convierte en ``vpn`` y ``トハ``).
Por eso, añadir una palabra japonesa a ``en/stopwords.txt`` no la elimina, salvo que coincida exactamente con una de las unidades de dos caracteres resultantes de esa división.
Utilice las palabras vacías principalmente para palabras en inglés y compruebe si surten efecto con la API ``_analyze`` de OpenSearch.

.. code-block:: bash

    curl -X POST "localhost:9200/fess.search/_analyze" -H "Content-Type: application/json" \
      -d '{"analyzer": "standard_search_analyzer", "text": "VPNとは"}'

Las palabras vacías se aplican tanto al indexar como al buscar.
Después de guardar el diccionario, recargue el índice de documentos como con los sinónimos y vuelva a rastrear para eliminarlas también de los documentos ya indexados.
Para saber cómo funcionan los campos por idioma, consulte :doc:`guide-09`.

Solución de problemas
=====================

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Síntoma
     - Qué comprobar
   * - Se registró un sinónimo, pero los resultados no cambian
     - ¿Se recargó el índice de documentos? ¿La entrada cumple las reglas de registro (hiragana, palabras de un solo carácter, etc.)?
   * - La coincidencia de clave no funciona
     - ¿Está vacío el campo «URL» de la pantalla de detalles? ¿Está la URL de la consulta entre ``"``? ¿Contienen las palabras clave del usuario exactamente la misma palabra que el término, como palabra independiente (otra forma, como el plural «reembolsos», no coincide)? ¿Se encuentra el documento objetivo con esa palabra?
   * - El impulso de documento no funciona
     - ¿Son documentos de un almacén de datos? ¿Se volvieron a registrar los documentos después de añadir la regla? ¿Termina la condición con un punto y coma?
   * - No se muestran las consultas relacionadas
     - ¿Coincide el término con toda la cadena de búsqueda? Si usa un tema propio, ¿está preparado para mostrar consultas relacionadas?
   * - Los indicadores de clics están vacíos
     - ¿Está activado «Registro de búsqueda» en [General]? ¿Pasan los enlaces de los resultados por ``/go/``? ¿El período contiene solo clics registrados antes de 15.9?

Artículos recomendados
======================

- Agregar los registros de búsqueda por su cuenta con OpenSearch Dashboards: :doc:`guide-22`
- Mejorar la búsqueda en documentos que mezclan japonés, inglés y chino: :doc:`guide-09`
- La causa de los cero resultados era la falta de documentos: :doc:`guide-04`
- Mostrar documentos de significado cercano aunque las palabras no coincidan: :doc:`guide-18`
- Gestionar como código la configuración de diccionarios y coincidencias de clave: :doc:`guide-16`

Referencias
===========

- `Registro de búsqueda <https://fess.codelibs.org/es/stable/admin/searchlog-guide.html>`__
- `Diccionario <https://fess.codelibs.org/es/stable/admin/dict-guide.html>`__
- `Diccionario de Sinónimos <https://fess.codelibs.org/es/stable/admin/synonym-guide.html>`__
- `Diccionario de Palabras Vacías <https://fess.codelibs.org/es/stable/admin/stopwords-guide.html>`__
- `Coincidencia de Clave <https://fess.codelibs.org/es/stable/admin/keymatch-guide.html>`__
- `Impulso de Documento <https://fess.codelibs.org/es/stable/admin/boostdoc-guide.html>`__
- `Consulta Relacionada <https://fess.codelibs.org/es/stable/admin/relatedquery-guide.html>`__
- `Mantenimiento <https://fess.codelibs.org/es/stable/admin/maintenance-guide.html>`__
