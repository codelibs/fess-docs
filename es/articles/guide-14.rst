===========================================================
Parte 14: Estrategias de escalado para sistemas de búsqueda
===========================================================

Introducción
=============

Cuando se introduce Fess a pequeña escala, a medida que crece el uso, surgen inevitablemente demandas como "más documentos", "más usuarios" y "búsquedas más rápidas".

En este artículo se explican las estrategias y los criterios de decisión para escalar gradualmente desde una configuración de servidor único a pequeña escala hasta una configuración de clúster a gran escala.

Audiencia objetivo
===================

- Personas que planifican operaciones de Fess a gran escala
- Personas que enfrentan problemas de rendimiento
- Personas que desean comprender los conceptos básicos de los clusters de OpenSearch

Etapas de escalado
===================

El escalado de Fess generalmente avanza a través de las siguientes etapas.

.. list-table:: Etapas de escalado
   :header-rows: 1
   :widths: 15 20 25 20 20

   * - Etapa
     - Configuración
     - Cantidad aprox. de documentos
     - Cantidad aprox. de usuarios
     - Costo
   * - S
     - Servidor único
     - Hasta 1 millón
     - Hasta 50
     - Bajo
   * - M
     - Configuración separada
     - Hasta 1 millón
     - Hasta 500
     - Medio
   * - L
     - Configuración de clúster
     - 1 millón a 10 millones
     - Hasta varios miles
     - Alto
   * - XL
     - Multi-instancia
     - 10 millones o más
     - Varios miles o más
     - Máximo

Etapa S: Configuración de servidor único
==========================================

Esto corresponde a la configuración de Docker Compose construida en la Parte 2.
Fess y OpenSearch se ejecutan en el mismo servidor.

Casos de uso
-------------

- Implementación inicial, PoC, organizaciones de pequeña a mediana escala
- Cantidad de documentos de 1 millón o menos
- Pocos usuarios de búsqueda simultáneos

Puntos de ajuste
-----------------

**Ajuste del heap de la JVM**

Configure el tamaño del heap de la JVM adecuadamente para Fess y OpenSearch respectivamente.

- Fess: Máximo 2 GB (valor predeterminado; el heap inicial es de 256 MB)
- OpenSearch: 50 % o menos de la memoria física, pero no más de 32 GB

**Pool de hilos**

Ajuste la cantidad de hilos de rastreo según la cantidad de núcleos de CPU del servidor.

Etapa M: Configuración separada
=================================

Separe físicamente el servidor de Fess y el servidor de OpenSearch.

Casos de uso
-------------

- Cuando aumentan los usuarios de búsqueda simultáneos y el rendimiento de búsqueda durante el rastreo se convierte en un problema
- Cuando la memoria o la CPU comienzan a ser insuficientes en la Etapa S

Configuración
--------------

::

    [Servidor Fess] <-> [Servidor OpenSearch]

Cambie el destino de conexión de OpenSearch en la configuración de Fess al servidor externo.

Beneficios
-----------

- Elimina la contención de recursos entre Fess (procesamiento de rastreo) y OpenSearch (procesamiento de búsqueda)
- Permite asignar recursos óptimos (CPU, memoria) a cada servidor
- La E/S de disco del servidor OpenSearch se vuelve independiente

Etapa L: Configuración de clúster
===================================

Configure OpenSearch como clúster para mejorar la redundancia y el rendimiento de búsqueda.

Casos de uso
-------------

- Cantidad de documentos de 1 millón a 10 millones
- Cuando se requiere alta disponibilidad
- Cuando se necesita mejorar el tiempo de respuesta de búsqueda

Ejemplo de configuración
--------------------------

::

    [Servidor Fess]
          |
    [Nodo OpenSearch 1] (Maestro/Datos)
    [Nodo OpenSearch 2] (Datos)
    [Nodo OpenSearch 3] (Datos)

El clúster de OpenSearch distribuye y replica datos utilizando los conceptos de shards y réplicas.

