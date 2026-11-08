======================================
Fess vs otras soluciones de búsqueda
======================================

Introducción
============

Al seleccionar un sistema de búsqueda de texto completo, existen diversas opciones disponibles.
Esta página compara Fess con las principales soluciones de búsqueda, explicando las características y los casos de uso apropiados para cada una.

.. note::

   Esta comparación se basa en información de enero de 2026.
   Para las funciones y cambios más recientes, consulte la documentación oficial de cada proyecto.

----

Fess vs OpenSearch/Elasticsearch independiente
================================================

Descripción general
-------------------

OpenSearch y Elasticsearch son potentes motores de búsqueda, pero usarlos de forma independiente requiere desarrollo adicional para crear un "sistema de búsqueda" completo.
Fess utiliza OpenSearch/Elasticsearch como su backend y proporciona un sistema de búsqueda completo listo para usar.

Comparación
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Característica
     - Fess
     - OpenSearch/Elasticsearch independiente
   * - Interfaz de búsqueda
     - ✅ Incluida
     - ❌ Requiere desarrollo
   * - Interfaz de administración
     - ✅ Panel de administración web
     - ❌ Requiere desarrollo o herramientas separadas
   * - Rastreador
     - ✅ Incluido (Web/Archivos/BD)
     - ❌ Requiere desarrollo o herramientas separadas
   * - Tiempo de implementación
     - Minutos (Docker)
     - Semanas a meses (incluyendo desarrollo)
   * - Personalización
     - Media (personalización JSP/CSS)
     - Alta (desarrollo completamente personalizado posible)
   * - Costo inicial
     - Bajo
     - Alto (costos de desarrollo)
   * - Costo operativo
     - Bajo a medio
     - Medio a alto
   * - Escalabilidad
     - Alta
     - Alta
   * - Conocimientos requeridos
     - Conocimientos básicos de TI
     - Programación y experiencia en motores de búsqueda

Cuándo elegir Fess
------------------

- **Cuando necesita construir un sistema de búsqueda rápidamente**
- **Cuando los recursos de desarrollo son limitados**
- **Cuando las funciones de búsqueda estándar son suficientes**
- **Cuando el rastreo web y la búsqueda de archivos son los principales casos de uso**

Cuándo elegir OpenSearch/Elasticsearch independiente
----------------------------------------------------

- **Cuando necesita una experiencia de búsqueda completamente personalizada**
- **Cuando integra la búsqueda en una aplicación existente**
- **Cuando se requiere lógica de búsqueda especial**
- **Cuando su equipo tiene experiencia en motores de búsqueda**

.. tip::

   Despues de implementar Fess, tambien puede construir una interfaz de búsqueda personalizada utilizando la API.
   Considere comenzar con Fess y personalizar según sea necesario.

----

Fess vs Apache Solr
====================

Descripción general
-------------------

Apache Solr es una plataforma de búsqueda de código abierto basada en Lucene.
Ofrece alta personalización, pero requiere más experiencia para la implementación y operación en comparación con Fess.

Comparación
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Característica
     - Fess
     - Apache Solr
   * - Interfaz de búsqueda
     - ✅ Incluida
     - ❌ Requiere desarrollo
   * - Interfaz de administración
     - ✅ Interfaz web intuitiva
     - △ Interfaz de administración técnica
   * - Rastreador
     - ✅ Incluido
     - ❌ Requiere herramienta separada (Nutch, etc.)
   * - Dificultad de configuración
     - Baja
     - Media a alta
   * - Documentación
     - ✅ Completa
     - ✅ Completa
   * - Soporte en la nube
     - ✅ Docker/Kubernetes
     - ✅ SolrCloud
   * - Comunidad
     - Enfocada en Japón
     - Global

Cuándo elegir Fess
------------------

- **Cuando el rastreo Web/Archivos es el principal caso de uso**
- **Cuando la gestión por interfaz gráfica es importante**
- **Cuando la facilidad de implementación es una prioridad**

Cuándo elegir Solr
------------------

- **Cuando ya tiene experiencia con Solr**
- **Cuando se necesita búsqueda distribuida con SolrCloud**
- **Cuando se requieren plugins específicos de Solr**

