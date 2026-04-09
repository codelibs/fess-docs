============================================================
Parte 8: Cultivar la calidad de busqueda -- Un ciclo de ajuste de busqueda basado en datos de comportamiento del usuario
============================================================

Introduccion
============

La implementacion de un sistema de busqueda no es el final del camino.
Una vez que los usuarios comienzan a utilizar la busqueda en la practica, pueden surgir comentarios como "no encuentro los resultados que esperaba" o "aparecen resultados irrelevantes en las primeras posiciones."

Este articulo presenta un ciclo de ajuste de calidad de busqueda que consiste en analizar los registros de busqueda para identificar problemas, implementar mejoras y medir su efectividad.
En lugar de lograr una calidad de busqueda perfecta de una sola vez, se trata de un enfoque de mejora continua basado en datos.

Audiencia objetivo
==================

- Administradores de sistemas de busqueda
- Personas que desean mejorar la calidad de busqueda
- Personas que ya operan Fess y han recibido comentarios de los usuarios

El ciclo de ajuste de calidad de busqueda
=========================================

La mejora de la calidad de busqueda sigue un ciclo de cuatro pasos:

1. **Analizar**: Revisar los registros de busqueda e identificar problemas
2. **Mejorar**: Implementar soluciones para los problemas identificados
3. **Verificar**: Confirmar la efectividad de las mejoras
4. **Continuar**: Repetir el ciclo para mejorar continuamente la calidad

Paso 1: Analisis de los registros de busqueda
==============================================

Como consultar los registros de busqueda
-----------------------------------------

Fess registra automaticamente el comportamiento de busqueda de los usuarios.
Puede consultar los registros de busqueda desde [Informacion del sistema] > [Registro de busqueda] en la consola de administracion.

Los registros de busqueda contienen la siguiente informacion:

- Palabras clave de busqueda
- Fecha y hora de busqueda
- Numero de resultados de busqueda
- Agente de usuario

Patrones a los que prestar atencion
------------------------------------

Al analizar los registros de busqueda, hay patrones especificos a los que debe prestar atencion.

**Consultas sin resultados**

Son consultas que devuelven cero resultados.
Es posible que la informacion que el usuario busca no exista, o que las palabras clave de busqueda no coincidan adecuadamente.

Por ejemplo, una busqueda de "viaje de empresa" no devuelve resultados, pero existe un documento titulado "actividad recreativa para empleados."
Esto puede resolverse configurando sinonimos.

**Consultas de alta frecuencia**

Las palabras clave buscadas con frecuencia representan necesidades de informacion importantes para la organizacion.
Verifique si se muestran resultados apropiados en las primeras posiciones para estas consultas.

**Registros de clics**

Son registros de que enlaces de los resultados de busqueda fueron clicados.
Si los primeros resultados no reciben clics y solo se hace clic en resultados de posiciones inferiores, hay margen de mejora en el ranking.

Paso 2: Implementacion de mejoras
==================================

Basandose en los resultados del analisis, implemente las siguientes mejoras de forma combinada.

Configuracion de sinonimos
---------------------------

Registre sinonimos para manejar variaciones en la escritura y abreviaturas.

Configurelos seleccionando el diccionario de sinonimos desde [Sistema] > [Diccionario] en la consola de administracion.

Ejemplo de configuracion:

::

    社員旅行,従業員レクリエーション,社内イベント
    PC,パソコン,コンピュータ
    AWS,Amazon Web Services
    k8s,Kubernetes

Al configurar sinonimos, la busqueda de un termino tambien devolvera documentos que contengan sus sinonimos.

Configuracion de Key Match
--------------------------

Esta funcion muestra un documento especifico en la primera posicion de los resultados para una palabra clave determinada.

Configurelo desde [Crawler] > [Key Match] en la consola de administracion.

Por ejemplo, puede configurar que la pagina del manual de liquidacion de gastos aparezca en la primera posicion cuando los usuarios busquen "liquidacion de gastos."

.. list-table:: Ejemplo de configuracion de Key Match
   :header-rows: 1
   :widths: 30 50 20

   * - Termino de busqueda
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

Configuracion de Document Boost
--------------------------------

