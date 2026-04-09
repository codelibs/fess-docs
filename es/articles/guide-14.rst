============================================================
Parte 14: Estrategias de escalado para sistemas de busqueda -- Expansion gradual de pequena a gran escala
============================================================

Introduccion
=============

Cuando se introduce Fess a pequena escala, a medida que crece el uso, surgen inevitablemente demandas como "mas documentos", "mas usuarios" y "busquedas mas rapidas".

En este articulo se explican las estrategias y los criterios de decision para escalar gradualmente desde una configuracion de servidor unico a pequena escala hasta una configuracion de cluster a gran escala.

Audiencia objetivo
===================

- Personas que planifican operaciones de Fess a gran escala
- Personas que enfrentan problemas de rendimiento
- Personas que desean comprender los conceptos basicos de los clusters de OpenSearch

Etapas de escalado
===================

El escalado de Fess generalmente avanza a traves de las siguientes etapas.

.. list-table:: Etapas de escalado
   :header-rows: 1
   :widths: 15 20 25 20 20

   * - Etapa
     - Configuracion
     - Cantidad aprox. de documentos
     - Cantidad aprox. de usuarios
     - Costo
   * - S
     - Servidor unico
     - Hasta 1 millon
     - Hasta 50
     - Bajo
   * - M
     - Configuracion separada
     - Hasta 1 millon
     - Hasta 500
     - Medio
   * - L
     - Configuracion de cluster
     - 1 millon a 10 millones
     - Hasta varios miles
     - Alto
   * - XL
     - Multi-instancia
     - 10 millones o mas
     - Varios miles o mas
     - Maximo

Etapa S: Configuracion de servidor unico
==========================================

Esto corresponde a la configuracion de Docker Compose construida en la Parte 2.
Fess y OpenSearch se ejecutan en el mismo servidor.

Casos de uso
-------------

- Implementacion inicial, PoC, organizaciones de pequena a mediana escala
- Cantidad de documentos de 1 millon o menos
- Pocos usuarios de busqueda simultaneos

Puntos de ajuste
-----------------

**Ajuste del heap de la JVM**

Configure el tamano del heap de la JVM adecuadamente para Fess y OpenSearch respectivamente.

- Fess: Maximo 2 GB (valor predeterminado; el heap inicial es de 256 MB)
- OpenSearch: 50 % o menos de la memoria fisica, pero no mas de 32 GB

**Pool de hilos**

Ajuste la cantidad de hilos de rastreo segun la cantidad de nucleos de CPU del servidor.

Etapa M: Configuracion separada
=================================

Separe fisicamente el servidor de Fess y el servidor de OpenSearch.

Casos de uso
-------------

- Cuando aumentan los usuarios de busqueda simultaneos y el rendimiento de busqueda durante el rastreo se convierte en un problema
- Cuando la memoria o la CPU comienzan a ser insuficientes en la Etapa S

Configuracion
--------------

::

    [Servidor Fess] <-> [Servidor OpenSearch]

Cambie el destino de conexion de OpenSearch en la configuracion de Fess al servidor externo.

Beneficios
-----------

- Elimina la contension de recursos entre Fess (procesamiento de rastreo) y OpenSearch (procesamiento de busqueda)
- Permite asignar recursos optimos (CPU, memoria) a cada servidor
- La E/S de disco del servidor OpenSearch se vuelve independiente

Etapa L: Configuracion de cluster
===================================

Configure OpenSearch como cluster para mejorar la redundancia y el rendimiento de busqueda.

Casos de uso
-------------

- Cantidad de documentos de 1 millon a 10 millones
- Cuando se requiere alta disponibilidad
- Cuando se necesita mejorar el tiempo de respuesta de busqueda

Ejemplo de configuracion
--------------------------

::

    [Servidor Fess]
          |
    [Nodo OpenSearch 1] (Maestro/Datos)
    [Nodo OpenSearch 2] (Datos)
    [Nodo OpenSearch 3] (Datos)

El cluster de OpenSearch distribuye y replica datos utilizando los conceptos de shards y replicas.

**Shards**: Dividen el indice y lo distribuyen en multiples nodos (procesamiento mas rapido mediante paralelizacion)

**Replicas**: Mantienen copias de los shards en nodos diferentes (redundancia en caso de fallos + paralelizacion de busquedas)

