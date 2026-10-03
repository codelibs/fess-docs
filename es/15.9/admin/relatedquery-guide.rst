====================
Consulta Relacionada
====================

Descripción general
===================

Aquí se explica la configuración de consulta relacionada.
Puede mejorar los resultados de búsqueda con las consultas relacionadas registradas.
Las consultas relacionadas se pueden utilizar como términos alternativos para los términos de búsqueda.


Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista para configurar consultas relacionadas que se muestra a continuación, haga clic en [Rastreador > Consulta relacionada] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración de consulta relacionada, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Término de búsqueda
:::::::::::::::::::

Especifique el término de búsqueda que desea coincidir con la consulta de búsqueda.

Consulta
::::::::

Especifique la consulta.

Host virtual
::::::::::::

Especifique el nombre de host del host virtual.
Para más detalles, consulte :doc:`Host virtual en la guía de configuración <../config/security-virtual-host>`.

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.

Generar a partir de los registros de búsqueda
---------------------------------------------

Haga clic en el botón [Generar a partir de los registros de búsqueda] de la página de lista para
crear consultas relacionadas a partir de los registros de búsqueda recientes. Una búsqueda que la
misma sesión de usuario hace poco después de otra (una errata seguida de su corrección, o un
término amplio seguido de otro más específico) cuenta como una reformulación. Para los términos
buscados con frecuencia, las reformulaciones más habituales pasan a ser las consultas relacionadas
del término.

Las consultas relacionadas se aplican a todos y amplían cada búsqueda de su término, por lo que la
generación es conservadora:

- Solo se usan las búsquedas que puede ver un invitado. Un registro de búsqueda solo se lee cuando
  todos sus roles cumplen ``suggest.search.log.permissions`` (el mismo ajuste que usa la sugerencia).
- No se usan términos de búsqueda que contengan un filtro de campo como ``label:"x"``, operadores,
  comodines, ``sort:`` o un ``+`` / ``-`` inicial.
- Las palabras registradas en [Sugerir > Palabra no deseada] no se usan ni como términos ni como
  consultas relacionadas.
- Un término y cada una de sus consultas relacionadas deben proceder de al menos
  ``related_query.generate.min.sessions`` sesiones, y las reformulaciones deben tener resultados.
- Las entradas se generan por separado para cada host virtual. Los registros de búsqueda sin host
  virtual se tratan como el host predeterminado.
- Los términos que ya tienen consultas relacionadas no se modifican (el resultado indica cuántos se
  omitieron), y no se crean más entradas de las que la caché de consultas relacionadas puede cargar
  (``page.relatedquery.max.fetch.size``).

Las consultas relacionadas generadas se pueden editar o eliminar como las registradas a mano. No se
pueden generar mientras "Registro de búsqueda" o "Registro de usuario" estén desactivados en
[Sistema > General], y no puede empezar una segunda ejecución mientras otra está en curso.

Los siguientes ajustes de ``fess_config.properties`` ajustan la generación.

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``related_query.generate.days``
     - Días de registros de búsqueda que se leen
     - ``30``
   * - ``related_query.generate.term.size``
     - Número máximo de términos por host virtual
     - ``100``
   * - ``related_query.generate.query.size``
     - Número máximo de consultas relacionadas por término
     - ``5``
   * - ``related_query.generate.min.sessions``
     - Número mínimo de sesiones en las que deben aparecer un término y su consulta relacionada
     - ``3``
   * - ``related_query.generate.session.interval``
     - Intervalo en el que una búsqueda cuenta como reformulación (minutos)
     - ``10``
   * - ``related_query.generate.seed.log.size``
     - Número máximo de registros de búsqueda leídos por término
     - ``1000``
   * - ``related_query.generate.seed.session.size``
     - Número máximo de sesiones leídas por término
     - ``200``
   * - ``related_query.generate.log.fetch.size``
     - Número máximo de búsquedas posteriores leídas por término
     - ``2000``
   * - ``related_query.generate.query.min.length``
     - Longitud mínima de un término y de una consulta relacionada (caracteres)
     - ``2``
   * - ``related_query.generate.query.max.length``
     - Longitud máxima de un término y de una consulta relacionada (caracteres)
     - ``50``

.. |image0| image:: ../../../resources/images/en/15.9/admin/relatedquery-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/relatedquery-2.png
