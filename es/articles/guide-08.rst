========================================
Parte 8: Cultivar la calidad de búsqueda
========================================

Introducción
============

La implementación de un sistema de búsqueda no es el final del camino.
Una vez que los usuarios comienzan a utilizar la búsqueda en la práctica, pueden surgir comentarios como "no encuentro los resultados que esperaba" o "aparecen resultados irrelevantes en las primeras posiciones."

Este artículo presenta un ciclo de ajuste de calidad de búsqueda que consiste en analizar los registros de búsqueda para identificar problemas, implementar mejoras y medir su efectividad.
En lugar de lograr una calidad de búsqueda perfecta de una sola vez, se trata de un enfoque de mejora continua basado en datos.

Audiencia objetivo
==================

- Administradores de sistemas de búsqueda
- Personas que desean mejorar la calidad de búsqueda
- Personas que ya operan Fess y han recibido comentarios de los usuarios

El ciclo de ajuste de calidad de búsqueda
=========================================

La mejora de la calidad de búsqueda sigue un ciclo de cuatro pasos:

1. **Analizar**: Revisar los registros de búsqueda e identificar problemas
2. **Mejorar**: Implementar soluciones para los problemas identificados
3. **Verificar**: Confirmar la efectividad de las mejoras
4. **Continuar**: Repetir el ciclo para mejorar continuamente la calidad

Paso 1: Análisis de los registros de búsqueda
==============================================

Cómo consultar los registros de búsqueda
-----------------------------------------

Fess registra automáticamente el comportamiento de búsqueda de los usuarios.
Puede consultar los registros de búsqueda desde [Información del sistema] > [Registro de búsqueda] en la consola de administración.

Los registros de búsqueda contienen la siguiente información:

- Palabras clave de búsqueda
- Fecha y hora de búsqueda
- Número de resultados de búsqueda
- Agente de usuario

Patrones a los que prestar atención
------------------------------------

Al analizar los registros de búsqueda, hay patrones específicos a los que debe prestar atención.

**Consultas sin resultados**

Son consultas que devuelven cero resultados.
Es posible que la información que el usuario busca no exista, o que las palabras clave de búsqueda no coincidan adecuadamente.

Por ejemplo, una búsqueda de "viaje de empresa" no devuelve resultados, pero existe un documento titulado "actividad recreativa para empleados."
Esto puede resolverse configurando sinónimos.

**Consultas de alta frecuencia**

Las palabras clave buscadas con frecuencia representan necesidades de información importantes para la organización.
Verifique si se muestran resultados apropiados en las primeras posiciones para estas consultas.

**Registros de clics**

Son registros de que enlaces de los resultados de búsqueda fueron clicados.
Si los primeros resultados no reciben clics y solo se hace clic en resultados de posiciones inferiores, hay margen de mejora en el ranking.

Paso 2: Implementación de mejoras
==================================

Basándose en los resultados del análisis, implemente las siguientes mejoras de forma combinada.

Configuración de sinónimos
---------------------------

Registre sinónimos para manejar variaciones en la escritura y abreviaturas.

Configúrelos seleccionando el diccionario de sinónimos desde [Sistema] > [Diccionario] en la consola de administración.

Ejemplo de configuración:

::

    社員旅行,従業員レクリエーション,社内イベント
    PC,パソコン,コンピュータ
    AWS,Amazon Web Services
    k8s,Kubernetes

Al configurar sinónimos, la búsqueda de un término también devolverá documentos que contengan sus sinónimos.

Configuración de Key Match
--------------------------

Esta función muestra un documento específico en la primera posición de los resultados para una palabra clave determinada.

Configúrelo desde [Crawler] > [Key Match] en la consola de administración.

Por ejemplo, puede configurar que la página del manual de liquidación de gastos aparezca en la primera posición cuando los usuarios busquen "liquidación de gastos."

.. list-table:: Ejemplo de configuración de Key Match
   :header-rows: 1
   :widths: 30 50 20

   * - Término de búsqueda
     - Consulta
     - Valor de boost
   * - 経費精算
     - url:https://portal/manual/expense.html
     - 100
   * - 有給申請
     - url:https://portal/manual/paid-leave.html
     - 100
   * - VPN接続
     - url:https://portal/manual/vpn-setup.html
     - 100

