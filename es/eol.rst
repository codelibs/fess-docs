================================
Periodo de soporte del producto
================================

Los productos que han superado su fecha de fin de vida (EOL) ya no recibiran mantenimiento ni actualizaciones.
CodeLibs Project recomienda encarecidamente migrar a una version con soporte.
Esto evita situaciones en las que los servicios y el soporte necesarios no esten disponibles.
La ultima version se puede descargar desde la `pagina de descargas <downloads.html>`__.

Si necesita soporte para productos que han superado su periodo de fin de vida, consulte el `soporte comercial <https://www.n2sm.net/products/n2search.html>`__.

.. warning::

   **Acciones recomendadas antes del fin de soporte**

   Antes de la fecha de fin de soporte, planifique y ejecute las siguientes acciones:

   1. **Crear copias de seguridad**: Respalde los archivos de configuracion y los datos de indices
   2. **Probar en entorno de staging**: Verifique el funcionamiento con la nueva version antes de la migracion a produccion
   3. **Revisar las notas de la version**: Compruebe los cambios incompatibles y las funciones obsoletas
   4. **Planificar el cronograma de migracion**: Cree un plan considerando los requisitos de tiempo de inactividad

Ruta de actualizacion
=====================

La siguiente tabla muestra la ruta de actualizacion recomendada desde su version actual a la ultima version.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Version actual
     - Ruta recomendada
     - Notas
   * - 15.x a 15.5
     - Actualizacion directa posible
     - Consulte la `Guia de actualizacion <15.5/install/upgrade.html>`__
   * - 14.x a 15.5
     - Actualizacion directa posible
     - Preste atencion a los cambios en los archivos de configuracion
   * - 13.x a 15.5
     - Se recomienda pasar por 14.x
     - Actualice en orden: 13.x a 14.19, luego a 15.5
   * - 12.x o anterior a 15.5
     - Se requiere actualizacion por etapas
     - Actualice de 1 a 2 versiones principales a la vez

.. note::

   Para procedimientos detallados de actualizacion, consulte la `Guia de actualizacion <15.5/install/upgrade.html>`__.
   Para entornos a gran escala o configuraciones complejas, recomendamos consultar el `soporte comercial <support-services.html>`__.

Recursos de migracion
=====================

Documentos utiles para la actualizacion:

- `Guia de actualizacion <15.5/install/upgrade.html>`__ - Pasos detallados desde la copia de seguridad hasta la finalizacion de la actualizacion
- `Notas de la version <https://github.com/codelibs/fess/releases>`__ - Cambios y notas para cada version
- `Solucion de problemas <15.5/install/troubleshooting.html>`__ - Problemas comunes y soluciones
- `Actualizacion con Docker <15.5/install/install-docker.html>`__ - Actualizacion en entornos Docker

Tabla de Mantenimiento
======================

La fecha de EOL de Fess es aproximadamente 18 meses despues del lanzamiento.

**Leyenda**:

- 🟢 **Con soporte**: Se proporcionan correcciones de seguridad y correcciones de errores
- 🟡 **Proximo al fin de soporte**: El soporte finaliza dentro de 6 meses
- 🔴 **Fin de soporte**: No se proporciona mantenimiento

Versiones actualmente soportadas
---------------------------------

.. tabularcolumns:: |p{3cm}|p{4cm}|p{3cm}|
.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Fess
     - Fecha de EOL
     - Estado
   * - 15.5.x
     - 2027-08-01
     - 🟢 Ultima (Recomendada)
   * - 15.4.x
     - 2027-06-01
     - 🟢 Con soporte
   * - 15.3.x
     - 2027-04-01
     - 🟢 Con soporte
   * - 15.2.x
     - 2027-03-01
     - 🟢 Con soporte
   * - 15.1.x
     - 2027-01-01
     - 🟢 Con soporte
   * - 15.0.x
     - 2026-12-01
     - 🟢 Con soporte
   * - 14.19.x
     - 2026-08-01
     - 🟡 Proximo al fin de soporte
   * - 14.18.x
     - 2026-05-01
     - 🟡 Proximo al fin de soporte
   * - 14.17.x
     - 2026-03-01
     - 🔴 Fin de soporte
   * - 14.16.x
     - 2026-02-01
     - 🔴 Fin de soporte
   * - 14.15.x
     - 2026-01-01
     - 🔴 Fin de soporte