Puntos de configuracion
-------------------------

- Numero de shards: Configurar segun la cantidad de documentos y el rendimiento de busqueda (referencia: 10-50 GB por shard)
- Numero de replicas: Al menos 1 (para garantizar la redundancia)
- Numero de nodos: Al menos 3 (quorum para la eleccion de maestro)

Etapa XL: Configuracion multi-instancia
=========================================

Configure multiples instancias de Fess para distribuir el procesamiento de rastreo y busqueda.

Casos de uso
-------------

- La cantidad de documentos supera los 10 millones
- Necesidad de ejecutar trabajos de rastreo masivos en paralelo
- Solicitudes de busqueda de alta frecuencia

Ejemplo de configuracion
--------------------------

::

    [Balanceador de carga]
      +-- [Instancia Fess 1] (Busqueda + Administracion)
      +-- [Instancia Fess 2] (Busqueda)
      +-- [Instancia Fess 3] (Solo rastreo)
              |
    [Cluster OpenSearch]
      +-- [Nodo 1] (Maestro)
      +-- [Nodo 2] (Datos)
      +-- [Nodo 3] (Datos)
      +-- [Nodo 4] (Datos)

A partir de Fess 15.6, la funcion de coordinador distribuido permite el control exclusivo de operaciones de mantenimiento (como la reconstruccion y limpieza de indices) entre multiples instancias de Fess.

Diagrama de flujo para decisiones de escalado
===============================================

Cuando se producen problemas de rendimiento, identifique la causa y considere las contramedidas en el siguiente orden.

**1. Cuando la busqueda es lenta**

- Verifique el estado del cluster de OpenSearch
- Verifique el uso del heap de la JVM
- Verifique el tamano del indice
- -> Considere la Etapa M (separacion) o la Etapa L (clustering)

**2. Cuando el rastreo es lento o no se completa**

- Verifique la cantidad de documentos a rastrear
- Ajuste la cantidad de hilos y el intervalo
- Verifique el impacto en la busqueda durante el rastreo
- -> Considere la Etapa M (separacion) o la Etapa XL (instancia dedicada al rastreo)

**3. Cuando hay muchos accesos simultaneos**

- Monitoree el tiempo de respuesta de busqueda
- Verifique el uso de CPU del servidor Fess
- -> Considere la Etapa XL (balanceador de carga + multiples instancias)

Ajuste de la JVM
==================

En cualquier etapa, el ajuste de la JVM tiene un impacto significativo en el rendimiento.

Parametros principales
-----------------------

.. list-table:: Parametros de la JVM
   :header-rows: 1
   :widths: 25 35 40

   * - Parametro
     - Descripcion
     - Valor recomendado
   * - ``-Xmx``
     - Tamano maximo del heap
     - 50 % o menos de la memoria fisica
   * - ``-Xms``
     - Tamano inicial del heap
     - Mismo valor que ``-Xmx``
   * - Configuracion de GC
     - Metodo de recoleccion de basura
     - G1GC (predeterminado)

Referencia para el tamano del heap
------------------------------------

- 1 millon o menos: 2-4 GB
- 1 millon a 5 millones: 8 GB
- 5 millones a 10 millones: 16 GB
- 10 millones o mas: 32 GB o mas (lado OpenSearch)

Resumen
========

En este articulo se explicaron las estrategias de escalado gradual para Fess.

- **Etapa S**: Servidor unico (hasta 1 millon de documentos)
- **Etapa M**: Separacion de Fess / OpenSearch (hasta 1 millon de documentos, soporte multiusuario)
- **Etapa L**: Clustering de OpenSearch (1 millon a 10 millones de documentos)
- **Etapa XL**: Multi-instancia de Fess (10 millones de documentos o mas)
- Diagrama de flujo para decisiones de escalado y ajuste de la JVM

Con el enfoque de "empezar pequeno y crecer segun sea necesario", es posible escalar de acuerdo con los requisitos manteniendo los costos bajo control.

En el proximo articulo se tratara la arquitectura de seguridad.

Referencias
============

- `Guia de instalacion de Fess <https://fess.codelibs.org/ja/15.5/install/index.html>`__

- `Configuracion de clusters de OpenSearch <https://opensearch.org/docs/latest/tuning-your-cluster/>`__