Configuración de Document Boost
--------------------------------

Ajusta la puntuación general de los documentos que coinciden con condiciones específicas.

Configúrelo desde [Crawler] > [Document Boost] en la consola de administración.

Por ejemplo, se pueden considerar las siguientes estrategias de boost:

- Aumentar la puntuación de los manuales oficiales (sitio del portal)
- Priorizar documentos con fechas de última modificación más recientes
- Aumentar la puntuación de documentos con una etiqueta específica (documentos oficiales)

Configuración de consultas relacionadas
----------------------------------------

Esta función sugiere palabras clave relacionadas en la página de resultados de búsqueda.
Ayuda a los usuarios a refinar su búsqueda o buscar desde un ángulo diferente.

Configúrelo desde [Crawler] > [Consulta relacionada] en la consola de administración.

Ejemplo de configuración:

::

    「VPN」→ 関連クエリ: 「VPN接続方法」「リモートワーク」「社外アクセス」

Configuración de palabras vacías
----------------------------------

Configure las palabras que deben ignorarse durante la búsqueda.
Las partículas comunes como "no", "wa" y "wo" se procesan de forma predeterminada, pero puede agregar palabras de ruido específicas de su sector según sea necesario.

Configúrelas seleccionando el diccionario de palabras vacías desde [Sistema] > [Diccionario] en la consola de administración.

Paso 3: Verificación de la efectividad
=======================================

Después de implementar las mejoras, verifique su efectividad.

Métodos de verificación
------------------------

**Cambio en la tasa de consultas sin resultados**

Verifique como ha cambiado la proporción de consultas sin resultados antes y después de la mejora.
Si la tasa de consultas sin resultados ha disminuido después de agregar sinónimos o configurar Key Match, puede concluir que la mejora fue efectiva.

**Cambio en la posición de los clics**

Verifique la distribución de en que posición de los resultados de búsqueda se hace clic.
Si la proporción de clics en los primeros resultados ha aumentado, puede concluir que el ranking ha mejorado.

**Verificación de palabras populares**

Verifique las palabras populares que se muestran en la página de búsqueda y las palabras clave buscadas con frecuencia agregadas a partir de los registros de búsqueda.
También es efectivo verificar manualmente si se devuelven resultados apropiados al buscar palabras populares.

Paso 4: Mejora continua
========================

El ajuste de la calidad de búsqueda no es algo que termine con un único esfuerzo.

Establecimiento de un ciclo operativo
--------------------------------------

Recomendamos establecer un ciclo operativo como el siguiente.

.. list-table:: Ejemplo de ciclo de ajuste
   :header-rows: 1
   :widths: 25 35 40

   * - Frecuencia
     - Acción
     - Detalles
   * - Semanal
     - Verificar consultas sin resultados
     - Verificar si hay nuevas consultas sin resultados y resolverlas con sinónimos o Key Match
   * - Mensual
     - Análisis general de registros de búsqueda
     - Revisar tendencias en consultas de alta frecuencia, tasas de clics y tasas de consultas sin resultados
   * - Trimestral
     - Revisión integral
     - Realizar una evaluación integral de la calidad de búsqueda y formular un plan de mejora

Comentarios de los usuarios
----------------------------

Además del análisis de registros, los comentarios de los usuarios reales también son una entrada importante para la mejora.
Establezca un mecanismo para recopilar comentarios como "no pude encontrar lo que buscaba con esta palabra clave" o "este resultado fue útil."

Resumen
=======

Este artículo presentó un ciclo de ajuste para mejorar continuamente la calidad de búsqueda.

- Análisis de registros de búsqueda (consultas sin resultados, consultas de alta frecuencia, registros de clics)
- Mejoras mediante sinónimos, Key Match, Document Boost y consultas relacionadas
- Métodos para verificar la efectividad de las mejoras
- Establecimiento de un ciclo operativo continuo

Cultivemos la calidad de búsqueda mediante mejoras basadas en datos, pasando de una "búsqueda que se usa" a una "búsqueda que es útil."

El próximo artículo tratará sobre la construcción de una infraestructura de búsqueda en entornos multilingües.

Referencias
===========

- `Fess Registro de búsqueda <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `Fess Gestión de diccionarios <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__