----

Fess vs Google Site Search / Custom Search
==========================================

Descripción general
-------------------

Google Site Search (GSS) fue descontinuado en 2018.
El sucesor, Google Custom Search (Programmable Search Engine), tiene limitaciones.
Fess es un objetivo de migración ideal desde GSS.

Comparación
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Característica
     - Fess
     - Google Custom Search
   * - Visualización de anuncios
     - ✅ Ninguna
     - ❌ Se muestran (nivel gratuito)
   * - Ubicación de datos
     - ✅ Autogestionado
     - ❌ Servidores de Google
   * - Control de índices
     - ✅ Control total
     - △ Limitado
   * - Personalización
     - ✅ Libremente personalizable
     - △ Limitada
   * - Búsqueda de contenido interno
     - ✅ Soportada
     - ❌ No soportada
   * - Costo mensual
     - Solo costos de servidor
     - Gratuito (con anuncios) a de pago
   * - Ajuste de relevancia de búsqueda
     - ✅ Ajuste detallado posible
     - △ Limitado

Cuándo elegir Fess
------------------

- **Cuando no desea mostrar anuncios**
- **Cuando el contenido interno debe ser buscable**
- **Cuando desea control sobre los resultados de búsqueda**
- **Cuando desea gestionar los datos usted mismo**

.. tip::

   Con Fess Site Search (FSS), puede implementar búsqueda en sitios
   simplemente insertando JavaScript, igual que Google Site Search.

----

Fess vs Productos de búsqueda comerciales
==========================================

Descripción general
-------------------

Comparación con productos comerciales como Microsoft SharePoint Search, Autonomy y Google Cloud Search.

Comparación
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Característica
     - Fess
     - Productos comerciales (General)
   * - Costo de licencia
     - ✅ Gratuito (OSS)
     - ❌ Costoso
   * - Dependencia del proveedor
     - ✅ Ninguna
     - ❌ Si
   * - Personalización
     - ✅ Código fuente disponible
     - △ Limitada
   * - Riqueza de funciones
     - ○ Básica a intermedia
     - ✅ Funciones avanzadas
   * - Soporte
     - △ Comunidad + Comercial
     - ✅ Soporte del proveedor
   * - Funciones de IA/ML
     - △ Sugerencias básicas
     - ✅ Funciones avanzadas de IA
   * - Integración empresarial
     - ○ Principales sistemas soportados
     - ✅ Amplia integración

Cuándo elegir Fess
------------------

- **Cuando desea minimizar costos**
- **Cuando desea evitar la dependencia del proveedor**
- **Cuando las funciones de búsqueda básicas son suficientes**
- **Cuando desea aprovechar el código abierto**

Cuándo elegir productos comerciales
------------------------------------

- **Cuando se necesitan funciones avanzadas de IA/ML**
- **Cuando se requiere soporte integral del proveedor**
- **Cuando se necesita integración con ecosistemas comerciales existentes**

.. note::

   La versión comercial de Fess, `N2 Search <https://www.n2sm.net/products/n2search.html>`__,
   proporciona funciones empresariales adicionales y soporte.

----

Guía de selección
=================

Utilice el siguiente diagrama de flujo para seleccionar la solución óptima:

::

    Tiene suficientes recursos de desarrollo?
          │
    ┌─────┴─────┐
    │           │
   Si          No
    │           │
    ▼           ▼
  Son los requisitos  →  Considere Fess
  especializados?
    │
    ├── Si → OpenSearch/Elasticsearch independiente
    │         o productos comerciales
    │
    └── No → Es suficiente Fess?
              │
              ├── Si → Fess
              │
              └── No → Reevaluar requisitos

Resumen
=======

Fess es una opción óptima como "sistema de búsqueda listo para usar" para muchos casos.

**Fortalezas de Fess**:

- Implementación en minutos
- Construir un sistema de búsqueda sin desarrollo
- Código abierto y gratuito

**Próximos pasos**:

1. Pruebe Fess con el `Inicio rápido <../quick-start.html>`__
2. Evalúe según sus requisitos
3. Consulte el `Soporte Comercial <../support-services.html>`__ si es necesario