Ajusta la puntuacion general de los documentos que coinciden con condiciones especificas.

Configurelo desde [Crawler] > [Document Boost] en la consola de administracion.

Por ejemplo, se pueden considerar las siguientes estrategias de boost:

- Aumentar la puntuacion de los manuales oficiales (sitio del portal)
- Priorizar documentos con fechas de ultima modificacion mas recientes
- Aumentar la puntuacion de documentos con una etiqueta especifica (documentos oficiales)

Configuracion de consultas relacionadas
----------------------------------------

Esta funcion sugiere palabras clave relacionadas en la pagina de resultados de busqueda.
Ayuda a los usuarios a refinar su busqueda o buscar desde un angulo diferente.

Configurelo desde [Crawler] > [Consulta relacionada] en la consola de administracion.

Ejemplo de configuracion:

::

    「VPN」→ 関連クエリ: 「VPN接続方法」「リモートワーク」「社外アクセス」

Configuracion de palabras vacias
----------------------------------

Configure las palabras que deben ignorarse durante la busqueda.
Las particulas comunes como "no", "wa" y "wo" se procesan de forma predeterminada, pero puede agregar palabras de ruido especificas de su sector segun sea necesario.

Configurelas seleccionando el diccionario de palabras vacias desde [Sistema] > [Diccionario] en la consola de administracion.

Paso 3: Verificacion de la efectividad
=======================================

Despues de implementar las mejoras, verifique su efectividad.

Metodos de verificacion
------------------------

**Cambio en la tasa de consultas sin resultados**

Verifique como ha cambiado la proporcion de consultas sin resultados antes y despues de la mejora.
Si la tasa de consultas sin resultados ha disminuido despues de agregar sinonimos o configurar Key Match, puede concluir que la mejora fue efectiva.

**Cambio en la posicion de los clics**

Verifique la distribucion de en que posicion de los resultados de busqueda se hace clic.
Si la proporcion de clics en los primeros resultados ha aumentado, puede concluir que el ranking ha mejorado.

**Verificacion de palabras populares**

Verifique las palabras populares que se muestran en la pagina de busqueda y las palabras clave buscadas con frecuencia agregadas a partir de los registros de busqueda.
Tambien es efectivo verificar manualmente si se devuelven resultados apropiados al buscar palabras populares.

Paso 4: Mejora continua
========================

El ajuste de la calidad de busqueda no es algo que termine con un unico esfuerzo.

Establecimiento de un ciclo operativo
--------------------------------------

Recomendamos establecer un ciclo operativo como el siguiente.

.. list-table:: Ejemplo de ciclo de ajuste
   :header-rows: 1
   :widths: 25 35 40

   * - Frecuencia
     - Accion
     - Detalles
   * - Semanal
     - Verificar consultas sin resultados
     - Verificar si hay nuevas consultas sin resultados y resolverlas con sinonimos o Key Match
   * - Mensual
     - Analisis general de registros de busqueda
     - Revisar tendencias en consultas de alta frecuencia, tasas de clics y tasas de consultas sin resultados
   * - Trimestral
     - Revision integral
     - Realizar una evaluacion integral de la calidad de busqueda y formular un plan de mejora

Comentarios de los usuarios
----------------------------

Ademas del analisis de registros, los comentarios de los usuarios reales tambien son una entrada importante para la mejora.
Establezca un mecanismo para recopilar comentarios como "no pude encontrar lo que buscaba con esta palabra clave" o "este resultado fue util."

Resumen
=======

Este articulo presento un ciclo de ajuste para mejorar continuamente la calidad de busqueda.

- Analisis de registros de busqueda (consultas sin resultados, consultas de alta frecuencia, registros de clics)
- Mejoras mediante sinonimos, Key Match, Document Boost y consultas relacionadas
- Metodos para verificar la efectividad de las mejoras
- Establecimiento de un ciclo operativo continuo

Cultivemos la calidad de busqueda mediante mejoras basadas en datos, pasando de una "busqueda que se usa" a una "busqueda que es util."

El proximo articulo tratara sobre la construccion de una infraestructura de busqueda en entornos multilingues.

Referencias
===========

- `Fess Registro de busqueda <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `Fess Gestion de diccionarios <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__