Versiones en fin de vida
-------------------------

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Fess
     - Fecha de EOL
   * - 14.14.x
     - 2025-11-01
   * - 14.13.x
     - 2025-10-01
   * - 14.12.x
     - 2025-08-01
   * - 14.11.x
     - 2025-04-01
   * - 14.10.x
     - 2025-01-01
   * - 14.9.x
     - 2024-12-01
   * - 14.8.x
     - 2024-11-01
   * - 14.7.x
     - 2024-09-01
   * - 14.6.x
     - 2024-07-01
   * - 14.5.x
     - 2024-05-01
   * - 14.4.x
     - 2024-02-24
   * - 14.3.x
     - 2023-12-28
   * - 14.2.x
     - 2023-10-26
   * - 14.1.x
     - 2023-09-08
   * - 14.0.x
     - 2023-08-08
   * - 13.16.x
     - 2023-06-07
   * - 13.15.x
     - 2023-03-22
   * - 13.14.x
     - 2023-02-03
   * - 13.13.x
     - 2022-11-25
   * - 13.12.x
     - 2022-09-23
   * - 13.11.x
     - 2022-08-10
   * - 13.10.x
     - 2022-05-11
   * - 13.9.x
     - 2022-02-18
   * - 13.8.x
     - 2021-12-18
   * - 13.7.x
     - 2021-11-13
   * - 13.6.x
     - 2021-08-11
   * - 13.5.x
     - 2021-06-02
   * - 13.4.x
     - 2021-04-01
   * - 13.3.x
     - 2021-01-31
   * - 13.2.x
     - 2020-12-25
   * - 13.1.x
     - 2020-11-20
   * - 13.0.x
     - 2020-10-10
   * - 12.7.x
     - 2020-11-20
   * - 12.6.x
     - 2020-09-26
   * - 12.5.x
     - 2020-07-29
   * - 12.4.x
     - 2020-05-14
   * - 12.3.x
     - 2020-02-23
   * - 12.2.x
     - 2020-12-13
   * - 12.1.x
     - 2019-08-19
   * - 12.0.x
     - 2019-06-02
   * - 11.4.x
     - 2019-03-23
   * - 11.3.x
     - 2019-02-14
   * - 11.2.x
     - 2018-12-15
   * - 11.1.x
     - 2018-11-11
   * - 11.0.x
     - 2018-08-13
   * - 10.3.x
     - 2018-05-24
   * - 10.2.x
     - 2018-02-30
   * - 10.1.x
     - 2017-12-09
   * - 10.0.x
     - 2017-08-05
   * - 9.4.x
     - 2016-11-21
   * - 9.3.x
     - 2016-05-06
   * - 9.2.x
     - 2015-12-28
   * - 9.1.x
     - 2015-09-26
   * - 9.0.x
     - 2015-08-07
   * - 8.x
     - 2014-08-23
   * - 7.x
     - 2014-02-03
   * - 6.x
     - 2013-09-02
   * - 5.x
     - 2013-06-15
   * - 4.x
     - 2012-06-19
   * - 3.x
     - 2011-09-07
   * - 2.x
     - 2011-07-16
   * - 1.x
     - 2011-04-10

Preguntas Frecuentes
====================

P: Puedo seguir usando Fess despues de que termine el periodo de soporte?
--------------------------------------------------------------------------

R: Tecnicamente es posible, pero no se proporcionaran correcciones de seguridad ni correcciones de errores.
Para mitigar los riesgos de seguridad, recomendamos encarecidamente actualizar a una version con soporte.

P: Cuanto tiempo tarda una actualizacion?
-------------------------------------------

R: Depende de la escala de su entorno, pero generalmente de 2 a 4 horas.
Para entornos a gran escala o configuraciones complejas, recomendamos probar primero en un entorno de staging.
Consulte la `Guia de actualizacion <15.5/install/upgrade.html>`__ para mas detalles.

P: Que debo hacer si encuentro un problema con una version en fin de vida?
---------------------------------------------------------------------------

R: Tiene las siguientes opciones:

1. **Actualizar a la ultima version**: La accion recomendada
2. **Preguntar en los foros de la comunidad**: Puede obtener consejos de otros usuarios
3. **Consultar el soporte comercial**: El `soporte comercial de N2SM <support-services.html>`__ puede proporcionar mantenimiento para versiones especificas

P: Que debo verificar antes de actualizar?
-------------------------------------------

R: Verifique lo siguiente:

1. Consulte las `Notas de la version <https://github.com/codelibs/fess/releases>`__ para cambios incompatibles
2. Verifique la compatibilidad de la version de OpenSearch
3. Si tiene personalizaciones, compruebe la compatibilidad de configuraciones y plugins
4. Cree copias de seguridad completas

P: La actualizacion en un entorno Docker requiere pasos especiales?
---------------------------------------------------------------------

R: Necesitara respaldar los volumenes de Docker y obtener los nuevos archivos de Docker Compose.
Consulte la `Guia de instalacion con Docker <15.5/install/install-docker.html>`__ para mas detalles.