**Shards**: Dividen el índice y lo distribuyen en múltiples nodos (procesamiento más rápido mediante paralelización)

**Réplicas**: Mantienen copias de los shards en nodos diferentes (redundancia en caso de fallos + paralelización de búsquedas)

Puntos de configuración
-------------------------

- Número de shards: Configurar según la cantidad de documentos y el rendimiento de búsqueda (referencia: 10-50 GB por shard)
- Número de réplicas: Al menos 1 (para garantizar la redundancia)
- Número de nodos: Al menos 3 (quorum para la elección de maestro)

Etapa XL: Configuración multi-instancia
=========================================

Configure múltiples instancias de Fess para distribuir el procesamiento de rastreo y búsqueda.

Casos de uso
-------------

- La cantidad de documentos supera los 10 millones
- Necesidad de ejecutar trabajos de rastreo masivos en paralelo
- Solicitudes de búsqueda de alta frecuencia

Ejemplo de configuración
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

A partir de Fess 15.6, la función de coordinador distribuido permite el control exclusivo de operaciones de mantenimiento (como la reconstrucción y limpieza de índices) entre múltiples instancias de Fess.

Diagrama de flujo para decisiones de escalado
===============================================

Cuando se producen problemas de rendimiento, identifique la causa y considere las contramedidas en el siguiente orden.

**1. Cuando la búsqueda es lenta**

- Verifique el estado del clúster de OpenSearch
- Verifique el uso del heap de la JVM
- Verifique el tamaño del índice
- -> Considere la Etapa M (separación) o la Etapa L (clustering)

**2. Cuando el rastreo es lento o no se completa**

- Verifique la cantidad de documentos a rastrear
- Ajuste la cantidad de hilos y el intervalo
- Verifique el impacto en la búsqueda durante el rastreo
- -> Considere la Etapa M (separación) o la Etapa XL (instancia dedicada al rastreo)

**3. Cuando hay muchos accesos simultáneos**

- Monitoree el tiempo de respuesta de búsqueda
- Verifique el uso de CPU del servidor Fess
- -> Considere la Etapa XL (balanceador de carga + múltiples instancias)

Ajuste de la JVM
==================

En cualquier etapa, el ajuste de la JVM tiene un impacto significativo en el rendimiento.

Parámetros principales
-----------------------

.. list-table:: Parámetros de la JVM
   :header-rows: 1
   :widths: 25 35 40

   * - Parámetro
     - Descripción
     - Valor recomendado
   * - ``-Xmx``
     - Tamaño máximo del heap
     - 50 % o menos de la memoria física
   * - ``-Xms``
     - Tamaño inicial del heap
     - Mismo valor que ``-Xmx``
   * - Configuración de GC
     - Método de recolección de basura
     - G1GC (predeterminado)

Referencia para el tamaño del heap
------------------------------------

- 1 millón o menos: 2-4 GB
- 1 millón a 5 millones: 8 GB
- 5 millones a 10 millones: 16 GB
- 10 millones o más: 32 GB o más (lado OpenSearch)

Resumen
========

En este artículo se explicaron las estrategias de escalado gradual para Fess.

- **Etapa S**: Servidor único (hasta 1 millón de documentos)
- **Etapa M**: Separación de Fess / OpenSearch (hasta 1 millón de documentos, soporte multiusuario)
- **Etapa L**: Clustering de OpenSearch (1 millón a 10 millones de documentos)
- **Etapa XL**: Multi-instancia de Fess (10 millones de documentos o más)
- Diagrama de flujo para decisiones de escalado y ajuste de la JVM

Con el enfoque de "empezar pequeño y crecer según sea necesario", es posible escalar de acuerdo con los requisitos manteniendo los costos bajo control.

En el próximo artículo se tratará la arquitectura de seguridad.

Referencias
============

- `Guía de instalación de Fess <https://fess.codelibs.org/ja/15.5/install/index.html>`__

- `Configuración de clusters de OpenSearch <https://opensearch.org/docs/latest/tuning-your-cluster/>`__
